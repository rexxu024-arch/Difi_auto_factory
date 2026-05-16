"""One-shot OpenClaw night shift runner.

This is not a startup/resume automation. It is a bounded overnight loop for the
current logged-in Windows session. It stops before the 06:00 ET shutdown window.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
LOG_CSV = DATABASE / "Night_Shift_Run_Log.csv"
STATE_JSON = DATABASE / "Night_Shift_State.json"
NY = ZoneInfo("America/New_York")


@dataclass(frozen=True)
class Step:
    name: str
    args: list[str]
    timeout: int
    min_hour: int | None = None
    max_hour: int | None = None
    every_cycles: int = 1
    network_write: bool = False


def now() -> datetime:
    return datetime.now(NY)


def today_at(hour: int, minute: int) -> datetime:
    current = now()
    target = current.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= current and hour < 12:
        target += timedelta(days=1)
    return target


def append_log(row: dict[str, object]) -> None:
    LOG_CSV.parent.mkdir(parents=True, exist_ok=True)
    exists = LOG_CSV.exists()
    fields = ["Timestamp", "Cycle", "Step", "Status", "ExitCode", "ElapsedSeconds", "Detail"]
    with LOG_CSV.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def write_state(payload: dict[str, object]) -> None:
    STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
    STATE_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def run_step(step: Step, cycle: int) -> bool:
    start = time.time()
    command = [str(PROJECT_ROOT / "scripts" / "openclaw-python.cmd"), *step.args]
    try:
        proc = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=step.timeout,
            shell=False,
        )
        elapsed = round(time.time() - start, 1)
        output = (proc.stdout or "").strip()
        append_log(
            {
                "Timestamp": now().strftime("%Y-%m-%d %H:%M:%S %z"),
                "Cycle": cycle,
                "Step": step.name,
                "Status": "OK" if proc.returncode == 0 else "FAIL",
                "ExitCode": proc.returncode,
                "ElapsedSeconds": elapsed,
                "Detail": output[-2000:],
            }
        )
        return proc.returncode == 0
    except subprocess.TimeoutExpired as exc:
        elapsed = round(time.time() - start, 1)
        append_log(
            {
                "Timestamp": now().strftime("%Y-%m-%d %H:%M:%S %z"),
                "Cycle": cycle,
                "Step": step.name,
                "Status": "TIMEOUT",
                "ExitCode": "TIMEOUT",
                "ElapsedSeconds": elapsed,
                "Detail": str(exc.stdout or "")[-2000:],
            }
        )
        return False
    except Exception as exc:  # noqa: BLE001
        elapsed = round(time.time() - start, 1)
        append_log(
            {
                "Timestamp": now().strftime("%Y-%m-%d %H:%M:%S %z"),
                "Cycle": cycle,
                "Step": step.name,
                "Status": "ERROR",
                "ExitCode": type(exc).__name__,
                "ElapsedSeconds": elapsed,
                "Detail": str(exc)[:2000],
            }
        )
        return False


def base_steps() -> list[Step]:
    return [
        Step(
            "memory_pressure_guard",
            [
                "modules\\memory_pressure_guard.py",
                "--execute",
                "--memory-soft-pct",
                "82",
                "--cpu-soft-pct",
                "85",
                "--close-all-project-idle",
                "--json",
            ],
            120,
        ),
        Step("system_resource_allocator", ["modules\\system_resource_allocator.py", "--json"], 90),
        Step("grunt_seed_if_empty", ["modules\\task_queue_modular.py", "--seed-default", "--only-if-empty"], 60),
        Step("grunt_once", ["modules\\grunt_engine.py", "--once"], 240),
        Step("local_factory_supervisor", ["modules\\factory_supervisor.py", "--execute-local", "--skip-network"], 620),
        Step("quality_floor_scan", ["modules\\quality_floor_guard.py", "--paths", "Database", "Review_Packets", "--limit", "80"], 240, every_cycles=2),
        Step(
            "poster_design_audit",
            [
                "modules\\printify_design_audit.py",
                "--product-type",
                "Poster",
                "--limit",
                "3",
                "--timestamped-output",
                "--sleep-seconds",
                "1",
            ],
            240,
            every_cycles=2,
        ),
        Step(
            "acrylic_design_audit",
            [
                "modules\\printify_design_audit.py",
                "--product-type",
                "Acrylic",
                "--limit",
                "3",
                "--timestamped-output",
                "--sleep-seconds",
                "1",
            ],
            240,
            every_cycles=2,
        ),
        Step("etsy_api_status", ["modules\\etsy_app_status_probe.py"], 120, every_cycles=2),
        Step("etsy_printify_external_poll", ["modules\\etsy_printify_external_poll.py", "--max-age-minutes", "120"], 150, every_cycles=2),
        Step("etsy_live_readonly", ["modules\\etsy_live_audit.py", "--limit", "10"], 180, every_cycles=3),
        Step("multi_track_monitor", ["modules\\multi_track_copy_monitor.py"], 120),
        Step("ebay_experiment_report", ["modules\\ebay_experiment_report.py"], 120),
        Step("ebay_traffic_diagnosis", ["modules\\ebay_traffic_diagnosis.py"], 120),
        Step("blueprint_next_plan", ["modules\\product_blueprint_next_plan.py"], 120, every_cycles=2),
        Step("factory_backlog", ["modules\\factory_backlog.py"], 120),
        Step("factory_morning_report", ["modules\\factory_morning_report.py"], 180, every_cycles=3),
        Step("rex_action_packet", ["modules\\daily_rex_support_packet.py"], 120, every_cycles=3),
        Step("daily_sitrep_prepare", ["modules\\daily_sitrep_builder.py"], 120, every_cycles=3),
        Step("grey_prepare_only", ["modules\\grey_memory_bridge.py", "--prepare"], 120, every_cycles=3),
        Step(
            "grey_bridge_advisory",
            [
                "modules\\grey_memory_bridge.py",
                "--question",
                "Night shift advisory only. Review latest state and return next tasks. No live mutations or spending.",
            ],
            180,
            every_cycles=4,
        ),
    ]


def late_night_steps() -> list[Step]:
    return [
        Step("edge_check", ["modules\\automation_browser.py", "--browser", "edge", "--port", "9223"], 60, min_hour=23, every_cycles=3),
        Step(
            "sellerhub_snapshot_readonly",
            ["modules\\ebay_sellerhub_snapshot.py", "--cdp-port", "9223", "--scrolls", "5"],
            360,
            min_hour=23,
            every_cycles=3,
        ),
        Step(
            "track_a_prepare_local",
            ["modules\\multi_track_copy_executor.py", "--track", "A_LOW_COMPETITION_NICHE", "--prepare", "--apply-local", "--limit", "5"],
            180,
            min_hour=23,
            every_cycles=4,
        ),
        Step(
            "track_a_sync_metadata_small",
            [
                "modules\\multi_track_copy_executor.py",
                "--sync-printify",
                "--limit",
                "3",
                "--sleep-min",
                "55",
                "--sleep-max",
                "140",
            ],
            900,
            min_hour=23,
            every_cycles=5,
            network_write=True,
        ),
    ]


def winddown_steps() -> list[Step]:
    return [
        Step("winddown_endurance", ["modules\\endurance_protocol.py", "--shutdown-winddown", "--execute", "--json"], 180),
        Step("factory_morning_report", ["modules\\factory_morning_report.py"], 180),
        Step("rex_action_packet", ["modules\\daily_rex_support_packet.py"], 120),
        Step("winddown_report", ["modules\\winddown_report_builder.py"], 120),
        Step("daily_sitrep", ["modules\\daily_sitrep_builder.py"], 120),
        Step("grey_prepare", ["modules\\grey_memory_bridge.py", "--prepare"], 120),
        Step("grey_api_supervisor", ["modules\\gemini_supervisor_checkin.py", "--allow-paid", "--force"], 300),
        Step(
            "gemini_thread_sync_idle",
            ["modules\\gemini_chat_sync.py", "--execute", "--wait-until-idle-minutes", "15"],
            1200,
        ),
    ]


def eligible(step: Step, cycle: int, current: datetime) -> bool:
    if cycle % step.every_cycles != 0:
        return False
    if step.min_hour is not None and current.hour < step.min_hour:
        return False
    if step.max_hour is not None and current.hour > step.max_hour:
        return False
    return True


def run_loop(interval_seconds: int, stop_at: datetime, winddown_at: datetime, max_cycles: int | None) -> int:
    cycle = 0
    steps = base_steps() + late_night_steps()
    append_log(
        {
            "Timestamp": now().strftime("%Y-%m-%d %H:%M:%S %z"),
            "Cycle": 0,
            "Step": "night_shift_start",
            "Status": "START",
            "ExitCode": 0,
            "ElapsedSeconds": 0,
            "Detail": f"stop_at={stop_at.isoformat()} winddown_at={winddown_at.isoformat()} interval={interval_seconds}",
        }
    )
    while now() < stop_at:
        cycle += 1
        current = now()
        if max_cycles and cycle > max_cycles:
            break
        write_state(
            {
                "status": "RUNNING",
                "cycle": cycle,
                "timestamp": current.isoformat(),
                "stop_at": stop_at.isoformat(),
                "winddown_at": winddown_at.isoformat(),
            }
        )
        if current >= winddown_at:
            for step in winddown_steps():
                if now() >= stop_at:
                    break
                run_step(step, cycle)
            break
        for step in steps:
            if now() >= min(stop_at, winddown_at):
                break
            if not eligible(step, cycle, current):
                continue
            run_step(step, cycle)
            time.sleep(3)
        remaining = (min(stop_at, winddown_at) - now()).total_seconds()
        if remaining <= 0:
            break
        time.sleep(min(interval_seconds, max(20, remaining)))
    write_state(
        {
            "status": "STOPPED",
            "cycle": cycle,
            "timestamp": now().isoformat(),
            "stop_at": stop_at.isoformat(),
            "winddown_at": winddown_at.isoformat(),
        }
    )
    append_log(
        {
            "Timestamp": now().strftime("%Y-%m-%d %H:%M:%S %z"),
            "Cycle": cycle,
            "Step": "night_shift_stop",
            "Status": "STOPPED",
            "ExitCode": 0,
            "ElapsedSeconds": 0,
            "Detail": "bounded runner exited before shutdown window",
        }
    )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run bounded OpenClaw overnight monthly tasks.")
    parser.add_argument("--interval-seconds", type=int, default=900)
    parser.add_argument("--stop-hour", type=int, default=5)
    parser.add_argument("--stop-minute", type=int, default=50)
    parser.add_argument("--winddown-hour", type=int, default=5)
    parser.add_argument("--winddown-minute", type=int, default=30)
    parser.add_argument("--max-cycles", type=int, default=0)
    args = parser.parse_args()
    stop_at = today_at(args.stop_hour, args.stop_minute)
    winddown_at = today_at(args.winddown_hour, args.winddown_minute)
    raise SystemExit(run_loop(args.interval_seconds, stop_at, winddown_at, args.max_cycles or None))


if __name__ == "__main__":
    main()
