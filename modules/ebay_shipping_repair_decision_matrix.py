from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATABASE = ROOT / "Database"
REPORTS = ROOT / "Reports"
AUDIT_CSV = DATABASE / "eBay_API_Inventory_Category_Audit.csv"
REPAIR_PLAN_CSV = DATABASE / "eBay_API_Repair_Plan.csv"
AD_SHORTLIST_CSV = DATABASE / "eBay_Ad_Rate_Execution_Shortlist_NoSticker.csv"
API_STATUS_JSON = DATABASE / "eBay_API_Status.json"
OUT_CSV = DATABASE / "eBay_Shipping_Repair_Decision_Matrix.csv"
OUT_MD = REPORTS / "eBay_Shipping_Repair_Decision_Matrix.md"
NY = ZoneInfo("America/New_York")


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\n", " ").replace("\r", " ")).strip()


def now_text() -> str:
    return datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S %z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: clean(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def latest_trading_verify_error() -> str:
    files = sorted((DATABASE / "eBay_Picture_Revise").glob("ebay_trading_picture_repair_dry_run_*.csv"))
    if not files:
        return ""
    newest = files[-1]
    rows = read_csv(newest)
    notes: list[str] = []
    for row in rows[:10]:
        note = clean(row.get("Trading_Revise_VerifyOnly_Note"))
        if note:
            notes.append(note)
    return " | ".join(notes)[:1200]


def account_policy_available(status: dict) -> bool:
    for probe in status.get("probes") or []:
        name = clean(probe.get("name"))
        if name == "fulfillment_policies":
            return bool(probe.get("ok"))
    return False


def api_policy_block_reason(status: dict) -> str:
    for probe in status.get("probes") or []:
        name = clean(probe.get("name"))
        if name != "fulfillment_policies":
            continue
        sample = probe.get("body_sample") or {}
        errors = sample.get("errors") or []
        if errors:
            return clean(errors[0].get("longMessage") or errors[0].get("message"))
    return ""


def index_by(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {clean(row.get(key)): row for row in rows if clean(row.get(key))}


def parse_money(value: str) -> float:
    try:
        return float(re.sub(r"[^0-9.]", "", value) or 0)
    except ValueError:
        return 0.0


def decide(row: dict[str, str], repair: dict[str, str], ad: dict[str, str], policy_ok: bool, trading_inventory_blocked: bool) -> dict[str, str]:
    flags = set(clean(row.get("Flags")).split("|")) if clean(row.get("Flags")) else set()
    product_type = clean(row.get("Product_Type_Inferred") or repair.get("Product_Type"))
    image_count = int(parse_money(row.get("Image_Count")))
    current_shipping = parse_money(row.get("Shipping_Cost"))
    views = int(parse_money(row.get("Views_30_Days")))
    item_id = clean(row.get("Item_ID"))

    if product_type == "Sticker":
        action = "FREEZE_STICKER_MONITOR_ONLY"
        reason = "Sticker lane is frozen; do not spend engineering or ad budget here."
    elif "API_READ_FAILED" in flags:
        action = "HOLD_API_READ_FAILED"
        reason = "Cannot safely repair an item that cannot be read back from eBay."
    elif image_count < 3:
        action = "HOLD_REBUILD_GALLERY_FIRST"
        reason = "Buyer-facing gallery is too thin; repair source mockups before pricing/ad experiments."
    elif current_shipping <= 0:
        action = "READY_FOR_AD_OR_COPY_TEST"
        reason = "Shipping already appears free or absent; proceed with ad/copy experiment guardrails."
    elif policy_ok:
        action = "CAN_USE_ACCOUNT_POLICY_REPAIR"
        reason = "Sell Account fulfillment policy API is available."
    elif trading_inventory_blocked:
        action = "SOURCE_REBUILD_OR_PRINTIFY_TEMPLATE_PROBE"
        reason = "eBay Trading verify blocks inventory-based listings; use Printify shipping_template probe or rebuild from source."
    else:
        action = "TRADING_VERIFY_ONE_ITEM_BEFORE_WRITE"
        reason = "No account policy; Trading route must be verified on one low-risk item before any write."

    ad_rate = clean(ad.get("Ad_Rate_Pct"))
    lane = clean(ad.get("Lane"))
    profit = clean(ad.get("Estimated_Profit_USD"))
    if action not in {"READY_FOR_AD_OR_COPY_TEST", "CAN_USE_ACCOUNT_POLICY_REPAIR"} and ad_rate:
        ad_gate = "BLOCK_AD_UNTIL_SHIPPING_GALLERY_REPAIRED"
    elif ad_rate:
        ad_gate = "AD_TEST_ALLOWED_AFTER_PROFIT_GUARD"
    else:
        ad_gate = "NO_AD_SHORTLIST"

    return {
        "Generated": now_text(),
        "Item_ID": item_id,
        "Product_Type": product_type,
        "Views_30_Days": clean(row.get("Views_30_Days")),
        "Current_Price": clean(row.get("Price")),
        "Current_Shipping": clean(row.get("Shipping_Cost")),
        "Image_Count": clean(row.get("Image_Count")),
        "Flags": clean(row.get("Flags")),
        "Repair_Priority": clean(repair.get("Priority")),
        "Repair_Group": clean(repair.get("Experiment_Group")),
        "Ad_Lane": lane,
        "Ad_Rate_Pct": ad_rate,
        "Estimated_Profit_USD": profit,
        "Decision": action,
        "Ad_Gate": ad_gate,
        "Reason": reason,
        "Title": clean(row.get("API_Title") or repair.get("Title")),
    }


def run() -> tuple[Path, Path]:
    REPORTS.mkdir(parents=True, exist_ok=True)
    audit = read_csv(AUDIT_CSV)
    repairs = index_by(read_csv(REPAIR_PLAN_CSV), "Item_ID")
    ad_by_item = index_by(read_csv(AD_SHORTLIST_CSV), "eBay_Item_ID")
    status = read_json(API_STATUS_JSON)
    policy_ok = account_policy_available(status)
    policy_reason = api_policy_block_reason(status)
    trading_note = latest_trading_verify_error()
    trading_inventory_blocked = "not allowed for inventory items" in trading_note.lower()

    rows = [
        decide(row, repairs.get(clean(row.get("Item_ID")), {}), ad_by_item.get(clean(row.get("Item_ID")), {}), policy_ok, trading_inventory_blocked)
        for row in audit
    ]
    fields = [
        "Generated",
        "Item_ID",
        "Product_Type",
        "Views_30_Days",
        "Current_Price",
        "Current_Shipping",
        "Image_Count",
        "Flags",
        "Repair_Priority",
        "Repair_Group",
        "Ad_Lane",
        "Ad_Rate_Pct",
        "Estimated_Profit_USD",
        "Decision",
        "Ad_Gate",
        "Reason",
        "Title",
    ]
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    decisions = Counter(row["Decision"] for row in rows)
    ad_gates = Counter(row["Ad_Gate"] for row in rows)
    lines = [
        "# eBay Shipping Repair Decision Matrix",
        "",
        f"Generated: {now_text()}",
        f"Rows: {len(rows)}",
        "",
        "## API Reality",
        "",
        f"- Sell Account fulfillment policy available: `{policy_ok}`",
        f"- Account API block: `{policy_reason or 'none'}`",
        f"- Trading inventory-listing block observed: `{trading_inventory_blocked}`",
        "",
        "## Decision Counts",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in decisions.most_common())
    lines.extend(["", "## Ad Gates", ""])
    lines.extend(f"- {key}: {value}" for key, value in ad_gates.most_common())
    lines.extend(
        [
            "",
            "## Operating Rule",
            "",
            "- Do not raise ad rate on items whose buyer-facing shipping/gallery is still broken.",
            "- Do not apply free-shipping prices unless the shipping charge is actually removed.",
            "- For Printify-owned eBay listings, prefer source rebuild or a one-item Printify `shipping_template=true` probe over Trading API revision.",
            "",
            f"CSV: {OUT_CSV}",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[EBAY-SHIPPING-MATRIX] rows={len(rows)} decisions={dict(decisions)} csv={OUT_CSV} md={OUT_MD}")
    return OUT_CSV, OUT_MD


def main() -> int:
    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
