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
AUDIT_CSV = DATABASE / "eBay_API_Inventory_Category_Audit.csv"
OUT_CSV = DATABASE / "eBay_API_Repair_Plan.csv"
OUT_MD = REPORTS / "eBay_API_Repair_Plan.md"
NY = ZoneInfo("America/New_York")


def clean(value) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\n", " ").replace("\r", " ")).strip()


def money(value) -> float:
    try:
        return float(re.sub(r"[^0-9.]", "", clean(value)) or "0")
    except ValueError:
        return 0.0


def product_type(row: dict[str, str]) -> str:
    inferred = clean(row.get("Product_Type_Inferred"))
    title = clean(row.get("API_Title") or row.get("Perf_Title")).lower()
    if inferred:
        return inferred
    if "sticker" in title:
        return "Sticker"
    if "acrylic" in title or "photo block" in title:
        return "Acrylic"
    if "poster" in title:
        return "Poster"
    return "Unknown"


def suggested_free_shipping_price(row: dict[str, str]) -> float:
    ptype = product_type(row)
    price = money(row.get("Price"))
    shipping = money(row.get("Shipping_Cost"))
    total = price + shipping
    if ptype == "Sticker":
        # Sticker expansion is frozen; only retain a break-even reference for legacy rows.
        return min(max(9.99, round(total - 0.29, 2)), 12.99)
    if ptype == "Poster":
        # 12x18 poster: reduce sticker shock from $34.99 + shipping to one clean price.
        return min(max(34.99, round(total - 3.99, 2)), 39.99)
    if ptype == "Acrylic":
        # Keep the high-end anchor, but stop showing a $100+ buyer total for 5x7 acrylic.
        return min(max(89.99, round(total - 10.99, 2)), 94.99)
    return round(total, 2)


def actions_for(row: dict[str, str]) -> list[str]:
    flags = set(clean(row.get("Flags")).split("|"))
    ptype = product_type(row)
    actions = []
    if ptype == "Sticker":
        return ["sticker_frozen_monitor_only"]
    if "SHIPPING_NOT_FREE" in flags:
        actions.append(f"convert_to_free_shipping_price_{suggested_free_shipping_price(row):.2f}")
    if "BRAND_LOW_TRUST" in flags:
        actions.append("set_brand_OpenClaw_Design_Studio")
    if "SHORT_DESCRIPTION_THIN" in flags:
        actions.append("rewrite_short_description_buyer_trust_snippet")
    if "LOW_GALLERY_COUNT" in flags:
        actions.append("hold_until_gallery_has_3plus_unique_images")
    if "CATEGORY_MISMATCH_ACRYLIC" in flags and ptype == "Acrylic":
        actions.append("review_acrylic_category_Frames_vs_Photo_Display")
    if "WORLDWIDE_SHIPPING_ENABLED" in flags:
        actions.append("review_worldwide_shipping_scope_for_POD")
    return actions or ["watch_no_action"]


def priority(row: dict[str, str]) -> str:
    flags = set(clean(row.get("Flags")).split("|"))
    if product_type(row) == "Sticker":
        return "STICKER_FROZEN"
    if "LOW_GALLERY_COUNT" in flags:
        return "HOLD_GALLERY_FIRST"
    if "SHIPPING_NOT_FREE" in flags or "BRAND_LOW_TRUST" in flags:
        return "REPAIR_BATCH_A"
    return "WATCH"


def run() -> int:
    if not AUDIT_CSV.exists():
        raise FileNotFoundError(f"Missing audit CSV: {AUDIT_CSV}")
    with AUDIT_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    out = []
    experiment_slots = 0
    for row in rows:
        ptype = product_type(row)
        prio = priority(row)
        experiment_group = ""
        if prio == "REPAIR_BATCH_A" and ptype in {"Poster", "Acrylic"}:
            experiment_slots += 1
            experiment_group = "TREATMENT_FREE_SHIP_BRAND_COPY" if experiment_slots <= 5 else (
                "CONTROL_UNCHANGED_72H" if experiment_slots <= 10 else "BACKLOG_AFTER_FIRST_10"
            )
        out.append(
            {
                "Item_ID": clean(row.get("Item_ID")),
                "Product_Type": ptype,
                "Views_30_Days": clean(row.get("Views_30_Days")),
                "Current_Price": f"{money(row.get('Price')):.2f}",
                "Current_Shipping": f"{money(row.get('Shipping_Cost')):.2f}",
                "Suggested_FreeShip_Price": f"{suggested_free_shipping_price(row):.2f}",
                "Brand_Target": "OpenClaw Design Studio",
                "Category_Path": clean(row.get("Category_Path")),
                "Image_Count": clean(row.get("Image_Count")),
                "Flags": clean(row.get("Flags")),
                "Priority": prio,
                "Experiment_Group": experiment_group,
                "Repair_Actions": "|".join(actions_for(row)),
                "Title": clean(row.get("API_Title") or row.get("Perf_Title")),
            }
        )
    fields = [
        "Item_ID",
        "Product_Type",
        "Views_30_Days",
        "Current_Price",
        "Current_Shipping",
        "Suggested_FreeShip_Price",
        "Brand_Target",
        "Category_Path",
        "Image_Count",
        "Flags",
        "Priority",
        "Experiment_Group",
        "Repair_Actions",
        "Title",
    ]
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out)
    pcounts = Counter(row["Priority"] for row in out)
    type_counts = Counter(row["Product_Type"] for row in out)
    lines = [
        "# eBay API Repair Plan",
        "",
        f"Generated: {datetime.now(NY).strftime('%Y-%m-%d %H:%M:%S %z')}",
        f"Rows planned: {len(out)}",
        "",
        "## Priority Counts",
        "",
    ]
    for key, value in pcounts.most_common():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Product Mix", ""])
    for key, value in type_counts.most_common():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Recommended First Repair Experiment",
            "",
            "1. Do not publish more low-ticket items until buyer-facing shipping is intentionally decided.",
            "2. Sticker is frozen: do not add sticker inventory; legacy stickers are monitor-only.",
            "3. First treatment group: the first 5 Poster/Acrylic `REPAIR_BATCH_A` rows get free-shipping price/brand/copy repair.",
            "4. Control group: the next 5 comparable Poster/Acrylic rows remain unchanged for 72 hours.",
            "5. If views/clicks lift, roll out to the remaining non-gallery-held products.",
            "",
            f"CSV: {OUT_CSV}",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[EBAY-REPAIR-PLAN] rows={len(out)} csv={OUT_CSV} md={OUT_MD}")
    for key, value in pcounts.most_common():
        print(f"[EBAY-REPAIR-PLAN] {key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
