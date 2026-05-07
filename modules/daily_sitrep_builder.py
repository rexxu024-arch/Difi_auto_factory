"""Build the daily strategic sitrep payload for Grey."""

from __future__ import annotations

import csv
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

BRIDGE_DIR = PROJECT_ROOT / "Review_Packets" / "Gemini_Bridge"
LATEST_SITREP = BRIDGE_DIR / "DAILY_SITREP_latest.md"


def _read(path: Path, max_chars: int = 6000) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[-max_chars:]


def _extract(report: str, label: str, default: str = "n/a") -> str:
    pattern = re.compile(rf"^- {re.escape(label)}:\s*(.+)$", re.MULTILINE)
    match = pattern.search(report)
    return match.group(1).strip() if match else default


def _cover_counts() -> dict[str, int]:
    path = PROJECT_ROOT / "Database" / "eBay_Cover_Replacement_Queue.csv"
    counts: dict[str, int] = {}
    if not path.exists():
        return counts
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            status = (row.get("Replacement_Status") or "UNKNOWN").strip()
            counts[status] = counts.get(status, 0) + 1
    return counts


def build(system_status: str = "NORMAL") -> str:
    BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")
    report = _read(PROJECT_ROOT / "Review_Packets" / "Latest" / "morning_report_latest.md")
    cover = _cover_counts()
    lines = [
        "[DAILY_SITREP_SYNC]",
        f"Timestamp: {now}",
        f"System_Status: {system_status}",
        "",
        "1. Cash-Flow Fortress:",
        f"- eBay: latest snapshot {_extract(report, 'Latest eBay snapshot')}; 0-view {_extract(report, '0-view rows in snapshot')}; nonzero {_extract(report, 'Rows with at least 1 view')}; General ads {_extract(report, 'General promoted rows in snapshot')}.",
        f"- Etsy Mirror: live digital {_extract(report, 'Etsy Digital live listings')}; confirmed spend {_extract(report, 'Etsy Digital confirmed listing-fee spend')}; public audit {_extract(report, 'Etsy Digital public audit active/readable')}.",
        f"- Printify/Cover Gate: done {cover.get('OLD_RETIRED_REPLACED_DONE', 0)}; ready {cover.get('READY_TO_REPLACE_VERIFIED', 0)}; review {cover.get('REVIEW_BEFORE_REPLACE', 0)}.",
        "",
        "2. The Syndicate:",
        "- Stock / FTP distribution: deferred; Printify/POD factory remains active priority.",
        "",
        "3. Roadblocks:",
        "- eBay 0-view remains high; ads alone are not enough.",
        "- Sticker Cover Gate is still the primary production blocker until remaining replacements are closed.",
        "- Etsy API approval remains separate from Printify/Etsy UI operations; listing-fee cap still applies.",
        "",
    ]
    text = "\n".join(lines)
    LATEST_SITREP.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(build())
