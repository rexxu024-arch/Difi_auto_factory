"""Prepare replacement-listing queue for risky non-sticker galleries.

This is separate from Cover Gate. These products may have a correct first
image, but their buyer-facing gallery contains custom/detail images that look
repetitive or confusing for Poster/Acrylic products. The safest proven repair
path is to build a clean replacement through the normal Printify pipeline with
official product mockups, verify live gallery, then retire the old listing.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


DATABASE_DIR = PROJECT_ROOT / "Database"
REPAIR_QUEUE = DATABASE_DIR / "Printify_Gallery_Repair_Queue.csv"
LIVE_AUDIT = DATABASE_DIR / "eBay_Live_Gallery_Duplicate_Audit.csv"
OUT_CSV = DATABASE_DIR / "eBay_Gallery_Replacement_Queue.csv"
OUT_MD = DATABASE_DIR / "eBay_Gallery_Replacement_Queue.md"

HEADERS = [
    "Priority",
    "ID",
    "Product_Type",
    "eBay_Item_ID",
    "Printify_Product_ID",
    "Gallery_Issue",
    "Replacement_SKU",
    "Replacement_Status",
    "Recommended_Action",
    "Notes",
]


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def next_fix_sku(old_id: str, existing_ids: set[str]) -> str:
    for number in range(1, 100):
        candidate = f"{old_id}-GALLERYFIX{number}"
        if candidate not in existing_ids:
            existing_ids.add(candidate)
            return candidate
    raise RuntimeError(f"Could not allocate replacement SKU for {old_id}")


def should_replace_live_gallery(row: dict[str, str]) -> bool:
    result = clean(row.get("Result")).upper()
    if not result or result == "OK":
        return False
    if "DUPLICATE" in result or "PRIMARY_DUPLICATE" in result:
        return True
    try:
        return int(clean(row.get("Duplicate_Source_Count")) or "0") > 0
    except ValueError:
        return False


def queue_row(
    *,
    priority: str,
    old_id: str,
    product_type: str,
    ebay_item_id: str,
    printify_product_id: str,
    issue: str,
    replacement_sku: str,
    status: str,
    action: str,
    notes: str,
) -> dict[str, str]:
    return {
        "Priority": priority,
        "ID": old_id,
        "Product_Type": product_type,
        "eBay_Item_ID": ebay_item_id,
        "Printify_Product_ID": printify_product_id,
        "Gallery_Issue": issue,
        "Replacement_SKU": replacement_sku,
        "Replacement_Status": status,
        "Recommended_Action": action,
        "Notes": notes,
    }


def build(limit: int = 0) -> list[dict[str, str]]:
    source = [
        row
        for row in read_csv(REPAIR_QUEUE)
        if clean(row.get("Issue")) == "CHECK_CUSTOM_GALLERY_REPEATS_RISK"
    ]
    live_source = [row for row in read_csv(LIVE_AUDIT) if should_replace_live_gallery(row)]
    existing_ids = {clean(row.get("ID")) for row in source + live_source}
    queued_ids: set[str] = set()
    rows: list[dict[str, str]] = []
    for row in live_source:
        old_id = clean(row.get("ID"))
        if not old_id or old_id in queued_ids:
            continue
        queued_ids.add(old_id)
        rows.append(
            queue_row(
                priority="100",
                old_id=old_id,
                product_type=clean(row.get("Product_Type")),
                ebay_item_id=clean(row.get("eBay_Item_ID")),
                printify_product_id=clean(row.get("Printify_Product_ID")),
                issue=clean(row.get("Result")) or "LIVE_GALLERY_DUPLICATE_RISK",
                replacement_sku=next_fix_sku(old_id, existing_ids),
                status="HOLD_OR_REBUILD_CLEAN_SOURCE",
                action="Do not revise this inventory listing through Trading API. Rebuild clean Printify product with verified source mockups, live-audit the buyer gallery, then retire the old item.",
                notes=(
                    "Live eBay buyer page shows repeated image URLs/slots; source-side Printify audit may miss this. "
                    f"pictures={clean(row.get('Picture_Count'))}; unique={clean(row.get('Unique_Source_Count'))}; "
                    f"dup={clean(row.get('Duplicate_Source_Count'))}; url={clean(row.get('URL'))}"
                ),
            )
        )
        if limit and len(rows) >= limit:
            break

    for row in source:
        old_id = clean(row.get("ID"))
        if not old_id or old_id in queued_ids:
            continue
        queued_ids.add(old_id)
        rows.append(
            queue_row(
                priority=clean(row.get("Priority")) or "96",
                old_id=old_id,
                product_type=clean(row.get("Product_Type")),
                ebay_item_id=clean(row.get("eBay_Item_ID")),
                printify_product_id=clean(row.get("Printify_Product_ID")),
                issue=clean(row.get("Issue")),
                replacement_sku=next_fix_sku(old_id, existing_ids),
                status="READY_FOR_LOCAL_DRAFT_WHEN_APPROVED",
                action="Create replacement product with clean official mockups, verify live gallery, then retire old listing.",
                notes="Do not bulk-publish until one GalleryFix sample passes Printify source audit and eBay live-gallery audit.",
            )
        )
        if limit and len(rows) >= limit:
            break

    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(row["Product_Type"] for row in rows)
    lines = [
        "# eBay Gallery Replacement Queue",
        "",
        f"- Rows: {len(rows)}",
        f"- By product type: {dict(sorted(counts.items()))}",
        "- This queue is for non-sticker custom-gallery risk after exact duplicate source repair is complete.",
        "- Replacement flow: local draft -> Printify clean official mockups -> live eBay gallery audit -> retire old listing.",
        "",
        "| Priority | ID | Type | eBay Item | Replacement SKU | Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['Priority']} | {row['ID']} | {row['Product_Type']} | "
            f"{row['eBay_Item_ID']} | {row['Replacement_SKU']} | {row['Replacement_Status']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[GALLERY-REPLACEMENT-QUEUE] rows={len(rows)} csv={OUT_CSV}")
    for product_type, count in sorted(counts.items()):
        print(f"[GALLERY-REPLACEMENT-QUEUE] {product_type}={count}")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    build(limit=args.limit)


if __name__ == "__main__":
    main()
