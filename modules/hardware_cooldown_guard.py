from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.hardware_heartbeat_monitor import LOG_PATH as HEARTBEAT_LOG
from modules.hardware_heartbeat_monitor import sample_heartbeat, write_heartbeat
from modules.memory_pressure_guard import run as run_memory_guard


DATABASE_DIR = PROJECT_ROOT / "Database"
STATE_PATH = DATABASE_DIR / "Hardware_Cooldown_State.json"
LOG_PATH = DATABASE_DIR / "Hardware_Cooldown_Log.csv"
NY = ZoneInfo("America/New_York")


def now():
    return datetime.now(NY)


def _recent_heartbeats(limit=6):
    if not HEARTBEAT_LOG.exists():
        return []
    try:
        with HEARTBEAT_LOG.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
            return list(csv.DictReader(handle))[-limit:]
    except Exception:
        return []


def _hot_streak(rows):
    streak = 0
    for row in reversed(rows):
        state = str(row.get("health_state") or "").upper()
        try:
            cpu = float(row.get("cpu_load_pct") or 0)
            mem = float(row.get("memory_used_pct") or 0)
        except ValueError:
            cpu = mem = 0
        hot = state in {"COOLDOWN", "CRITICAL"} or cpu >= 90 or mem >= 92
        # Plain WARM can be caused by moderate memory pressure on this laptop.
        # Treat it as a reason to optimize/reduce concurrency, not as proof that
        # the machine must pause. Only sustained high CPU or near-hard memory
        # pressure contributes to the cooling streak.
        warm = hot or cpu >= 80 or mem >= 88
        if warm:
            streak += 1
        else:
            break
    return streak


def _write_log(row):
    exists = LOG_PATH.exists()
    with LOG_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def evaluate(cooldown_minutes=20, sustained_warm_streak=3):
    DATABASE_DIR.mkdir(exist_ok=True)
    heartbeat = sample_heartbeat()
    memory_guard_state = None
    try:
        should_optimize = (
            heartbeat.memory_used_pct is not None
            and heartbeat.memory_used_pct >= 82
        ) or (
            heartbeat.cpu_load_pct is not None
            and heartbeat.cpu_load_pct >= 85
        )
        if should_optimize:
            memory_guard_state = run_memory_guard(
                execute=True,
                memory_soft_pct=82,
                cpu_soft_pct=85,
                close_all_project_idle=True,
            )
            if memory_guard_state.get("memory_after") != heartbeat.memory_used_pct:
                heartbeat = sample_heartbeat()
        if (
            heartbeat.temperature_c is None
            and heartbeat.cpu_load_pct is not None
            and heartbeat.cpu_load_pct >= 90
        ):
            # CPU readings can briefly spike during WMI/PowerShell sampling.
            # Verify once before arming a real cool-down.
            import time

            time.sleep(10)
            verify = sample_heartbeat()
            if (verify.cpu_load_pct or 0) < 80 and (verify.memory_used_pct or 0) < 90:
                heartbeat = verify
    except Exception as exc:  # noqa: BLE001
        memory_guard_state = {
            "decision": "MEMORY_GUARD_ERROR",
            "reason": f"{type(exc).__name__}: {exc}",
        }
    write_heartbeat(heartbeat)
    rows = _recent_heartbeats(limit=max(6, sustained_warm_streak + 1))
    streak = _hot_streak(rows)

    health = heartbeat.health_state.upper()
    reasons = [heartbeat.reason]
    active = False
    minutes = 0

    if health == "CRITICAL":
        active = True
        minutes = max(cooldown_minutes, 45)
        reasons.append("critical heartbeat")
    elif health == "COOLDOWN":
        active = True
        minutes = max(cooldown_minutes, 30)
        reasons.append("cooldown heartbeat")
    elif streak >= sustained_warm_streak:
        if memory_guard_state and memory_guard_state.get("decision") == "MEMORY_OK_CONTINUE":
            reasons.append(f"sustained warm streak={streak}; cleanup succeeded, no pause")
        else:
            active = True
            minutes = cooldown_minutes
            reasons.append(f"sustained warm streak={streak}; cleanup insufficient")

    cooldown_until = now() + timedelta(minutes=minutes) if active else now()
    state = {
        "timestamp": now().isoformat(timespec="seconds"),
        "active": active,
        "cooldown_until": cooldown_until.isoformat(timespec="seconds"),
        "cooldown_minutes": minutes,
        "health_state": heartbeat.health_state,
        "reason": "; ".join(part for part in reasons if part),
        "hot_streak": streak,
        "heartbeat": asdict(heartbeat),
        "memory_guard": memory_guard_state,
        "resource_policy": "optimize first, pause only after cleanup fails to bring pressure back under guardrails",
        "allowed_during_cooldown": ["hardware_heartbeat", "memory_cleanup", "report_batch", "local_light", "queue_planning", "api_read", "online_publish_safe"],
        "blocked_during_cooldown": ["image_batch", "asset_build", "market_research", "single_browser_task"],
    }
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    _write_log(
        {
            "Timestamp": state["timestamp"],
            "Active": str(active),
            "Cooldown_Until": state["cooldown_until"],
            "Cooldown_Minutes": str(minutes),
            "Health_State": heartbeat.health_state,
            "CPU_Load_Pct": heartbeat.cpu_load_pct,
            "Memory_Used_Pct": heartbeat.memory_used_pct,
            "Temperature_C": heartbeat.temperature_c,
            "Reason": state["reason"],
            "Hot_Streak": str(streak),
        }
    )
    return state


def main():
    parser = argparse.ArgumentParser(description="OpenClaw hardware cooldown guard.")
    parser.add_argument("--cooldown-minutes", type=int, default=20)
    parser.add_argument("--sustained-warm-streak", type=int, default=3)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    state = evaluate(cooldown_minutes=args.cooldown_minutes, sustained_warm_streak=args.sustained_warm_streak)
    if args.json:
        print(json.dumps(state, indent=2, ensure_ascii=False))
    else:
        print(
            f"[COOLDOWN-GUARD] active={state['active']} health={state['health_state']} "
            f"until={state['cooldown_until']} reason={state['reason']}"
        )


if __name__ == "__main__":
    main()
