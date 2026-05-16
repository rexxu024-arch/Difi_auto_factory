"""Audit Etsy digital listings/queues for too-few preview images.

Etsy Seller Hub explicitly warns "Add more photos" on listings with sparse
visuals. This module is local/API-safe: it does not edit Etsy, publish, or spend.
It creates a repair queue for digital products that need richer preview sets.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "Database"
REVIEW = ROOT / "Review_Packets"

LIVE_AUDIT = DATABASE / "Etsy_Digital_Live_Audit.csv"
UPLOAD_QUEUE = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
REPAIR_CSV = DATABASE / "Etsy_Digital_Photo_Gap_Repair_Queue.csv"
PHOTO_REPAIR_LOG = DATABASE / "Etsy_Digital_Photo_Repair_Log.csv"
REPORT = REVIEW / "ETSY_DIGITAL_PHOTO_GAP_REPAIR.md"

MIN_PREVIEW_IMAGES = 4


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def et_now() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def image_count(row: dict[str, str]) -> int | None:
    for key in ("Image_Count", "image_count", "Images", "images", "Photo_Count", "photo_count"):
        value = clean(row.get(key))
        if value.isdigit():
            return int(value)
    populated = 0
    for key, value in row.items():
        lower = str(key).lower()
        if ("preview" in lower or "image" in lower or "photo" in lower) and clean(value):
            if Path(clean(value)).suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                populated += 1
    return populated if populated else None


def row_id(row: dict[str, str]) -> str:
    for key in ("ID", "Sku", "SKU", "listing_id", "Etsy_Listing_ID", "Listing_ID"):
        value = clean(row.get(key))
        if value:
            return value
    return ""


def completed_repair_ids() -> set[str]:
    completed: set[str] = set()
    for row in read_csv(PHOTO_REPAIR_LOG):
        status = clean(row.get("Status"))
        if status not in {"REPAIRED", "SKIP_ALREADY_RICH"}:
            continue
        try:
            after_count = int(clean(row.get("After_Count")) or "0")
        except ValueError:
            after_count = 0
        if after_count >= MIN_PREVIEW_IMAGES:
            item_id = clean(row.get("ID"))
            if item_id:
                completed.add(item_id)
    return completed


def run() -> None:
    sources = [(LIVE_AUDIT, "live_audit"), (UPLOAD_QUEUE, "launch_queue")]
    repairs: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    completed = completed_repair_ids()
    live_rich_ids: set[str] = set()
    for row in read_csv(LIVE_AUDIT):
        rid = row_id(row)
        count = image_count(row)
        if rid and count is not None and count >= MIN_PREVIEW_IMAGES:
            live_rich_ids.add(rid)
    for path, source_name in sources:
        for row in read_csv(path):
            rid = row_id(row)
            if not rid:
                continue
            if rid in completed or rid in live_rich_ids:
                continue
            count = image_count(row)
            if count is None:
                count = 1 if "Digital" in clean(row).lower() else 0
            if count >= MIN_PREVIEW_IMAGES:
                continue
            key = (source_name, rid)
            if key in seen:
                continue
            seen.add(key)
            repairs.append(
                {
                    "Source": source_name,
                    "ID": rid,
                    "Current_Image_Count": str(count),
                    "Required_Minimum": str(MIN_PREVIEW_IMAGES),
                    "Repair_Action": "BUILD_4_TO_6_PREVIEW_SET",
                    "Preview_Set": "cover, content_preview, identity_locked_use_case_mockup, detail_zoom, download_info",
                    "Fee_Action": "NO_NEW_LISTING_FEE_IF_EDIT_EXISTING",
                    "Note": "Etsy UI flagged sparse-photo listings as search-visibility improvement candidates.",
                }
            )
    fields = [
        "Source",
        "ID",
        "Current_Image_Count",
        "Required_Minimum",
        "Repair_Action",
        "Preview_Set",
        "Fee_Action",
        "Note",
    ]
    write_csv(REPAIR_CSV, repairs, fields)
    lines = [
        "# Etsy Digital Photo Gap Repair",
        "",
        f"Generated: {et_now()}",
        f"Minimum preview images: {MIN_PREVIEW_IMAGES}",
        f"Repair candidates: {len(repairs)}",
        "",
        "Rule: editing an existing Etsy listing does not create a new $0.20 listing fee; deleting/replacing does. Prefer editing sparse digital listings to add preview photos.",
        "",
        "Use-case mockup rule: the product/design identity must be locked from the original production or cover image with a high image-reference weight. Only environment, camera, crop, and lighting may change. Prompt language should include: preserve exact product design, no redesign, no pattern changes. Any subject/pattern/color/proportion drift is a HOLD.",
        "",
    ]
    for row in repairs[:30]:
        lines.append(f"- {row['ID']} ({row['Source']}): {row['Current_Image_Count']} images -> {row['Repair_Action']}")
    if len(repairs) > 30:
        lines.append(f"- ... {len(repairs) - 30} more in CSV.")
    lines.extend(["", "Output:", f"- {REPAIR_CSV.relative_to(ROOT)}"])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Etsy digital photo gap audit: repairs={len(repairs)}")
    print(f"repair={REPAIR_CSV}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    run()
