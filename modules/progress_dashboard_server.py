"""Local read-only OpenClaw progress dashboard.

This is intentionally simple: one stdlib HTTP server, one JSON endpoint, and a
small auto-refreshing page. It does not publish, spend, or mutate marketplace
state. Its only job is to make the long monthly shift visible outside chat.
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import re
import subprocess
import time
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse
from zoneinfo import ZoneInfo

from monthly_shift_visible_brief import (
    BRIEF_FILE,
    COMMAND_PROJECT,
    DATABASE_DIR,
    ET,
    PROJECT_ROOT,
    STATE_FILE,
    TRIGGER_FILE,
    load_json,
    parse_state,
    parse_stamp,
    progress_score,
    project_dashboard,
    read_csv,
    recent_items,
    remaining_line,
    summarize_recent,
)


PID_FILE = DATABASE_DIR / "Monthly_Shift_Loop.pid"
DASHBOARD_PID_FILE = DATABASE_DIR / "OpenClaw_Progress_Dashboard.pid"
SHIFT_DUTY_WINDOW_FILE = DATABASE_DIR / "Monthly_Shift_Duty_Window.json"
ADOBE_QA_FILE = DATABASE_DIR / "Adobe_Stock_Rex_Visual_QA.csv"
ADOBE_UPLOAD_READY_FILE = DATABASE_DIR / "Adobe_Stock_Daily_Upload_Ready.csv"
ADOBE_LOCAL_UPSCALED_FILE = DATABASE_DIR / "Adobe_Stock_Local_Upscaled_Candidates.csv"
ADOBE_FIRST_SUBMIT_FILE = DATABASE_DIR / "Adobe_Stock_First_Submit_7.csv"
ADOBE_MARKET_SAMPLE_FILE = DATABASE_DIR / "Adobe_Stock_Market_Sample_MJ_Dispatch_Queue.csv"
STAMP_RE = re.compile(r"^- (?P<stamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) EDT \| (?P<body>.*)$")
LOOP_START_RE = re.compile(r"^- (?P<stamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) EDT \| START (?P<num>\d+) (?P<name>\S+)")
LOOP_END_RE = re.compile(r"^- (?P<stamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) EDT \| END (?P<num>\d+) (?P<name>\S+) (?P<status>OK|RC=\d+|TIMEOUT)")
BOOT_CACHE: dict[str, Any] = {"checked_at": 0.0, "boot_time": None}
PROJECT_DETAIL_KEYS = {
    "printify_etsy": ("etsy", "printify", "publish", "v155", "supervisor"),
    "first_audit": ("first_audit", "shock", "studio"),
    "adobe_stock": ("adobe", "stock"),
    "ebay": ("ebay", "market_learning"),
    "project_mirror": ("project_mirror", "mirror"),
}
PROJECT_META = {
    "overall": {"title": "Overall", "short": "Overall"},
    "printify_etsy": {"title": "Printify / Etsy Main", "short": "Printify / Etsy"},
    "first_audit": {"title": "First Audit Demo", "short": "First Audit"},
    "adobe_stock": {"title": "Adobe Stock Factory", "short": "Adobe Stock"},
    "project_mirror": {"title": "Project Mirror", "short": "Project Mirror"},
    "ebay": {"title": "eBay Repair / Experiments", "short": "eBay"},
}
PROJECT_SLUGS = {
    "overall": "overall",
    "printify": "printify_etsy",
    "etsy": "printify_etsy",
    "printify_etsy": "printify_etsy",
    "first-audit": "first_audit",
    "first_audit": "first_audit",
    "adobe": "adobe_stock",
    "adobe-stock": "adobe_stock",
    "adobe_stock": "adobe_stock",
    "mirror": "project_mirror",
    "project-mirror": "project_mirror",
    "project_mirror": "project_mirror",
    "ebay": "ebay",
}
ERROR_PATTERNS = ("error", "fail", "traceback", "timeout", "exception", "blocked", "invalid", "unauthorized")
PROJECT_THUMB_DIRS = {
    "first_audit": [
        PROJECT_ROOT / "First_Audit_Release",
        PROJECT_ROOT / "Review_Packets" / "First_Audit_001",
    ],
    "project_mirror": [
        PROJECT_ROOT / "Review_Packets" / "Project_Mirror",
        DATABASE_DIR,
    ],
    "printify_etsy": [
        PROJECT_ROOT / "Review_Packets",
        PROJECT_ROOT / "Outputs",
    ],
    "adobe_stock": [
        PROJECT_ROOT / "adobe_stock_factory" / "upload_ready",
        PROJECT_ROOT / "adobe_stock_factory" / "assets",
        PROJECT_ROOT / "Review_Packets",
    ],
    "ebay": [PROJECT_ROOT / "Review_Packets"],
}
PROJECT_MVP_TOTAL_HOURS = {
    # Heuristic MVP targets, not lifetime business completion.
    "printify_etsy": 70,
    "first_audit": 110,
    "adobe_stock": 85,
    "project_mirror": 24,
    "ebay": 35,
}
DAILY_TASK_DEFS = [
    {
        "id": "etsy_pod_daily",
        "project_id": "printify_etsy",
        "title": "Etsy POD high-quality listing drip",
        "target_min": 3,
        "target_max": 5,
        "unit": "POD listings",
        "note": "Poster/Acrylic first. Digital stays secondary; Sticker expansion is frozen.",
        "priority": 1,
    },
    {
        "id": "printify_visual_qa",
        "project_id": "printify_etsy",
        "title": "Printify/Etsy visual QA",
        "target_min": 8,
        "target_max": 12,
        "unit": "design/gallery checks",
        "note": "Catch duplicate galleries, wrong covers, wrong production images before scaling.",
        "priority": 2,
    },
    {
        "id": "adobe_qa_assets",
        "project_id": "adobe_stock",
        "title": "Adobe Stock QA-passed assets",
        "target_min": 25,
        "target_max": 50,
        "unit": "QA-passed assets",
        "note": "Daily target becomes 50 once the first submission flow is proven.",
        "priority": 1,
    },
    {
        "id": "adobe_metadata_rows",
        "project_id": "adobe_stock",
        "title": "Adobe metadata/IP-risk prep",
        "target_min": 25,
        "target_max": 50,
        "unit": "metadata rows",
        "note": "Separate stock CSV/database from Etsy/eBay so the brands never pollute each other.",
        "priority": 2,
    },
    {
        "id": "ebay_quality_actions",
        "project_id": "ebay",
        "title": "eBay high-quality experiment / repair",
        "target_min": 1,
        "target_max": 3,
        "unit": "safe actions",
        "note": "Use API where possible; otherwise Seller Hub only for low-risk repairs or reads.",
        "priority": 3,
    },
    {
        "id": "first_audit_assets",
        "project_id": "first_audit",
        "title": "First Audit premium asset work",
        "target_min": 1,
        "target_max": 3,
        "unit": "release assets",
        "note": "Lower daily urgency until early June, but quality bar stays top 1%.",
        "priority": 4,
    },
    {
        "id": "mirror_dna",
        "project_id": "project_mirror",
        "title": "Project Mirror premium DNA extraction",
        "target_min": 3,
        "target_max": 5,
        "unit": "A/B pairs or DNA refs",
        "note": "Use premium reference DNA to improve First Audit and high-ticket POD.",
        "priority": 5,
    },
]


def window_label(now: datetime, minutes: int) -> str:
    start = now - timedelta(minutes=minutes)
    return f"{start.strftime('%H:%M:%S')} - {now.strftime('%H:%M:%S')} ET"


def compact_label(value: str, limit: int = 120) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def stamp_from_item(item: dict[str, Any]) -> datetime | None:
    stamp = str(item.get("stamp") or "")
    return parse_stamp(stamp)


def completed_since(completed: list[dict[str, Any]], start: datetime) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for item in completed:
        stamp = stamp_from_item(item)
        if stamp and stamp >= start:
            result.append(item)
    return result


def tail_int(item: dict[str, Any], pattern: str) -> int:
    text = " ".join(str(item.get(key) or "") for key in ("tail", "name", "status"))
    match = re.search(pattern, text)
    if not match:
        return 0
    try:
        return int(match.group(1))
    except (TypeError, ValueError):
        return 0


def sum_tail_int(items: list[dict[str, Any]], command_names: set[str], pattern: str) -> int:
    total = 0
    for item in items:
        if str(item.get("name") or "") in command_names:
            total += tail_int(item, pattern)
    return total


def count_commands(items: list[dict[str, Any]], prefixes: tuple[str, ...]) -> int:
    return sum(1 for item in items if str(item.get("name") or "").startswith(prefixes))


def count_csv_matching(path: Path, terms: tuple[str, ...]) -> int:
    rows = read_csv(path)
    total = 0
    lowered_terms = tuple(term.lower() for term in terms)
    for row in rows:
        blob = " ".join(str(value) for value in row.values()).lower()
        if any(term in blob for term in lowered_terms):
            total += 1
    return total


def unique_csv_values(path: Path, fields: tuple[str, ...]) -> set[str]:
    values: set[str] = set()
    for row in read_csv(path):
        for field in fields:
            value = str(row.get(field) or "").strip()
            if value:
                values.add(value)
                break
    return values


def unique_project_mirror_pairs() -> int:
    pairs = unique_csv_values(DATABASE_DIR / "Project_Mirror_AB_Scorecard.csv", ("Pair_ID",))
    if pairs:
        return len(pairs)
    rows = read_csv(DATABASE_DIR / "Project_Mirror_AB_Scorecard.csv")
    return len(rows) // 2


def file_updated_since(path: Path, start: datetime) -> bool:
    if not path.exists():
        return False
    try:
        updated = datetime.fromtimestamp(path.stat().st_mtime, ET)
    except OSError:
        return False
    return updated >= start


def count_etsy_pod_published_since(start: datetime) -> int:
    ids: set[str] = set()
    for row in read_csv(DATABASE_DIR / "Etsy_Printify_Launch_Log.csv"):
        action = str(row.get("Action") or "").upper()
        status = str(row.get("Status") or "").upper()
        if action not in {"PUBLISH", "EXTERNAL_POLL"} or "PUBLISHED" not in status:
            continue
        stamp = parse_iso_et(row.get("Timestamp"))
        if not stamp or stamp < start:
            continue
        value = str(row.get("ID") or row.get("Printify_Etsy_Product_ID") or "").strip()
        if value:
            ids.add(value)
    return len(ids)


def count_printify_visual_qa_assets() -> int:
    ids = unique_csv_values(DATABASE_DIR / "Printify_Gallery_Duplicate_Audit.csv", ("ID", "Printify_Product_ID"))
    ids.update(unique_csv_values(DATABASE_DIR / "Printify_Production_Design_Audit.csv", ("ID", "Printify_Product_ID")))
    return len(ids)


def count_ebay_report_refreshes_since(start: datetime) -> int:
    diagnosis = any(
        file_updated_since(path, start)
        for path in (
            DATABASE_DIR / "eBay_Traffic_Diagnosis.csv",
            DATABASE_DIR / "eBay_Traffic_Diagnosis.md",
        )
    )
    experiment = any(
        file_updated_since(path, start)
        for path in (
            DATABASE_DIR / "eBay_Traffic_Experiment_Report.csv",
            DATABASE_DIR / "eBay_Traffic_Experiment_Report.md",
        )
    )
    return int(diagnosis) + int(experiment)


def process_alive(pid: int) -> bool:
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}"],
            text=True,
            capture_output=True,
            timeout=5,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except Exception:
        return False
    return str(pid) in (result.stdout or "")


def loop_pid_state() -> dict[str, Any]:
    if not PID_FILE.exists():
        return {"alive": False, "pid": None, "reason": "pid file missing"}
    try:
        pid = int(PID_FILE.read_text(encoding="utf-8").strip())
    except ValueError:
        return {"alive": False, "pid": None, "reason": "pid file unreadable"}
    return {"alive": process_alive(pid), "pid": pid, "reason": ""}


def windows_boot_time() -> datetime | None:
    now_monotonic = time.monotonic()
    cached = BOOT_CACHE.get("boot_time")
    if cached and now_monotonic - float(BOOT_CACHE.get("checked_at") or 0) < 300:
        return cached
    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToString('o')",
            ],
            text=True,
            capture_output=True,
            timeout=8,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        raw = (result.stdout or "").strip().splitlines()[0]
        parsed = datetime.fromisoformat(raw)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=ET)
        parsed = parsed.astimezone(ET)
    except Exception:
        parsed = None
    BOOT_CACHE["checked_at"] = now_monotonic
    BOOT_CACHE["boot_time"] = parsed
    return parsed


def parse_iso_et(value: object) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=ET)
    return parsed.astimezone(ET)


def next_shift_end(value: datetime) -> datetime:
    target = value.replace(hour=6, minute=0, second=0, microsecond=0)
    return target if value < target else target + timedelta(days=1)


def first_start_since(cutoff: datetime | None = None) -> datetime | None:
    if not STATE_FILE.exists():
        return None
    for line in STATE_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = LOOP_START_RE.match(line)
        if not match:
            continue
        stamp = parse_stamp(match.group("stamp"))
        if not stamp:
            continue
        if cutoff and stamp < cutoff:
            continue
        return stamp
    return None


def current_shift_window(now: datetime) -> dict[str, Any]:
    """Return the user-facing workday window.

    The denominator Rex cares about is not Windows uptime. It is the current
    monthly-task shift: first "continue monthly tasks" / long-loop start until
    the active weather/hardware duty deadline. The old 05:30/06:00 cutoff is
    only a no-forecast fallback; thermal/weather data wins when present.
    """
    payload = load_json(SHIFT_DUTY_WINDOW_FILE, {})
    start = parse_iso_et(payload.get("shift_start_et"))
    end = parse_iso_et(payload.get("shift_end_target_et"))
    if start and end and start <= now < end:
        return {"start": start, "end": end, "source": payload.get("source") or "shift-window-file"}

    # If the old window expired, infer from today's visible state.
    six_am_today = now.replace(hour=6, minute=0, second=0, microsecond=0)
    cycle_cutoff = six_am_today if now >= six_am_today else six_am_today - timedelta(days=1)
    inferred = first_start_since(cycle_cutoff) or now
    end = next_shift_end(inferred)
    repaired = {
        "shift_start_et": inferred.isoformat(),
        "shift_end_target_et": end.isoformat(),
        "source": "progress_dashboard_inferred",
        "note": "Inferred because no active Monthly_Shift_Duty_Window.json existed.",
    }
    try:
        SHIFT_DUTY_WINDOW_FILE.write_text(json.dumps(repaired, indent=2), encoding="utf-8")
    except OSError:
        pass
    return {"start": inferred, "end": end, "source": repaired["source"]}


def merge_intervals(intervals: list[tuple[datetime, datetime]], bridge_seconds: int = 20) -> list[tuple[datetime, datetime]]:
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda item: item[0])
    merged: list[tuple[datetime, datetime]] = [ordered[0]]
    bridge = timedelta(seconds=bridge_seconds)
    for start, end in ordered[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end + bridge:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))
    return merged


def duty_cycle_payload(now: datetime, pid_state: dict[str, Any]) -> dict[str, Any]:
    shift_window = current_shift_window(now)
    window_start = shift_window["start"]
    window_end = shift_window["end"]
    boot_time = windows_boot_time()
    available_seconds = max((now - window_start).total_seconds(), 1)
    intervals: list[tuple[datetime, datetime]] = []
    open_starts: dict[str, datetime] = {}
    first_event: datetime | None = None
    last_event: datetime | None = None

    if STATE_FILE.exists():
        for line in STATE_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
            start_match = LOOP_START_RE.match(line)
            if start_match:
                stamp = parse_stamp(start_match.group("stamp"))
                if not stamp:
                    continue
                if stamp < window_start:
                    continue
                key = start_match.group("num")
                open_starts[key] = stamp
                first_event = min(first_event, stamp) if first_event else stamp
                last_event = max(last_event, stamp) if last_event else stamp
                continue

            end_match = LOOP_END_RE.match(line)
            if not end_match:
                continue
            stamp = parse_stamp(end_match.group("stamp"))
            if not stamp or stamp < window_start:
                continue
            key = end_match.group("num")
            start = open_starts.pop(key, None)
            if start:
                intervals.append((start, max(stamp, start)))
            first_event = min(first_event, stamp) if first_event else stamp
            last_event = max(last_event, stamp) if last_event else stamp

    if pid_state.get("alive"):
        for start in open_starts.values():
            if start <= now:
                intervals.append((start, now))

    merged = merge_intervals(intervals)
    productive_seconds = sum((end - start).total_seconds() for start, end in merged)
    productive_seconds = min(productive_seconds, available_seconds)
    idle_seconds = max(available_seconds - productive_seconds, 0)
    percent = round((productive_seconds / available_seconds) * 100, 1)
    return {
        "percent": percent,
        "productive_minutes": round(productive_seconds / 60, 1),
        "available_minutes": round(available_seconds / 60, 1),
        "idle_minutes": round(idle_seconds / 60, 1),
        "window_start_et": window_start.isoformat(),
        "window_end_target_et": window_end.isoformat(),
        "boot_time_et": boot_time.isoformat() if boot_time else None,
        "source": shift_window.get("source"),
        "interval_count": len(merged),
        "first_event_et": first_event.isoformat() if first_event else None,
        "last_event_et": last_event.isoformat() if last_event else None,
        "status_class": "ok" if percent >= 95 else ("warn" if percent >= 80 else "bad"),
        "label": f"{percent}% productive this shift",
        "method": "START/END intervals from Monthly_Shift_Loop_State.md; denominator is shift start through now, target ends at adaptive weather/hardware duty deadline.",
    }


def read_recent_state_events(limit: int = 18) -> list[dict[str, str]]:
    if not STATE_FILE.exists():
        return []
    events: list[dict[str, str]] = []
    for line in STATE_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()[-250:]:
        match = STAMP_RE.match(line)
        if not match:
            continue
        events.append({"stamp": match.group("stamp"), "body": match.group("body")})
    return events[-limit:]


def active_age_minutes(latest_start: dict[str, Any] | None) -> float | None:
    if not latest_start:
        return None
    stamp = parse_stamp(str(latest_start.get("stamp") or ""))
    if not stamp:
        return None
    return round((datetime.now(ET) - stamp).total_seconds() / 60, 1)


def group_recent(completed: list[dict[str, Any]], minutes: int) -> dict[str, list[dict[str, Any]]]:
    now = datetime.now(ET)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in recent_items(completed, now, minutes):
        grouped.setdefault(str(item.get("project") or "Other"), []).append(item)
    return grouped


def project_key_for_command(command: str) -> str:
    label = COMMAND_PROJECT.get(command, command).lower()
    if "first audit" in label or "first_audit" in label or "shock" in label:
        return "first_audit"
    if "adobe" in label or "stock" in label:
        return "adobe_stock"
    if "ebay" in label:
        return "ebay"
    if "mirror" in label:
        return "project_mirror"
    if "etsy" in label or "printify" in label or "publish" in label:
        return "printify_etsy"
    return "overall"


def project_key_for_backlog(row: dict[str, Any]) -> str:
    haystack = " ".join(
        str(row.get(field, ""))
        for field in ("Lane", "Task", "Status", "Command", "Done_When")
    ).lower()
    for project, tokens in PROJECT_DETAIL_KEYS.items():
        if any(token in haystack for token in tokens):
            return project
    return "overall"


def build_project_details(
    dashboard: dict[str, Any],
    completed: list[dict[str, Any]],
    latest_start: dict[str, Any] | None,
    current_command: str,
) -> dict[str, Any]:
    rows = read_csv(DATABASE_DIR / "Factory_Backlog.csv")
    details: dict[str, Any] = {
        "overall": {
            "title": "Overall",
            "percent": progress_score(dashboard),
            "done": [],
            "working_on": [],
            "next": [],
            "notes": [remaining_line(dashboard)],
        },
        "printify_etsy": {"title": "Printify / Etsy", "percent": dashboard["printify_pct"], "done": [], "working_on": [], "next": [], "notes": []},
        "first_audit": {"title": "First Audit", "percent": dashboard["first_pct"], "done": [], "working_on": [], "next": [], "notes": []},
        "adobe_stock": {"title": "Adobe Stock", "percent": dashboard["adobe_pct"], "done": [], "working_on": [], "next": [], "notes": []},
        "ebay": {"title": "eBay", "percent": dashboard["ebay_pct"], "done": [], "working_on": [], "next": [], "notes": []},
        "project_mirror": {"title": "Project Mirror", "percent": dashboard["mirror_pct"], "done": [], "working_on": [], "next": [], "notes": []},
    }

    current_project = project_key_for_command(current_command)
    current_note = f"Running now: {current_command}"
    if latest_start:
        current_note += f" since {latest_start.get('stamp')}"
    details.setdefault(current_project, details["overall"])["working_on"].append(current_note)
    details["overall"]["working_on"].append(current_note)

    for item in completed[-18:]:
        project = project_key_for_command(str(item.get("name") or ""))
        line = compact_label(
            f"{item.get('stamp', '')} | {item.get('name', '')} | {item.get('status', '')}"
            + (f" | {item.get('tail')}" if item.get("tail") else ""),
            150,
        )
        if line not in details[project]["done"]:
            details[project]["done"].append(line)
        if line not in details["overall"]["done"]:
            details["overall"]["done"].append(line)

    for row in rows:
        project = project_key_for_backlog(row)
        status = str(row.get("Status") or "").upper()
        task = compact_label(str(row.get("Task") or row.get("Command") or "Unnamed task"))
        command = compact_label(str(row.get("Command") or ""), 80)
        line = f"{task} [{status or 'NO_STATUS'}]"
        if command:
            line += f" - {command}"

        target = details.get(project, details["overall"])
        if status.startswith("DONE"):
            if len(target["done"]) < 10:
                target["done"].append(line)
        elif status.startswith(("WAIT", "READY", "HOLD")):
            if len(target["working_on"]) < 8:
                target["working_on"].append(line)
        else:
            if len(target["next"]) < 8:
                target["next"].append(line)

    details["printify_etsy"]["notes"] = [
        f"Etsy live: digital {dashboard['digital_live']}, POD {dashboard['pod_live']}; spend ${dashboard['etsy_spend']:.2f}/${dashboard['etsy_cap']:.2f}.",
        "Daily direction: prioritize high-quality POD over more low-value digital volume.",
    ]
    details["first_audit"]["notes"] = [
        f"Release folders/manifest count: {dashboard['first_done']}/30.",
        "Priority is temporarily lowered because cousin review moved to early June.",
        "Top-tier First Audit assets require Rex visual approval before premium upscale.",
    ]
    details["adobe_stock"]["notes"] = [
        (
            f"Expanded DNA: {dashboard.get('adobe_expanded_rows', 0)}; daily queue: "
            f"{dashboard.get('adobe_daily_queue_rows', 0)}; generated batch: {dashboard.get('adobe_rows', 0)}."
        ),
        (
            f"Image QA pass: {dashboard.get('adobe_image_pass', 0)}; metadata QA pass: "
            f"{dashboard.get('adobe_metadata_pass', 0)}; upload-ready: "
            f"{dashboard.get('adobe_upload_ready', 0)}; strict curated: "
            f"{dashboard.get('adobe_curated_ready', 0)}; UI status: "
            f"{dashboard.get('adobe_ui_status') or 'not checked'}."
        ),
        "Current P1: get the first conservative Adobe Stock pilot through Contributor upload, then target 50 QA-passed images/day.",
        "Keep this visually separated from Etsy/eBay; stock assets are material/background bricks, not studio products.",
    ]
    details["ebay"]["notes"] = [
        "Publish path still needs clean shipping/source readback before scaling.",
        "Sticker expansion is frozen; focus on poster/acrylic/high-value experiments.",
    ]
    details["project_mirror"]["notes"] = [
        f"A/B pairs scored: {dashboard['mirror_pairs']}.",
        "Purpose: distill premium reference DNA before promoting to Studio-grade products.",
    ]

    for value in details.values():
        for bucket in ("done", "working_on", "next", "notes"):
            value[bucket] = value[bucket][:10] or ["No current entries in this bucket."]
    return details


def normalize_project_id(value: str) -> str:
    key = (value or "overall").strip().lower()
    return PROJECT_SLUGS.get(key, "overall")


def status_for_project(project_id: str, dashboard: dict[str, Any], pid_state: dict[str, Any]) -> dict[str, str]:
    blockers = " | ".join(str(item) for item in dashboard.get("blockers", []))
    if not pid_state.get("alive"):
        return {"label": "ERROR", "class": "bad", "reason": "long-shift loop is not alive"}
    if project_id == "ebay" and "eBay publish frozen" in blockers:
        return {"label": "READ/DIAG", "class": "warn", "reason": "publish path frozen; read/diagnostic work only"}
    if project_id == "adobe_stock" and "Adobe waiting image QA" in blockers:
        return {"label": "NEEDS QA", "class": "warn", "reason": "image QA is the next gate"}
    if project_id == "adobe_stock" and "Adobe Contributor login needed" in blockers:
        return {"label": "LOGIN", "class": "warn", "reason": "Contributor login is needed before upload automation"}
    if project_id == "printify_etsy" and dashboard.get("etsy_spend", 0) >= dashboard.get("etsy_cap", 50):
        return {"label": "SPEND CAP", "class": "bad", "reason": "Etsy fee cap reached"}
    return {"label": "RUNNING", "class": "ok", "reason": "no immediate Rex intervention"}


def today_etsy_spend() -> float:
    today = datetime.now(ET).date().isoformat()
    total = 0.0
    for row in read_csv(DATABASE_DIR / "Etsy_Fee_Ledger.csv"):
        status = str(row.get("Status", ""))
        if not status.startswith("CONFIRMED"):
            continue
        stamp_blob = " ".join(str(row.get(name, "")) for name in ("Timestamp", "ET_Timestamp", "Created_At", "Date"))
        if today not in stamp_blob:
            continue
        raw = str(row.get("Confirmed_Spent_USD") or "0").replace("$", "").strip()
        try:
            total += float(raw)
        except ValueError:
            continue
    return round(total, 2)


def latest_output_for_project(project_id: str, completed: list[dict[str, Any]], details: dict[str, Any]) -> str:
    for item in reversed(completed):
        if project_key_for_command(str(item.get("name") or "")) == project_id:
            tail = str(item.get("tail") or "").strip()
            return compact_label(tail or str(item.get("name") or ""), 110)
    done = details.get(project_id, {}).get("done", [])
    if done:
        return compact_label(str(done[0]), 110)
    return "No recent output recorded."


def eta_for_project(project_id: str, progress: dict[str, int]) -> dict[str, Any]:
    if project_id == "overall":
        hours = sum(
            max(0, PROJECT_MVP_TOTAL_HOURS[key] * (100 - progress[key]) / 100)
            for key in PROJECT_MVP_TOTAL_HOURS
        )
        return {
            "hours_remaining": round(hours, 1),
            "label": f"{round(hours, 1)}h to current multi-project MVP",
            "basis": "Sum of project MVP remaining-hour estimates.",
        }
    total = PROJECT_MVP_TOTAL_HOURS.get(project_id, 20)
    hours = max(0, total * (100 - progress.get(project_id, 0)) / 100)
    return {
        "hours_remaining": round(hours, 1),
        "label": f"{round(hours, 1)}h remaining",
        "basis": f"Estimated MVP total {total}h x remaining progress.",
    }


def pipeline_cards(
    dashboard: dict[str, Any],
    completed: list[dict[str, Any]],
    details: dict[str, Any],
    pid_state: dict[str, Any],
) -> list[dict[str, Any]]:
    progress = {
        "overall": progress_score(dashboard),
        "printify_etsy": dashboard["printify_pct"],
        "first_audit": dashboard["first_pct"],
        "adobe_stock": dashboard["adobe_pct"],
        "project_mirror": dashboard["mirror_pct"],
        "ebay": dashboard["ebay_pct"],
    }
    etsy_today = today_etsy_spend()
    costs = {
        "overall": f"Etsy ${etsy_today:.2f} today / ${dashboard['etsy_spend']:.2f} total",
        "printify_etsy": f"Etsy ${etsy_today:.2f} today; cap ${dashboard['etsy_cap']:.2f}",
        "first_audit": "Tracked $0.00; MJ upscale only after Rex approval",
        "adobe_stock": "Tracked $0.00; no listing fee; upload waits for Contributor login",
        "project_mirror": "Tracked $0.00; reference/DNA work",
        "ebay": "Tracked $0.00; read/diagnostic work",
    }
    cards = []
    for project_id in ("overall", "printify_etsy", "first_audit", "adobe_stock", "project_mirror", "ebay"):
        status = status_for_project(project_id, dashboard, pid_state)
        eta = eta_for_project(project_id, progress)
        latest_output = latest_output_for_project(project_id, completed, details)
        if project_id == "adobe_stock":
            latest_output = (
                f"DNA {dashboard.get('adobe_expanded_rows', 0)}, generated {dashboard.get('adobe_rows', 0)}, "
                f"image QA {dashboard.get('adobe_image_pass', 0)}, metadata QA {dashboard.get('adobe_metadata_pass', 0)}, "
                f"upload-ready {dashboard.get('adobe_upload_ready', 0)}, UI {dashboard.get('adobe_ui_status') or 'not checked'}"
            )
        cards.append(
            {
                "id": project_id,
                "title": PROJECT_META[project_id]["title"],
                "short": PROJECT_META[project_id]["short"],
                "progress": progress[project_id],
                "status": status["label"],
                "status_class": status["class"],
                "status_reason": status["reason"],
                "daily_cost": costs[project_id],
                "eta": eta,
                "latest_output": latest_output,
            }
        )
    return cards


def project_log_tail(project_id: str, limit: int = 50) -> list[str]:
    if not STATE_FILE.exists():
        return []
    lines = STATE_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
    result: list[str] = []
    for line in reversed(lines):
        lowered = line.lower()
        if project_id == "overall" or any(token in lowered for token in PROJECT_DETAIL_KEYS.get(project_id, ())):
            result.append(line)
        if len(result) >= limit:
            break
    return list(reversed(result))


def project_error_blocks(project_id: str, limit: int = 8) -> list[dict[str, str]]:
    sources = [STATE_FILE, PROJECT_ROOT / "PROGRESS_LOG.md", DATABASE_DIR / "Etsy_API_Status.json", PROJECT_ROOT / "Account_Risk_State.json"]
    blocks: list[dict[str, str]] = []
    tokens = PROJECT_DETAIL_KEYS.get(project_id, ())
    for source in sources:
        if not source.exists():
            continue
        text = source.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        matched: list[str] = []
        for line in lines[-500:]:
            lowered = line.lower()
            if not any(pattern in lowered for pattern in ERROR_PATTERNS):
                continue
            if project_id != "overall" and tokens and not any(token in lowered for token in tokens):
                continue
            matched.append(line)
        if matched:
            blocks.append({"source": str(source), "text": "\n".join(matched[-12:])})
        if len(blocks) >= limit:
            break
    return blocks


def newest_image(paths: list[Path]) -> Path | None:
    images: list[Path] = []
    for root in paths:
        if not root.exists():
            continue
        if root.is_file() and root.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            images.append(root)
            continue
        for suffix in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
            images.extend(root.rglob(suffix))
    if not images:
        return None
    return max(images, key=lambda p: p.stat().st_mtime)


def thumbnail_data_uri(project_id: str) -> dict[str, str] | None:
    image = newest_image(PROJECT_THUMB_DIRS.get(project_id, []))
    if not image:
        return None
    try:
        data = image.read_bytes()
    except OSError:
        return None
    # Keep the HUD light. If the latest image is huge, still show the path and skip inline base64.
    if len(data) > 1_500_000:
        return {"path": str(image), "data_uri": "", "note": "Latest image is larger than 1.5 MB; open path directly."}
    mime = "image/png" if image.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(data).decode("ascii")
    return {"path": str(image), "data_uri": f"data:{mime};base64,{encoded}", "note": ""}


def daily_task_counts(completed: list[dict[str, Any]], shift_start: datetime) -> dict[str, int]:
    # These counters are deliberately anchored to durable artifacts instead of
    # repeated loop command counts. The long shift re-runs many jobs by design;
    # counting command executions would make the HUD look busier than the real
    # production state.
    etsy_published = count_etsy_pod_published_since(shift_start)
    printify_visual_checks = count_printify_visual_qa_assets()
    adobe_qa_ready = sum(
        1
        for row in read_csv(DATABASE_DIR / "Adobe_Stock_Pilot_Batch.csv")
        if str(row.get("QA_Status") or "").startswith("QA_PASS")
    )
    adobe_metadata_rows = sum(
        1
        for row in read_csv(DATABASE_DIR / "Adobe_Stock_Metadata_QA.csv")
        if str(row.get("QA_Status") or "") == "METADATA_QA_PASS"
    )
    ebay_actions = count_ebay_report_refreshes_since(shift_start)
    first_audit_assets = len(read_csv(DATABASE_DIR / "First_Audit_001_Asset_Manifest.csv"))
    mirror_pairs = unique_project_mirror_pairs()
    return {
        "etsy_pod_daily": etsy_published,
        "printify_visual_qa": printify_visual_checks,
        "adobe_qa_assets": adobe_qa_ready,
        "adobe_metadata_rows": adobe_metadata_rows,
        "ebay_quality_actions": ebay_actions,
        "first_audit_assets": first_audit_assets,
        "mirror_dna": mirror_pairs,
    }


def daily_task_payload(
    dashboard: dict[str, Any],
    completed: list[dict[str, Any]],
    now: datetime,
    duty_cycle: dict[str, Any],
) -> dict[str, Any]:
    shift_start = parse_iso_et(duty_cycle.get("window_start_et")) or now
    shift_end = parse_iso_et(duty_cycle.get("window_end_target_et")) or next_shift_end(now)
    counts = daily_task_counts(completed, shift_start)
    tasks: list[dict[str, Any]] = []
    for task_def in DAILY_TASK_DEFS:
        done = int(counts.get(task_def["id"], 0))
        target_min = int(task_def["target_min"])
        target_max = int(task_def["target_max"])
        pct = int(min(100, round((done / max(target_max, 1)) * 100)))
        if done >= target_max:
            status, status_class = "DONE", "ok"
        elif done >= target_min:
            status, status_class = "ON TRACK", "ok"
        elif done > 0:
            status, status_class = "PARTIAL", "warn"
        else:
            status, status_class = "PENDING", "warn"
        if task_def["id"] == "ebay_quality_actions" and any("eBay publish frozen" in str(item) for item in dashboard.get("blockers", [])):
            status = "REPAIR ONLY"
            status_class = "warn"
        if task_def["id"] == "etsy_pod_daily" and dashboard.get("etsy_spend", 0) >= dashboard.get("etsy_cap", 50):
            status = "SPEND CAP"
            status_class = "bad"
        tasks.append(
            {
                **task_def,
                "done": done,
                "percent": pct,
                "status": status,
                "status_class": status_class,
                "gap_to_min": max(0, target_min - done),
                "gap_to_max": max(0, target_max - done),
            }
        )

    by_project: dict[str, list[dict[str, Any]]] = {}
    for task in tasks:
        by_project.setdefault(str(task["project_id"]), []).append(task)
    for project_tasks in by_project.values():
        project_tasks.sort(key=lambda item: int(item.get("priority", 99)))

    required = len(tasks)
    on_track = sum(1 for task in tasks if task["status_class"] == "ok")
    active = sum(1 for task in tasks if task["done"] > 0)
    return {
        "shift_start_et": shift_start.isoformat(),
        "shift_end_target_et": shift_end.isoformat(),
        "tasks": tasks,
        "by_project": by_project,
        "summary": {
            "on_track": on_track,
            "active": active,
            "total": required,
            "label": f"{on_track}/{required} daily lanes on track, {active}/{required} have movement today.",
        },
    }


def read_work_proofs(limit: int = 12) -> list[dict[str, Any]]:
    path = DATABASE_DIR / "Work_Proof_Log.jsonl"
    if not path.exists():
        latest = load_json(DATABASE_DIR / "Work_Proof_Latest.json", {})
        return [latest] if latest else []
    rows: list[dict[str, Any]] = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines()[-max(limit * 4, 40) :]:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    except OSError:
        return []
    return rows[-limit:]


def two_hour_progress_payload(completed: list[dict[str, Any]], now: datetime) -> dict[str, Any]:
    recent_120 = group_recent(completed, 120)
    grouped = groupedEntries = {
        project: len(items)
        for project, items in sorted(recent_120.items(), key=lambda item: (-len(item[1]), item[0]))
    }
    proofs = read_work_proofs(limit=10)
    proof_items: list[dict[str, Any]] = []
    for proof in reversed(proofs[-8:]):
        proof_items.append(
            {
                "time": proof.get("recorded_at_et") or proof.get("ended_at_et") or "",
                "source": proof.get("source") or "",
                "project": proof.get("project") or "",
                "summary": proof.get("summary") or "",
                "artifacts": proof.get("artifacts") or [],
            }
        )
    top = next(iter(grouped.items()), ("none", 0))
    return {
        "window": window_label(now, 120),
        "grouped_counts": grouped,
        "total_completed": sum(grouped.values()),
        "top_project": top[0],
        "top_count": top[1],
        "work_proofs": proof_items,
        "judgment": (
            "Active progress detected across multiple projects."
            if sum(grouped.values()) > 0
            else "No completed command in the last 2 hours; check loop/blocker."
        ),
    }


def project_payload(project_id: str) -> dict[str, Any]:
    project_id = normalize_project_id(project_id)
    base = dashboard_payload()
    cards = {card["id"]: card for card in base["pipeline_cards"]}
    detail = base["project_details"].get(project_id, base["project_details"]["overall"])
    return {
        "updated_at_et": base["updated_at_et"],
        "project_id": project_id,
        "card": cards.get(project_id, cards["overall"]),
        "detail": detail,
        "log_tail": project_log_tail(project_id),
        "errors": project_error_blocks(project_id),
        "thumbnail": thumbnail_data_uri(project_id),
        "loop": base["loop"],
        "blockers": base["blockers"],
        "rex_actions": base.get("rex_actions", []),
        "daily_tasks": base["daily_tasks"]["by_project"].get(project_id, []),
    }


def dashboard_payload() -> dict[str, Any]:
    now = datetime.now(ET)
    completed, latest_start = parse_state()
    dashboard = project_dashboard()
    trigger = load_json(TRIGGER_FILE, {})
    pid_state = loop_pid_state()
    current_count = max((int(item["num"]) for item in completed), default=0)
    latest_end = completed[-1] if completed else None
    current_command = trigger.get("current_command") or (latest_start or {}).get("name") or "unknown"
    recent_30 = group_recent(completed, 30)
    recent_120 = group_recent(completed, 120)
    details = build_project_details(dashboard, completed, latest_start, str(current_command))
    duty_cycle = duty_cycle_payload(now, pid_state)
    daily_tasks = daily_task_payload(dashboard, completed, now, duty_cycle)

    return {
        "updated_at_et": now.isoformat(timespec="seconds"),
        "windows": {
            "last_10": window_label(now, 30),
            "last_60": window_label(now, 120),
            "auto_refresh": "15 seconds",
            "hourly_detail": "project details refresh from local state every 15 seconds; page shell hard-reloads hourly",
            "log_retention": "12h active detail compaction; 7d archive window for verified history",
        },
        "loop": {
            **pid_state,
            "total_completed": current_count,
            "current_command": current_command,
            "latest_start": latest_start,
            "latest_end": latest_end,
            "active_age_minutes": active_age_minutes(latest_start),
        },
        "duty_cycle": duty_cycle,
        "daily_tasks": daily_tasks,
        "projects": {
            "overall": progress_score(dashboard),
            "printify_etsy": dashboard["printify_pct"],
            "first_audit": dashboard["first_pct"],
            "adobe_stock": dashboard["adobe_pct"],
            "ebay": dashboard["ebay_pct"],
            "project_mirror": dashboard["mirror_pct"],
        },
        "counters": {
            "etsy_digital_live": dashboard["digital_live"],
            "etsy_pod_live": dashboard["pod_live"],
            "etsy_spend": dashboard["etsy_spend"],
            "etsy_cap": dashboard["etsy_cap"],
            "first_audit_done": dashboard["first_done"],
            "adobe_mentor_rows": dashboard["adobe_mentor_rows"],
            "adobe_production_rows": dashboard["adobe_rows"],
            "adobe_expanded_rows": dashboard.get("adobe_expanded_rows", 0),
            "adobe_daily_queue_rows": dashboard.get("adobe_daily_queue_rows", 0),
            "adobe_image_pass": dashboard.get("adobe_image_pass", 0),
            "adobe_metadata_pass": dashboard.get("adobe_metadata_pass", 0),
            "adobe_upload_ready": dashboard.get("adobe_upload_ready", 0),
            "adobe_curated_ready": dashboard.get("adobe_curated_ready", 0),
            "adobe_ui_status": dashboard.get("adobe_ui_status", ""),
            "project_mirror_pairs": dashboard["mirror_pairs"],
            "v7_ready": dashboard["v7_ready"],
        },
        "blockers": dashboard["blockers"],
        "rex_actions": dashboard.get("rex_actions", []),
        "visual_qa": adobe_visual_review_summary(),
        "remaining": remaining_line(dashboard),
        "recent": {
            "last_10_min_summary": summarize_recent(completed, latest_start, now, minutes=30, verbose=True),
            "last_60_min_summary": summarize_recent(completed, latest_start, now, minutes=120, verbose=True),
            "last_10_min": recent_30,
            "last_60_min": recent_120,
        },
        "two_hour_progress": two_hour_progress_payload(completed, now),
        "pipeline_cards": pipeline_cards(dashboard, completed, details, pid_state),
        "project_details": details,
        "events": read_recent_state_events(),
        "brief_file": str(BRIEF_FILE),
    }


ADOBE_QA_FIELDS = ["Parent_Asset_ID", "Decision", "Reason", "Updated_ET"]


def write_dict_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def project_relative_path(path_text: str) -> Path | None:
    if not path_text:
        return None
    path = Path(path_text)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    try:
        resolved = path.resolve()
        resolved.relative_to(PROJECT_ROOT.resolve())
    except (OSError, ValueError):
        return None
    return resolved


def adobe_decisions() -> dict[str, dict[str, str]]:
    return {
        row.get("Parent_Asset_ID", ""): row
        for row in read_csv(ADOBE_QA_FILE)
        if row.get("Parent_Asset_ID")
    }


def adobe_quality_by_asset() -> dict[str, dict[str, str]]:
    return {
        row.get("Parent_Asset_ID", ""): row
        for row in read_csv(ADOBE_LOCAL_UPSCALED_FILE)
        if row.get("Parent_Asset_ID")
    }


def interleave_by_family(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    order: list[str] = []
    for item in items:
        family = str(item.get("family") or item.get("source") or "Other")
        if family not in grouped:
            grouped[family] = []
            order.append(family)
        grouped[family].append(item)
    mixed: list[dict[str, Any]] = []
    while any(grouped.values()):
        for family in order:
            if grouped[family]:
                mixed.append(grouped[family].pop(0))
    return mixed


def adobe_visual_review_summary() -> dict[str, Any]:
    ready = read_csv(ADOBE_UPLOAD_READY_FILE)
    decisions = adobe_decisions()
    first_submit = read_csv(ADOBE_FIRST_SUBMIT_FILE)
    counts = {"PASS": 0, "REJECT": 0, "HOLD": 0, "PENDING": 0}
    samples: list[dict[str, str]] = []
    for row in ready:
        parent_id = str(row.get("Parent_Asset_ID") or "").strip()
        decision = str(decisions.get(parent_id, {}).get("Decision") or "PENDING").upper()
        if decision not in counts:
            decision = "PENDING"
        counts[decision] += 1
        if decision in {"PENDING", "HOLD"} and len(samples) < 5:
            samples.append(
                {
                    "id": parent_id,
                    "family": str(row.get("Family") or ""),
                    "title": str(row.get("Title") or ""),
                    "decision": decision,
                }
            )
    if not samples:
        for row in first_submit[:7]:
            samples.append(
                {
                    "id": str(row.get("Parent_Asset_ID") or ""),
                    "family": str(row.get("Family") or ""),
                    "title": str(row.get("Title") or ""),
                    "decision": "FIRST_SUBMIT",
                }
            )
    return {
        "adobe_qa_url": "/adobe-qa",
        "ready_count": len(ready),
        "first_submit_count": len(first_submit),
        "counts": counts,
        "needs_rex_count": counts["PENDING"] + counts["HOLD"],
        "samples": samples,
        "first_submit_csv": str(ADOBE_FIRST_SUBMIT_FILE),
        "ready_csv": str(ADOBE_UPLOAD_READY_FILE),
    }


def adobe_qa_payload() -> dict[str, Any]:
    ready = read_csv(ADOBE_UPLOAD_READY_FILE)
    decisions = adobe_decisions()
    quality = adobe_quality_by_asset()
    items: list[dict[str, Any]] = []
    for index, row in enumerate(ready, start=1):
        parent_id = str(row.get("Parent_Asset_ID") or "")
        decision = decisions.get(parent_id, {})
        decision_value = str(decision.get("Decision") or "PENDING").upper()
        if decision_value != "PENDING":
            continue
        qrow = quality.get(parent_id, {})
        local_path = str(row.get("Local_Path") or "")
        items.append(
            {
                "index": index,
                "parent_asset_id": parent_id,
                "family": row.get("Family", ""),
                "title": row.get("Title", ""),
                "filename": row.get("Filename", ""),
                "local_path": local_path,
                "image_url": f"/asset?path={local_path}",
                "decision": decision_value,
                "reason": decision.get("Reason", ""),
                "updated_et": decision.get("Updated_ET", ""),
                "width": qrow.get("Width", ""),
                "height": qrow.get("Height", ""),
                "pixels": qrow.get("Pixels", ""),
                "edge_score": qrow.get("Edge_Detail_Score", ""),
                "qa_status": qrow.get("QA_Status", row.get("Status", "")),
                "issues": qrow.get("Issues", ""),
                "source": "upload_ready",
            }
        )
    # Rex training queue: show locally upscaled Adobe candidates that have not
    # received a Rex decision yet, even when the local automated QA is holding
    # them. These are not upload-ready, but they are useful visual training
    # material and make the QA page non-empty while new MJ grids are still
    # harvesting.
    for row in read_csv(ADOBE_LOCAL_UPSCALED_FILE):
        parent_id = str(row.get("Parent_Asset_ID") or "").strip()
        if not parent_id:
            continue
        decision = decisions.get(parent_id, {})
        decision_value = str(decision.get("Decision") or "PENDING").upper()
        if decision_value != "PENDING":
            continue
        local_path = str(row.get("Upscaled_Path") or row.get("Source_Path") or "")
        if not local_path:
            continue
        resolved = project_relative_path(local_path)
        if not resolved or not resolved.exists():
            continue
        qa_status = str(row.get("QA_Status") or "")
        items.append(
            {
                "index": 0,
                "parent_asset_id": parent_id,
                "family": row.get("Family", ""),
                "title": row.get("Title", ""),
                "filename": Path(local_path).name,
                "local_path": str(resolved),
                "image_url": f"/asset?path={resolved}",
                "decision": decision_value,
                "reason": decision.get("Reason", ""),
                "updated_et": decision.get("Updated_ET", ""),
                "width": row.get("Width", ""),
                "height": row.get("Height", ""),
                "pixels": row.get("Pixels", ""),
                "edge_score": row.get("Edge_Detail_Score", ""),
                "qa_status": qa_status,
                "issues": row.get("Issues", ""),
                "source": "local_upscaled_candidate",
            }
        )
    market_items: list[dict[str, Any]] = []
    for row in read_csv(ADOBE_MARKET_SAMPLE_FILE):
        sku = str(row.get("Internal_SKU") or row.get("Source_Queue_ID") or "").strip()
        output_folder = str(row.get("Output_Folder") or "").strip()
        grid = str(row.get("Grid_File") or "").strip()
        if not grid and sku and output_folder:
            # The harvester can download a grid before the CSV row is rewritten
            # by a later recovery pass. The QA UI is Rex's training surface, so
            # prefer the physical file if it exists instead of hiding real work.
            expected = PROJECT_ROOT / output_folder / f"{sku}_Grid.png"
            if expected.exists():
                grid = str(expected)
        grid_path = project_relative_path(grid)
        if not grid_path or not grid_path.exists():
            continue
        parent_id = sku
        decision = decisions.get(parent_id, {})
        decision_value = str(decision.get("Decision") or "PENDING").upper()
        if decision_value != "PENDING":
            continue
        concept = str(row.get("Concept_Name") or "")
        family = concept.split(" / ")[0] if concept else "Market sample"
        market_items.append(
            {
                "index": 0,
                "parent_asset_id": parent_id,
                "family": family,
                "title": row.get("Adobe_Title", ""),
                "filename": Path(grid).name,
                "local_path": str(grid_path),
                "image_url": f"/asset?path={grid_path}",
                "decision": decision_value,
                "reason": decision.get("Reason", ""),
                "updated_et": decision.get("Updated_ET", ""),
                "width": "grid",
                "height": "draft",
                "pixels": "",
                "edge_score": "",
                "qa_status": "MARKET_TRAINING_GRID",
                "issues": row.get("Review_Note", ""),
                "source": "market_training",
            }
        )
    # Put mixed market-training grids first because Rex is training taste before
    # upload. Interleave them so one material family does not dominate the page.
    items = interleave_by_family(market_items) + items
    for index, item in enumerate(items, start=1):
        item["index"] = index
    counts: dict[str, int] = {}
    for item in items:
        counts[item["decision"]] = counts.get(item["decision"], 0) + 1
    source_counts: dict[str, int] = {}
    for item in items:
        source = str(item.get("source") or "unknown")
        source_counts[source] = source_counts.get(source, 0) + 1
    return {
        "updated_at_et": datetime.now(ET).isoformat(timespec="seconds"),
        "count": len(items),
        "counts": counts,
        "source_counts": source_counts,
        "items": items,
        "qa_file": str(ADOBE_QA_FILE),
    }


def save_adobe_decision(payload: dict[str, Any]) -> dict[str, Any]:
    parent_id = str(payload.get("parent_asset_id") or "").strip()
    decision = str(payload.get("decision") or "").strip().upper()
    reason = str(payload.get("reason") or "").strip()
    if not parent_id:
        raise ValueError("missing parent_asset_id")
    if decision not in {"PASS", "REJECT", "HOLD", "PENDING"}:
        raise ValueError("decision must be PASS, REJECT, HOLD, or PENDING")
    rows = read_csv(ADOBE_QA_FILE)
    by_id = {row.get("Parent_Asset_ID", ""): row for row in rows if row.get("Parent_Asset_ID")}
    if decision == "PENDING":
        by_id.pop(parent_id, None)
    else:
        by_id[parent_id] = {
            "Parent_Asset_ID": parent_id,
            "Decision": decision,
            "Reason": reason,
            "Updated_ET": datetime.now(ET).strftime("%Y-%m-%d %H:%M EDT"),
        }
    write_dict_rows(ADOBE_QA_FILE, list(by_id.values()), ADOBE_QA_FIELDS)
    return {"ok": True, "parent_asset_id": parent_id, "decision": decision}


ADOBE_QA_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Adobe Stock QA</title>
  <style>
    :root { color-scheme: dark; --bg:#0f1215; --panel:#171b20; --line:#303743; --text:#f3f5f7; --muted:#a6b0ba; --ok:#69d6a3; --bad:#ff6b6b; --warn:#ffd166; --blue:#8ecae6; }
    body { margin:0; background:var(--bg); color:var(--text); font-family:Segoe UI, Arial, sans-serif; }
    main { max-width:1520px; margin:0 auto; padding:20px; }
    header { display:flex; justify-content:space-between; gap:16px; align-items:flex-end; margin-bottom:14px; }
    h1 { margin:0; font-size:25px; }
    .sub { color:var(--muted); font-size:13px; margin-top:6px; }
    a { color:var(--blue); text-decoration:none; }
    .stats { display:flex; gap:8px; flex-wrap:wrap; }
    .badge { padding:7px 10px; border-radius:999px; font-weight:800; font-size:12px; letter-spacing:.04em; background:#25303b; }
    .pass { background:#173228; color:var(--ok); }
    .reject { background:#392127; color:var(--bad); }
    .hold { background:#3a321e; color:var(--warn); }
    .pending { background:#26303a; color:#cbd5df; }
    .grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; }
    .card { background:var(--panel); border:1px solid var(--line); border-radius:12px; overflow:hidden; box-shadow:0 10px 24px rgba(0,0,0,.18); }
    .card.pass-card { border-color:#28765e; }
    .card.reject-card { border-color:#743240; opacity:.72; }
    .card.hold-card { border-color:#80662c; }
    .image-wrap { background:#0a0d10; min-height:220px; display:flex; align-items:center; justify-content:center; }
    img { width:100%; height:260px; object-fit:contain; display:block; }
    .body { padding:12px; }
    .title { font-weight:850; line-height:1.25; margin-bottom:7px; }
    .meta { color:var(--muted); font-size:12px; line-height:1.4; margin-bottom:9px; }
    textarea { width:100%; min-height:54px; border-radius:8px; border:1px solid #3b4653; background:#10151b; color:var(--text); padding:8px; resize:vertical; box-sizing:border-box; }
    .buttons { display:grid; grid-template-columns:repeat(5,1fr); gap:7px; margin-top:8px; }
    button { border:0; border-radius:8px; padding:9px 7px; cursor:pointer; font-weight:800; color:#0d1116; }
    button.pass { background:var(--ok); color:#07130e; }
    button.reject { background:var(--bad); color:#170607; }
    button.hold { background:var(--warn); color:#1b1300; }
    button.pending { background:#cbd5df; color:#10151b; }
    button.submit { background:#8ecae6; color:#07131a; }
    button.selected { outline:3px solid #f3f5f7; outline-offset:2px; }
    @media (max-width:1180px) { .grid { grid-template-columns:repeat(2,minmax(0,1fr)); } }
    @media (max-width:760px) { .grid { grid-template-columns:1fr; } header { display:block; } }
  </style>
</head>
<body>
<main>
  <header>
    <div>
      <h1>Adobe Stock Visual QA</h1>
      <div class="sub">Market-training grids are mixed by material family first; upload-ready images follow. Pass/Reject/Hold writes to <code>Database\Adobe_Stock_Rex_Visual_QA.csv</code>. Auto-refreshes every 20s.</div>
      <div class="sub"><a href="/">Back to HUD</a></div>
    </div>
    <div id="stats" class="stats"></div>
  </header>
  <section id="grid" class="grid"></section>
</main>
<script>
const safe = value => String(value ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const pendingDecisions = {};
function cls(decision) { return String(decision || 'PENDING').toLowerCase(); }
function button(item, decision, label) {
  const selected = String(item.decision || 'PENDING').toUpperCase() === decision ? ' selected' : '';
  return `<button class="${cls(decision)}${selected}" onclick="setPendingDecision('${safe(item.parent_asset_id)}','${decision}', this)">${label}</button>`;
}
function render(data) {
  const counts = data.counts || {};
  const sources = data.source_counts || {};
  document.getElementById('stats').innerHTML = ['PASS','REJECT','HOLD','PENDING'].map(k => `<span class="badge ${cls(k)}">${k}: ${counts[k] || 0}</span>`).join('') +
    `<span class="badge">Training: ${sources.market_training || 0}</span><span class="badge">Upload-ready: ${sources.upload_ready || 0}</span>`;
  document.getElementById('grid').innerHTML = (data.items || []).map(item => {
    const c = cls(item.decision);
    const commentId = `comment-${safe(item.parent_asset_id)}`;
    const pending = pendingDecisions[item.parent_asset_id] || item.decision || 'PENDING';
    return `<article class="card ${c}-card">
      <div class="image-wrap"><img loading="lazy" src="${safe(item.image_url)}" alt="${safe(item.parent_asset_id)}"></div>
      <div class="body">
        <div class="title">${item.index}. ${safe(item.family)} <span class="badge">${safe(item.source || '')}</span> <span class="badge ${c}">${safe(item.decision)}</span></div>
        <div class="meta">${safe(item.title)}<br>${safe(item.parent_asset_id)}<br>${safe(item.width)} x ${safe(item.height)} px - edge ${safe(item.edge_score || '--')} - ${safe(item.qa_status)}${item.issues ? '<br>Issues: ' + safe(item.issues) : ''}</div>
        <textarea id="${commentId}" placeholder="Rex comment / why pass or reject">${safe(item.reason)}</textarea>
        <div class="buttons">
          ${button({...item, decision: pending}, 'PASS', 'Positive')}
          ${button({...item, decision: pending}, 'REJECT', 'Negative')}
          ${button({...item, decision: pending}, 'HOLD', 'Rework')}
          ${button({...item, decision: pending}, 'PENDING', 'Clear')}
          <button class="submit" onclick="submitDecision('${safe(item.parent_asset_id)}')">Submit</button>
        </div>
      </div>
    </article>`;
  }).join('');
}
function setPendingDecision(parentId, decision, el) {
  pendingDecisions[parentId] = decision;
  const box = el.closest('.buttons');
  box.querySelectorAll('button').forEach(btn => btn.classList.remove('selected'));
  el.classList.add('selected');
}
async function submitDecision(parentId) {
  const decision = pendingDecisions[parentId] || 'PENDING';
  await saveDecision(parentId, decision);
}
async function saveDecision(parentId, decision) {
  const reason = document.getElementById(`comment-${parentId}`)?.value || '';
  const res = await fetch('/api/adobe-qa/decision', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({parent_asset_id:parentId, decision, reason})});
  if (!res.ok) alert(await res.text());
  await refresh();
}
async function refresh() {
  const res = await fetch('/api/adobe-qa', {cache:'no-store'});
  render(await res.json());
}
refresh();
setInterval(refresh, 20000);
</script>
</body>
</html>
"""


HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>OpenClaw HUD</title>
  <style>
    :root { color-scheme: dark; --bg:#0f1215; --panel:#171b20; --muted:#a6b0ba; --text:#f3f5f7; --ok:#69d6a3; --warn:#ffd166; --bad:#ff6b6b; --line:#303743; --blue:#8ecae6; }
    body { margin:0; font-family:Segoe UI, Arial, sans-serif; background:var(--bg); color:var(--text); }
    main { max-width:1480px; margin:0 auto; padding:22px; }
    header { display:flex; align-items:flex-end; justify-content:space-between; gap:16px; margin-bottom:18px; }
    h1 { margin:0; font-size:26px; letter-spacing:.2px; }
    .sub { color:var(--muted); font-size:13px; margin-top:6px; }
    .badge { padding:7px 10px; border-radius:999px; font-weight:800; font-size:12px; letter-spacing:.04em; }
    .ok { background:#1f352b; color:var(--ok); }
    .warn { background:#3a321e; color:var(--warn); }
    .bad { background:#392127; color:var(--bad); }
    .grid { display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:12px; }
    .card { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:14px; box-shadow:0 10px 28px rgba(0,0,0,.16); }
    .rex-panel { margin-bottom:12px; border:1px solid var(--line); border-radius:12px; padding:15px; background:#10151b; box-shadow:0 12px 32px rgba(0,0,0,.18); }
    .rex-panel.needs { border-color:#9d6b2a; background:linear-gradient(180deg,#22190d,#10151b); }
    .rex-panel.clear { border-color:#2c604f; background:linear-gradient(180deg,#0d1f1b,#10151b); }
    .rex-panel-head { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; }
    .rex-headline { margin-top:5px; color:#f6f8fb; font-size:20px; font-weight:850; line-height:1.25; }
    .rex-action-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; margin-top:12px; }
    .rex-action-card { border:1px solid #3b4653; background:#121820; border-radius:10px; padding:11px; }
    .rex-action-card.warn { border-color:#8a6d2e; background:#1d1a12; }
    .rex-action-card.bad { border-color:#8b3541; background:#211318; }
    .rex-action-card b { display:block; color:#f7fafc; margin-bottom:5px; }
    .rex-action-card span { display:block; color:var(--muted); font-size:12px; line-height:1.35; margin-top:5px; }
    .qa-panel { margin-bottom:12px; border:1px solid #384657; border-radius:12px; padding:15px; background:#10151b; box-shadow:0 12px 32px rgba(0,0,0,.18); }
    .qa-panel.needs { border-color:#bf9b30; background:linear-gradient(180deg,#251f0d,#10151b); }
    .qa-panel.clear { border-color:#2c604f; background:linear-gradient(180deg,#0d1f1b,#10151b); }
    .qa-head { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; }
    .qa-title { margin-top:5px; color:#f6f8fb; font-size:20px; font-weight:850; line-height:1.25; }
    .qa-actions { display:flex; flex-wrap:wrap; gap:9px; margin-top:12px; align-items:center; }
    .qa-button { display:inline-flex; align-items:center; justify-content:center; padding:10px 14px; border-radius:10px; border:1px solid #6cd6bf; background:#12302d; color:#eafff8; font-weight:900; }
    .qa-button.secondary { border-color:#435160; background:#131a22; color:#cbd6df; }
    .qa-stats { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }
    .qa-samples { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; margin-top:10px; }
    .qa-sample { border:1px solid #35404c; border-radius:9px; padding:9px; background:#121820; color:var(--muted); font-size:12px; line-height:1.35; }
    .qa-sample b { display:block; color:#f4f7fa; font-size:13px; margin-bottom:3px; }
    .pipeline { cursor:pointer; transition:border-color .2s, transform .2s; min-height:210px; display:flex; flex-direction:column; gap:9px; }
    .pipeline:hover { border-color:#70e1c8; transform:translateY(-1px); }
    .span2 { grid-column:span 2; }
    .span3 { grid-column:span 3; }
    .span4 { grid-column:span 4; }
    .span6 { grid-column:span 6; }
    .label { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.08em; }
    .title { font-size:16px; font-weight:750; color:#dfe7ef; min-height:40px; }
    .num { font-size:34px; font-weight:900; margin:0; }
    .bar { height:9px; border-radius:999px; background:#2a3038; overflow:hidden; }
    .bar > div { height:100%; background:linear-gradient(90deg,#70e1c8,#62d490); width:0; transition:width .35s; }
    .meta { color:var(--muted); font-size:13px; line-height:1.35; }
    .meta b { color:#dbe2e9; }
    .kv { display:grid; grid-template-columns:180px 1fr; gap:8px; font-size:14px; }
    .kv b { color:var(--muted); font-weight:600; }
    .duty-main { display:flex; align-items:center; justify-content:space-between; gap:10px; margin:8px 0; }
    .duty-main .duty-num { font-size:34px; font-weight:900; color:#fff; }
    .duty-detail { color:var(--muted); font-size:12px; line-height:1.45; }
    .duty-target { color:#dbe2e9; font-family:Consolas, ui-monospace, monospace; font-size:12px; }
    .mono { font-family:Consolas, ui-monospace, monospace; font-size:13px; }
    .events { max-height:300px; overflow:auto; }
    .event { border-top:1px solid var(--line); padding:8px 0; }
    .event:first-child { border-top:0; }
    .muted { color:var(--muted); }
    .pulse-head { display:flex; justify-content:space-between; align-items:baseline; gap:12px; margin:2px 0 10px; }
    .pulse-title { font-size:17px; font-weight:850; color:#f6f8fb; }
    .pulse-window { color:var(--muted); font-size:12px; font-family:Consolas, ui-monospace, monospace; }
    .pulse-kpi { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; margin-bottom:10px; }
    .kpi { border:1px solid #37414e; background:#11161c; border-radius:9px; padding:9px 10px; }
    .kpi b { display:block; font-size:22px; line-height:1; color:#ffffff; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    .kpi span { display:block; margin-top:4px; color:var(--muted); font-size:12px; }
    .chip-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; }
    .chip { border:1px solid #303946; background:#10151b; border-radius:9px; padding:9px 10px; min-height:62px; }
    .chip.priority { border-color:#6cd6bf; background:linear-gradient(180deg,#10201f,#10151b); }
    .chip.warn-chip { border-color:#64542a; background:#1d1a12; }
    .chip strong { display:flex; justify-content:space-between; gap:8px; font-size:14px; color:#eef4f8; }
    .chip .count { color:#70e1c8; font-size:16px; }
    .chip small { display:block; color:var(--muted); margin-top:6px; line-height:1.35; word-break:break-word; }
    .proof-list { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; margin-top:10px; }
    .proof-item { border:1px solid #33404c; background:#10151b; border-radius:9px; padding:9px 10px; }
    .proof-item b { display:block; color:#f4f7fa; margin-bottom:4px; }
    .proof-item small { color:var(--muted); line-height:1.35; display:block; }
    .daily-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; margin-top:10px; }
    .daily-task { border:1px solid #313a45; background:#10151b; border-radius:10px; padding:12px; min-height:130px; }
    .daily-task.key { border-color:#6cd6bf; background:linear-gradient(180deg,#10201f,#10151b); }
    .daily-head { display:flex; align-items:flex-start; justify-content:space-between; gap:10px; }
    .daily-title { font-size:15px; font-weight:800; color:#f4f7fa; line-height:1.25; }
    .daily-progress { font-size:24px; font-weight:900; margin:8px 0 6px; }
    .daily-note { color:var(--muted); font-size:12px; line-height:1.35; margin-top:7px; }
    .role-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:9px; margin-top:10px; }
    .role-box { background:#10151b; border:1px solid #313a45; border-radius:9px; padding:10px; }
    .role-box b { display:block; color:#f4f7fa; margin-bottom:5px; }
    .role-box span { color:var(--muted); font-size:12px; line-height:1.35; }
    details.raw { margin-top:9px; color:var(--muted); }
    details.raw summary { cursor:pointer; font-size:12px; letter-spacing:.03em; }
    details.raw p { margin:7px 0 0; font-size:12px; line-height:1.35; color:#8d98a4; }
    .divider { height:1px; background:var(--line); margin:14px 0; }
    a { color:var(--blue); text-decoration:none; }
    a:hover { text-decoration:underline; }
    @media (max-width:1120px) { .grid { grid-template-columns:1fr 1fr; } .span2,.span3,.span4,.span6 { grid-column:span 2; } }
    @media (max-width:1120px) { .daily-grid,.role-grid,.rex-action-grid { grid-template-columns:1fr; } }
  </style>
</head>
<body>
<main>
  <header>
    <div>
      <h1>OpenClaw V13 Observability HUD</h1>
      <div class="sub" id="refreshStatus">Read-only local dashboard. Auto-refreshes every 15 seconds.</div>
    </div>
    <div id="alive" class="badge warn">loading</div>
  </header>

  <section id="rexActionPanel" class="rex-panel clear">
    <div class="rex-panel-head">
      <div>
        <div class="label">Rex Action Required</div>
        <div id="rexActionHeadline" class="rex-headline">Checking blockers...</div>
      </div>
      <div id="rexActionBadge" class="badge warn">LOADING</div>
    </div>
    <div id="rexActionList" class="rex-action-grid"></div>
  </section>

  <section id="visualQaPanel" class="qa-panel clear">
    <div class="qa-head">
      <div>
        <div class="label">Visual QA Queue</div>
        <div id="visualQaHeadline" class="qa-title">Checking images that need Rex review...</div>
      </div>
      <div id="visualQaBadge" class="badge warn">LOADING</div>
    </div>
    <div id="visualQaStats" class="qa-stats"></div>
    <div class="qa-actions">
      <a class="qa-button" href="/adobe-qa">Open Adobe Stock Review UI</a>
      <a class="qa-button secondary" href="/project/adobe_stock">Open Adobe Detail</a>
    </div>
    <div id="visualQaSamples" class="qa-samples"></div>
  </section>

  <section class="grid" id="pipelineGrid"></section>

  <section class="grid" style="margin-top:12px;">
    <div class="card span6">
      <div class="pulse-head">
        <div>
          <div class="label">Daily Operating Targets</div>
          <div class="pulse-title" id="dailySummary">loading daily lanes...</div>
        </div>
        <div id="dailyWindow" class="pulse-window">--</div>
      </div>
      <div id="dailyTaskGrid" class="daily-grid"></div>
    </div>
    <div class="card span6">
      <div class="label">What "Long Shift Alive" Means</div>
      <div class="role-grid">
        <div class="role-box"><b>Background worker</b><span>Runs only validated conveyor-belt tasks from backlog/state files. It should not make strategy, account-risk, pricing, visual, or platform judgment calls.</span></div>
        <div class="role-box"><b>HUD</b><span>Reads local state every 15 seconds and turns work into visible progress, daily quotas, project ETA, logs, thumbnails, and CODEX_NEEDED blockers.</span></div>
        <div class="role-box"><b>Chat-Codex</b><span>Primary supervisor and decision layer. Until a lane is proven stable, I should stay involved in 95%+ of non-trivial work and take over any untrusted decision.</span></div>
      </div>
    </div>
    <div class="card span2">
      <div class="label">Current Loop</div>
      <div class="kv">
        <b>PID</b><span id="pid" class="mono">--</span>
        <b>Total completed</b><span id="completed" class="mono">--</span>
        <b>Current command</b><span id="cmd" class="mono">--</span>
        <b>Active age</b><span id="age" class="mono">--</span>
        <b>Updated</b><span id="updated" class="mono">--</span>
      </div>
      <div class="divider"></div>
      <div class="label">Duty Cycle This Shift</div>
      <div class="duty-main">
        <span id="dutyPct" class="duty-num">--%</span>
        <span id="dutyBadge" class="badge warn">loading</span>
      </div>
      <div class="bar"><div id="dutyBar"></div></div>
      <p id="dutyDetail" class="duty-detail">--</p>
      <p id="dutyTarget" class="duty-target">--</p>
    </div>
    <div class="card span4">
      <div class="label">Progress Pulse</div>
      <div class="pulse-head">
        <div class="pulse-title">Last 30 minutes</div>
        <div id="last10Window" class="pulse-window">--</div>
      </div>
      <div class="pulse-kpi">
        <div class="kpi"><b id="last10Total">--</b><span>tasks done</span></div>
        <div class="kpi"><b id="last10Top">--</b><span>top lane</span></div>
        <div class="kpi"><b id="last10Cmd">--</b><span>now</span></div>
      </div>
      <div id="last10Chips" class="chip-grid"></div>
      <details class="raw">
        <summary>raw command names</summary>
        <p id="last10Raw" class="mono">--</p>
      </details>
      <div class="divider"></div>
      <div class="pulse-head">
        <div class="pulse-title">Last 2 hours</div>
        <div id="last60Window" class="pulse-window">--</div>
      </div>
      <div id="last60Chips" class="chip-grid"></div>
      <details class="raw">
        <summary>raw 2-hour summary</summary>
        <p id="last60Raw" class="mono">--</p>
      </details>
      <div class="label">Remaining / Blockers</div>
      <p id="remaining">--</p>
    </div>
    <div class="card span6 events">
      <div class="label">Recent Raw Events</div>
      <div id="events"></div>
    </div>
    <div class="card span6">
      <div class="pulse-head">
        <div>
          <div class="label">Two-Hour Progress Judgment</div>
          <div class="pulse-title" id="twoHourJudgment">loading...</div>
        </div>
        <div id="twoHourWindow" class="pulse-window">--</div>
      </div>
      <div class="pulse-kpi">
        <div class="kpi"><b id="twoHourTotal">--</b><span>commands completed</span></div>
        <div class="kpi"><b id="twoHourTop">--</b><span>top project</span></div>
        <div class="kpi"><b id="twoHourProofs">--</b><span>work proofs</span></div>
      </div>
      <div id="twoHourChips" class="chip-grid"></div>
      <div class="label" style="margin-top:12px;">Latest Concrete Proof</div>
      <div id="workProofList" class="proof-list"></div>
    </div>
  </section>
</main>
<script>
const ids = (id) => document.getElementById(id);
const safe = (value) => String(value ?? '').replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function badgeClass(value) { return value === 'bad' ? 'bad' : value === 'warn' ? 'warn' : 'ok'; }
const PROJECT_IMPORTANCE = {
  'Adobe Stock factory': 1,
  'Printify QA': 2,
  'Etsy POD marketplace drip': 3,
  'Etsy/Printify reconciliation': 4,
  'First Audit private studio': 5,
  'Project Mirror DNA': 6,
  'eBay recovery': 7,
  'Etsy V7 digital lab': 8,
};
function commandList(items, limit=3) {
  const names = [...new Set((items || []).map(item => item.name).filter(Boolean))];
  const visible = names.slice(0, limit).join(', ');
  const extra = names.length > limit ? ` +${names.length - limit} more` : '';
  return visible ? `${visible}${extra}` : 'No command detail';
}
function groupedEntries(grouped) {
  return Object.entries(grouped || {}).map(([project, items]) => ({
    project,
    count: (items || []).length,
    commands: commandList(items),
    latest: (items || []).slice(-1)[0]?.tail || '',
    rank: PROJECT_IMPORTANCE[project] || 99,
  })).sort((a, b) => a.rank - b.rank || b.count - a.count || a.project.localeCompare(b.project));
}
function renderPulse(grouped, targetId, options={}) {
  const entries = groupedEntries(grouped);
  const max = options.max || 8;
  const important = new Set(['Adobe Stock factory', 'Printify QA', 'Etsy POD marketplace drip', 'First Audit private studio']);
  ids(targetId).innerHTML = entries.slice(0, max).map(entry => `
    <div class="chip ${important.has(entry.project) ? 'priority' : ''}">
      <strong><span>${safe(entry.project)}</span><span class="count">${entry.count}</span></strong>
      <small>${safe(entry.commands)}</small>
      ${entry.latest ? `<small>${safe(entry.latest)}</small>` : ''}
    </div>`).join('') || '<div class="chip warn-chip"><strong><span>No recent completions</span><span class="count">0</span></strong><small>Loop may be waiting or blocked. Check current command.</small></div>';
  return entries;
}
function compactNow(value) {
  if (!value) return '--';
  return String(value).replace(/_/g, ' ').slice(0, 13);
}
function fmtTime(value) {
  if (!value) return '--';
  try {
    return new Date(value).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
  } catch {
    return String(value).slice(11, 16);
  }
}
function renderDuty(duty) {
  duty = duty || {};
  const pct = Number(duty.percent ?? 0);
  ids('dutyPct').textContent = `${Number.isFinite(pct) ? pct : 0}%`;
  ids('dutyBar').style.width = `${Math.max(0, Math.min(100, Number.isFinite(pct) ? pct : 0))}%`;
  const label = pct >= 95 ? 'PERFECT' : pct >= 80 ? 'WATCH' : 'LOW';
  ids('dutyBadge').textContent = label;
  ids('dutyBadge').className = `badge ${badgeClass(duty.status_class)}`;
  ids('dutyDetail').textContent = `${duty.productive_minutes ?? '--'}m working / ${duty.available_minutes ?? '--'}m shift elapsed; idle ${duty.idle_minutes ?? '--'}m.`;
  ids('dutyTarget').textContent = `Shift ${fmtTime(duty.window_start_et)} -> ${fmtTime(duty.window_end_target_et)} ET; target 95%+ until adaptive duty deadline.`;
}
function renderCards(cards) {
  ids('pipelineGrid').innerHTML = cards.map(card => `
    <div class="card pipeline" onclick="location.href='/project/${card.id}'">
      <div style="display:flex;justify-content:space-between;gap:8px;align-items:flex-start;">
        <div class="title">${safe(card.title)}</div>
        <div class="badge ${badgeClass(card.status_class)}">${safe(card.status)}</div>
      </div>
      <div class="num">${card.progress}%</div>
      <div class="bar"><div style="width:${card.progress}%"></div></div>
      <div class="meta"><b>Cost:</b> ${safe(card.daily_cost)}</div>
      <div class="meta"><b>ETA:</b> ${safe(card.eta?.label || '--')}</div>
      <div class="meta"><b>Latest:</b> ${safe(card.latest_output)}</div>
      <div class="meta"><b>Reason:</b> ${safe(card.status_reason)}</div>
    </div>`).join('');
}
function renderDailyTasks(daily) {
  daily = daily || {tasks: [], summary: {}};
  ids('dailySummary').textContent = daily.summary?.label || 'No daily task data yet.';
  ids('dailyWindow').textContent = `${fmtTime(daily.shift_start_et)} -> ${fmtTime(daily.shift_end_target_et)} ET`;
  const tasks = (daily.tasks || []).slice().sort((a, b) => (a.priority || 99) - (b.priority || 99));
  ids('dailyTaskGrid').innerHTML = tasks.map(task => {
    const key = ['etsy_pod_daily', 'adobe_qa_assets', 'ebay_quality_actions'].includes(task.id);
    const target = task.target_min === task.target_max ? `${task.target_max}` : `${task.target_min}-${task.target_max}`;
    return `<div class="daily-task ${key ? 'key' : ''}">
      <div class="daily-head">
        <div>
          <div class="label">${safe((task.project_id || '').replace('_', ' / '))}</div>
          <div class="daily-title">${safe(task.title)}</div>
        </div>
        <span class="badge ${badgeClass(task.status_class)}">${safe(task.status)}</span>
      </div>
      <div class="daily-progress">${task.done}/${target} <span class="muted" style="font-size:13px">${safe(task.unit)}</span></div>
      <div class="bar"><div style="width:${Math.max(0, Math.min(100, task.percent || 0))}%"></div></div>
      <div class="daily-note">${safe(task.note)} ${task.gap_to_min ? `Gap to minimum: ${task.gap_to_min}.` : 'Minimum covered or not required.'}</div>
    </div>`;
  }).join('') || '<div class="daily-task"><div class="daily-title">No daily tasks configured</div></div>';
}
function renderRexActions(actions) {
  actions = actions || [];
  const panel = ids('rexActionPanel');
  const badge = ids('rexActionBadge');
  const headline = ids('rexActionHeadline');
  if (!actions.length) {
    panel.className = 'rex-panel clear';
    badge.textContent = 'CLEAR';
    badge.className = 'badge ok';
    headline.textContent = 'No Rex action needed. Blocked lanes=0; safe lanes continue.';
    ids('rexActionList').innerHTML = '<div class="rex-action-card"><b>System behavior</b><span>Codex should keep executing monthly tasks. If a lane blocks later, only that lane is parked.</span></div>';
    return;
  }
  panel.className = 'rex-panel needs';
  badge.textContent = 'REX NEEDED';
  badge.className = actions.some(a => a.severity === 'bad') ? 'badge bad' : 'badge warn';
  headline.textContent = `${actions.length} parked lane(s). Only these need Rex; other safe lanes continue.`;
  ids('rexActionList').innerHTML = actions.map(a => {
    const blob = `${a.project || ''} ${a.title || ''}`.toLowerCase();
    const actionUrl = blob.includes('adobe') ? '/adobe-qa' : (blob.includes('ebay') ? '/project/ebay' : '');
    const actionLabel = blob.includes('adobe') ? 'Review Adobe samples' : (blob.includes('ebay') ? 'Open eBay status' : 'Open detail');
    return `<div class="rex-action-card ${badgeClass(a.severity)}">
    <b>${safe(a.project)} — ${safe(a.title)}</b>
    <span><strong>Rex:</strong> ${safe(a.rex_needed)}</span>
    <span><strong>Codex meanwhile:</strong> ${safe(a.system_action)}</span>
    ${actionUrl ? `<span><a class="qa-button secondary" href="${actionUrl}" style="margin-top:8px;padding:7px 10px;">${safe(actionLabel)}</a></span>` : ''}
  </div>`;
  }).join('');
}
function renderVisualQa(qa) {
  qa = qa || {counts: {}, needs_rex_count: 0, ready_count: 0, first_submit_count: 0, samples: []};
  const panel = ids('visualQaPanel');
  const badge = ids('visualQaBadge');
  const headline = ids('visualQaHeadline');
  const needs = Number(qa.needs_rex_count || 0);
  panel.className = needs > 0 ? 'qa-panel needs' : 'qa-panel clear';
  badge.textContent = needs > 0 ? 'REX QA' : 'QA CLEAR';
  badge.className = needs > 0 ? 'badge warn' : 'badge ok';
  headline.textContent = needs > 0
    ? `${needs} Adobe Stock image(s) need Rex pass/reject/hold. Open the review UI before upload.`
    : `No pending Adobe Stock image QA. First-submit set has ${qa.first_submit_count || 0} image(s).`;
  const counts = qa.counts || {};
  ids('visualQaStats').innerHTML = [
    ['Ready', qa.ready_count || 0, 'ok'],
    ['First submit', qa.first_submit_count || 0, 'ok'],
    ['PASS', counts.PASS || 0, 'ok'],
    ['REJECT', counts.REJECT || 0, 'bad'],
    ['HOLD', counts.HOLD || 0, 'warn'],
    ['PENDING', counts.PENDING || 0, needs > 0 ? 'warn' : 'ok'],
  ].map(([label, value, cls]) => `<span class="badge ${cls}">${safe(label)}: ${safe(value)}</span>`).join('');
  ids('visualQaSamples').innerHTML = (qa.samples || []).map(item => `<div class="qa-sample">
    <b>${safe(item.family || 'Adobe Stock')} · ${safe(item.decision || 'PENDING')}</b>
    ${safe(item.title || item.id || '')}<br><span class="mono">${safe(item.id || '')}</span>
  </div>`).join('') || '<div class="qa-sample"><b>No pending/hold sample.</b>Use the Adobe review UI only when new images are staged.</div>';
}
function renderTwoHourProgress(twoHour) {
  twoHour = twoHour || {grouped_counts: {}, work_proofs: []};
  ids('twoHourJudgment').textContent = twoHour.judgment || 'No two-hour data yet.';
  ids('twoHourWindow').textContent = twoHour.window || '--';
  ids('twoHourTotal').textContent = twoHour.total_completed ?? 0;
  ids('twoHourTop').textContent = twoHour.top_project || '--';
  ids('twoHourProofs').textContent = (twoHour.work_proofs || []).length;
  const entries = Object.entries(twoHour.grouped_counts || {}).sort((a,b) => b[1] - a[1]);
  ids('twoHourChips').innerHTML = entries.slice(0, 8).map(([project, count]) => `
    <div class="chip ${count > 0 ? 'priority' : ''}">
      <strong><span>${safe(project)}</span><span class="count">${safe(count)}</span></strong>
      <small>Completed commands in the last 120 minutes.</small>
    </div>`).join('') || '<div class="chip warn-chip"><strong><span>No recent completions</span><span class="count">0</span></strong><small>Check loop state and blocked lanes.</small></div>';
  ids('workProofList').innerHTML = (twoHour.work_proofs || []).slice(0, 6).map(proof => `
    <div class="proof-item">
      <b>${safe(proof.project || 'OpenClaw')} Â· ${safe(proof.source || 'proof')}</b>
      <small>${safe(proof.summary || '')}</small>
      <small class="mono">${safe(proof.time || '')}</small>
    </div>`).join('') || '<div class="proof-item"><b>No proof yet</b><small>Work proof recorder has not written recent entries.</small></div>';
}
async function refresh() {
  try {
    const res = await fetch('/api/status', {cache:'no-store'});
    const data = await res.json();
    ids('alive').textContent = data.loop.alive ? 'LONG SHIFT ALIVE' : 'LONG SHIFT NOT RUNNING';
    ids('alive').className = data.loop.alive ? 'badge ok' : 'badge bad';
    renderCards(data.pipeline_cards || []);
    renderDailyTasks(data.daily_tasks);
    renderRexActions(data.rex_actions || []);
    renderVisualQa(data.visual_qa || {});
    renderTwoHourProgress(data.two_hour_progress || {});
    ids('pid').textContent = data.loop.pid ?? '--';
    ids('completed').textContent = data.loop.total_completed;
    ids('cmd').textContent = data.loop.current_command;
    ids('age').textContent = data.loop.active_age_minutes == null ? '--' : `${data.loop.active_age_minutes} min`;
    ids('updated').textContent = data.updated_at_et;
    renderDuty(data.duty_cycle);
    ids('refreshStatus').textContent = `Read-only local dashboard. Auto-refreshes every ${data.windows.auto_refresh}. Last refresh: ${data.updated_at_et}`;
    ids('last10Window').textContent = data.windows.last_10;
    ids('last60Window').textContent = data.windows.last_60;
    const last10Entries = renderPulse(data.recent.last_10_min, 'last10Chips', {max: 6});
    renderPulse(data.recent.last_60_min, 'last60Chips', {max: 8});
    const total10 = last10Entries.reduce((sum, entry) => sum + entry.count, 0);
    ids('last10Total').textContent = total10;
    ids('last10Top').textContent = last10Entries[0] ? last10Entries[0].project.replace(' factory', '').replace(' marketplace drip', '') : '--';
    ids('last10Cmd').textContent = compactNow(data.loop.current_command);
    ids('last10Raw').textContent = data.recent.last_10_min_summary;
    ids('last60Raw').textContent = data.recent.last_60_min_summary;
    ids('remaining').innerHTML = `${safe(data.remaining)}<br><span class="${data.blockers.length ? 'warn' : 'muted'}">Blockers: ${data.blockers.length ? safe(data.blockers.join(', ')) : 'none right now'}</span>`;
    ids('events').innerHTML = data.events.slice().reverse().map(e => `<div class="event"><span class="muted mono">${safe(e.stamp)}</span><br><span class="mono">${safe(e.body)}</span></div>`).join('');
  } catch (err) {
    ids('alive').textContent = 'DASHBOARD ERROR';
    ids('alive').className = 'badge bad';
    ids('last10Raw').textContent = String(err);
  }
}
document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });
refresh();
setInterval(refresh, 15000);
setInterval(() => window.location.reload(), 3600000);
</script>
</body>
</html>
"""


DETAIL_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>OpenClaw Project Detail</title>
  <style>
    :root { color-scheme: dark; --bg:#0f1215; --panel:#171b20; --muted:#a6b0ba; --text:#f3f5f7; --ok:#69d6a3; --warn:#ffd166; --bad:#ff6b6b; --line:#303743; --blue:#8ecae6; }
    body { margin:0; font-family:Segoe UI, Arial, sans-serif; background:var(--bg); color:var(--text); }
    main { max-width:1420px; margin:0 auto; padding:22px; }
    header { display:flex; justify-content:space-between; gap:16px; align-items:flex-end; margin-bottom:16px; }
    h1 { margin:0; font-size:25px; }
    a { color:var(--blue); text-decoration:none; }
    .grid { display:grid; grid-template-columns:repeat(12,1fr); gap:12px; }
    .card { grid-column:span 4; background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:14px; }
    .wide { grid-column:span 8; }
    .full { grid-column:span 12; }
    .label { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.08em; }
    .num { font-size:40px; font-weight:900; margin:5px 0; }
    .badge { padding:7px 10px; border-radius:999px; font-weight:800; font-size:12px; display:inline-block; }
    .ok { background:#1f352b; color:var(--ok); }
    .warn { background:#3a321e; color:var(--warn); }
    .bad { background:#392127; color:var(--bad); }
    .bar { height:9px; border-radius:999px; background:#2a3038; overflow:hidden; }
    .bar > div { height:100%; background:linear-gradient(90deg,#70e1c8,#62d490); width:0; transition:width .35s; }
    .mono, pre { font-family:Consolas, ui-monospace, monospace; font-size:12px; }
    pre { white-space:pre-wrap; overflow:auto; max-height:470px; margin:8px 0 0; padding:12px; background:#101419; border:1px solid var(--line); border-radius:8px; }
    ul { margin:8px 0 0; padding-left:19px; }
    li { margin:6px 0; line-height:1.35; }
    img { max-width:100%; border-radius:8px; border:1px solid var(--line); background:#0b0d10; }
    .muted { color:var(--muted); }
    .daily-list { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:9px; margin-top:9px; }
    .daily-item { border:1px solid #313a45; border-radius:9px; background:#10151b; padding:10px; }
    .daily-item strong { display:flex; justify-content:space-between; gap:10px; color:#f4f7fa; }
    .daily-item .done { font-size:20px; font-weight:900; margin:8px 0 5px; }
    .daily-item small { color:var(--muted); line-height:1.35; }
    @media (max-width:980px) { .card,.wide,.full { grid-column:span 12; } }
    @media (max-width:980px) { .daily-list { grid-template-columns:1fr; } }
  </style>
</head>
<body>
<main>
  <header>
    <div>
      <a href="/">Back to macro HUD</a>
      <h1 id="title">Project Detail</h1>
      <div class="muted" id="updated">--</div>
    </div>
    <div id="status" class="badge warn">loading</div>
  </header>
  <section class="grid">
    <div class="card">
      <div class="label">Progress</div>
      <div class="num" id="progress">--%</div>
      <div class="bar"><div id="bar"></div></div>
      <p class="muted" id="reason">--</p>
    </div>
    <div class="card">
      <div class="label">Cost / Latest Output</div>
      <p id="cost">--</p>
      <p id="latest" class="muted">--</p>
    </div>
    <div class="card">
      <div class="label">Loop</div>
      <p class="mono" id="loop">--</p>
    </div>
    <div class="card full">
      <div class="label">Daily Tasks For This Project</div>
      <div id="dailyTasks" class="daily-list"></div>
    </div>
    <div class="card wide">
      <div class="label">Done / Verified</div>
      <ul id="done"></ul>
    </div>
    <div class="card">
      <div class="label">Thumbnail Preview</div>
      <div id="thumb" class="muted">No thumbnail yet.</div>
    </div>
    <div class="card">
      <div class="label">Working On / Blocked</div>
      <ul id="working"></ul>
    </div>
    <div class="card">
      <div class="label">Next / Not Started</div>
      <ul id="next"></ul>
    </div>
    <div class="card">
      <div class="label">Notes</div>
      <ul id="notes"></ul>
    </div>
    <div class="card full">
      <div class="label">Payload / Error Inspection</div>
      <div id="errors" class="muted">No recent errors or payload failures detected for this project.</div>
    </div>
    <div class="card full">
      <div class="label">Live Console Log Tail - Last 50 Matching Entries</div>
      <pre id="logs">loading...</pre>
    </div>
  </section>
</main>
<script>
const projectId = "__PROJECT_ID__";
const ids = id => document.getElementById(id);
const safe = value => String(value ?? '').replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const listHtml = items => (items || ['No current entries.']).map(item => `<li>${safe(item)}</li>`).join('');
const cls = value => value === 'bad' ? 'bad' : value === 'warn' ? 'warn' : 'ok';
function renderDailyTasks(tasks) {
  ids('dailyTasks').innerHTML = (tasks || []).map(task => {
    const target = task.target_min === task.target_max ? `${task.target_max}` : `${task.target_min}-${task.target_max}`;
    return `<div class="daily-item">
      <strong><span>${safe(task.title)}</span><span class="badge ${cls(task.status_class)}">${safe(task.status)}</span></strong>
      <div class="done">${task.done}/${target} <span class="muted" style="font-size:12px">${safe(task.unit)}</span></div>
      <small>${safe(task.note)} ${task.gap_to_min ? `Gap to minimum: ${task.gap_to_min}.` : 'Minimum covered or not required.'}</small>
    </div>`;
  }).join('') || '<div class="daily-item"><strong><span>No daily lane assigned.</span></strong><small>This project is not part of the current daily operating quota.</small></div>';
}
async function refresh() {
  try {
    const res = await fetch(`/api/project/${projectId}`, {cache:'no-store'});
    const data = await res.json();
    const card = data.card;
    ids('title').textContent = card.title;
    ids('updated').textContent = `Updated ${data.updated_at_et}`;
    ids('status').textContent = card.status;
    ids('status').className = `badge ${cls(card.status_class)}`;
    ids('progress').textContent = `${card.progress}%`;
    ids('bar').style.width = `${card.progress}%`;
    ids('reason').textContent = card.status_reason;
    ids('cost').textContent = card.daily_cost;
    ids('latest').textContent = card.latest_output;
    ids('loop').textContent = `alive=${data.loop.alive} pid=${data.loop.pid || '--'} completed=${data.loop.total_completed} current=${data.loop.current_command}`;
    renderDailyTasks(data.daily_tasks);
    ids('done').innerHTML = listHtml(data.detail.done);
    ids('working').innerHTML = listHtml(data.detail.working_on);
    ids('next').innerHTML = listHtml(data.detail.next);
    ids('notes').innerHTML = listHtml(data.detail.notes);
    ids('logs').textContent = (data.log_tail || []).join('\n') || 'No matching log lines.';
    if (data.errors && data.errors.length) {
      ids('errors').innerHTML = data.errors.map(block => `<p class="muted">${safe(block.source)}</p><pre>${safe(block.text)}</pre>`).join('');
    } else {
      ids('errors').textContent = 'No recent errors or payload failures detected for this project.';
    }
    if (data.thumbnail && data.thumbnail.data_uri) {
      ids('thumb').innerHTML = `<img src="${data.thumbnail.data_uri}" alt="latest thumbnail"><p class="muted mono">${safe(data.thumbnail.path)}</p>`;
    } else if (data.thumbnail && data.thumbnail.path) {
      ids('thumb').innerHTML = `<p class="muted">${safe(data.thumbnail.note)}</p><p class="mono">${safe(data.thumbnail.path)}</p>`;
    } else {
      ids('thumb').textContent = 'No thumbnail yet.';
    }
  } catch (err) {
    ids('status').textContent = 'DASHBOARD ERROR';
    ids('status').className = 'badge bad';
    ids('logs').textContent = String(err);
  }
}
document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });
refresh();
setInterval(refresh, 15000);
setInterval(() => window.location.reload(), 3600000);
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in {"/", "/index.html"}:
            self._send(200, HTML.encode("utf-8"), "text/html; charset=utf-8")
            return
        if path == "/adobe-qa":
            self._send(200, ADOBE_QA_HTML.encode("utf-8"), "text/html; charset=utf-8")
            return
        if path == "/api/adobe-qa":
            payload = json.dumps(adobe_qa_payload(), ensure_ascii=False, indent=2).encode("utf-8")
            self._send(200, payload, "application/json; charset=utf-8")
            return
        if path == "/asset":
            query = parse_qs(urlparse(self.path).query)
            asset_path = project_relative_path((query.get("path") or [""])[0])
            if not asset_path or not asset_path.exists() or not asset_path.is_file():
                self._send(404, b"asset not found", "text/plain; charset=utf-8")
                return
            suffix = asset_path.suffix.lower()
            content_type = "image/jpeg" if suffix in {".jpg", ".jpeg"} else "image/png" if suffix == ".png" else "application/octet-stream"
            self._send(200, asset_path.read_bytes(), content_type)
            return
        if path.startswith("/project/"):
            project_id = normalize_project_id(path.split("/", 2)[2])
            body = DETAIL_HTML.replace("__PROJECT_ID__", project_id).encode("utf-8")
            self._send(200, body, "text/html; charset=utf-8")
            return
        if path == "/api/status":
            payload = json.dumps(dashboard_payload(), ensure_ascii=False, indent=2).encode("utf-8")
            self._send(200, payload, "application/json; charset=utf-8")
            return
        if path.startswith("/api/project/"):
            project_id = normalize_project_id(path.split("/", 3)[3])
            payload = json.dumps(project_payload(project_id), ensure_ascii=False, indent=2).encode("utf-8")
            self._send(200, payload, "application/json; charset=utf-8")
            return
        self._send(404, b"not found", "text/plain; charset=utf-8")

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/adobe-qa/decision":
            length = int(self.headers.get("Content-Length") or "0")
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
                result = save_adobe_decision(payload)
                body = json.dumps(result, ensure_ascii=False).encode("utf-8")
                self._send(200, body, "application/json; charset=utf-8")
            except Exception as exc:
                self._send(400, str(exc).encode("utf-8"), "text/plain; charset=utf-8")
            return
        self._send(404, b"not found", "text/plain; charset=utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()

    DATABASE_DIR.mkdir(exist_ok=True)
    DASHBOARD_PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"OpenClaw progress dashboard: http://{args.host}:{args.port}/")
    try:
        server.serve_forever()
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
