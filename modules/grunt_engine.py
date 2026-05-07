from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import system_resource_allocator
from modules.hardware_heartbeat_monitor import sample_heartbeat, write_heartbeat
from modules.quality_floor_guard import audit as quality_audit
from modules.task_queue_modular import claim_next, seed_default_tasks, update_task


DATABASE_DIR = PROJECT_ROOT / "Database"
RUN_LOG = DATABASE_DIR / "Grunt_Engine_Run_Log.csv"
STATE_PATH = DATABASE_DIR / "Grunt_Engine_State.json"
MAINTENANCE_PLAN = DATABASE_DIR / "Grunt_Maintenance_Plan.json"
LOCK_PATH = DATABASE_DIR / "Grunt_Engine.lock"
NY = ZoneInfo("America/New_York")

ALLOWED_ACTIONS = {
    "hardware_heartbeat",
    "hardware_cooldown_guard",
    "local_supervisor_refresh",
    "quality_floor_scan",
    "copy_signal_refresh",
    "market_signal_refresh",
    "multi_track_experiment_plan",
    "rest_log_compression_plan",
}

REST_ALLOWED = {"hardware_heartbeat", "hardware_cooldown_guard", "rest_log_compression_plan", "quality_floor_scan"}


def now():
    return datetime.now(NY)


@contextmanager
def engine_lock(stale_seconds: int = 900):
    DATABASE_DIR.mkdir(exist_ok=True)
    payload = {
        "pid": os.getpid(),
        "created_at": now().isoformat(timespec="seconds"),
    }
    handle = None
    try:
        try:
            handle = os.open(str(LOCK_PATH), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            try:
                age = time.time() - LOCK_PATH.stat().st_mtime
            except OSError:
                age = 0
            if age > stale_seconds:
                try:
                    LOCK_PATH.unlink()
                except OSError:
                    pass
                handle = os.open(str(LOCK_PATH), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            else:
                yield False
                return
        os.write(handle, json.dumps(payload).encode("utf-8"))
        yield True
    finally:
        if handle is not None:
            try:
                os.close(handle)
            except OSError:
                pass
            try:
                LOCK_PATH.unlink()
            except OSError:
                pass


def append_log(row):
    RUN_LOG.parent.mkdir(exist_ok=True)
    fields = [
        "Timestamp",
        "Task_ID",
        "Action",
        "Status",
        "Decision",
        "Resource_Window",
        "Resource_Reason",
        "ReturnCode",
        "Detail",
    ]
    exists = RUN_LOG.exists()
    with RUN_LOG.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow({key: row.get(key, "") for key in fields})


def write_state(row, allocation, heartbeat):
    state = {
        "updated_at": now().isoformat(timespec="seconds"),
        "last_run": row,
        "allocation": asdict(allocation),
        "heartbeat": asdict(heartbeat),
    }
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def _normalize_command(command: str) -> str:
    command = (command or "").strip()
    if command.startswith("py modules\\"):
        return "cmd /c scripts\\openclaw-python.cmd " + command[len("py ") :]
    if command.startswith("python modules\\"):
        return "cmd /c scripts\\openclaw-python.cmd " + command[len("python ") :]
    if command.startswith("scripts\\openclaw-python.cmd "):
        return "cmd /c " + command
    return command


def _powershell_safe_command(command: str) -> bool:
    if not command or any(token in command.lower() for token in [" rm ", " del ", " remove-item ", "shutdown", "restart-computer"]):
        return False
    normalized = _normalize_command(command)
    return (
        command.startswith("py modules\\")
        or command.startswith("python modules\\")
        or normalized.startswith("cmd /c scripts\\openclaw-python.cmd modules\\")
    )


def maintenance_plan():
    """Write a rest-window plan without forcing disruptive actions."""
    plan = {
        "generated_at": now().isoformat(timespec="seconds"),
        "rest_window": "04:00-06:00 America/New_York",
        "safe_automatic": [
            "compress old CSV/LOG reports into Review_Packets or Database archive",
            "refresh hardware heartbeat",
            "run quality floor scan on recent generated outputs",
            "git status/read-only report",
        ],
        "requires_rex_or_explicit_flag": [
            "Windows restart / cold boot",
            "battery charge-discharge cycle",
            "defrag/optimize-volume on SSD or system disk",
            "permanent deletion rather than quarantine",
        ],
        "reason": "Rest actions can interrupt Rex or wear storage/battery if done blindly. The engine plans them but does not execute disruptive actions unattended.",
    }
    MAINTENANCE_PLAN.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(f"[GRUNT-MAINTENANCE] {MAINTENANCE_PLAN}")
    return plan


def _run_command(command: str, timeout: int):
    if not _powershell_safe_command(command):
        return 126, "", f"blocked unsafe or unknown command: {command}"
    command = _normalize_command(command)
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    return completed.returncode, completed.stdout, ""


def _run_task(task, dry_run=False):
    if task.action not in ALLOWED_ACTIONS:
        if not dry_run:
            update_task(task.task_id, status="FAILED", last_error=f"action not allowed: {task.action}")
        return "FAILED", "action not allowed", 126
    if task.action == "hardware_heartbeat":
        if not dry_run:
            heartbeat = sample_heartbeat()
            write_heartbeat(heartbeat)
            detail = json.dumps(asdict(heartbeat), ensure_ascii=False)[:1000]
            update_task(task.task_id, status="DONE", result_summary=detail)
        else:
            detail = "dry-run heartbeat"
        return "DRY_RUN" if dry_run else "DONE", detail, 0
    if task.action == "rest_log_compression_plan":
        if not dry_run:
            detail = json.dumps(maintenance_plan(), ensure_ascii=False)[:1000]
            update_task(task.task_id, status="DONE", result_summary=detail)
        else:
            detail = "dry-run maintenance plan"
        return "DRY_RUN" if dry_run else "DONE", detail, 0
    if dry_run:
        return "DRY_RUN", f"would run: {task.command}", 0
    code, output, error = _run_command(task.command, task.timeout_seconds)
    detail = (output or error or "")[:1000]
    if code == 0:
        qa_failures = []
        if task.expected_outputs:
            rows = quality_audit(task.expected_outputs, profile=task.qa_profile, limit=20, execute_quarantine=False)
            qa_failures = [row for row in rows if row.verdict != "PASS"]
        if qa_failures:
            update_task(task.task_id, status="QUARANTINED", last_error=f"{len(qa_failures)} output(s) failed quality floor", result_summary=detail)
            return "QUARANTINED", f"{len(qa_failures)} output(s) failed quality floor", code
        update_task(task.task_id, status="DONE", result_summary=detail)
        return "DONE", detail, code
    status = "FAILED" if task.attempts >= task.max_attempts else "DEFERRED"
    update_task(task.task_id, status=status, last_error=detail)
    return status, detail, code


def allowed_classes_for_window(window_name, policy):
    for window in policy.get("windows", []):
        if window.get("name") == window_name:
            return set(window.get("preferred_classes") or [])
    return set()


def run_once(dry_run=False):
    with engine_lock() as acquired:
        if not acquired:
            row = {
                "Timestamp": now().isoformat(timespec="seconds"),
                "Task_ID": "",
                "Action": "",
                "Status": "LOCKED",
                "Decision": "SKIP",
                "Resource_Window": "",
                "Resource_Reason": "another grunt engine instance is already running",
                "ReturnCode": 0,
                "Detail": str(LOCK_PATH),
            }
            append_log(row)
            return row
        return _run_once_unlocked(dry_run=dry_run)


def _run_once_unlocked(dry_run=False):
    policy = system_resource_allocator.ensure_policy()
    allocation, snapshot = system_resource_allocator.choose_allocation(task_class="auto", priority=50)
    heartbeat = sample_heartbeat()
    write_heartbeat(heartbeat)
    if allocation.decision == "PAUSE_COOLDOWN":
        detail = f"resource cooldown: {allocation.reason}"
        row = {
            "Timestamp": now().isoformat(timespec="seconds"),
            "Task_ID": "",
            "Action": "",
            "Status": "PAUSE_COOLDOWN",
            "Decision": allocation.decision,
            "Resource_Window": allocation.window,
            "Resource_Reason": allocation.reason,
            "ReturnCode": "",
            "Detail": detail,
        }
        append_log(row)
        write_state(row, allocation, heartbeat)
        return row

    allowed_classes = allowed_classes_for_window(allocation.window, policy)
    allowed_actions = REST_ALLOWED if allocation.window == "rest_maintenance" else None
    task = claim_next(allowed_classes=allowed_classes, allowed_actions=allowed_actions, mutate=not dry_run)
    if not task:
        row = {
            "Timestamp": now().isoformat(timespec="seconds"),
            "Task_ID": "",
            "Action": "",
            "Status": "NO_TASK",
            "Decision": allocation.decision,
            "Resource_Window": allocation.window,
            "Resource_Reason": allocation.reason,
            "ReturnCode": 0,
            "Detail": f"allowed_classes={','.join(sorted(allowed_classes))}",
        }
        append_log(row)
        write_state(row, allocation, heartbeat)
        return row

    status, detail, code = _run_task(task, dry_run=dry_run)
    row = {
        "Timestamp": now().isoformat(timespec="seconds"),
        "Task_ID": task.task_id,
        "Action": task.action,
        "Status": status,
        "Decision": allocation.decision,
        "Resource_Window": allocation.window,
        "Resource_Reason": allocation.reason,
        "ReturnCode": code,
        "Detail": detail,
    }
    append_log(row)
    write_state(row, allocation, heartbeat)
    return row


def main():
    parser = argparse.ArgumentParser(description="OpenClaw 24/7 Grunt Engine.")
    parser.add_argument("--seed-default", action="store_true")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--loop", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--interval-seconds", type=int, default=300)
    parser.add_argument("--iterations", type=int, default=0)
    parser.add_argument("--maintenance-plan", action="store_true")
    args = parser.parse_args()
    if args.seed_default:
        added = seed_default_tasks()
        print(json.dumps({"added": len(added)}, indent=2))
        return
    if args.maintenance_plan:
        print(json.dumps(maintenance_plan(), indent=2))
        return

    iteration = 0
    while True:
        result = run_once(dry_run=args.dry_run)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if args.once or not args.loop:
            break
        iteration += 1
        if args.iterations and iteration >= args.iterations:
            break
        sleep_seconds = max(30, args.interval_seconds)
        time.sleep(sleep_seconds)


if __name__ == "__main__":
    main()
