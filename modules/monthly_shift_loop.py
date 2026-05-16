"""Primitive long-shift runner for OpenClaw monthly tasks.

This is intentionally boring C-Class infrastructure. It cycles through a
fixed safe task list until the time box ends. It does not stop just because
one task has no work, and it does not try to be a smart daemon.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, time as day_time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    from modules.system_resource_allocator import choose_allocation
except ModuleNotFoundError:
    from system_resource_allocator import choose_allocation


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
STATE_FILE = DATABASE_DIR / "Monthly_Shift_Loop_State.md"
SHIFT_DUTY_WINDOW_FILE = DATABASE_DIR / "Monthly_Shift_Duty_Window.json"
THERMAL_TASK_SCHEDULE_FILE = DATABASE_DIR / "Thermal_Task_Schedule.json"
TRIGGER_FILE = DATABASE_DIR / "OpenClaw_Next_Action.trigger.json"
LOCK_FILE = DATABASE_DIR / "Monthly_Shift_Loop.pid"
NIGHT_QUEUE_FILE = DATABASE_DIR / "Night_Queue.csv"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
ET = ZoneInfo("America/New_York")
SYSTEM_FAILURE_RCS = {1073807364, 3221225794}


def python_executable() -> Path | str:
    venv_python = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return venv_python
    return "py"


PY_EXE = python_executable()


@dataclass(frozen=True)
class ShiftCommand:
    name: str
    args: tuple[str, ...]
    timeout_seconds: int = 900
    task_class: str = "local_light"
    priority: int = 80


COMMANDS: tuple[ShiftCommand, ...] = (
    # 2026-05-16 three-day revenue override:
    # 1) Adobe Stock production quality, 2) sticker bundles for Etsy,
    # 3) daily Etsy/eBay marketplace drip under guards.
    ShiftCommand("adobe_stock_codex_ab_groups", ("modules/adobe_stock_codex_ab_groups.py",), 900, "local_light", 98),
    ShiftCommand("adobe_stock_ab_mj_queue", ("modules/adobe_stock_ab_mj_dispatch_queue.py",), 900, "local_light", 98),
    ShiftCommand("adobe_stock_ab_mj_dispatch", ("modules/shock_and_awe_mj_dispatcher.py", "--queue", "Database/Adobe_Stock_Codex_AB_MJ_Dispatch_Queue.csv", "--limit", "3"), 1200, "image_batch", 97),
    ShiftCommand("adobe_stock_scaffold", ("modules/adobe_stock_scaffold.py",), 900, "local_light", 96),
    ShiftCommand("adobe_stock_mentor_expander", ("modules/adobe_stock_mentor_expander.py", "--per-family", "20", "--daily-limit", "50"), 900, "market_research", 96),
    ShiftCommand("adobe_stock_two_layer_schema", ("modules/adobe_stock_two_layer_schema.py",), 900, "local_light", 95),
    ShiftCommand("adobe_stock_pilot_batch", ("modules/adobe_stock_pilot_batch.py", "--target", "25", "--mode", "prepare"), 900, "asset_build", 95),
    ShiftCommand("adobe_stock_image_qa", ("modules/adobe_stock_image_qa.py", "--source", "auto", "--limit", "50"), 900, "qa_batch", 95),
    ShiftCommand("adobe_stock_metadata_qa", ("modules/adobe_stock_metadata_qa.py", "--limit", "50"), 900, "local_light", 95),
    ShiftCommand("adobe_stock_curated_pilot_pack", ("modules/adobe_stock_curated_pilot_pack.py", "--limit", "14", "--profile", "strict-premium"), 900, "asset_build", 95),
    ShiftCommand("adobe_stock_upload_ready_pack", ("modules/adobe_stock_upload_ready_pack.py", "--limit", "10", "--max-per-family", "2"), 900, "asset_build", 95),
    ShiftCommand("sticker_market_research_gate", ("modules/market_research_gate.py",), 900, "local_light", 88),
    ShiftCommand("sticker_liquidation_builder", ("modules/sticker_liquidation_builder.py",), 1200, "sticker_zip_packaging", 88),
    ShiftCommand("etsy_external_poll", ("modules/etsy_printify_external_poll.py", "--limit", "12"), 900, "api_read", 80),
    ShiftCommand("etsy_pod_selector", ("modules/etsy_pod_candidate_selector.py", "--limit", "25"), 900, "local_light", 82),
    ShiftCommand("etsy_pod_publish_drip", ("modules/printify_etsy_launch.py", "--limit", "1", "--publish"), 1800, "online_publish_safe", 82),
    ShiftCommand("etsy_digital_packet", ("modules/etsy_darwinian_lab_listing_packet.py", "--limit", "20"), 900, "local_light", 75),
    ShiftCommand("etsy_package_builder", ("modules/etsy_darwinian_lab_package_builder.py", "--limit", "20"), 900, "sticker_zip_packaging", 75),
    ShiftCommand("etsy_preview_builder", ("modules/etsy_digital_preview_builder.py", "--limit", "120"), 900, "asset_build", 75),
    ShiftCommand("printify_gallery_duplicate_audit", ("modules/printify_gallery_duplicate_audit.py", "--limit", "30"), 900, "qa_batch", 80),
    ShiftCommand("printify_design_audit", ("modules/printify_design_audit.py", "--limit", "3", "--sleep-seconds", "1"), 1200, "qa_batch", 80),
    ShiftCommand("ebay_traffic_diagnosis", ("modules/ebay_traffic_diagnosis.py",), 900, "api_read", 78),
    ShiftCommand("ebay_experiment_report", ("modules/ebay_experiment_report.py",), 900, "local_light", 78),
    ShiftCommand("project_mirror_scorecard", ("modules/project_mirror_ab_scorecard.py",), 900, "local_light", 70),
    ShiftCommand("first_audit_guard", ("modules/first_audit_guard.py", "--allow-findings"), 600, "local_light", 65),
    ShiftCommand("first_audit_contact_sheet", ("modules/first_audit_release_contact_sheet.py",), 900, "asset_build", 65),
    ShiftCommand("first_audit_extension_specs", ("modules/first_audit_extension_spec_builder.py",), 900, "local_light", 65),
    ShiftCommand("first_audit_lookbook", ("modules/first_audit_lookbook_builder.py",), 900, "asset_build", 65),
)


def et_now() -> datetime:
    return datetime.now(ET)


def log_line(message: str) -> None:
    DATABASE_DIR.mkdir(exist_ok=True)
    stamp = et_now().strftime("%Y-%m-%d %H:%M:%S %Z")
    with STATE_FILE.open("a", encoding="utf-8") as handle:
        handle.write(f"- {stamp} | {message}\n")


def update_trigger(status: str, command_name: str, completed: int, deadline: datetime) -> None:
    payload = {
        "updated_at_et": et_now().isoformat(),
        "status": status,
        "current_command": command_name,
        "commands_completed": completed,
        "deadline_et": deadline.isoformat(),
        "instruction": "Continue monthly tasks unless Rex explicitly stops the run.",
    }
    TRIGGER_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def append_progress(summary: str) -> None:
    stamp = et_now().strftime("%Y-%m-%d %H:%M:%S %Z")
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## {stamp} - monthly_shift_loop\n{summary}\n")


def append_night_queue(command: ShiftCommand, decision: str, reason: str) -> None:
    exists = NIGHT_QUEUE_FILE.exists()
    with NIGHT_QUEUE_FILE.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "queued_at_et",
                "command",
                "task_class",
                "priority",
                "decision",
                "reason",
                "status",
            ],
        )
        if not exists:
            writer.writeheader()
        writer.writerow(
            {
                "queued_at_et": et_now().isoformat(timespec="seconds"),
                "command": command.name,
                "task_class": command.task_class,
                "priority": command.priority,
                "decision": decision,
                "reason": reason,
                "status": "queued_for_cool_window",
            }
        )


def pid_is_alive(pid: int) -> bool:
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}"],
            text=True,
            capture_output=True,
            timeout=10,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except Exception:
        return False
    return str(pid) in (result.stdout or "")


def acquire_singleton_lock() -> bool:
    DATABASE_DIR.mkdir(exist_ok=True)
    current_pid = os.getpid()
    if LOCK_FILE.exists():
        try:
            existing_pid = int(LOCK_FILE.read_text(encoding="utf-8").strip())
        except ValueError:
            existing_pid = 0
        if existing_pid and existing_pid != current_pid and pid_is_alive(existing_pid):
            print(f"[SHIFT-LOCKED] existing monthly shift pid={existing_pid}; exiting duplicate.")
            return False
    LOCK_FILE.write_text(str(current_pid), encoding="utf-8")
    return True


def release_singleton_lock() -> None:
    try:
        if LOCK_FILE.exists() and LOCK_FILE.read_text(encoding="utf-8").strip() == str(os.getpid()):
            LOCK_FILE.unlink()
    except OSError:
        pass


def next_winddown_time() -> datetime:
    now = et_now()
    today_winddown = datetime.combine(now.date(), day_time(5, 30), tzinfo=ET)
    return today_winddown if now < today_winddown else today_winddown + timedelta(days=1)


def next_shutdown_time(value: datetime) -> datetime:
    today_shutdown = datetime.combine(value.date(), day_time(6, 0), tzinfo=ET)
    return today_shutdown if value < today_shutdown else today_shutdown + timedelta(days=1)


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def parse_iso(value: object) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=ET)
    return parsed.astimezone(ET)


def thermal_duty_deadline(start: datetime) -> tuple[datetime, str]:
    schedule = load_json(THERMAL_TASK_SCHEDULE_FILE, {})
    windows = schedule.get("cool_heavy_windows") or []
    for window in windows:
        win_start = parse_iso(window.get("start_et"))
        win_end = parse_iso(window.get("end_et"))
        if not win_start or not win_end:
            continue
        if start <= win_end:
            # If Rex starts before a cool window, keep the light queue alive until
            # the cool window opens, then run heavy work until that window ends.
            return win_end, f"weather_cool_window:{win_start.isoformat()}->{win_end.isoformat()}"
    return next_winddown_time(), "fallback_0530_no_weather_window"


def ensure_shift_duty_window(start: datetime, deadline: datetime, deadline_source: str) -> dict:
    """Keep the user's workday window stable across loop restarts.

    Rex wants utilization measured from the first "continue monthly tasks"
    shift start to the weather/resource duty deadline, not from Windows boot
    time and not from each subprocess restart. If the current window is still
    active, keep it, extending it only when the new thermal schedule permits a
    longer safe window.
    """
    existing = load_json(SHIFT_DUTY_WINDOW_FILE, {})
    existing_end = parse_iso(existing.get("shift_end_target_et"))
    existing_start = parse_iso(existing.get("shift_start_et"))
    if existing_end and existing_start and start < existing_end:
        desired_note = "Duty cycle window: adaptive weather/resource deadline. Historical 06:00 is only a fallback."
        if deadline > existing_end or existing.get("deadline_source") != deadline_source or existing.get("note") != desired_note:
            existing["shift_end_target_et"] = deadline.isoformat()
            existing["deadline_source"] = deadline_source
            existing["note"] = desired_note
            existing["updated_at_et"] = start.isoformat()
            SHIFT_DUTY_WINDOW_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        return existing

    payload = {
        "shift_start_et": start.isoformat(),
        "shift_end_target_et": deadline.isoformat(),
        "source": "monthly_shift_loop",
        "deadline_source": deadline_source,
        "note": "Duty cycle window: adaptive weather/resource deadline. Historical 06:00 is only a fallback.",
    }
    SHIFT_DUTY_WINDOW_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def calculate_deadline(max_minutes: int, ignore_winddown: bool) -> datetime:
    now = et_now()
    if max_minutes <= 0:
        if ignore_winddown:
            return now + timedelta(days=1)
        deadline, _source = thermal_duty_deadline(now)
        return deadline

    max_deadline = now + timedelta(minutes=max_minutes)
    if ignore_winddown:
        return max_deadline
    return min(max_deadline, next_winddown_time())


def run_command(command: ShiftCommand) -> tuple[int, str]:
    script_path = PROJECT_ROOT / command.args[0]
    if not script_path.exists():
        return 127, f"SKIP missing {command.args[0]}"

    try:
        completed = subprocess.run(
            [str(PY_EXE), str(script_path), *command.args[1:]],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            timeout=command.timeout_seconds,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except subprocess.TimeoutExpired as exc:
        output = ((exc.stdout or "") + "\n" + (exc.stderr or "")).strip()
        return 124, f"TIMEOUT after {command.timeout_seconds}s | {output[-1000:]}"

    output = ((completed.stdout or "") + "\n" + (completed.stderr or "")).strip()
    return completed.returncode, output[-1400:]


def allocation_allows(command: ShiftCommand) -> bool:
    try:
        allocation, _snapshot = choose_allocation(task_class=command.task_class, priority=command.priority)
    except Exception as exc:
        log_line(f"RESOURCE_GUARD_ERROR {command.name} {type(exc).__name__}: {exc}; allow conservative run")
        return True

    if allocation.decision in {"PAUSE_COOLDOWN", "DEFER_TO_NIGHT"}:
        log_line(
            f"THERMAL_DEFER {command.name} class={command.task_class} "
            f"decision={allocation.decision} window={allocation.window} reason={allocation.reason}"
        )
        append_night_queue(command, allocation.decision, allocation.reason)
        return False

    if allocation.decision == "RUN_CONSERVATIVE":
        log_line(
            f"THERMAL_CONSERVATIVE {command.name} class={command.task_class} "
            f"window={allocation.window} reason={allocation.reason}"
        )
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-minutes", type=int, default=0, help="0 means run until the dynamic weather/resource duty deadline.")
    parser.add_argument("--min-minutes", type=int, default=285, help="Compatibility flag; no early exit.")
    parser.add_argument("--sleep-seconds", type=int, default=10)
    parser.add_argument("--max-commands", type=int, default=0, help="Test valve. 0 means loop until deadline.")
    parser.add_argument("--ignore-winddown", action="store_true")
    args = parser.parse_args()

    if not acquire_singleton_lock():
        return 0

    try:
        start = et_now()
        if args.max_minutes <= 0 and not args.ignore_winddown:
            deadline, deadline_source = thermal_duty_deadline(start)
        else:
            deadline = calculate_deadline(args.max_minutes, args.ignore_winddown)
            deadline_source = "manual_max_minutes_or_ignore_winddown"
        duty_window = ensure_shift_duty_window(start, deadline, deadline_source)
        DATABASE_DIR.mkdir(exist_ok=True)
        if not STATE_FILE.exists():
            STATE_FILE.write_text("# OpenClaw Monthly Shift Loop\n\n## Events\n", encoding="utf-8")
        with STATE_FILE.open("a", encoding="utf-8") as handle:
            handle.write(
                "\n## Session\n"
                f"- start_et: {start.isoformat()}\n"
                f"- deadline_et: {deadline.isoformat()}\n"
                f"- duty_start_et: {duty_window.get('shift_start_et')}\n"
                f"- duty_end_target_et: {duty_window.get('shift_end_target_et')}\n"
                f"- command_count: {len(COMMANDS)}\n\n"
            )

        completed_count = 0
        command_index = 0
        consecutive_system_failures = 0
        update_trigger("RUNNING", "init", completed_count, deadline)
        log_line("SHIFT_START primitive while loop active")

        while et_now() < deadline:
            command = COMMANDS[command_index % len(COMMANDS)]
            command_index += 1
            if not allocation_allows(command):
                if command_index % len(COMMANDS) == 0:
                    time.sleep(max(args.sleep_seconds, 10))
                continue
            update_trigger("RUNNING", command.name, completed_count, deadline)
            log_line(f"START {completed_count + 1} {command.name}")

            rc, tail = run_command(command)
            completed_count += 1
            status = "OK" if rc == 0 else f"RC={rc}"
            one_line_tail = tail.replace("\r", " ").replace("\n", " ")[:500]
            log_line(f"END {completed_count} {command.name} {status} | {one_line_tail}")

            if rc in SYSTEM_FAILURE_RCS:
                consecutive_system_failures += 1
                log_line(
                    f"SYSTEM_FAILURE {consecutive_system_failures}/3 {command.name} {status} "
                    "breaking for clean watchdog restart"
                )
                if consecutive_system_failures >= 3:
                    append_progress(
                        f"- monthly shift system-level subprocess failures reached 3; "
                        f"last={command.name}; status={status}; exiting for clean watchdog restart."
                    )
                    break
            else:
                consecutive_system_failures = 0

            if completed_count % 6 == 0:
                append_progress(
                    f"- monthly shift still running; commands_completed={completed_count}; "
                    f"last={command.name}; status={status}"
                )

            if args.max_commands and completed_count >= args.max_commands:
                log_line("TEST_STOP max_commands reached")
                break
            if et_now() >= deadline:
                break
            time.sleep(max(args.sleep_seconds, 0))

        update_trigger("DONE", "none", completed_count, deadline)
        summary = (
            f"- shift completed; commands_completed={completed_count}; "
            f"start_et={start.isoformat()}; end_et={et_now().isoformat()}; "
            f"deadline_et={deadline.isoformat()}"
        )
        append_progress(summary)
        log_line("SHIFT_DONE " + summary)
        print(summary)
        return 0
    finally:
        release_singleton_lock()


if __name__ == "__main__":
    raise SystemExit(main())
