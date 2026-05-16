"""Add richer preview images to already-published Etsy digital listings.

This is an edit path, not a new-listing path: it does not create listings,
activate drafts, or reserve/spend the $0.20 Etsy listing fee. It only appends
prepared preview images to listings that already exist and have fewer than the
target number of photos.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import etsy_api


DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"

QUEUE = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
PREVIEWS = DATABASE / "Etsy_Digital_Preview_Assets.csv"
LOG = DATABASE / "Etsy_Digital_Photo_Repair_Log.csv"
REPORT = REVIEW / "ETSY_DIGITAL_PHOTO_REPAIR_UPLOAD_REPORT.md"

TARGET_IMAGE_COUNT = 5
LOG_FIELDS = [
    "Timestamp",
    "ID",
    "Etsy_Listing_ID",
    "Before_Count",
    "After_Count",
    "Uploaded",
    "Status",
    "Note",
]


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def et_now() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def append_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def queue_by_id() -> dict[str, dict[str, str]]:
    return {clean(row.get("ID")): row for row in read_csv(QUEUE) if clean(row.get("ID"))}


def preview_rows() -> list[dict[str, str]]:
    return read_csv(PREVIEWS)


def preview_paths(row: dict[str, str]) -> list[Path]:
    paths: list[Path] = []
    for index in range(1, 10):
        value = clean(row.get(f"Preview_{index}"))
        if not value:
            continue
        path = Path(value)
        if path.exists():
            paths.append(path)
    return paths


def completed_ids(target: int) -> set[str]:
    completed: set[str] = set()
    for row in read_csv(LOG):
        item_id = clean(row.get("ID"))
        if not item_id:
            continue
        if clean(row.get("Status")) not in {"REPAIRED", "SKIP_ALREADY_RICH"}:
            continue
        try:
            after_count = int(clean(row.get("After_Count")) or "0")
        except ValueError:
            after_count = 0
        if after_count >= target:
            completed.add(item_id)
    return completed


def get_image_count(listing_id: str) -> int:
    data = etsy_api.request("GET", f"/listings/{listing_id}/images")
    return int(data.get("count") or len(data.get("results") or []))


def upload_image(shop_id: int, listing_id: str, path: Path, rank: int) -> dict:
    with path.open("rb") as handle:
        files = {"image": (path.name, handle, "image/jpeg")}
        return etsy_api.request(
            "POST",
            f"/shops/{shop_id}/listings/{listing_id}/images",
            data={"rank": rank},
            files=files,
        )


def repair(limit: int, dry_run: bool, ids: set[str] | None = None, target: int = TARGET_IMAGE_COUNT) -> dict:
    shop_id = int(etsy_api.first_shop_id())
    queue = queue_by_id()
    results: list[dict[str, str]] = []
    considered = 0
    completed = set() if ids else completed_ids(target)
    uploaded_total = 0

    for preview in preview_rows():
        item_id = clean(preview.get("ID"))
        if not item_id or (ids and item_id not in ids):
            continue
        if item_id in completed:
            continue
        qrow = queue.get(item_id) or {}
        listing_id = clean(qrow.get("Etsy_Listing_ID"))
        if not listing_id:
            continue
        paths = preview_paths(preview)
        if len(paths) < target:
            results.append(
                {
                    "Timestamp": et_now(),
                    "ID": item_id,
                    "Etsy_Listing_ID": listing_id,
                    "Before_Count": "",
                    "After_Count": "",
                    "Uploaded": "0",
                    "Status": "HOLD_PREVIEW_SET_INCOMPLETE",
                    "Note": f"Only {len(paths)} local previews found.",
                }
            )
            continue

        considered += 1
        before = get_image_count(listing_id)
        if before >= target:
            results.append(
                {
                    "Timestamp": et_now(),
                    "ID": item_id,
                    "Etsy_Listing_ID": listing_id,
                    "Before_Count": str(before),
                    "After_Count": str(before),
                    "Uploaded": "0",
                    "Status": "SKIP_ALREADY_RICH",
                    "Note": "Listing already has target image count.",
                }
            )
        else:
            needed = paths[before:target]
            if dry_run:
                after = before
                status = "DRY_RUN_WOULD_UPLOAD"
                uploaded = 0
                note = "; ".join(path.name for path in needed)
            else:
                uploaded = 0
                for offset, path in enumerate(needed, start=before + 1):
                    upload_image(shop_id, listing_id, path, offset)
                    uploaded += 1
                after = get_image_count(listing_id)
                uploaded_total += uploaded
                status = "REPAIRED" if after >= min(target, before + uploaded) else "REPAIR_UNCERTAIN"
                note = "; ".join(path.name for path in needed)
            results.append(
                {
                    "Timestamp": et_now(),
                    "ID": item_id,
                    "Etsy_Listing_ID": listing_id,
                    "Before_Count": str(before),
                    "After_Count": str(after),
                    "Uploaded": str(uploaded),
                    "Status": status,
                    "Note": note[:500],
                }
            )

        if considered >= limit:
            break

    if not dry_run and results:
        append_csv(LOG, results, LOG_FIELDS)
    write_report(results, dry_run=dry_run, uploaded_total=uploaded_total)
    return {
        "dry_run": dry_run,
        "considered": considered,
        "uploaded": uploaded_total,
        "results": results,
        "report": str(REPORT),
    }


def write_report(rows: list[dict[str, str]], dry_run: bool, uploaded_total: int) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Etsy Digital Photo Repair Upload Report",
        "",
        f"Generated: {et_now()}",
        f"Mode: {'DRY_RUN' if dry_run else 'EXECUTE'}",
        f"Uploaded images: {uploaded_total}",
        "",
        "Rule: this edits existing active listings only. It does not create a new listing and does not spend a new Etsy listing fee.",
        "",
    ]
    for row in rows:
        lines.append(
            f"- {row['ID']} / {row['Etsy_Listing_ID']}: {row['Status']} "
            f"{row['Before_Count']}->{row['After_Count']} uploaded={row['Uploaded']}"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Append missing preview images to active Etsy digital listings.")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--execute", action="store_true", help="Actually upload images. Default is dry-run.")
    parser.add_argument("--id", action="append", default=[])
    parser.add_argument("--target", type=int, default=TARGET_IMAGE_COUNT)
    args = parser.parse_args()
    ids = set(args.id) or None
    result = repair(limit=args.limit, dry_run=not args.execute, ids=ids, target=args.target)
    print(result)


if __name__ == "__main__":
    main()
