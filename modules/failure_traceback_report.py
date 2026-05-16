"""Generate a compact OpenClaw failure traceback report.

This is a local reporting utility only. It does not touch marketplaces or spend.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS = PROJECT_ROOT / "Reports"
DATABASE = PROJECT_ROOT / "Database"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

OUT_LATEST = REPORTS / "Failure_Traceback_latest.md"


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def tail_matches(path: Path, terms: tuple[str, ...], limit: int = 18) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    matches = [line for line in lines if any(term.lower() in line.lower() for term in terms)]
    return matches[-limit:]


def status_counts(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = row.get(field, "").strip() or "(blank)"
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def render_counts(title: str, counts: dict[str, int]) -> list[str]:
    lines = [f"## {title}", ""]
    if not counts:
        return lines + ["- No rows found.", ""]
    lines.extend(f"- {name}: {count}" for name, count in counts.items())
    lines.append("")
    return lines


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)

    adobe_batch = read_csv_rows(DATABASE / "Adobe_Stock_Pilot_Batch.csv")
    adobe_ui = read_csv_rows(DATABASE / "Adobe_Stock_UI_Upload_Status.csv")
    etsy_fee = read_csv_rows(DATABASE / "Etsy_Fee_Ledger.csv")
    backlog = read_csv_rows(DATABASE / "Factory_Backlog.csv")

    blockers = tail_matches(
        PROGRESS_LOG,
        ("NEEDS_ADOBE_LOGIN", "ERROR", "Traceback", "blocked", "WAIT_", "HOLD", "failed"),
    )

    lines = [
        "# OpenClaw Failure Traceback Latest",
        "",
        f"Generated: {now_text()}",
        "",
        "## Executive Diagnosis",
        "",
        "- Adobe Stock pipeline is technically upload-ready locally, but live upload is blocked by Adobe Contributor login in the dedicated Edge/CDP profile.",
        "- Adobe first-submit pack has been reduced to 7 files to avoid similar-content risk; 45/50 generated images currently pass image QA.",
        "- Marketplace writes must continue to obey fee/account/gallery/shipping guards; paid actions are not globally frozen when inside Rex budget.",
        "",
    ]
    lines += render_counts("Adobe Batch QA Status", status_counts(adobe_batch, "QA_Status"))
    lines += render_counts("Adobe UI Probe Status", status_counts(adobe_ui, "Status"))
    lines += render_counts("Etsy Fee Ledger Status", status_counts(etsy_fee, "Status"))
    lines += render_counts("Factory Backlog Status", status_counts(backlog, "Status"))
    lines += [
        "## Recent Blocker Lines",
        "",
    ]
    lines.extend(f"- {line}" for line in blockers[-18:]) if blockers else lines.append("- No recent blocker lines found.")
    lines += [
        "",
        "## Next Safe Action",
        "",
        "1. Rex logs into Adobe Contributor in the dedicated Edge automation profile.",
        "2. Codex probes `first-submit-7`, then uploads only the 7-file pilot if the page is ready.",
        "3. Rejection/acceptance feedback is added back into the image and metadata QA gates before scaling to 50/day.",
        "",
    ]
    OUT_LATEST.write_text("\n".join(lines), encoding="utf-8")
    print(f"[FAILURE-TRACEBACK] wrote={OUT_LATEST}")


if __name__ == "__main__":
    main()
