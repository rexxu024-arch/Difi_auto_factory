"""Freeze the rejected Adobe Stock flat-texture pilot.

Rex rejected the first Adobe Stock material batch because it was flat,
procedural, and not commercially attractive enough. This script marks the
affected local queues as HOLD/REJECTED so they cannot be accidentally uploaded
after the Contributor account login is available.
"""

from __future__ import annotations

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

TARGETS = [
    DATABASE / "Adobe_Stock_Pilot_Batch.csv",
    DATABASE / "Adobe_Stock_Upload_Ready.csv",
    DATABASE / "Adobe_Stock_First_Submit_7.csv",
    DATABASE / "Adobe_Stock_Curated_Pilot.csv",
    DATABASE / "Adobe_Stock_Curated_Pilot_strict_premium.csv",
    DATABASE / "Adobe_Stock_UI_Upload_Status.csv",
]

REPORT = REVIEW / "Adobe_Stock_Failure_Traceback_20260516.md"
REJECT_STATUS = "REJECTED_BY_REX_ADOBE_MACRO_HOTFIX_20260516"
REJECT_REASON = (
    "Rejected pilot: flat/procedural texture batch lacked macro-photography depth, "
    "real MJ U-button/2x-upscale provenance, and buyer-grade commercial value."
)


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]], headers: list[str]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def mark_rows(path: Path) -> tuple[int, int]:
    rows = read_rows(path)
    if not rows:
        return 0, 0
    headers = list(rows[0].keys())
    for extra in ("QA_Status", "Upload_Status", "Status", "Reject_Reason", "Rejected_At_ET"):
        if extra not in headers:
            headers.append(extra)
    changed = 0
    for row in rows:
        current = " ".join(str(value) for value in row.values()).upper()
        if "UPLOADED" in current or "SUBMITTED" in current:
            continue
        row["QA_Status"] = "HOLD_FLAT_LOW_VALUE_PREVIOUS_PILOT"
        row["Upload_Status"] = "HOLD_DO_NOT_UPLOAD"
        row["Status"] = REJECT_STATUS
        row["Reject_Reason"] = REJECT_REASON
        row["Rejected_At_ET"] = now_text()
        changed += 1
    write_rows(path, rows, headers)
    return len(rows), changed


def build_report(results: list[tuple[Path, int, int]]) -> None:
    lines = [
        "# Adobe Stock Failure Traceback",
        "",
        f"Generated: {now_text()}",
        "",
        "## Root Cause",
        "",
        "- The first Adobe pilot over-optimized for procedural safety and under-optimized for buyer value.",
        "- QA accepted long-edge/metadata checks but did not require macro-photography depth or real MJ upscale provenance.",
        "- Upload-ready pack trusted local generated files and therefore could package flat assets after login became available.",
        "",
        "## Corrective Action",
        "",
        "- Existing pilot/upload-ready/first-submit rows are frozen as HOLD_DO_NOT_UPLOAD.",
        "- New Adobe assets must use the macro-photography DNA prompt spine.",
        "- New Adobe assets must pass OpenClaw's stricter 8MP+ redline and carry MJ U-button/2x-upscale provenance.",
        "- No 1024 drafts, sliced grid quarters, or procedural placeholders can enter upload-ready state.",
        "",
        "## Files Marked",
        "",
    ]
    for path, total, changed in results:
        lines.append(f"- `{path.relative_to(PROJECT_ROOT)}`: rows={total}, marked_hold={changed}")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    assert_adobe_write_paths([path for path in TARGETS if path.exists()] + [REPORT])
    results = [(path, *mark_rows(path)) for path in TARGETS if path.exists()]
    build_report(results)
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        changed = sum(item[2] for item in results)
        handle.write(
            f"\n- {now_text()}: Adobe Stock failed flat pilot frozen; marked_hold={changed}; "
            f"report={REPORT.relative_to(PROJECT_ROOT)}.\n"
        )
    print(f"[ADOBE-REJECT-PILOT] marked_hold={sum(item[2] for item in results)} report={REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
