"""Estimate OpenClaw monthly-task runway and alert before the queue runs thin.

This is a no-spend, local-only guard. It exists because "continue monthly
tasks" should not become a tiny loop that runs out of useful work and waits for
Rex to notice. If the durable backlog appears to have two days or less of
meaningful work, this script writes a Rex/Gemini packet asking for the next
strategic task block while the current work continues.
"""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
GEMINI_BRIDGE = REVIEW / "Gemini_Bridge"

BACKLOG = DATABASE / "Factory_Backlog.csv"
STATE_PATH = DATABASE / "Monthly_Task_Runway_State.json"
REX_PACKET = REVIEW / "Rex_Monthly_Task_Runway_latest.md"
GEMINI_PACKET = GEMINI_BRIDGE / "MONTHLY_TASK_RUNWAY_ALERT_latest.md"
MONTHLY_TASKS = PROJECT_ROOT / "OPENCLAW_MONTHLY_TASKS.md"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"

NY_TZ = ZoneInfo("America/New_York")
LOW_WATER_DAYS = 2.0
DAILY_CAPACITY_UNITS = 8.0

DONE_PREFIXES = ("DONE", "BLOCKED")
LOW_VALUE_LANES = {"control", "supervisor:local", "grey_web_sync"}
LANE_WEIGHTS = {
    "first_audit": 1.45,
    "private_showcase": 1.35,
    "etsy_darwinian_lab": 1.20,
    "etsy": 1.05,
    "market_learning": 0.95,
    "project_mirror": 1.15,
    "gallery_integrity": 0.80,
    "image_integrity": 0.90,
    "fallback_income": 0.75,
    "infrastructure": 0.55,
    "r_and_d": 0.80,
}


def now_et() -> datetime:
    return datetime.now(NY_TZ)


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def status_effort(status: str) -> float:
    upper = status.upper()
    if upper.startswith(DONE_PREFIXES):
        return 0.0
    if upper.startswith("READY"):
        return 1.0
    if upper.startswith("WAIT_RESOURCE") or upper.startswith("WAIT_COOLDOWN"):
        return 0.45
    if upper.startswith("WAITING_FOR") or upper.startswith("WAIT_"):
        return 0.70
    if upper.startswith("HOLD"):
        return 0.35
    return 0.60


def lane_weight(lane: str) -> float:
    if lane in LOW_VALUE_LANES:
        return 0.25
    if lane.startswith("supervisor:"):
        return 0.45
    return LANE_WEIGHTS.get(lane, 0.85)


def active_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    active: list[dict[str, str]] = []
    for row in rows:
        status = clean(row.get("Status")).upper()
        if status.startswith(DONE_PREFIXES):
            continue
        active.append(row)
    return active


def weighted_units(row: dict[str, str]) -> float:
    return status_effort(clean(row.get("Status"))) * lane_weight(clean(row.get("Lane")))


def monthly_task_headings() -> list[str]:
    if not MONTHLY_TASKS.exists():
        return []
    text = MONTHLY_TASKS.read_text(encoding="utf-8", errors="ignore")
    headings = []
    for line in text.splitlines():
        match = re.match(r"^##+\s+(.+)$", line.strip())
        if match:
            heading = match.group(1).strip()
            if heading and not heading.lower().startswith(("status", "lane", "tasks")):
                headings.append(heading)
    return headings


def load_previous_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_progress_once(alert: bool, changed: bool, estimated_days: float, open_count: int) -> None:
    if not alert and not changed:
        return
    stamp = now_et().strftime("%Y-%m-%d %H:%M:%S %Z")
    line = (
        f"\n- {stamp}: Monthly runway monitor {'ALERT' if alert else 'refreshed'}; "
        f"estimated_remaining_days={estimated_days:.2f}; open_backlog_rows={open_count}; "
        f"packet={GEMINI_PACKET.relative_to(PROJECT_ROOT)}.\n"
    )
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(line)


def main() -> None:
    GEMINI_BRIDGE.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)

    rows = read_csv(BACKLOG)
    open_rows = active_rows(rows)
    units = sum(weighted_units(row) for row in open_rows)
    estimated_days = units / DAILY_CAPACITY_UNITS if DAILY_CAPACITY_UNITS else 999.0
    alert = estimated_days <= LOW_WATER_DAYS

    ready_count = sum(1 for row in open_rows if clean(row.get("Status")).upper().startswith("READY"))
    waiting_count = sum(1 for row in open_rows if clean(row.get("Status")).upper().startswith("WAIT"))
    hold_count = sum(1 for row in open_rows if clean(row.get("Status")).upper().startswith("HOLD"))

    top_rows = sorted(
        open_rows,
        key=lambda row: (weighted_units(row), int(clean(row.get("Priority")) or 0)),
        reverse=True,
    )[:10]
    top_tasks = [
        {
            "priority": clean(row.get("Priority")),
            "lane": clean(row.get("Lane")),
            "status": clean(row.get("Status")),
            "task": clean(row.get("Task")),
        }
        for row in top_rows
    ]

    state = {
        "timestamp_et": now_et().isoformat(timespec="seconds"),
        "alert": alert,
        "threshold_days": LOW_WATER_DAYS,
        "daily_capacity_units": DAILY_CAPACITY_UNITS,
        "weighted_remaining_units": round(units, 2),
        "estimated_remaining_days": round(estimated_days, 2),
        "backlog_rows": len(rows),
        "open_backlog_rows": len(open_rows),
        "ready_rows": ready_count,
        "waiting_rows": waiting_count,
        "hold_rows": hold_count,
        "monthly_task_headings": monthly_task_headings(),
        "top_open_tasks": top_tasks,
        "recommendation": (
            "Backlog is below the two-day runway. Ask Rex/Gemini for the next strategic task block while continuing current work."
            if alert
            else "Runway is above the two-day warning line. Continue monthly tasks normally."
        ),
    }

    previous = load_previous_state()
    changed = previous.get("alert") != alert or previous.get("open_backlog_rows") != len(open_rows)
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    packet_lines = [
        "# Monthly Task Runway Alert",
        "",
        f"Timestamp ET: {state['timestamp_et']}",
        f"Alert: {'YES' if alert else 'NO'}",
        f"Estimated remaining runway: {estimated_days:.2f} days",
        f"Open backlog rows: {len(open_rows)} / {len(rows)}",
        f"Ready / waiting / hold rows: {ready_count} / {waiting_count} / {hold_count}",
        "",
        "## Meaning",
        "",
        (
            "The current executable backlog appears to contain two days or less of meaningful work. "
            "Codex should keep working the current queue, but Rex/Gemini should prepare the next high-value task block now."
            if alert
            else "The current backlog does not require a low-water warning yet."
        ),
        "",
        "## Top Open Tasks",
        "",
    ]
    for item in top_tasks:
        packet_lines.append(f"- P{item['priority']} {item['lane']} [{item['status']}]: {item['task']}")
    packet_lines.extend(
        [
            "",
            "## Suggested Next Task Sources",
            "",
            "- More V15.5 high-value Etsy/eBay POD experiments if marketplace guards stay clean.",
            "- First Audit / Cyber-Renaissance top-candidate review and Rex-selected upscale queue.",
            "- Project Mirror accepted reference pool and Mentor-Hub-grade DNA distillation.",
            "- Adobe Stock scaffold only after P0/P1 are waiting or stable.",
            "",
            "## Codex Rule",
            "",
            "Do not idle when this alert fires. Continue the current backlog and notify Rex/Gemini that the strategic queue needs replenishment.",
        ]
    )
    packet_text = "\n".join(packet_lines) + "\n"
    REX_PACKET.write_text(packet_text, encoding="utf-8")
    GEMINI_PACKET.write_text(packet_text, encoding="utf-8")

    write_progress_once(alert, changed, estimated_days, len(open_rows))
    print(
        f"[RUNWAY] alert={alert} days={estimated_days:.2f} "
        f"open={len(open_rows)} ready={ready_count} waiting={waiting_count} packet={GEMINI_PACKET}"
    )


if __name__ == "__main__":
    main()
