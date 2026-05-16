from __future__ import annotations

import csv
import json
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
OUT_CSV = DATABASE / "eBay_Source_Sync_Root_Cause.csv"
OUT_MD = REPORTS / "eBay_Source_Sync_Root_Cause.md"
NY = ZoneInfo("America/New_York")


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


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
    except Exception:
        return {}


def money(value: str) -> float:
    try:
        return float(clean(value).replace("$", "") or 0)
    except ValueError:
        return 0.0


def now_text() -> str:
    return datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S %z")


def api_blockers(status: dict) -> list[str]:
    blockers: list[str] = []
    for probe in status.get("probes") or []:
        name = clean(probe.get("name"))
        error_id = clean(probe.get("error_id"))
        message = clean(probe.get("message"))
        body = probe.get("body_sample")
        long_message = ""
        if isinstance(body, dict):
            errors = body.get("errors")
            if isinstance(errors, list) and errors:
                long_message = clean(errors[0].get("longMessage"))
        if error_id == "20403" or "not eligible for Business Policy" in long_message:
            blockers.append(f"{name}: BUSINESS_POLICY_NOT_ELIGIBLE")
        elif message:
            blockers.append(f"{name}: {message}")
    return blockers


def build() -> tuple[Path, Path]:
    readback = read_csv(DATABASE / "eBay_Clean_Clone_Readback_Gate.csv")
    category = read_csv(DATABASE / "eBay_API_Inventory_Category_Audit.csv")
    free_shipping_probe = read_csv(DATABASE / "Printify_Free_Shipping_Source_Probe.csv")
    template_probe = read_csv(DATABASE / "eBay_Printify_Shipping_Template_Probe_Execution.csv")
    api_status = read_json(DATABASE / "eBay_API_Status.json")
    risk_state = read_json(DATABASE / "Account_Risk_State.json")

    source_free_ok = {
        row["Printify_Product_ID"]: row
        for row in free_shipping_probe
        if clean(row.get("Result")) == "OK" and clean(row.get("After_Free_Shipping")).lower() == "true"
    }
    category_by_item = {clean(row.get("Item_ID")): row for row in category}
    template_by_item = {clean(row.get("eBay_Item_ID")): row for row in template_probe}

    rows: list[dict[str, str]] = []
    for row in readback:
        item_id = clean(row.get("eBay_Item_ID"))
        product_id = clean(row.get("Printify_Product_ID"))
        cat = category_by_item.get(item_id, {})
        template = template_by_item.get(item_id, {})
        shipping = money(row.get("Shipping_Cost", ""))
        flags = clean(row.get("Flags") or cat.get("Flags"))
        probable_cause: list[str] = []
        next_action: list[str] = []
        if shipping > 0:
            probable_cause.append("EBAY_FRONTEND_STILL_BUYER_PAID_SHIPPING")
        if product_id in source_free_ok:
            probable_cause.append("PRINTIFY_SOURCE_FREE_SHIPPING_PATCH_DID_NOT_PROPAGATE")
        if "BRAND_LOW_TRUST" in flags:
            probable_cause.append("PRINTIFY_ORIGIN_BRAND_STILL_PUBLIC")
        if "CATEGORY_MISMATCH_ACRYLIC" in flags:
            probable_cause.append("ACRYLIC_CATEGORY_MISMATCH")
        if clean(template.get("Result")) == "DRY_RUN_READY":
            next_action.append("OPTIONAL_ONE_ITEM_SHIPPING_TEMPLATE_PROBE_ONLY_WHEN_RISK_GUARD_ALLOWS")
        if shipping > 0:
            next_action.append("KEEP_EBAY_PAID_PUBLISH_FROZEN")
        if "BRAND_LOW_TRUST" in flags:
            next_action.append("REBUILD_OR_DIRECT_EDIT_PUBLIC_SELLER_FIELDS_BEFORE_MORE_AD_SPEND")
        if "CATEGORY_MISMATCH_ACRYLIC" in flags:
            next_action.append("FIX_ACRYLIC_CATEGORY_BEFORE_SCALE")
        rows.append(
            {
                "Timestamp": now_text(),
                "Workbook_ID": clean(row.get("Workbook_ID")),
                "Product_Type": clean(row.get("Product_Type") or cat.get("Product_Type_Inferred")),
                "eBay_Item_ID": item_id,
                "Printify_Product_ID": product_id,
                "Price": clean(row.get("Price") or cat.get("Price")),
                "Shipping_Cost": clean(row.get("Shipping_Cost") or cat.get("Shipping_Cost")),
                "Brand": clean(row.get("Brand") or cat.get("Brand")),
                "Category_Path": clean(cat.get("Category_Path")),
                "Image_Count": clean(row.get("Image_Count") or cat.get("Image_Count")),
                "Source_Free_Patched": "YES" if product_id in source_free_ok else "NO_OR_UNKNOWN",
                "Template_Probe_Result": clean(template.get("Result")),
                "Flags": flags,
                "Probable_Cause": "|".join(probable_cause) or "NO_MAJOR_CAUSE_DETECTED",
                "Next_Action": "|".join(next_action) or "MONITOR_ONLY",
            }
        )

    fields = [
        "Timestamp",
        "Workbook_ID",
        "Product_Type",
        "eBay_Item_ID",
        "Printify_Product_ID",
        "Price",
        "Shipping_Cost",
        "Brand",
        "Category_Path",
        "Image_Count",
        "Source_Free_Patched",
        "Template_Probe_Result",
        "Flags",
        "Probable_Cause",
        "Next_Action",
    ]
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    flag_counts: Counter[str] = Counter()
    cause_counts: Counter[str] = Counter()
    for row in rows:
        for flag in row["Flags"].split("|"):
            if flag:
                flag_counts[flag] += 1
        for cause in row["Probable_Cause"].split("|"):
            if cause:
                cause_counts[cause] += 1

    blockers = api_blockers(api_status)
    states = risk_state.get("states") if isinstance(risk_state, dict) else {}
    ebay_risk = (states.get("ebay") or risk_state.get("ebay") or {}) if isinstance(risk_state, dict) else {}
    lines = [
        "# eBay Source Sync Root Cause",
        "",
        f"Generated: {now_text()}",
        f"Rows analyzed: {len(rows)}",
        "",
        "## Decision",
        "",
        "- Keep eBay paid/live publish frozen until buyer-facing shipping, brand, and category readback pass.",
        "- The current account can read Inventory and Marketing APIs, but Account Business Policy endpoints return not eligible.",
        "- Do not spend more ads on affected listings until the public buyer-facing listing fields are corrected.",
        "",
        "## Current Risk Guard",
        "",
        f"- risk_state: {clean(ebay_risk.get('risk_state'))}",
        f"- paid_publish_allowed: {ebay_risk.get('paid_publish_allowed')}",
        "",
        "## API Blockers",
        "",
    ]
    lines.extend(f"- {item}" for item in blockers or ["None detected"])
    lines.extend(["", "## Cause Counts", ""])
    lines.extend(f"- {key}: {value}" for key, value in cause_counts.most_common())
    lines.extend(["", "## Flag Counts", ""])
    lines.extend(f"- {key}: {value}" for key, value in flag_counts.most_common())
    lines.extend(
        [
            "",
            "## Safe Next Step",
            "",
            "1. Keep marketplace writes blocked.",
            "2. If Rex explicitly accepts the risk later, run exactly one Printify shipping-template-only probe, then re-run readback.",
            "3. If the one-item probe does not clear buyer-paid shipping, abandon Printify-source repair for eBay and use direct marketplace correction or rebuild from a clean integration path.",
            "",
            f"CSV: {OUT_CSV}",
        ]
    )
    OUT_MD.parent.mkdir(exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[EBAY-ROOT-CAUSE] rows={len(rows)} csv={OUT_CSV} md={OUT_MD}")
    return OUT_CSV, OUT_MD


def main() -> int:
    build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
