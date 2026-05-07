from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import time
import urllib.request
from dataclasses import asdict
from datetime import datetime, time as dtime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.memory_pressure_guard import run as run_memory_guard
from modules.system_resource_allocator import sample_resources


DATABASE_DIR = PROJECT_ROOT / "Database"
STATE_PATH = DATABASE_DIR / "Endurance_Protocol_State.json"
LOG_PATH = DATABASE_DIR / "Endurance_Protocol_Log.csv"
REBOOT_DECISION_PATH = DATABASE_DIR / "Daily_Reboot_Decision.json"
SHUTDOWN_DECISION_PATH = DATABASE_DIR / "Daily_Shutdown_Decision.json"
NY = ZoneInfo("America/New_York")

AUTOMATION_PROFILE = Path(os.getenv("OPENCLAW_AUTOMATION_PROFILE") or r"C:\openclaw_edge_profile")
AUTOMATION_CDP_PORT = int(os.getenv("OPENCLAW_CDP_PORT") or "9223")
UI_MAX_SECONDS = 3 * 60 * 60

STRONG_WRITE_KEYWORDS = (
    "etsy_digital_ui_publisher",
    "printify_full_pipeline",
    "printify_mockup_ui_uploader",
    "printify_publish_scheduler",
    "multi_track_copy_executor.py --sync-printify",
    "ebay_ui_title_revise",
    "publish",
    "upload",
)

SAFE_STOP_KEYWORDS = STRONG_WRITE_KEYWORDS + (
    "grunt_engine.py --loop",
    "grunt_engine.py --once",
)

BROWSER_DRIVER_NAMES = {
    "chromedriver",
    "msedgedriver",
    "playwright",
}


def now() -> datetime:
    return datetime.now(NY)


def now_text() -> str:
    return now().strftime("%Y-%m-%d %H:%M:%S %z")


def _append_log(row: dict) -> None:
    LOG_PATH.parent.mkdir(exist_ok=True)
    fields = [
        "Timestamp",
        "Action",
        "Decision",
        "Memory_Pct",
        "CPU_Pct",
        "Killed_Count",
        "Strong_Write_Active",
        "Detail",
    ]
    exists = LOG_PATH.exists()
    with LOG_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow({key: row.get(key, "") for key in fields})


def _http_json(url: str, timeout: int = 3):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        payload = response.read()
    return json.loads(payload.decode("utf-8", errors="replace")) if payload else {}


def _cdp_running(port: int = AUTOMATION_CDP_PORT) -> bool:
    try:
        _http_json(f"http://127.0.0.1:{port}/json/version")
        return True
    except Exception:
        return False


def _state() -> dict:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def update_ui_session() -> dict:
    state = _state()
    running = _cdp_running()
    if running:
        state.setdefault("ui_session_started_at", now().isoformat(timespec="seconds"))
    else:
        state.pop("ui_session_started_at", None)
    state["ui_session_running"] = running
    state["updated_at"] = now().isoformat(timespec="seconds")
    _write_state(state)
    return state


def ui_session_seconds(state: dict | None = None) -> int:
    state = state or _state()
    started = state.get("ui_session_started_at")
    if not started:
        return 0
    try:
        dt = datetime.fromisoformat(started)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=NY)
        return max(0, int((now() - dt).total_seconds()))
    except Exception:
        return 0


def _powershell_json(script: str, timeout: int = 30):
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    if completed.returncode != 0 and not completed.stdout.strip():
        raise RuntimeError(completed.stderr.strip() or f"PowerShell exit {completed.returncode}")
    text = completed.stdout.strip()
    if not text:
        return []
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return []


def project_automation_processes() -> list[dict]:
    profile = str(AUTOMATION_PROFILE).replace("\\", "\\\\")
    script = rf"""
$items = Get-CimInstance Win32_Process | Where-Object {{
  ($_.Name -match 'msedge|chrome|chromedriver|msedgedriver|playwright') -and
  (
    $_.CommandLine -match 'remote-debugging-port={AUTOMATION_CDP_PORT}' -or
    $_.CommandLine -match '{profile}' -or
    $_.Name -match 'chromedriver|msedgedriver|playwright'
  )
}} | Select-Object ProcessId,Name,CommandLine
$items | ConvertTo-Json -Depth 3
"""
    data = _powershell_json(script)
    if isinstance(data, dict):
        return [data]
    return data if isinstance(data, list) else []


def terminate_project_automation_processes(execute: bool = False) -> list[dict]:
    killed: list[dict] = []
    for proc in project_automation_processes():
        pid = int(proc.get("ProcessId") or 0)
        name = str(proc.get("Name") or "")
        if not pid:
            continue
        row = {"pid": pid, "name": name, "action": "WOULD_TERMINATE" if not execute else "TERMINATE"}
        if execute:
            try:
                subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], cwd=PROJECT_ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=15)
            except Exception as exc:  # noqa: BLE001
                row["error"] = f"{type(exc).__name__}: {exc}"
        killed.append(row)
    return killed


def strong_write_active() -> dict:
    script = r"""
$rows = Get-CimInstance Win32_Process | Where-Object {
  $_.Name -match 'python|py|node|powershell|cmd' -and $_.CommandLine
} | Select-Object ProcessId,Name,CommandLine
$rows | ConvertTo-Json -Depth 3
"""
    data = _powershell_json(script)
    rows = [data] if isinstance(data, dict) else (data if isinstance(data, list) else [])
    matches = []
    for row in rows:
        cmd = str(row.get("CommandLine") or "").lower()
        if "openclaw_difi" not in cmd and "scripts\\openclaw-python" not in cmd:
            continue
        if any(token.lower() in cmd for token in STRONG_WRITE_KEYWORDS):
            matches.append({"pid": row.get("ProcessId"), "name": row.get("Name"), "command": cmd[:240]})
    lock_active = False
    lock_path = DATABASE_DIR / "Grunt_Engine.lock"
    if lock_path.exists():
        try:
            lock_active = time.time() - lock_path.stat().st_mtime < 30 * 60
        except OSError:
            lock_active = True
    return {"active": bool(matches) or lock_active, "matches": matches, "grunt_lock_active": lock_active}


def stop_openclaw_write_processes(execute: bool = False) -> list[dict]:
    script = r"""
$rows = Get-CimInstance Win32_Process | Where-Object {
  $_.Name -match 'python|py|node|powershell|cmd' -and $_.CommandLine
} | Select-Object ProcessId,Name,CommandLine
$rows | ConvertTo-Json -Depth 3
"""
    data = _powershell_json(script)
    rows = [data] if isinstance(data, dict) else (data if isinstance(data, list) else [])
    stopped: list[dict] = []
    for row in rows:
        pid = int(row.get("ProcessId") or 0)
        name = str(row.get("Name") or "")
        cmd = str(row.get("CommandLine") or "")
        low = cmd.lower()
        if not pid:
            continue
        if "openclaw_difi" not in low and "scripts\\openclaw-python" not in low:
            continue
        if not any(token.lower() in low for token in SAFE_STOP_KEYWORDS):
            continue
        item = {
            "pid": pid,
            "name": name,
            "action": "WOULD_STOP_OPENCLAW_WRITE" if not execute else "STOP_OPENCLAW_WRITE",
            "command": cmd[:240],
        }
        if execute:
            try:
                subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], cwd=PROJECT_ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=15)
            except Exception as exc:  # noqa: BLE001
                item["error"] = f"{type(exc).__name__}: {exc}"
        stopped.append(item)
    return stopped


def should_enter_cooldown(snapshot=None, ui_seconds: int | None = None) -> tuple[bool, list[str]]:
    snapshot = snapshot or sample_resources()
    ui_seconds = ui_session_seconds() if ui_seconds is None else ui_seconds
    reasons: list[str] = []
    if ui_seconds >= UI_MAX_SECONDS:
        reasons.append(f"Edge CDP UI session exceeded {UI_MAX_SECONDS // 3600}h ({ui_seconds}s)")
    if snapshot.memory_used_pct is not None and snapshot.memory_used_pct >= 88:
        reasons.append(f"memory elevated {snapshot.memory_used_pct:.1f}%")
    if snapshot.cpu_load_pct is not None and snapshot.cpu_load_pct >= 90:
        reasons.append(f"cpu high {snapshot.cpu_load_pct:.1f}%")
    return bool(reasons), reasons


def enter_cooldown(execute: bool = False, reason: str = "") -> dict:
    memory_state = run_memory_guard(execute=execute)
    killed = terminate_project_automation_processes(execute=execute)
    state = _state()
    state.update(
        {
            "updated_at": now().isoformat(timespec="seconds"),
            "mode": "COOLDOWN",
            "reason": reason,
            "memory_guard": memory_state,
            "terminated_processes": killed,
            "allowed_work": ["local CSV/XLSX planning", "report generation", "Printify API read/write when no browser needed", "risk/QA code"],
            "blocked_work": ["Edge CDP UI automation", "image-heavy batch generation", "broad marketplace RPA"],
        }
    )
    state.pop("ui_session_started_at", None)
    _write_state(state)
    snapshot = sample_resources()
    _append_log(
        {
            "Timestamp": now_text(),
            "Action": "enter_cooldown",
            "Decision": "EXECUTED" if execute else "DRY_RUN",
            "Memory_Pct": snapshot.memory_used_pct,
            "CPU_Pct": snapshot.cpu_load_pct,
            "Killed_Count": len(killed),
            "Strong_Write_Active": "",
            "Detail": reason,
        }
    )
    return state


def daily_reboot_due(check_time: datetime | None = None) -> bool:
    check_time = check_time or now()
    return dtime(4, 0) <= check_time.time() <= dtime(4, 20)


def daily_reboot_check(execute: bool = False, force: bool = False) -> dict:
    write_state = strong_write_active()
    due = force or daily_reboot_due()
    decision = "SKIP_NOT_DUE"
    detail = "outside 04:00-04:20 America/New_York"
    if due and write_state["active"]:
        decision = "SKIP_STRONG_WRITE_ACTIVE"
        detail = json.dumps(write_state, ensure_ascii=False)[:500]
    elif due:
        decision = "REBOOT_SCHEDULED" if execute else "REBOOT_READY_DRY_RUN"
        detail = "queues clear; logs/state written"
        if execute:
            subprocess.Popen(
                ["shutdown", "/r", "/t", "30", "/c", "OpenClaw daily endurance reboot"],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    snapshot = sample_resources()
    result = {
        "timestamp": now_text(),
        "decision": decision,
        "execute": execute,
        "due": due,
        "strong_write": write_state,
        "snapshot": asdict(snapshot),
        "detail": detail,
    }
    REBOOT_DECISION_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    _append_log(
        {
            "Timestamp": now_text(),
            "Action": "daily_reboot_check",
            "Decision": decision,
            "Memory_Pct": snapshot.memory_used_pct,
            "CPU_Pct": snapshot.cpu_load_pct,
            "Killed_Count": 0,
            "Strong_Write_Active": str(write_state["active"]),
            "Detail": detail,
        }
    )
    return result


def daily_shutdown_due(check_time: datetime | None = None) -> bool:
    check_time = check_time or now()
    return dtime(6, 0) <= check_time.time() <= dtime(6, 20)


def daily_shutdown_check(execute: bool = False, force: bool = False) -> dict:
    """Daily 06:00 ET hardware rest.

    This intentionally does not bypass Windows login. Rex powers the machine on
    and logs in; Startup then restores Codex/OpenClaw automation.
    """
    write_state = strong_write_active()
    due = force or daily_shutdown_due()
    snapshot = sample_resources()
    decision = "SKIP_NOT_DUE"
    detail = "outside 06:00-06:20 America/New_York"
    shutdown_delay = 0
    if due:
        state = _state()
        state.update(
            {
                "updated_at": now().isoformat(timespec="seconds"),
                "mode": "DAILY_SHUTDOWN_PREP",
                "reason": "06:00 ET hardware rest; Rex will power on manually",
                "strong_write": write_state,
                "startup_recovery": "scripts\\run_codex.bat after Windows login",
            }
        )
        _write_state(state)
        if write_state["active"]:
            decision = "SHUTDOWN_SCHEDULED_WITH_5M_GRACE" if execute else "SHUTDOWN_READY_WITH_5M_GRACE_DRY_RUN"
            detail = "strong write indicators present; giving 5 minute graceful shutdown delay"
            shutdown_delay = 300
        else:
            decision = "SHUTDOWN_SCHEDULED" if execute else "SHUTDOWN_READY_DRY_RUN"
            detail = "queues clear; daily hardware rest"
            shutdown_delay = 60
        if execute:
            subprocess.Popen(
                [
                    "shutdown",
                    "/s",
                    "/t",
                    str(shutdown_delay),
                    "/c",
                    "OpenClaw daily 6AM ET hardware rest. Rex will power on manually.",
                ],
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    result = {
        "timestamp": now_text(),
        "decision": decision,
        "execute": execute,
        "due": due,
        "shutdown_delay_seconds": shutdown_delay,
        "strong_write": write_state,
        "snapshot": asdict(snapshot),
        "detail": detail,
        "password_boundary": "Windows password is not bypassed; recovery resumes after Rex logs in.",
    }
    SHUTDOWN_DECISION_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    _append_log(
        {
            "Timestamp": now_text(),
            "Action": "daily_shutdown_check",
            "Decision": decision,
            "Memory_Pct": snapshot.memory_used_pct,
            "CPU_Pct": snapshot.cpu_load_pct,
            "Killed_Count": 0,
            "Strong_Write_Active": str(write_state["active"]),
            "Detail": detail,
        }
    )
    return result


def shutdown_winddown(execute: bool = False, force_stop: bool = False) -> dict:
    """05:30 ET winddown: stop starting risky work and prepare 06:00 shutdown."""
    snapshot = sample_resources()
    cdp_state = update_ui_session()
    memory_state = run_memory_guard(execute=execute)
    stopped_ui = []
    stopped_writes = []
    mode = "PRE_SHUTDOWN_WINDDOWN"
    if force_stop:
        stopped_ui = terminate_project_automation_processes(execute=execute)
        stopped_writes = stop_openclaw_write_processes(execute=execute)
        mode = "PRE_SHUTDOWN_FORCE_STOP"
    state = _state()
    state.update(
        {
            "updated_at": now().isoformat(timespec="seconds"),
            "mode": mode,
            "reason": "05:30-06:00 ET winddown before daily shutdown",
            "new_task_policy": "Only local optimization, reports, queue planning, memory cleanup, and checkpointing. No new marketplace writes or browser UI tasks.",
            "target_shutdown": "06:00 America/New_York",
            "memory_guard": memory_state,
            "stopped_ui_processes": stopped_ui,
            "stopped_write_processes": stopped_writes,
        }
    )
    _write_state(state)
    result = {
        "timestamp": now_text(),
        "decision": mode if execute else f"{mode}_DRY_RUN",
        "execute": execute,
        "force_stop": force_stop,
        "snapshot": asdict(snapshot),
        "memory_guard_decision": memory_state.get("decision"),
        "stopped_ui_count": len(stopped_ui),
        "stopped_write_count": len(stopped_writes),
        "detail": state["new_task_policy"],
    }
    _append_log(
        {
            "Timestamp": now_text(),
            "Action": "shutdown_winddown",
            "Decision": result["decision"],
            "Memory_Pct": snapshot.memory_used_pct,
            "CPU_Pct": snapshot.cpu_load_pct,
            "Killed_Count": len(stopped_ui) + len(stopped_writes),
            "Strong_Write_Active": str(strong_write_active()["active"]),
            "Detail": result["detail"],
        }
    )
    return result


def preflight(execute: bool = False) -> dict:
    state = update_ui_session()
    snapshot = sample_resources()
    ui_seconds = ui_session_seconds(state)
    need_cooldown, reasons = should_enter_cooldown(snapshot=snapshot, ui_seconds=ui_seconds)
    if need_cooldown:
        cooldown_state = enter_cooldown(execute=execute, reason="; ".join(reasons))
        decision = "COOLDOWN_ENTERED" if execute else "COOLDOWN_RECOMMENDED"
    else:
        cooldown_state = None
        decision = "CONTINUE"
    result = {
        "timestamp": now_text(),
        "decision": decision,
        "execute": execute,
        "ui_session_seconds": ui_seconds,
        "snapshot": asdict(snapshot),
        "reasons": reasons,
        "cooldown": cooldown_state,
    }
    _write_state({**state, **result})
    _append_log(
        {
            "Timestamp": now_text(),
            "Action": "preflight",
            "Decision": decision,
            "Memory_Pct": snapshot.memory_used_pct,
            "CPU_Pct": snapshot.cpu_load_pct,
            "Killed_Count": len((cooldown_state or {}).get("terminated_processes", [])),
            "Strong_Write_Active": "",
            "Detail": "; ".join(reasons),
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenClaw Endurance Protocol: cooldown, daily reboot gate, and browser-driver hygiene.")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--cooldown", action="store_true")
    parser.add_argument("--daily-reboot-check", action="store_true")
    parser.add_argument("--daily-shutdown-check", action="store_true")
    parser.add_argument("--shutdown-winddown", action="store_true")
    parser.add_argument("--force-stop", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--force-due", action="store_true", help="Treat the daily reboot window as due; still respects strong-write detection.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.cooldown:
        result = enter_cooldown(execute=args.execute, reason="manual/endurance cooldown request")
    elif args.daily_reboot_check:
        result = daily_reboot_check(execute=args.execute, force=args.force_due)
    elif args.daily_shutdown_check:
        result = daily_shutdown_check(execute=args.execute, force=args.force_due)
    elif args.shutdown_winddown:
        result = shutdown_winddown(execute=args.execute, force_stop=args.force_stop)
    else:
        result = preflight(execute=args.execute or args.preflight)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"[ENDURANCE] {result.get('decision')} detail={result.get('detail') or '; '.join(result.get('reasons', []))}")


if __name__ == "__main__":
    main()
