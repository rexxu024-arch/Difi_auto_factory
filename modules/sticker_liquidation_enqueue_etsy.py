"""Enqueue ready sticker-liquidation ZIP bundles for Etsy API publishing.

This is a narrow bridge from the local sticker bundle builder into the existing
Etsy digital publisher queue. It does not publish or spend by itself.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
WORK_ROOT = DATABASE / "Sticker_Liquidation"
SUMMARY = WORK_ROOT / "Sticker_Liquidation_Pack_Summary.csv"
METADATA = WORK_ROOT / "Etsy_Sticker_Liquidation_Metadata.csv"
QUEUE = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
DIGITAL_METADATA = DATABASE / "Digital_Etsy_Metadata.csv"


QUEUE_FIELDS = [
    "Timestamp",
    "Batch_ID",
    "ID",
    "Title",
    "Price",
    "Zip_Path",
    "Zip_MB",
    "QA_Status",
    "QA_Reason",
    "Projected_Fee_USD",
    "Fee_Status",
    "Launch_Status",
    "Etsy_Listing_ID",
    "Notes",
    "Preview_Image",
    "Shadow_Status",
    "Shadow_Check_Due_At",
    "Shadow_Last_Checked_At",
    "Shadow_HTTP_Status",
    "Shadow_Public_URL",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def enqueue(limit: int) -> dict:
    summaries = {row.get("pack_id", ""): row for row in read_csv(SUMMARY)}
    metadata_rows = read_csv(METADATA)
    queue_rows = read_csv(QUEUE)
    digital_metadata = read_csv(DIGITAL_METADATA)
    queued_ids = {row.get("ID", "") for row in queue_rows}
    metadata_ids = {row.get("ID", "") for row in digital_metadata}
    metadata_changed = False
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    batch_id = f"STICKER-LIQ-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    added = []

    for row in metadata_rows:
        pack_id = row.get("pack_id", "")
        if not pack_id:
            continue
        summary = summaries.get(pack_id, {})
        if row.get("publish_guard") != "PASS_LOCAL_READY_NOT_PUBLISHED":
            continue
        if summary.get("status") != "READY":
            continue
        if not row.get("zip_path") or not row.get("preview_path"):
            continue
        if pack_id not in queued_ids:
            queue_rows.append(
                {
                    "Timestamp": now,
                    "Batch_ID": batch_id,
                    "ID": pack_id,
                    "Title": row.get("title", ""),
                    "Price": str(row.get("price", "")).replace("$", "") or "5.99",
                    "Zip_Path": row.get("zip_path", ""),
                    "Zip_MB": summary.get("zip_total_mb", ""),
                    "QA_Status": "PASS_STICKER_BUNDLE_LOCAL_READY",
                    "QA_Reason": f"{summary.get('asset_count', '')} PNG assets; {summary.get('etsy_file_count', '')} Etsy ZIP parts <=20MB each",
                    "Projected_Fee_USD": "0.20",
                    "Fee_Status": "",
                    "Launch_Status": "READY_API_PUBLISH",
                    "Etsy_Listing_ID": "",
                    "Notes": "Sticker liquidation digital bundle; specs in description; multi-part ZIP upload.",
                    "Preview_Image": row.get("preview_path", ""),
                    "Shadow_Status": "",
                    "Shadow_Check_Due_At": "",
                    "Shadow_Last_Checked_At": "",
                    "Shadow_HTTP_Status": "",
                    "Shadow_Public_URL": "",
                }
            )
            added.append(pack_id)
        if pack_id not in metadata_ids:
            digital_metadata.append(
                {
                    "Timestamp": now,
                    "ID": pack_id,
                    "Title": row.get("title", ""),
                    "Description": row.get("description", ""),
                    "Tags": row.get("tags", ""),
                    "Price": str(row.get("price", "")).replace("$", "") or "5.99",
                    "Zip_Path": row.get("zip_path", ""),
                    "Zip_MB": summary.get("zip_total_mb", ""),
                    "Status": "READY_STICKER_BUNDLE_API_QUEUE",
                    "Preview_Image": row.get("preview_path", ""),
                }
            )
            metadata_ids.add(pack_id)
            metadata_changed = True
        if len(added) >= limit:
            break

    if added:
        fields = list(queue_rows[0].keys()) if queue_rows else QUEUE_FIELDS
        for field in QUEUE_FIELDS:
            if field not in fields:
                fields.append(field)
        write_csv(QUEUE, queue_rows, fields)
    if metadata_changed and digital_metadata:
        meta_fields = list(digital_metadata[0].keys())
        for field in ["Timestamp", "ID", "Title", "Description", "Tags", "Price", "Zip_Path", "Zip_MB", "Status", "Preview_Image"]:
            if field not in meta_fields:
                meta_fields.append(field)
        write_csv(DIGITAL_METADATA, digital_metadata, meta_fields)
    return {"added": len(added), "ids": added, "queue": str(QUEUE)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()
    print(enqueue(args.limit))


if __name__ == "__main__":
    main()
