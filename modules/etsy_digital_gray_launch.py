"""Stage and guard Etsy digital printable gray-launch batches.

This module is intentionally conservative with money: it can prepare a paid
Etsy launch queue, but it records listing fees as spent only after a confirmed
publish/create response. If Etsy auth/account risk is not clear, the batch is
staged and blocked before fee spend.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.image_quality_gate import _metrics, _verdict
from modules.risk_guard import RiskBlocked, assert_allowed, assert_etsy_fee_batch_allowed, fee_kill_switch

DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
METADATA_PATH = DATABASE / "Digital_Etsy_Metadata.csv"
QUEUE_PATH = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
QA_PATH = DATABASE / "Etsy_Digital_QA_Report.csv"
FEE_LEDGER_PATH = DATABASE / "Etsy_Fee_Ledger.csv"
REPORT_PATH = REVIEW / f"ETSY_DIGITAL_TRAFFIC_PENETRATION_REPORT_{datetime.now():%Y%m%d}.md"

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
]

QA_FIELDS = [
    "Timestamp",
    "ID",
    "Zip_Path",
    "Zip_MB",
    "Zip_Status",
    "Image_Count",
    "Readme_Present",
    "Worst_Image_Status",
    "Worst_Image_Reason",
    "QA_Status",
    "QA_Reason",
]

FEE_FIELDS = [
    "Timestamp",
    "Batch_ID",
    "ID",
    "Action",
    "Expected_Fee_USD",
    "Confirmed_Spent_USD",
    "Status",
    "Reference",
]


@dataclass
class QaResult:
    status: str
    reason: str
    image_count: int
    readme_present: bool
    zip_mb: float
    worst_status: str
    worst_reason: str


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _append_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def _existing_ids(path: Path) -> set[str]:
    return {row.get("ID", "") for row in _read_csv(path) if row.get("ID")}


def _confirmed_spend_today() -> float:
    today = datetime.now().strftime("%Y-%m-%d")
    total = 0.0
    for row in _read_csv(FEE_LEDGER_PATH):
        if str(row.get("Timestamp", "")).startswith(today) and str(row.get("Status", "")).startswith("CONFIRMED"):
            try:
                total += float(row.get("Confirmed_Spent_USD") or 0)
            except ValueError:
                pass
    return total


def _select_candidates(limit: int) -> list[dict]:
    queued = _existing_ids(QUEUE_PATH)
    candidates = []
    for row in _read_csv(METADATA_PATH):
        if row.get("ID") in queued:
            continue
        if row.get("Status") != "READY_FOR_ETSY_DRAFT":
            continue
        candidates.append(row)
        if len(candidates) >= limit:
            break
    return candidates


def _audit_image(path: Path) -> tuple[str, str]:
    metrics = _metrics(path)
    return _verdict(metrics)


def qa_zip(row: dict) -> QaResult:
    zip_path = Path(row["Zip_Path"])
    reasons: list[str] = []
    image_count = 0
    readme_present = False
    worst_status = "PASS"
    worst_reason = ""
    zip_mb = 0.0

    if not zip_path.exists():
        return QaResult("HOLD", "ZIP_MISSING", 0, False, 0.0, "HOLD", "ZIP_MISSING")
    zip_mb = zip_path.stat().st_size / (1024 * 1024)
    if zip_mb <= 0:
        reasons.append("ZIP_EMPTY")
    if zip_mb > 20:
        reasons.append("ZIP_OVER_ETSY_20MB_LIMIT")

    tmp_dir = zip_path.parent / "_qa_extract_tmp"
    if tmp_dir.exists():
        for old in tmp_dir.glob("*"):
            try:
                old.unlink()
            except OSError:
                pass
    tmp_dir.mkdir(exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, "r") as archive:
            names = archive.namelist()
            readme_present = any(name.lower().endswith(".txt") and "readme" in name.lower() for name in names)
            jpgs = [name for name in names if name.lower().endswith((".jpg", ".jpeg"))]
            image_count = len(jpgs)
            if image_count < 5:
                reasons.append("LESS_THAN_5_PRINT_RATIOS")
            if not readme_present:
                reasons.append("README_MISSING")
            for name in jpgs:
                archive.extract(name, tmp_dir)
                image_path = tmp_dir / name
                with Image.open(image_path) as image:
                    width, height = image.size
                status, reason = _audit_image(image_path)
                if min(width, height) < 3000:
                    status = "HOLD"
                    reason = (reason + ";LOW_PRINT_DIMENSION").strip(";")
                if status == "HOLD":
                    worst_status = "HOLD"
                    worst_reason = reason
                    reasons.append(f"{Path(name).name}:{reason or status}")
                elif status == "REVIEW_RECOMMENDED" and worst_status == "PASS":
                    worst_status = status
                    worst_reason = reason
    except zipfile.BadZipFile:
        reasons.append("BAD_ZIP")
    finally:
        for old in tmp_dir.rglob("*"):
            try:
                if old.is_file():
                    old.unlink()
            except OSError:
                pass
        try:
            tmp_dir.rmdir()
        except OSError:
            pass

    if any("ZIP_" in reason or "LESS_THAN" in reason or "README" in reason for reason in reasons):
        status = "HOLD"
    elif any("SHADOW_CLIPPING" in reason or "HIGHLIGHT_CLIPPING" in reason or "LOW_PRINT_DIMENSION" in reason for reason in reasons):
        status = "HOLD"
    elif worst_status == "REVIEW_RECOMMENDED":
        status = "PASS_REVIEW_NOTE"
    else:
        status = "PASS"
    return QaResult(status, "; ".join(reasons), image_count, readme_present, zip_mb, worst_status, worst_reason)


def _mark_metadata(ids: set[str], status: str) -> None:
    rows = _read_csv(METADATA_PATH)
    for row in rows:
        if row.get("ID") in ids:
            row["Status"] = status
    if rows:
        _write_csv(METADATA_PATH, rows, list(rows[0].keys()))


def stage(limit: int, publish_attempt: bool = False) -> dict:
    config = fee_kill_switch()
    listing_fee = float(config.get("expected_listing_fee_usd", 0.20) if config else 0.20)
    candidates = _select_candidates(limit)
    if not candidates:
        return {"selected": 0, "qa_pass": 0, "queued": 0, "blocked": "NO_CANDIDATES"}

    daily_spend = _confirmed_spend_today()
    assert_etsy_fee_batch_allowed(len(candidates), daily_spend_so_far=daily_spend)

    batch_id = f"ETSY-DIGITAL-{datetime.now():%Y%m%d-%H%M%S}"
    qa_rows: list[dict] = []
    queue_rows: list[dict] = []
    fee_rows: list[dict] = []
    passed_ids: set[str] = set()
    blocked_note = ""

    try:
        assert_allowed("etsy", "paid_publish")
        launch_status = "READY_TO_PUBLISH"
    except RiskBlocked as exc:
        launch_status = "READY_BLOCKED_ETSY_AUTH"
        blocked_note = str(exc)

    for row in candidates:
        qa = qa_zip(row)
        qa_rows.append(
            {
                "Timestamp": _now(),
                "ID": row["ID"],
                "Zip_Path": row["Zip_Path"],
                "Zip_MB": f"{qa.zip_mb:.2f}",
                "Zip_Status": "OK" if qa.status != "HOLD" else "REVIEW",
                "Image_Count": qa.image_count,
                "Readme_Present": qa.readme_present,
                "Worst_Image_Status": qa.worst_status,
                "Worst_Image_Reason": qa.worst_reason,
                "QA_Status": qa.status,
                "QA_Reason": qa.reason,
            }
        )
        if not qa.status.startswith("PASS"):
            queue_status = "HOLD_QA_FAILED"
            notes = qa.reason
        else:
            queue_status = launch_status
            notes = blocked_note
            passed_ids.add(row["ID"])
        queue_rows.append(
            {
                "Timestamp": _now(),
                "Batch_ID": batch_id,
                "ID": row["ID"],
                "Title": row["Title"],
                "Price": row["Price"],
                "Zip_Path": row["Zip_Path"],
                "Zip_MB": f"{qa.zip_mb:.2f}",
                "QA_Status": qa.status,
                "QA_Reason": qa.reason,
                "Projected_Fee_USD": f"{listing_fee:.2f}" if qa.status.startswith("PASS") else "0.00",
                "Fee_Status": "RESERVED_NOT_SPENT" if qa.status.startswith("PASS") else "NOT_RESERVED_QA_HOLD",
                "Launch_Status": queue_status,
                "Etsy_Listing_ID": "",
                "Notes": notes,
            }
        )
        fee_rows.append(
            {
                "Timestamp": _now(),
                "Batch_ID": batch_id,
                "ID": row["ID"],
                "Action": "RESERVE_LISTING_FEE" if qa.status.startswith("PASS") else "NO_RESERVE_QA_HOLD",
                "Expected_Fee_USD": f"{listing_fee:.2f}" if qa.status.startswith("PASS") else "0.00",
                "Confirmed_Spent_USD": "0.00",
                "Status": "RESERVED_NOT_SPENT" if qa.status.startswith("PASS") else "QA_HOLD",
                "Reference": "",
            }
        )

    _append_csv(QA_PATH, qa_rows, QA_FIELDS)
    _append_csv(QUEUE_PATH, queue_rows, QUEUE_FIELDS)
    _append_csv(FEE_LEDGER_PATH, fee_rows, FEE_FIELDS)
    _mark_metadata(passed_ids, "GRAY_QUEUE_RESERVED_NOT_SPENT")

    if publish_attempt and passed_ids and launch_status == "READY_TO_PUBLISH":
        # Paid Etsy creation is intentionally not implemented until OAuth and a
        # one-listing idempotency proof are available. This prevents accidental
        # duplicate $0.20 fee spend during API bring-up.
        pass

    return {
        "batch_id": batch_id,
        "selected": len(candidates),
        "qa_pass": len(passed_ids),
        "qa_hold": len(candidates) - len(passed_ids),
        "queued": len(queue_rows),
        "reserved_fee_usd": round(len(passed_ids) * listing_fee, 2),
        "confirmed_spent_usd": 0.0,
        "launch_status": launch_status,
        "blocked_note": blocked_note,
    }


def write_report(result: dict) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    config = fee_kill_switch()
    batch_cap = float(config.get("batch_fee_cap_usd", 2.0) if config else 2.0)
    daily_cap = float(config.get("daily_listing_fee_cap_usd", 6.0) if config else 6.0)
    queue_rows = _read_csv(QUEUE_PATH)
    latest_batch = [row for row in queue_rows if row.get("Batch_ID") == result.get("batch_id")]
    lines = [
        "# Etsy Digital Gray Launch - Traffic Penetration Report",
        "",
        f"- Generated: {datetime.now():%Y-%m-%d %H:%M:%S %z} (America/New_York)",
        f"- Batch: {result.get('batch_id', 'N/A')}",
        f"- Batch hard cap: ${batch_cap:.2f}",
        f"- Daily hard cap: ${daily_cap:.2f}",
        f"- Selected listings: {result.get('selected', 0)}",
        f"- QA pass/reserved: {result.get('qa_pass', 0)}",
        f"- QA hold: {result.get('qa_hold', 0)}",
        f"- Reserved fee: ${result.get('reserved_fee_usd', 0):.2f}",
        f"- Confirmed spent: ${result.get('confirmed_spent_usd', 0):.2f}",
        f"- Launch status: {result.get('launch_status', 'UNKNOWN')}",
        "",
        "## Guardrail Verdict",
        "",
    ]
    if result.get("launch_status") == "READY_BLOCKED_ETSY_AUTH":
        lines.extend(
            [
                "- Paid Etsy publish is blocked before spend because account/API access is not yet clean.",
                "- This is the correct money-sensitive behavior: no retry storm, no duplicate fee risk, no listing fee burned while auth is ambiguous.",
            ]
        )
    elif result.get("launch_status") == "READY_TO_PUBLISH":
        lines.append("- Etsy appears eligible for publish, but first paid create still requires a one-listing idempotency proof before scaling.")
    else:
        lines.append("- No publish action was attempted.")
    lines.extend(
        [
            "",
            "## First Batch Items",
            "",
            "| ID | Price | ZIP MB | QA | Fee | Launch Status |",
            "|---|---:|---:|---|---:|---|",
        ]
    )
    for row in latest_batch:
        lines.append(
            f"| {row.get('ID')} | ${row.get('Price')} | {row.get('Zip_MB')} | {row.get('QA_Status')} | "
            f"${row.get('Projected_Fee_USD')} | {row.get('Launch_Status')} |"
        )
    lines.extend(
        [
            "",
            "## Tomorrow Morning Readout Logic",
            "",
            "- If Etsy access is restored overnight: publish only up to the first 10 passed items, then read views/favorites/orders and compare against the $6 daily cap.",
            "- If all first 10 get 0 views after the initial indexing window: stop further fee spend, rewrite SEO around lower-competition long-tail terms, and test a different digital-product angle before scaling.",
            "- If Etsy access remains blocked: report 0 spend, 10 staged products, and the exact account/API blocker instead of pretending traffic data exists.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[REPORT] {REPORT_PATH}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--publish-attempt", action="store_true")
    args = parser.parse_args()
    result = stage(limit=args.limit, publish_attempt=args.publish_attempt)
    write_report(result)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
