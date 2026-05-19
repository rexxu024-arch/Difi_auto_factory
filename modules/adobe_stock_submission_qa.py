"""Reconcile Adobe Stock submitted/pending upload folders against local QA.

This is a local-only audit. It never opens Adobe Contributor, uploads files,
or changes the submission ledger. Its job is to keep Rex-facing state honest:
which files are already submitted, which are pending human/captcha handling,
and whether the local image/CSV packets remain mechanically sound.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image

from adobe_stock_isolation import assert_adobe_write_paths
from adobe_stock_quality_policy import validate_adobe_production_image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
FACTORY = PROJECT_ROOT / "adobe_stock_factory" / "upload_ready"
HOLD_FACTORY = PROJECT_ROOT / "adobe_stock_factory" / "hold_training_reference_not_for_submit"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
LEDGER = DATABASE / "Adobe_Stock_Submission_Ledger.csv"
OUT = DATABASE / "Adobe_Stock_Submission_QA.csv"
REPORT = REVIEW / "Adobe_Stock_Submission_QA_latest.md"
NY_TZ = ZoneInfo("America/New_York")

PUBLIC_BAN_TERMS = {
    "openclaw",
    "first audit",
    "sweatshop",
    "etsy",
    "ebay",
    "printify",
    "midjourney",
    "codex",
    "gemini",
    "claude",
    "deepseek",
    "dify",
    "rex",
    "grey",
}

FIELDS = [
    "Filename",
    "Batch",
    "Ledger_Status",
    "Local_File",
    "File_Exists",
    "Width",
    "Height",
    "Pixels",
    "Format",
    "File_Bytes",
    "Edge_Detail_Score",
    "Sharp_Tile_Coverage",
    "Metadata_CSV",
    "Title",
    "Keyword_Count",
    "Created_Using_AI_Local_Assumption",
    "Public_Metadata_Status",
    "Image_QA_Status",
    "Duplicate_Status",
    "Packet_QA_Status",
    "Issues",
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


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


def folder_for(batch: str) -> Path:
    for root in (FACTORY, HOLD_FACTORY):
        direct = root / batch
        if direct.exists():
            return direct
    for root in (FACTORY, HOLD_FACTORY):
        matches = sorted(path for path in root.glob(f"*{batch}*") if path.is_dir())
        if matches:
            return matches[0]
    return FACTORY / batch


def metadata_rows_by_folder(folder: Path) -> dict[str, tuple[Path, dict[str, str]]]:
    rows: dict[str, tuple[Path, dict[str, str]]] = {}
    if not folder.exists():
        return rows
    for csv_path in sorted(folder.glob("*.csv")):
        for row in read_rows(csv_path):
            filename = clean(row.get("Filename")).lower()
            if filename:
                rows.setdefault(filename, (csv_path, row))
    return rows


def safe_project_path(path: Path) -> str:
    if not path or str(path) == ".":
        return ""
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT))
    except (OSError, ValueError):
        return str(path)


def public_metadata_status(title: str, keywords: str) -> tuple[str, str]:
    text = f"{title} {keywords}".lower()
    hits = sorted(term for term in PUBLIC_BAN_TERMS if term in text)
    if hits:
        return "HOLD_PUBLIC_BAN_TERM", ", ".join(hits)
    keyword_count = len([part for part in keywords.split(",") if clean(part)])
    if keyword_count < 15:
        return "HOLD_TOO_FEW_KEYWORDS", f"keyword_count={keyword_count}"
    if len(title) > 70:
        return "HOLD_TITLE_OVER_70_CHARS", f"title_len={len(title)}"
    return "PASS_PUBLIC_METADATA_LOCAL", ""


def average_hash(path: Path) -> str:
    with Image.open(path) as image:
        gray = image.convert("L").resize((8, 8))
        pixels = list(gray.getdata())
    avg = sum(pixels) / len(pixels)
    bits = "".join("1" if pixel >= avg else "0" for pixel in pixels)
    return f"{int(bits, 2):016x}"


def hamming_hex(left: str, right: str) -> int:
    return bin(int(left, 16) ^ int(right, 16)).count("1")


def build(limit: int = 0) -> list[dict[str, str]]:
    assert_adobe_write_paths((OUT, REPORT))
    ledger_rows = read_rows(LEDGER)
    if limit:
        ledger_rows = ledger_rows[:limit]
    folder_cache: dict[str, dict[str, tuple[Path, dict[str, str]]]] = {}
    output: list[dict[str, str]] = []
    seen_hashes: list[tuple[str, str]] = []

    for row in ledger_rows:
        filename = clean(row.get("Filename"))
        batch = clean(row.get("Batch"))
        folder = folder_for(batch)
        image_path = folder / filename
        metadata_rows = folder_cache.setdefault(batch, metadata_rows_by_folder(folder))
        csv_path, metadata = metadata_rows.get(filename.lower(), (Path(), {}))
        title = clean(metadata.get("Title"))
        keywords = clean(metadata.get("Keywords"))
        keyword_count = len([part for part in keywords.split(",") if clean(part)])
        metadata_status, metadata_issue = public_metadata_status(title, keywords)
        issues: list[str] = []
        if metadata_issue:
            issues.append(metadata_issue)
        if not metadata:
            issues.append("filename missing from batch Adobe CSV")

        qa_status = "HOLD_FILE_MISSING"
        duplicate_status = "NOT_CHECKED"
        info: dict[str, str] = {}
        file_exists = image_path.exists()
        if file_exists:
            ok, qa_status, info = validate_adobe_production_image(
                image_path,
                {},
                require_macro_prompt=False,
                require_upscale_provenance=False,
            )
            if info.get("Quality_Reasons"):
                issues.append(info["Quality_Reasons"])
            try:
                current_hash = average_hash(image_path)
                duplicate_status = "PASS_UNIQUE_WITHIN_LEDGER"
                for prior_filename, prior_hash in seen_hashes:
                    distance = hamming_hex(current_hash, prior_hash)
                    if distance <= 4:
                        duplicate_status = f"WARN_NEAR_DUPLICATE_OF:{prior_filename}:HAMMING_{distance}"
                        break
                seen_hashes.append((filename, current_hash))
            except Exception as exc:  # noqa: BLE001
                duplicate_status = f"WARN_HASH_ERROR:{type(exc).__name__}"
        else:
            issues.append("local image file missing")

        packet_status = "PASS_SUBMITTED_OR_PENDING_PACKET_QA"
        if not file_exists or not qa_status.startswith("QA_PASS") or not metadata_status.startswith("PASS"):
            packet_status = "HOLD_PACKET_QA_REVIEW"
        elif duplicate_status.startswith("WARN_NEAR_DUPLICATE"):
            packet_status = "PASS_WITH_SIMILAR_CONTENT_WARNING"

        output.append(
            {
                "Filename": filename,
                "Batch": batch,
                "Ledger_Status": clean(row.get("Status")),
                "Local_File": safe_project_path(image_path) if image_path.exists() else str(image_path),
                "File_Exists": "yes" if file_exists else "no",
                "Width": info.get("Width", ""),
                "Height": info.get("Height", ""),
                "Pixels": info.get("Pixels", ""),
                "Format": info.get("Format", ""),
                "File_Bytes": info.get("File_Bytes", ""),
                "Edge_Detail_Score": info.get("Edge_Detail_Score", ""),
                "Sharp_Tile_Coverage": info.get("Sharp_Tile_Coverage", ""),
                "Metadata_CSV": safe_project_path(csv_path),
                "Title": title,
                "Keyword_Count": str(keyword_count),
                "Created_Using_AI_Local_Assumption": "must be checked in Adobe Contributor; local CSV cannot set checkbox",
                "Public_Metadata_Status": metadata_status,
                "Image_QA_Status": qa_status,
                "Duplicate_Status": duplicate_status,
                "Packet_QA_Status": packet_status,
                "Issues": " | ".join(issues),
            }
        )
    return output


def write_report(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row.get("Packet_QA_Status", "") for row in rows)
    ledger_counts = Counter(row.get("Ledger_Status", "") for row in rows)
    batch_counts = Counter(row.get("Batch", "") for row in rows)
    pending = [row for row in rows if "PENDING_HUMAN_VERIFICATION" in row.get("Ledger_Status", "")]
    lines = [
        "# Adobe Stock Submission QA",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Ledger rows checked: {len(rows)}",
        f"- Packet QA status: {dict(status_counts)}",
        f"- Ledger status: {dict(ledger_counts)}",
        f"- Batch mix: {dict(batch_counts)}",
        f"- Pending human/captcha verification: {len(pending)}",
        "",
        "## Guard Decision",
        "",
    ]
    if pending:
        lines.append("- Do not upload or submit additional Adobe batches until the existing pending-human/captcha batch is resolved or intentionally abandoned.")
    elif rows and all(row.get("Packet_QA_Status", "").startswith("PASS") for row in rows):
        lines.append("- Local packets are mechanically sound; wait for Adobe acceptance/rejection feedback before scaling.")
    else:
        lines.append("- Local packet issues exist; resolve holds before any further Adobe upload.")
    lines.extend(["", "## Rows Needing Attention", ""])
    attention = [row for row in rows if not row.get("Packet_QA_Status", "").startswith("PASS_SUBMITTED")]
    if not attention:
        lines.append("- None.")
    for row in attention[:25]:
        lines.append(
            f"- {row['Filename']} | {row['Packet_QA_Status']} | {row['Ledger_Status']} | "
            f"{row['Duplicate_Status']} | {row['Issues']}"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row.get("Packet_QA_Status", "") for row in rows)
    pending = sum(1 for row in rows if "PENDING_HUMAN_VERIFICATION" in row.get("Ledger_Status", ""))
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock submission QA reconciled; rows={len(rows)}; "
            f"packet_status={dict(status_counts)}; pending_human_verification={pending}; no upload/spend.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    rows = build(limit=max(0, args.limit))
    write_rows(OUT, rows)
    write_report(rows)
    append_progress(rows)
    print(f"[ADOBE-SUBMISSION-QA] rows={len(rows)} csv={OUT} report={REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
