"""Prepare a concrete Adobe Stock pilot batch.

This is a local-only bridge between the Adobe pilot queue and the first
submission batch. It does not upload, spend, or touch any marketplace.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from adobe_stock_isolation import assert_adobe_write_paths


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

PILOT_QUEUE = DATABASE / "Adobe_Stock_Pilot_Queue.csv"
DAILY_QUEUE = DATABASE / "Adobe_Stock_Daily_Production_Queue.csv"
PRODUCTION_LINE = DATABASE / "Adobe_Stock_Production_Line.csv"
OUT_BATCH = DATABASE / "Adobe_Stock_Pilot_Batch.csv"
OUT_PACKET = REVIEW / "Adobe_Stock_Pilot_Batch_latest.md"

DEFAULT_TARGET = 25
STOCK_PRODUCT_PRIORITY = {
    "Stock_Texture": 1,
    "Stock_Background": 2,
    "Stock_Seamless_Pattern": 3,
    "Stock_Isolated_Material": 4,
}
KEYWORD_TAIL = [
    "commercial use",
    "design resource",
    "digital background",
    "decorative surface",
    "high resolution",
    "stock image",
    "graphic resource",
    "material study",
    "surface design",
    "abstract art",
    "visual texture",
    "printable background",
    "modern decor",
    "creative asset",
    "tactile design",
    "sensory texture",
    "interior backdrop",
    "branding background",
    "editorial layout",
    "presentation background",
    "web banner",
    "social media design",
    "packaging design",
    "premium material",
    "copy space",
    "design template",
    "neutral backdrop",
    "decorative pattern",
    "creative workspace",
    "marketing background",
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in (DAILY_QUEUE, PRODUCTION_LINE, PILOT_QUEUE):
        for row in read_csv(path):
            key = row.get("Queue_ID") or row.get("Asset_ID") or row.get("Expanded_DNA_ID") or str(row)
            if key in seen:
                continue
            seen.add(key)
            rows.append(row)
    return rows


def row_sort_key(row: dict[str, str]) -> tuple[int, str]:
    product_type = row.get("Product_Type", "") or row.get("Asset_Type", "")
    family = row.get("Family", "")
    return (STOCK_PRODUCT_PRIORITY.get(product_type, 99), family)


def normalize_keywords(value: str) -> str:
    seen: set[str] = set()
    keywords: list[str] = []
    for raw in [*value.replace(";", ",").split(","), *KEYWORD_TAIL]:
        keyword = " ".join(raw.strip().lower().split())
        if not keyword or keyword in seen:
            continue
        seen.add(keyword)
        keywords.append(keyword)
        if len(keywords) >= 50:
            break
    return ",".join(keywords)


def select_balanced_rows(rows: list[dict[str, str]], target: int, max_per_family: int = 4) -> list[dict[str, str]]:
    buckets: dict[str, list[dict[str, str]]] = {}
    for row in sorted(rows, key=row_sort_key):
        family = row.get("Family", "").strip() or "unknown"
        buckets.setdefault(family, []).append(row)

    selected: list[dict[str, str]] = []
    family_counts: dict[str, int] = {}
    while buckets and len(selected) < target:
        progressed = False
        for family in sorted(list(buckets)):
            if len(selected) >= target:
                break
            if family_counts.get(family, 0) >= max_per_family:
                buckets.pop(family, None)
                continue
            bucket = buckets.get(family, [])
            if not bucket:
                buckets.pop(family, None)
                continue
            selected.append(bucket.pop(0))
            family_counts[family] = family_counts.get(family, 0) + 1
            progressed = True
            if not bucket:
                buckets.pop(family, None)
        if not progressed:
            break

    if len(selected) < target:
        selected_keys = {row.get("Queue_ID") or row.get("Asset_ID") or row.get("Expanded_DNA_ID") or str(row) for row in selected}
        for row in sorted(rows, key=row_sort_key):
            key = row.get("Queue_ID") or row.get("Asset_ID") or row.get("Expanded_DNA_ID") or str(row)
            if key in selected_keys:
                continue
            selected.append(row)
            if len(selected) >= target:
                break
    return selected[:target]


def normalize_row(row: dict[str, str], index: int, mode: str) -> dict[str, str]:
    queue_id = row.get("Asset_ID") or row.get("ID") or f"ADOBE-PILOT-{index:04d}"
    source_path = row.get("Source_Path", "").strip()
    qa_status = row.get("QA_Status", "PENDING_IMAGE").strip() or "PENDING_IMAGE"
    upload_status = row.get("Upload_Status", "BLOCKED_UNTIL_IMAGE_QA").strip()
    if source_path and qa_status.startswith("QA_PASS"):
        batch_status = "READY_FOR_METADATA_QA_NOT_UPLOADED"
        next_action = "Run metadata QA, then submit only after Rex/guard approval."
    elif source_path:
        batch_status = "READY_FOR_IMAGE_QA_NOT_UPLOADED"
        next_action = "Run image QA before any Adobe CSV submission."
    else:
        batch_status = "READY_FOR_MJ_RELAXED_DRAFT_NO_UPLOAD"
        next_action = "Generate 4K stock asset in MJ relaxed mode, then attach Source_Path."

    keywords = normalize_keywords(row.get("Adobe_Keywords", ""))
    return {
        "Batch_ID": f"ADOBE-BATCH-{index:04d}",
        "Queue_ID": queue_id,
        "Mode": mode,
        "Status": batch_status,
        "Family": row.get("Family", ""),
        "Product_Type": row.get("Product_Type") or row.get("Asset_Type", ""),
        "Target_Filename": row.get("Target_Filename", ""),
        "Source_Path": source_path,
        "QA_Status": qa_status,
        "Upload_Status": upload_status,
        "Adobe_Title": row.get("Adobe_Title", ""),
        "Adobe_Keywords": keywords,
        "Adobe_Category": row.get("Adobe_Category", ""),
        "Created_Using_AI": row.get("Created_Using_AI", "true"),
        "Release_Required": row.get("Release_Required", "false"),
        "MJ_Prompt": row.get("MJ_Prompt") or row.get("Prompt", ""),
        "Next_Action": next_action,
    }


def build_batch(target: int, mode: str) -> list[dict[str, str]]:
    rows = source_rows()
    if not rows:
        raise RuntimeError("No Adobe Stock source rows found. Run adobe_stock_scaffold.py and adobe_stock_pilot_queue.py first.")
    usable = [
        row
        for row in rows
        if "HOLD" not in (row.get("QA_Status", "") + row.get("Upload_Status", "") + row.get("Status", "")).upper()
    ]
    selected = select_balanced_rows(usable, target)
    return [normalize_row(row, index, mode) for index, row in enumerate(selected, start=1)]


def write_packet(batch: list[dict[str, str]], mode: str) -> None:
    family_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for row in batch:
        family_counts[row["Family"]] = family_counts.get(row["Family"], 0) + 1
        status_counts[row["Status"]] = status_counts.get(row["Status"], 0) + 1

    lines = [
        "# Adobe Stock Pilot Batch",
        "",
        f"Generated: {now_text()}",
        f"Mode: {mode}",
        "",
        "## Output",
        "",
        f"- Batch rows: {len(batch)}",
        f"- Batch CSV: `{OUT_BATCH.relative_to(PROJECT_ROOT)}`",
        "",
        "## Status Counts",
        "",
    ]
    lines.extend(f"- {status}: {count}" for status, count in sorted(status_counts.items()))
    lines.extend(["", "## Family Mix", ""])
    lines.extend(f"- {family}: {count}" for family, count in sorted(family_counts.items()))
    lines.extend(
        [
            "",
            "## Hard Guards",
            "",
            "- This batch is local prep only: no upload, no spend, no marketplace write.",
            "- Keep Adobe Stock assets store-agnostic; do not reuse Etsy, eBay, Printify, or First Audit hero assets.",
            "- Every submitted file must be marked as created using generative AI tools in Adobe Contributor.",
            "- Do not submit rows until image QA and metadata QA both pass.",
            "",
            "## Next Step",
            "",
            "Run `py .\\modules\\adobe_stock_metadata_qa.py --limit 50`, then generate only QA-clean rows.",
        ]
    )
    OUT_PACKET.parent.mkdir(parents=True, exist_ok=True)
    OUT_PACKET.write_text("\n".join(lines), encoding="utf-8")


def append_progress(batch: list[dict[str, str]], mode: str) -> None:
    ready_for_mj = sum(1 for row in batch if row["Status"] == "READY_FOR_MJ_RELAXED_DRAFT_NO_UPLOAD")
    ready_for_qa = sum(1 for row in batch if row["Status"] == "READY_FOR_IMAGE_QA_NOT_UPLOADED")
    ready_for_meta = sum(1 for row in batch if row["Status"] == "READY_FOR_METADATA_QA_NOT_UPLOADED")
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock pilot batch prepared; rows={len(batch)}; "
            f"mode={mode}; ready_for_mj={ready_for_mj}; ready_for_image_qa={ready_for_qa}; "
            f"ready_for_metadata_qa={ready_for_meta}; no upload/spend.\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=DEFAULT_TARGET)
    parser.add_argument("--mode", choices=["prepare", "refresh"], default="prepare")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    assert_adobe_write_paths((OUT_BATCH, OUT_PACKET))
    batch = build_batch(args.target, args.mode)
    if not args.dry_run:
        write_csv(OUT_BATCH, batch)
        write_packet(batch, args.mode)
        append_progress(batch, args.mode)
    print(
        f"[ADOBE-BATCH] rows={len(batch)} mode={args.mode} dry_run={args.dry_run} "
        f"ready_for_mj={sum(1 for row in batch if row['Status'] == 'READY_FOR_MJ_RELAXED_DRAFT_NO_UPLOAD')} "
        f"batch={OUT_BATCH}"
    )


if __name__ == "__main__":
    main()
