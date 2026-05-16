"""Scheduled Gemini/Grey supervisor check-in for OpenClaw.

This is the low-friction API monitor layer. It is advisory only: Gemini/Grey
responses are parsed into local review queues and never mutate marketplace or
production data directly.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import gemini_smoke_test, grey_memory_bridge

DATABASE = PROJECT_ROOT / "Database"
STATE_JSON = DATABASE / "Gemini_Supervisor_Checkin_State.json"
RUN_LOG = DATABASE / "Gemini_Supervisor_Checkin_Log.csv"
NY_TZ = ZoneInfo("America/New_York")

FREE_CHECKIN_MINUTES = 180
PAID_CHECKIN_MINUTES = 720
HEALTH_CHECK_MINUTES = 360


def now() -> datetime:
    return datetime.now(NY_TZ)


def now_text() -> str:
    return now().isoformat(timespec="seconds")


def read_state() -> dict:
    if not STATE_JSON.exists():
        return {}
    try:
        return json.loads(STATE_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_state(payload: dict) -> None:
    STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
    STATE_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def minutes_since(value: str | None) -> int:
    if not value:
        return 10**9
    try:
        prior = datetime.fromisoformat(value)
        if prior.tzinfo is None:
            prior = prior.replace(tzinfo=NY_TZ)
        return int((now() - prior.astimezone(NY_TZ)).total_seconds() // 60)
    except ValueError:
        return 10**9


def append_log(status: str, detail: str) -> None:
    import csv

    RUN_LOG.parent.mkdir(parents=True, exist_ok=True)
    exists = RUN_LOG.exists()
    with RUN_LOG.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        if not exists:
            writer.writerow(["Timestamp", "Status", "Detail"])
        writer.writerow([now_text(), status, detail[:2000]])


def due(state: dict, key: str, interval_minutes: int, force: bool) -> bool:
    return force or minutes_since(state.get(key)) >= interval_minutes


def routine_question() -> str:
    return (
        "Perform a strategic supervisor check-in for OpenClaw. "
        "Use the repo context packet only. Return concise JSON-style recommendations for: "
        "1) whether current task priority is correct, 2) any risk/failure pattern Codex may be missing, "
        "3) one next action if the current lane stalls. Do not request secrets. Do not recommend PPC/Priority ads. "
        "Do not ask for broad new tasks unless all current P0/P1 lanes are blocked."
    )


def paid_question() -> str:
    return (
        "High-stakes OpenClaw advisor pass. Review spend/risk/priority only. "
        "Escalate only if the current plan could waste money, hurt accounts, or miss Rex's business goal. "
        "Return actionable recommendations, not motivational prose."
    )


def run(force: bool = False, allow_paid: bool = False, dry_run: bool = False) -> dict:
    state = read_state()
    actions: list[dict[str, object]] = []

    health_due = due(state, "last_free_health_at", HEALTH_CHECK_MINUTES, force)
    free_due = due(state, "last_free_checkin_at", FREE_CHECKIN_MINUTES, force)
    paid_due = allow_paid and due(state, "last_paid_checkin_at", PAID_CHECKIN_MINUTES, force)

    if dry_run:
        result = {
            "status": "DRY_RUN",
            "timestamp": now_text(),
            "health_due": health_due,
            "free_due": free_due,
            "paid_due": paid_due,
            "allow_paid": allow_paid,
        }
        write_state({**state, **result})
        append_log("DRY_RUN", json.dumps(result, ensure_ascii=False))
        return result

    if health_due:
        health = gemini_smoke_test.run("free")
        state["last_free_health_at"] = now_text()
        actions.append({"action": "free_health", "status": health.get("status")})

    free_ok = True
    if free_due:
        free_result = grey_memory_bridge.send(routine_question(), tier="free")
        state["last_free_checkin_at"] = now_text()
        free_ok = free_result.get("status") == "OK"
        actions.append(
            {
                "action": "free_supervisor",
                "status": free_result.get("status"),
                "tasks": free_result.get("tasks"),
            }
        )

    # Paid API is intentionally sparse. It is for high-stakes oversight and
    # free-tier failure recovery, not routine token burn.
    if paid_due or (allow_paid and not free_ok):
        paid_result = grey_memory_bridge.send(paid_question(), tier="paid")
        state["last_paid_checkin_at"] = now_text()
        actions.append(
            {
                "action": "paid_supervisor",
                "status": paid_result.get("status"),
                "tasks": paid_result.get("tasks"),
            }
        )

    status = "OK" if actions else "SKIPPED_NOT_DUE"
    result = {
        "status": status,
        "timestamp": now_text(),
        "actions": actions,
        "next_free_due_minutes": max(0, FREE_CHECKIN_MINUTES - minutes_since(state.get("last_free_checkin_at"))),
        "next_paid_due_minutes": max(0, PAID_CHECKIN_MINUTES - minutes_since(state.get("last_paid_checkin_at"))),
    }
    write_state({**state, **result})
    append_log(status, json.dumps(actions, ensure_ascii=False))
    return result


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="OpenClaw Gemini/Grey supervisor check-in")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--allow-paid", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(force=args.force, allow_paid=args.allow_paid, dry_run=args.dry_run), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
