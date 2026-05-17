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


def _backlog_brief() -> str:
    path = PROJECT_ROOT / "Database" / "Factory_Backlog.csv"
    if not path.exists():
        return "Factory backlog missing."
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    counts: dict[str, int] = {}
    ready_rows: list[dict[str, str]] = []
    for row in rows:
        status = (row.get("Status") or "UNKNOWN").strip()
        counts[status] = counts.get(status, 0) + 1
        if status in {"READY", "READY_MONITOR"}:
            ready_rows.append(row)
    ready_rows.sort(key=lambda r: int(re.sub(r"[^0-9-]", "", r.get("Priority", "0")) or 0), reverse=True)
    top_ready = "; ".join(
        f"P{row.get('Priority')} {row.get('Lane')}: {row.get('Task')}"
        for row in ready_rows[:3]
    )
    if not top_ready:
        top_ready = "none; current high-priority work is blocked by platform guard, MJ wait, or Rex visual selection."
    return f"status_counts={counts}; top_ready={top_ready}"


def _count_csv(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def _csv_status_counts(path: Path, field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    if not path.exists():
        return counts
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            status = (row.get(field) or "UNKNOWN").strip()
            counts[status] = counts.get(status, 0) + 1
    return counts


def _adobe_brief() -> str:
    batch_counts = _csv_status_counts(PROJECT_ROOT / "Database" / "Adobe_Stock_Pilot_Batch.csv", "QA_Status")
    upload_ready = _count_csv(PROJECT_ROOT / "Database" / "Adobe_Stock_Upload_Ready.csv")
    first_submit = _count_csv(PROJECT_ROOT / "Database" / "Adobe_Stock_First_Submit_7.csv")
    ui_counts = _csv_status_counts(PROJECT_ROOT / "Database" / "Adobe_Stock_UI_Upload_Status.csv", "Status")
    qa_pass = batch_counts.get("QA_PASS_READY_FOR_ADOBE_CSV", 0)
    holds = sum(count for status, count in batch_counts.items() if status.startswith("HOLD"))
    ui_status = ", ".join(f"{key}:{value}" for key, value in ui_counts.items()) or "not probed"
    return (
        f"generated/QA-ready {qa_pass}; held {holds}; upload-ready index {upload_ready}; "
        f"first-submit pack {first_submit}; UI probe {ui_status}"
    )


def _execution_decision_lines() -> list[str]:
    path = PROJECT_ROOT / "Database" / "Factory_Backlog.csv"
    ready_rows: list[dict[str, str]] = []
    guarded_rows: list[dict[str, str]] = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                status = (row.get("Status") or "").strip()
                if status in {"READY", "READY_MONITOR"}:
                    ready_rows.append(row)
                elif status.startswith(("WAIT", "HOLD", "BLOCKED")):
                    guarded_rows.append(row)
    ready_rows.sort(key=lambda r: int(re.sub(r"[^0-9-]", "", r.get("Priority", "0")) or 0), reverse=True)
    guarded_rows.sort(key=lambda r: int(re.sub(r"[^0-9-]", "", r.get("Priority", "0")) or 0), reverse=True)

    lines = [
        "- Decision model: classify work as S-Class strategic asset build or C-Class routing/maintenance before acting.",
        "- Current priority ladder: Adobe Stock first-submit / 50-day material factory > safe POD marketplace learning > First Audit premium assets for early-June cousin review > reporting/admin cleanup.",
        "- Current rejection list: no Sticker expansion, no blind low-price volume, no First Audit asset leakage into public channels, no marketplace write when fee/account/gallery/shipping guards are dirty.",
        "- Loop policy: after each concrete task, refresh backlog and continue; if a long-tail item burns abnormal time after 90% completion, log it and defer instead of draining compute.",
        "- Gemini role: API Grey provides advisory cross-checks; daily web-thread sync is for Rex/Grey visibility; Codex final action follows local physical truth and guard files.",
    ]
    if ready_rows:
        ready = "; ".join(
            f"P{row.get('Priority')} {row.get('Lane')} => {row.get('Task')}"
            for row in ready_rows[:3]
        )
        lines.append(f"- Next executable queue: {ready}.")
    else:
        lines.append("- Next executable queue: no clean READY row; continue with guard-safe local QA, packaging, or asset preparation.")
    if guarded_rows:
        guarded = "; ".join(
            f"P{row.get('Priority')} {row.get('Lane')} blocked by {row.get('Status')}"
            for row in guarded_rows[:3]
        )
        lines.append(f"- Active guard pressure: {guarded}.")
    return lines


def _monthly_loop_failure_traceback() -> list[str]:
    path = BRIDGE_DIR / "TO_GREY_MONTHLY_LOOP_FAILURE_TRACEBACK_latest.md"
    if not path.exists():
        return ["- No monthly-loop failure traceback packet found yet."]
    text = _read(path, max_chars=4200)
    wanted: list[str] = []
    capture = False
    for line in text.splitlines():
        if line.startswith("## Rex's Requirement Was Not Ambiguous"):
            capture = True
        elif line.startswith("## Corrected Model"):
            capture = True
        elif line.startswith("## New Guardrail To Audit"):
            capture = True
        elif line.startswith("## Codex Self-Correction Commitment"):
            capture = True
        elif line.startswith("## ") and capture:
            capture = False
        if capture and line.strip():
            wanted.append(line)
    if not wanted:
        wanted = text.splitlines()[-40:]
    return [f"- {line}" if not line.startswith(("#", "-", "1.", "2.", "3.", "4.", "5.", "6.")) else line for line in wanted[:80]]


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
        f"- Printify QA: Cover Gate retired/replaced {cover.get('OLD_RETIRED_REPLACED_DONE', 0)}; gallery custom-risk {_extract(report, 'Printify gallery duplicate audit CHECK_CUSTOM_GALLERY_REPEATS_RISK')}; gallery exact-duplicate {_extract(report, 'Printify gallery duplicate audit CHECK_EXACT_DUPLICATE')}; gallery OK {_extract(report, 'Printify gallery duplicate audit OK')}.",
        "",
        "2. The Syndicate:",
        f"- Adobe Stock factory: {_adobe_brief()}.",
        "- FTP/multi-stock distribution: deferred until the Adobe Contributor pilot produces acceptance/rejection feedback.",
        "",
        "3. Codex Decision Logic:",
        *_execution_decision_lines(),
        f"- Current backlog read: {_backlog_brief()}",
        "",
        "4. Monthly Loop Failure Traceback For Grey:",
        *_monthly_loop_failure_traceback(),
        "",
        "5. Roadblocks:",
        "- Adobe Contributor live upload is blocked until Rex logs into the dedicated Edge/CDP profile; local first-submit pack is ready.",
        "- eBay 0-view remains high; ads alone are not enough, and Printify-origin active items are not fully writable through Inventory API.",
        "- Gallery Integrity remains a publish guard: repeated/risky buyer-facing image galleries must be repaired or isolated before scaling POD.",
        "- Etsy listing-fee cap still applies; paid actions are allowed only inside Rex budget and account-safety guards.",
        "",
    ]
    text = "\n".join(lines)
    LATEST_SITREP.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(build())
