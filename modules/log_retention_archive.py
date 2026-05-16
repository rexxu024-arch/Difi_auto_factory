"""Compact OpenClaw progress logs on a half-day cadence.

This script is intentionally conservative:
- it only compacts PROGRESS_LOG.md;
- it creates a full backup before rewriting anything;
- it archives raw old entries instead of deleting them;
- it keeps recent entries, risk anchors, and compact project progress in the
  active log.

Current policy: run compaction every 12 hours, while retaining seven days of
raw recent entries in the active log. Older verified details are archived.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
ARCHIVE_DIR = PROJECT_ROOT / "Reports" / "Log_Archives"
STATE_FILE = PROJECT_ROOT / "Database" / "Log_Retention_State.json"
BRIEF_SCRIPT = PROJECT_ROOT / "modules" / "monthly_shift_visible_brief.py"
ET = ZoneInfo("America/New_York")

ENTRY_RE = re.compile(
    r"^## (?P<stamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) EDT - (?P<title>.+)$",
    re.MULTILINE,
)
RISK_RE = re.compile(
    r"\b("
    r"ERROR|FAIL|FAILED|FAILURE|BLOCK|BLOCKED|BLOCKER|HOLD|MISSING|"
    r"TIMEOUT|ANOMALY|WARNING|WARN|RISK|REX|NEED|NEEDS|AUTH|LOGIN|"
    r"RC=\d+|NOT READY|NOT_READY|PENDING|STUCK|INVALID|EXPIRED"
    r")\b",
    re.IGNORECASE,
)


@dataclass
class Entry:
    stamp: datetime
    title: str
    body: str


def now_et() -> datetime:
    return datetime.now(ET)


def parse_stamp(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=ET)


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def should_run(force: bool) -> bool:
    if force:
        return True
    state = load_json(STATE_FILE, {})
    last_run = state.get("last_run_et")
    if not last_run:
        return True
    try:
        parsed = datetime.fromisoformat(str(last_run))
    except ValueError:
        return True
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=ET)
    return now_et() - parsed.astimezone(ET) >= timedelta(hours=12)


def split_entries(text: str) -> tuple[str, list[Entry]]:
    matches = list(ENTRY_RE.finditer(text))
    if not matches:
        return text, []
    header = text[: matches[0].start()].strip()
    entries: list[Entry] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        entries.append(
            Entry(
                stamp=parse_stamp(match.group("stamp")),
                title=match.group("title").strip(),
                body=body,
            )
        )
    return header, entries


def compact_line(value: str, limit: int = 190) -> str:
    value = re.sub(r"\s+", " ", value).strip(" -")
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def extract_risk_anchors(entries: list[Entry], limit: int = 80) -> list[str]:
    anchors: list[str] = []
    seen: set[str] = set()
    for entry in reversed(entries):
        for line in entry.body.splitlines():
            if not RISK_RE.search(line):
                continue
            clean = compact_line(line)
            if not clean or clean in seen:
                continue
            seen.add(clean)
            anchors.append(f"- {entry.stamp:%Y-%m-%d}: {clean}")
            if len(anchors) >= limit:
                return list(reversed(anchors))
    return list(reversed(anchors))


def build_progress_dashboard() -> str:
    if not BRIEF_SCRIPT.exists():
        return "- Progress dashboard unavailable: monthly_shift_visible_brief.py missing."
    try:
        result = subprocess.run(
            [sys.executable, str(BRIEF_SCRIPT), "--hourly"],
            cwd=str(PROJECT_ROOT),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"- Progress dashboard unavailable: {compact_line(str(exc), 140)}."

    output = (result.stdout or result.stderr or "").strip()
    if not output:
        return f"- Progress dashboard unavailable: brief script returned code {result.returncode}."
    lines = [compact_line(line, 240) for line in output.splitlines() if line.strip()]
    return "\n".join(f"- {line}" for line in lines[:12])


def write_archive_index(
    archive_file: Path,
    backup_file: Path,
    archived_count: int,
    kept_count: int,
    cutoff: datetime,
    dashboard: str,
) -> None:
    index = ARCHIVE_DIR / "Progress_Archive_Index.md"
    existing = index.read_text(encoding="utf-8") if index.exists() else "# Progress Archive Index\n"
    block = (
        f"\n## {now_et():%Y-%m-%d %H:%M:%S} EDT\n\n"
        f"- Cutoff: entries before {cutoff:%Y-%m-%d %H:%M:%S} EDT were compacted out of active log.\n"
        f"- Full backup: `{backup_file.name}`\n"
        f"- Archived raw entries: `{archive_file.name}` ({archived_count} entries)\n"
        f"- Active raw entries kept: {kept_count}\n"
        f"- Active log model: progress dashboard + risk anchors + last 7 days raw log.\n\n"
        "### Dashboard Snapshot\n\n"
        f"{dashboard}\n"
    )
    index.write_text(existing.rstrip() + "\n" + block, encoding="utf-8")


def compact_log(force: bool = False, dry_run: bool = False, quiet: bool = False) -> int:
    if not PROGRESS_LOG.exists():
        if not quiet:
            print("LOG_RETENTION_MISSING progress log not found")
        return 1
    if not should_run(force):
        return 0

    timestamp = now_et()
    cutoff = timestamp - timedelta(days=7)
    text = PROGRESS_LOG.read_text(encoding="utf-8", errors="replace")
    header, entries = split_entries(text)
    if not entries:
        if not quiet:
            print("LOG_RETENTION_NO_ENTRIES no dated progress entries found")
        return 0

    old_entries = [entry for entry in entries if entry.stamp < cutoff]
    recent_entries = [entry for entry in entries if entry.stamp >= cutoff]
    risk_anchors = extract_risk_anchors(entries)
    dashboard = build_progress_dashboard()

    if dry_run:
        print(
            "LOG_RETENTION_DRY_RUN "
            f"total={len(entries)} archive={len(old_entries)} keep={len(recent_entries)} "
            f"risk_anchors={len(risk_anchors)} cutoff={cutoff:%Y-%m-%d}"
        )
        return 0

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = timestamp.strftime("%Y%m%d_%H%M%S")
    backup_file = ARCHIVE_DIR / f"PROGRESS_LOG_FULL_BACKUP_{stamp}.md"
    archive_file = ARCHIVE_DIR / f"PROGRESS_LOG_ARCHIVED_OLD_ENTRIES_{stamp}.md"
    backup_file.write_text(text, encoding="utf-8")
    archive_file.write_text(
        "# Archived PROGRESS_LOG Entries\n\n"
        f"- Archived at: {timestamp:%Y-%m-%d %H:%M:%S} EDT\n"
        f"- Cutoff: older than {cutoff:%Y-%m-%d %H:%M:%S} EDT\n"
        f"- Entry count: {len(old_entries)}\n\n"
        + ("\n\n".join(entry.body for entry in old_entries) if old_entries else "_No entries were old enough to archive._")
        + "\n",
        encoding="utf-8",
    )

    active_parts = [
        "# Progress Log",
        "",
        "This file is compacted on a seven-day retention cycle. Completed and verified historical details are archived under `Reports/Log_Archives/`; active memory keeps progress bars, risk anchors, and the last seven days of raw entries.",
        "",
        "## Rolling Progress Dashboard",
        "",
        dashboard,
        "",
        "## Open Issues / Risk Anchors",
        "",
        "\n".join(risk_anchors) if risk_anchors else "- No older risk anchors detected during the latest compaction.",
        "",
        "## Recent Raw Log (Last 7 Days)",
        "",
        "\n\n".join(entry.body for entry in recent_entries) if recent_entries else "_No recent raw entries in the active window._",
        "",
    ]
    PROGRESS_LOG.write_text("\n".join(active_parts), encoding="utf-8")

    state = {
        "last_run_et": timestamp.isoformat(),
        "cutoff_et": cutoff.isoformat(),
        "retention_days": 7,
        "compaction_interval_hours": 12,
        "progress_log": str(PROGRESS_LOG),
        "archive_dir": str(ARCHIVE_DIR),
        "full_backup": str(backup_file),
        "archived_entries_file": str(archive_file),
        "archived_entry_count": len(old_entries),
        "active_recent_entry_count": len(recent_entries),
        "risk_anchor_count": len(risk_anchors),
    }
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    write_archive_index(archive_file, backup_file, len(old_entries), len(recent_entries), cutoff, dashboard)
    if not quiet:
        print(
            "LOG_RETENTION_ARCHIVED "
            f"archive={len(old_entries)} keep={len(recent_entries)} "
            f"backup={backup_file.name} active={PROGRESS_LOG.name}"
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Run even if the seven-day interval has not elapsed.")
    parser.add_argument("--dry-run", action="store_true", help="Print compaction counts without writing files.")
    parser.add_argument("--quiet", action="store_true", help="Suppress no-op output.")
    args = parser.parse_args()
    return compact_log(force=args.force, dry_run=args.dry_run, quiet=args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
