"""Recover Adobe Stock local-upscaled candidate index from files on disk.

The daily MJ queue can be rebuilt for a new date, but already harvested and
locally upscaled images remain in Output/Adobe_Stock/Daily_Production_Upscaled.
This recovery pass reattaches metadata, Rex visual decisions, and submission
ledger state so upload-ready packaging never collapses to zero simply because
the active queue rolled over.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from adobe_stock_quality_policy import validate_adobe_production_image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
SOURCE_META = DATABASE / "Adobe_Stock_Daily_Production_Queue.csv"
REX_QA = DATABASE / "Adobe_Stock_Rex_Visual_QA.csv"
LEDGER = DATABASE / "Adobe_Stock_Submission_Ledger.csv"
OUT = DATABASE / "Adobe_Stock_Local_Upscaled_Candidates.csv"
REPORT = REVIEW / "Adobe_Stock_Local_Upscaled_Candidates_Recovered_latest.md"
UPSCALED_DIR = PROJECT_ROOT / "Output" / "Adobe_Stock" / "Daily_Production_Upscaled"
ET = ZoneInfo("America/New_York")

FIELDS = [
    "Asset_ID",
    "Parent_Asset_ID",
    "Family",
    "Title",
    "Keywords",
    "Category",
    "Created_Using_AI",
    "Source_Path",
    "Upscaled_Path",
    "Source_Width",
    "Source_Height",
    "Width",
    "Height",
    "Pixels",
    "File_Bytes",
    "Edge_Detail_Score",
    "Sharp_Tile_Coverage",
    "QA_Status",
    "Upload_Status",
    "Issues",
]

FILENAME_RE = re.compile(
    r"^adobe_stock_(?P<date>\d{8})_(?P<seq>\d{3})_(?P<variant>u[1-4])_3000x2000\.(?:jpg|jpeg)$",
    re.IGNORECASE,
)


def now_text() -> str:
    return datetime.now(ET).strftime("%Y-%m-%d %H:%M:%S %Z")


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\r", " ").replace("\n", " ").split()).strip()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def existing_index() -> dict[str, dict[str, str]]:
    """Reuse prior image metrics when the recovered file did not change.

    Full edge/tile sharpness scoring across hundreds of 3000x2000 images is
    intentionally expensive. The recovery task may run many times inside the
    long shift, so it should only rescore files whose bytes changed.
    """
    rows: dict[str, dict[str, str]] = {}
    for row in read_rows(OUT):
        key = clean(row.get("Upscaled_Path"))
        if key:
            rows[key] = row
    return rows


def metadata_by_sequence() -> dict[str, dict[str, str]]:
    by_seq: dict[str, dict[str, str]] = {}
    for row in read_rows(SOURCE_META):
        queue_id = clean(row.get("Queue_ID"))
        seq = queue_id.rsplit("-", 1)[-1]
        if seq:
            by_seq.setdefault(seq, row)
    return by_seq


def rex_decisions() -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    for row in read_rows(REX_QA):
        parent = clean(row.get("Parent_Asset_ID"))
        if parent:
            out[parent] = (clean(row.get("Decision")).upper(), clean(row.get("Reason")))
    return out


def ledger_statuses() -> dict[str, str]:
    statuses: dict[str, str] = {}
    for row in read_rows(LEDGER):
        filename = clean(row.get("Filename")).lower()
        status = clean(row.get("Status")).upper()
        if filename and status:
            statuses[filename] = status
    return statuses


def pending_source_path(date: str, seq: str, variant: str) -> Path:
    return PROJECT_ROOT / "adobe_stock_factory" / "Pending_Upscale" / f"adobe_stock_{date}_{seq}_{variant.lower()}.png"


def build() -> list[dict[str, str]]:
    meta = metadata_by_sequence()
    decisions = rex_decisions()
    ledger = ledger_statuses()
    prior_index = existing_index()
    rows: list[dict[str, str]] = []
    for path in sorted(UPSCALED_DIR.glob("adobe_stock_*_3000x2000.jpg")):
        match = FILENAME_RE.match(path.name)
        if not match:
            continue
        date = match.group("date")
        seq = match.group("seq")
        variant = match.group("variant").upper()
        source_meta = meta.get(seq, {})
        parent_id = f"ADOBE-STOCK-{date}-{seq}-{variant}"
        asset_id = f"{parent_id}-LOCAL3000"
        pending_source = pending_source_path(date, seq, variant)
        filename_for_ledger = path.name.replace("_", "-").replace("-3000x2000", "")
        filename_for_ledger = filename_for_ledger.lower()
        filename_for_ledger = filename_for_ledger.replace("adobe-stock-", "adobe-stock-")
        filename_for_ledger = filename_for_ledger.replace(".jpeg", ".jpg")
        # Ledger/upload folders use adobe-stock-YYYYMMDD-NNN-uX.jpg.
        filename_for_ledger = f"adobe-stock-{date}-{seq}-{variant.lower()}.jpg"

        upscaled_rel = str(path.relative_to(PROJECT_ROOT))
        previous = prior_index.get(upscaled_rel, {})
        if previous and previous.get("File_Bytes") == str(path.stat().st_size) and previous.get("Width"):
            info = {
                "Width": previous.get("Width", ""),
                "Height": previous.get("Height", ""),
                "Pixels": previous.get("Pixels", ""),
                "File_Bytes": previous.get("File_Bytes", ""),
                "Edge_Detail_Score": previous.get("Edge_Detail_Score", ""),
                "Sharp_Tile_Coverage": previous.get("Sharp_Tile_Coverage", ""),
                "Quality_Reasons": previous.get("Issues", ""),
            }
            qa_status = previous.get("QA_Status") or "HOLD_UNKNOWN_PRIOR_QA"
            ok = qa_status.startswith("QA_PASS")
        else:
            row_for_qa = {
                "Source_Provenance": "local_resolution_upscale_from_mj_u_button",
                "Status": "local_resolution_upscale",
                "MJ_Prompt": clean(source_meta.get("MJ_Prompt")),
                "Prompt": clean(source_meta.get("MJ_Prompt")),
                "Source_Path": str(pending_source.relative_to(PROJECT_ROOT)) if pending_source.exists() else "",
            }
            ok, qa_status, info = validate_adobe_production_image(path, row_for_qa)
        decision, note = decisions.get(parent_id, ("PENDING", ""))
        ledger_status = ledger.get(filename_for_ledger, "")
        upload_status = "QA_PASS_NOT_UPLOADED" if ok else "HOLD_DO_NOT_UPLOAD"
        issues = info.get("Quality_Reasons") or info.get("File_Size_Warning") or ""
        if ledger_status:
            upload_status = ledger_status
        elif decision == "REJECT":
            qa_status = "HOLD_REX_REJECTED_NO_UPLOAD"
            upload_status = "HOLD_DO_NOT_UPLOAD"
            issues = ";".join(part for part in (issues, "REX_REJECTED_VISUAL_DIRECTION", note) if part)
        elif decision == "HOLD":
            qa_status = "HOLD_REX_REVIEW_NO_UPLOAD"
            upload_status = "HOLD_DO_NOT_UPLOAD"
            issues = ";".join(part for part in (issues, "REX_HELD_FOR_REVIEW", note) if part)

        rows.append(
            {
                "Asset_ID": asset_id,
                "Parent_Asset_ID": parent_id,
                "Family": clean(source_meta.get("Family")) or f"Sequence {seq}",
                "Title": clean(source_meta.get("Adobe_Title")) or "High resolution texture background",
                "Keywords": clean(source_meta.get("Adobe_Keywords")) or "texture background,background,texture,abstract,design,commercial use",
                "Category": clean(source_meta.get("Adobe_Category")) or "8",
                "Created_Using_AI": clean(source_meta.get("Created_Using_AI")) or "true",
                "Source_Path": str(pending_source.relative_to(PROJECT_ROOT)) if pending_source.exists() else "",
                "Upscaled_Path": upscaled_rel,
                "Source_Width": "",
                "Source_Height": "",
                "Width": info.get("Width", ""),
                "Height": info.get("Height", ""),
                "Pixels": info.get("Pixels", ""),
                "File_Bytes": info.get("File_Bytes", ""),
                "Edge_Detail_Score": info.get("Edge_Detail_Score", ""),
                "Sharp_Tile_Coverage": info.get("Sharp_Tile_Coverage", ""),
                "QA_Status": qa_status,
                "Upload_Status": upload_status,
                "Issues": issues,
            }
        )
    return rows


def write_report(rows: list[dict[str, str]]) -> None:
    qa_counts = Counter(row.get("QA_Status", "") for row in rows)
    upload_counts = Counter(row.get("Upload_Status", "") for row in rows)
    ready = [
        row
        for row in rows
        if row.get("QA_Status", "").startswith("QA_PASS")
        and row.get("Upload_Status") == "QA_PASS_NOT_UPLOADED"
    ]
    lines = [
        "# Adobe Stock Local Upscaled Candidate Recovery",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Existing local-upscaled files indexed: {len(rows)}",
        f"- Ready and not yet uploaded/submitted: {len(ready)}",
        f"- QA status: {dict(qa_counts)}",
        f"- Upload/ledger status: {dict(upload_counts)}",
        f"- Output CSV: `{OUT.relative_to(PROJECT_ROOT)}`",
        "",
        "## Policy",
        "",
        "- This is local index recovery only; no Adobe upload, no marketplace write, no paid action.",
        "- Ledger submitted/pending files remain blocked from new upload packs.",
        "- Rex rejected/held assets stay out of upload packs even if mechanically sharp.",
        "",
        "## First Ready Rows",
        "",
    ]
    for row in ready[:25]:
        lines.append(f"- {row['Parent_Asset_ID']} | {row['Family']} | {row['Upscaled_Path']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    ready = sum(
        1
        for row in rows
        if row.get("QA_Status", "").startswith("QA_PASS")
        and row.get("Upload_Status") == "QA_PASS_NOT_UPLOADED"
    )
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock recovered existing local-upscaled index; "
            f"indexed={len(rows)}; ready_not_uploaded={ready}; no upload/spend.\n"
        )


def main() -> int:
    rows = build()
    write_rows(OUT, rows)
    write_report(rows)
    append_progress(rows)
    ready = sum(
        1
        for row in rows
        if row.get("QA_Status", "").startswith("QA_PASS")
        and row.get("Upload_Status") == "QA_PASS_NOT_UPLOADED"
    )
    print(f"[ADOBE-RECOVER-UPSCALED] indexed={len(rows)} ready_not_uploaded={ready} csv={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
