from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "Database"
REPORTS = ROOT / "Reports"
AUDIT = DATABASE / "Printify_Sales_Channel_Audit.csv"
OUT_CSV = DATABASE / "Printify_Free_Shipping_Repair_Plan.csv"
OUT_MD = REPORTS / "Printify_Free_Shipping_Repair_Plan.md"
NY = ZoneInfo("America/New_York")


def clean(value) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\n", " ").replace("\r", " ")).strip()


def now_et() -> str:
    return datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S %z")


def decision(row: dict[str, str]) -> str:
    state = clean(row.get("Free_Shipping_State"))
    external = clean(row.get("External_ID"))
    locked = clean(row.get("Locked")).lower() == "true"
    title = clean(row.get("Printify_Title")).lower()
    if locked:
        return "HOLD_LOCKED_PRODUCT"
    if state == "FREE_SHIPPING_TRUE":
        return "PASS_ALREADY_FREE_SHIPPING"
    if not external:
        return "SOURCE_PATCH_BEFORE_PUBLISH"
    if "clean_clone" in clean(row.get("Workbook_ID")).lower():
        return "SOURCE_PATCH_THEN_EBAY_READBACK"
    if "vintage study" in title or "quiet minimal" in title or "moody collector" in title:
        return "SOURCE_PATCH_THEN_MARKETPLACE_SEO_OVERRIDE"
    return "SOURCE_PATCH_CANDIDATE"


def run() -> int:
    if not AUDIT.exists():
        raise FileNotFoundError(f"Run printify_sales_channel_audit.py first: {AUDIT}")
    with AUDIT.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    out = []
    for row in rows:
        item = dict(row)
        item["Repair_Decision"] = decision(row)
        item["Repair_Risk"] = (
            "NO_MARKETPLACE_WRITE_IN_PLAN; source patch must be tested on one item, then read back eBay/Etsy front-end."
        )
        out.append(item)

    fields = list(out[0].keys()) if out else [
        "Timestamp",
        "Workbook_ID",
        "Repair_Decision",
        "Repair_Risk",
    ]
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out)

    counts = Counter(row["Repair_Decision"] for row in out)
    lines = [
        "# Printify Free Shipping Repair Plan",
        "",
        f"Generated: {now_et()}",
        f"Rows: {len(out)}",
        "",
        "## Decision Counts",
        "",
    ]
    for key, value in counts.most_common():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Next Safe Action",
            "",
            "1. Test one `SOURCE_PATCH_THEN_EBAY_READBACK` item by updating Printify source `sales_channel_properties.free_shipping=true` only.",
            "2. If eBay still reads buyer-paid shipping, abandon source patch and rebuild from a clean product created with free shipping from birth.",
            "3. Do not increase ad rates until the readback gate passes free shipping and brand/gallery checks.",
            "",
            f"CSV: {OUT_CSV}",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[PRINTIFY-FREE-SHIP-PLAN] rows={len(out)} counts={dict(counts)} csv={OUT_CSV} md={OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
