"""Build a Midjourney dispatch queue for the V7 Etsy Darwinian Lab.

This module converts the no-fee concept queue into a production queue that can
be consumed by the existing Shock & Awe Midjourney dispatcher/harvester. It does
not publish listings and does not spend Etsy listing fees.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATABASE = ROOT / "Database"
SOURCE_QUEUE = DATABASE / "Etsy_Darwinian_Lab_V7_Queue.csv"
MJ_QUEUE = DATABASE / "Etsy_Darwinian_Lab_V7_MJ_Dispatch_Queue.csv"
NY_TZ = ZoneInfo("America/New_York")

MJ_FIELDS = [
    "Internal_SKU",
    "Source_SKU",
    "Track",
    "Pool_ID",
    "Pool_Name",
    "Concept_Name",
    "Listing_Type",
    "Format",
    "Price_USD",
    "Etsy_Title",
    "Etsy_Tags",
    "Etsy_Description",
    "Constraint_Profile",
    "MJ_Master_Prompt",
    "QA_Requirements",
    "Output_Folder",
    "Dispatch_Status",
    "Dispatched_At_ET",
    "Dispatch_Error",
    "Harvest_Status",
    "Harvest_Error",
    "Grid_Message_ID",
    "Grid_File",
    "U1_File",
    "U2_File",
    "U3_File",
    "U4_File",
    "Last_Harvest_ET",
    "Visual_QA_Status",
    "Publish_Status",
    "Created_At_ET",
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %z")


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\n", " ").replace("\r", " ").split()).strip()


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing queue: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_existing_status() -> dict[str, dict[str, str]]:
    if not MJ_QUEUE.exists():
        return {}
    rows, _ = read_csv(MJ_QUEUE)
    return {clean(row.get("Internal_SKU")): row for row in rows if clean(row.get("Internal_SKU"))}


def selected_source_rows(
    source_rows: list[dict[str, str]],
    per_pool: int,
    limit: int | None,
    existing_skus: set[str],
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    pool_counts: dict[str, int] = defaultdict(int)
    for row in source_rows:
        sku = clean(row.get("SKU"))
        if not sku or sku in existing_skus:
            continue
        if clean(row.get("Asset_Status")) not in {"", "STAGED_CONCEPT_ONLY"}:
            continue
        pool_id = clean(row.get("Pool_ID"))
        if pool_counts[pool_id] >= per_pool:
            continue
        selected.append(row)
        pool_counts[pool_id] += 1
        if limit and len(selected) >= limit:
            break
    return selected


def build_mj_row(row: dict[str, str], existing: dict[str, str] | None = None) -> dict[str, str]:
    sku = clean(row.get("SKU"))
    existing = existing or {}
    out = f"Output/Etsy/Darwinian_Lab/V7/{sku}"
    return {
        "Internal_SKU": sku,
        "Source_SKU": sku,
        "Track": clean(row.get("Track")),
        "Pool_ID": clean(row.get("Pool_ID")),
        "Pool_Name": clean(row.get("Pool_Name")),
        "Concept_Name": clean(row.get("Concept_Name")),
        "Listing_Type": clean(row.get("Listing_Type")),
        "Format": clean(row.get("Format")),
        "Price_USD": clean(row.get("Price_USD")),
        "Etsy_Title": clean(row.get("Etsy_Title")),
        "Etsy_Tags": clean(row.get("Etsy_Tags")),
        "Etsy_Description": clean(row.get("Etsy_Description")),
        "Constraint_Profile": clean(row.get("Constraint_Profile")),
        "MJ_Master_Prompt": clean(row.get("MJ_Master_Prompt")),
        "QA_Requirements": clean(row.get("QA_Requirements")),
        "Output_Folder": existing.get("Output_Folder") or out,
        "Dispatch_Status": existing.get("Dispatch_Status") or "READY_FOR_MJ",
        "Dispatched_At_ET": existing.get("Dispatched_At_ET") or "",
        "Dispatch_Error": existing.get("Dispatch_Error") or "",
        "Harvest_Status": existing.get("Harvest_Status") or "",
        "Harvest_Error": existing.get("Harvest_Error") or "",
        "Grid_Message_ID": existing.get("Grid_Message_ID") or "",
        "Grid_File": existing.get("Grid_File") or "",
        "U1_File": existing.get("U1_File") or "",
        "U2_File": existing.get("U2_File") or "",
        "U3_File": existing.get("U3_File") or "",
        "U4_File": existing.get("U4_File") or "",
        "Last_Harvest_ET": existing.get("Last_Harvest_ET") or "",
        "Visual_QA_Status": existing.get("Visual_QA_Status") or "PENDING_IMAGE_GENERATION",
        "Publish_Status": existing.get("Publish_Status") or "NOT_PUBLISHED_NO_FEE_SPENT",
        "Created_At_ET": existing.get("Created_At_ET") or now_text(),
    }


def update_source_status(source_rows: list[dict[str, str]], source_fields: list[str], selected: list[dict[str, str]]) -> None:
    selected_skus = {clean(row.get("SKU")) for row in selected}
    for field in ["Asset_Status", "Publish_Status"]:
        if field not in source_fields:
            source_fields.append(field)
    for row in source_rows:
        if clean(row.get("SKU")) in selected_skus:
            row["Asset_Status"] = "QUEUED_FOR_MJ"
            row["Publish_Status"] = "NOT_PUBLISHED_ASSET_GENERATION"
    write_csv(SOURCE_QUEUE, source_rows, source_fields)


def build_queue(per_pool: int = 1, limit: int | None = None) -> int:
    source_rows, source_fields = read_csv(SOURCE_QUEUE)
    existing = load_existing_status()
    selected = selected_source_rows(source_rows, max(1, per_pool), limit, set(existing))
    if not selected:
        print("[ETSY-V7-MJ-IDLE] no source rows selected")
        return 0
    rows = list(existing.values()) + [build_mj_row(row, existing.get(clean(row.get("SKU")))) for row in selected]
    write_csv(MJ_QUEUE, rows, MJ_FIELDS)
    update_source_status(source_rows, source_fields, selected)
    print(f"[ETSY-V7-MJ-QUEUE] rows={len(rows)} per_pool={per_pool} csv={MJ_QUEUE}")
    for row in rows:
        print(f"[ETSY-V7-MJ-QUEUE] {row['Internal_SKU']} {row['Pool_ID']} {row['Concept_Name']} status={row['Dispatch_Status']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build V7 Etsy Darwinian Lab MJ dispatch queue")
    parser.add_argument("--per-pool", type=int, default=1)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    return build_queue(per_pool=args.per_pool, limit=args.limit or None)


if __name__ == "__main__":
    raise SystemExit(main())
