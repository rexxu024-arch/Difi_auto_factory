"""Build a no-write clean-clone plan for weak eBay listings.

The current eBay/Printify path cannot safely patch Printify-owned active
listings through Trading API. This module turns the audit findings into a
replacement plan: create cleaner future clones, then retire the weak originals
only after the clone is live and verified.
"""

from __future__ import annotations

import argparse
import csv
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
SOURCE = DATABASE / "eBay_API_Repair_Plan.csv"
OUT = DATABASE / "eBay_Clean_Clone_Experiment_Plan.csv"
REPORT = REPORTS / "eBay_Clean_Clone_Experiment_Plan.md"
NY_TZ = ZoneInfo("America/New_York")


def clean(value: object) -> str:
    return str(value or "").strip()


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else [
        "Generated_At",
        "Experiment_Group",
        "Old_Item_ID",
        "Clone_Strategy",
        "Status",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def clone_title(title: str, product_type: str) -> str:
    base = clean(title)
    replacements = [
        ("Deep Work Visual Poster", "Quiet Luxury Study Poster"),
        ("Smoky Jade Wall Art", "Smoky Jade Reading Nook Art"),
        ("Quiet Luxury Shelf Decor", "Quiet Luxury Desk Relic"),
        ("Meditation Room Jade Relic", "Meditation Room Acrylic Relic"),
        ("Sticker Set", "Sticker Pack"),
    ]
    for old, new in replacements:
        base = base.replace(old, new)
    # The API audit sometimes surfaces title fragments that already accumulated
    # repetitive SEO filler. Do not let those become the next experiment.
    words = base.split()
    cleaned_words: list[str] = []
    seen_trigrams: set[tuple[str, str, str]] = set()
    for word in words:
        if cleaned_words and cleaned_words[-1].lower() == word.lower():
            continue
        trial = cleaned_words[-2:] + [word]
        tri = tuple(w.lower().strip(",|-") for w in trial)
        if len(tri) == 3 and tri in seen_trigrams:
            continue
        cleaned_words.append(word)
        if len(tri) == 3:
            seen_trigrams.add(tri)
    base = " ".join(cleaned_words)
    lowered = base.lower()
    if product_type.lower() == "acrylic" and "deep work desk visual" in lowered:
        base = "Deep Work Desk Visual 5x7 Acrylic Block Quiet Luxury Office Decor"
    elif product_type.lower() == "acrylic" and lowered.count("collector") >= 2:
        base = "Smoky Jade Desk Relic 5x7 Acrylic Block Quiet Luxury Shelf Decor"
    elif product_type.lower() == "acrylic" and "lantern shadowbound" in lowered:
        base = base.replace("Collector", "Display Decor")
    elif product_type.lower() == "acrylic" and "collector office" in lowered:
        base = base.replace("Collector Office", "Office Relic")
    if product_type.lower() == "acrylic" and "Acrylic" not in base:
        base = f"{base} Acrylic Block"
    if product_type.lower() == "poster" and "Poster" not in base:
        base = f"{base} Matte Poster"
    base = " ".join(base.split())
    if product_type.lower() == "acrylic" and len(base) < 68:
        base = f"{base} Desk Display Gift"
    if product_type.lower() == "poster" and len(base) < 68:
        base = f"{base} Library Wall Decor"
    if product_type.lower() == "sticker" and len(base) < 68:
        base = f"{base} Laptop Journal Gift"
    if len(base) <= 79:
        return base.rstrip(" -|,")
    clipped = base[:79].rstrip(" -|,")
    if " " in clipped:
        clipped = clipped.rsplit(" ", 1)[0]
    return clipped.rstrip(" -|,")


def build(limit: int = 10) -> int:
    source = read_csv(SOURCE)
    candidates = [
        row for row in source
        if clean(row.get("Priority")) in {"REPAIR_BATCH_A", "HOLD_GALLERY_FIRST"}
        and clean(row.get("Product_Type")).lower() != "sticker"
    ]
    candidates.sort(key=lambda row: (
        clean(row.get("Priority")) != "REPAIR_BATCH_A",
        clean(row.get("Product_Type")),
        clean(row.get("Item_ID")),
    ))
    rows: list[dict[str, str]] = []
    for index, row in enumerate(candidates[: max(1, limit)], start=1):
        product_type = clean(row.get("Product_Type")) or "Unknown"
        old_item = clean(row.get("Item_ID"))
        priority = clean(row.get("Priority"))
        flags = clean(row.get("Flags"))
        title = clean(row.get("Title"))
        suggested_price = clean(row.get("Suggested_FreeShip_Price")) or clean(row.get("Current_Price"))
        if priority == "HOLD_GALLERY_FIRST":
            status = "WAIT_GALLERY_REBUILD_BEFORE_CLONE"
            strategy = "repair_gallery_source_then_clone"
        else:
            status = "READY_FOR_CLEAN_CLONE_DRAFT"
            strategy = "clone_with_free_shipping_openclaw_brand_buyer_trust_copy"
        rows.append(
            {
                "Generated_At": now_text(),
                "Experiment_Group": f"CLEAN_CLONE_A_{index:02d}",
                "Old_Item_ID": old_item,
                "Product_Type": product_type,
                "Old_Title": title,
                "Clone_Title_Target": clone_title(title, product_type),
                "Clone_Price_Free_Shipping_USD": suggested_price,
                "Brand_Target": "OpenClaw Design Studio",
                "Gallery_Gate": "PASS_REQUIRED_3PLUS_UNIQUE_IMAGES",
                "Shipping_Gate": "FREE_SHIPPING_PRICE_INCLUDES_PRINTIFY_SHIPPING",
                "Retire_Old_Rule": "retire old listing only after clone is live, buyer page audited, and duplicate risk cleared",
                "Source_Flags": flags,
                "Clone_Strategy": strategy,
                "Status": status,
            }
        )
    write_csv(OUT, rows)
    counts = Counter(row["Status"] for row in rows)
    lines = [
        "# eBay Clean-Clone Experiment Plan",
        "",
        f"Generated: {now_text()} America/New_York",
        "",
        "No live eBay listings were changed. This is a replacement plan for Printify-owned listings that cannot be safely patched via Trading API.",
        "",
        "## Counts",
        "",
    ]
    for key, count in sorted(counts.items()):
        lines.append(f"- {key}: {count}")
    lines.extend(["", "## Candidates", ""])
    for row in rows:
        lines.append(f"### {row['Experiment_Group']} / old item {row['Old_Item_ID']}")
        lines.append(f"- Type: {row['Product_Type']}")
        lines.append(f"- Status: {row['Status']}")
        lines.append(f"- Clone title target: {row['Clone_Title_Target']}")
        lines.append(f"- Free-shipping price target: ${row['Clone_Price_Free_Shipping_USD']}")
        lines.append(f"- Flags: {row['Source_Flags']}")
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[EBAY-CLEAN-CLONE] rows={len(rows)} csv={OUT} report={REPORT}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build eBay clean-clone replacement plan")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    return build(args.limit)


if __name__ == "__main__":
    raise SystemExit(main())
