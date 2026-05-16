"""Move V7 Darwinian Lab upload packages into the guarded Etsy publish queue."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
UPLOAD_QUEUE = DATABASE / "Etsy_Darwinian_Lab_V7_Upload_Queue.csv"
GRAY_QUEUE = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
METADATA = DATABASE / "Digital_Etsy_Metadata.csv"

GRAY_FIELDS = [
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
]

METADATA_FIELDS = [
    "Timestamp",
    "ID",
    "Title",
    "Description",
    "Tags",
    "Price",
    "Zip_Path",
    "Zip_MB",
    "Status",
    "Preview_Image",
]


def now_text() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    all_fields = list(fields)
    for row in rows:
        for key in row:
            if key not in all_fields:
                all_fields.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=all_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def file_mb(path_text: str) -> str:
    path = Path(path_text)
    if not path.exists():
        return ""
    return f"{path.stat().st_size / (1024 * 1024):.2f}"


def is_publishable(row: dict[str, str]) -> bool:
    if row.get("Package_Status") != "READY_FOR_SPOTCHECK_NO_FEE_SPENT":
        return False
    if row.get("Publish_Status") == "PUBLISHED_UI_CONFIRMED":
        return False
    if not Path(row.get("Digital_Zip", "")).exists():
        return False
    if not Path(row.get("Preview_Image", "")).exists():
        return False
    return row.get("Launch_Readiness") in {"READY_FOR_METADATA_QA", "READY_AFTER_UPSCALE_REVIEW"}


def enqueue(limit: int) -> dict[str, int]:
    upload_rows = read_csv(UPLOAD_QUEUE)
    gray_rows = read_csv(GRAY_QUEUE)
    metadata_rows = read_csv(METADATA)
    queued_ids = {row.get("ID") for row in gray_rows}
    metadata_ids = {row.get("ID") for row in metadata_rows}
    batch_id = f"ETSY-V7-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    added = 0
    for row in upload_rows:
        if added >= limit:
            break
        item_id = row.get("Internal_SKU", "")
        if not item_id or item_id in queued_ids or not is_publishable(row):
            continue
        qa_note = "; ".join(part for part in [row.get("Visual_QA_Status"), row.get("Visual_QA_Flags"), row.get("Readiness_Note")] if part)
        gray_rows.append(
            {
                "Timestamp": now_text(),
                "Batch_ID": batch_id,
                "ID": item_id,
                "Title": row.get("Etsy_Title", ""),
                "Price": row.get("Price_USD", ""),
                "Zip_Path": row.get("Digital_Zip", ""),
                "Zip_MB": file_mb(row.get("Digital_Zip", "")),
                "QA_Status": "PASS",
                "QA_Reason": qa_note,
                "Projected_Fee_USD": "0.20",
                "Fee_Status": "RESERVED_NOT_SPENT",
                "Launch_Status": "READY_API_PUBLISH",
                "Etsy_Listing_ID": "",
                "Notes": f"V7 Darwinian Lab candidate from {row.get('Pool_ID')} / {row.get('Pool_Name')}.",
                "Preview_Image": row.get("Preview_Image", ""),
            }
        )
        if item_id not in metadata_ids:
            metadata_rows.append(
                {
                    "Timestamp": now_text(),
                    "ID": item_id,
                    "Title": row.get("Etsy_Title", ""),
                    "Description": row.get("Etsy_Description", ""),
                    "Tags": row.get("Etsy_Tags", ""),
                    "Price": row.get("Price_USD", ""),
                    "Zip_Path": row.get("Digital_Zip", ""),
                    "Zip_MB": file_mb(row.get("Digital_Zip", "")),
                    "Status": "READY_API_PUBLISH",
                    "Preview_Image": row.get("Preview_Image", ""),
                }
            )
        queued_ids.add(item_id)
        added += 1
    write_csv(GRAY_QUEUE, gray_rows, GRAY_FIELDS)
    write_csv(METADATA, metadata_rows, METADATA_FIELDS)
    return {"added": added, "gray_rows": len(gray_rows), "metadata_rows": len(metadata_rows)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=4)
    args = parser.parse_args()
    print(enqueue(args.limit))


if __name__ == "__main__":
    main()
