"""Acceptance test for the OpenClaw continuation contract.

This is intentionally a local, boring verification script. It cannot force the
Codex app's heartbeat delivery layer to emit a message, but it verifies every
piece we control:

- current-thread heartbeat automation is active and minute-based
- the local long-shift loop is alive or repairable through ensure script
- visible progress text includes real project counters
- turn-close hook leaves the continuation trigger
- dashboard answers locally
- weather/hardware duty deadline is adaptive, not hard-coded 06:00
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
AUTOMATIONS_DIR = Path(os.environ.get("USERPROFILE", "")) / ".codex" / "automations"
AUTOMATION_ID = "openclaw-current-thread-work-bridge"
AUTOMATION_FILE = AUTOMATIONS_DIR / AUTOMATION_ID / "automation.toml"
ENSURE_SCRIPT = PROJECT_ROOT / "scripts" / "ensure_monthly_shift_running.ps1"
TURN_CLOSE_HOOK = PROJECT_ROOT / "scripts" / "openclaw_turn_close_hook.ps1"
TRIGGER_FILE = DATABASE_DIR / "OpenClaw_Chat_Turn_Close.trigger.json"
DUTY_WINDOW_FILE = DATABASE_DIR / "Monthly_Shift_Duty_Window.json"
DASHBOARD_URL = "http://127.0.0.1:8787/api/status"


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def run_ps(script: Path, timeout: int = 60) -> tuple[int, str]:
    completed = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script),
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        timeout=timeout,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    output = ((completed.stdout or "") + "\n" + (completed.stderr or "")).strip()
    return completed.returncode, output


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}


def check_automation() -> Check:
    if not AUTOMATION_FILE.exists():
        return Check("heartbeat_automation", False, f"missing {AUTOMATION_FILE}")
    text = AUTOMATION_FILE.read_text(encoding="utf-8", errors="ignore")
    required = [
        'kind = "heartbeat"',
        'status = "ACTIVE"',
        'rrule = "FREQ=MINUTELY;INTERVAL=1"',
        "Always choose NOTIFY",
        "ensure_monthly_shift_running.ps1",
    ]
    missing = [needle for needle in required if needle not in text]
    return Check(
        "heartbeat_automation",
        not missing,
        "minute active notify bridge" if not missing else "missing: " + ", ".join(missing),
    )


def check_ensure() -> tuple[Check, str]:
    rc, output = run_ps(ENSURE_SCRIPT, timeout=90)
    good = rc == 0 and "[SHIFT-" in output and "10M_PROGRESS:" in output
    detail = output.replace("\r", " ").replace("\n", " ")[:900]
    return Check("ensure_long_shift", good, detail), output


def check_turn_close() -> Check:
    rc, output = run_ps(TURN_CLOSE_HOOK, timeout=90)
    trigger = read_json(TRIGGER_FILE)
    good = (
        rc == 0
        and TRIGGER_FILE.exists()
        and trigger.get("intent") == "continue_monthly_tasks"
        and trigger.get("role") == "primary_turn_close_continuation"
        and "TURN_CLOSE_HOOK:" in output
    )
    return Check(
        "turn_close_trigger",
        good,
        f"trigger={TRIGGER_FILE}; summary={output.replace(chr(10), ' ')[:500]}",
    )


def check_dashboard() -> Check:
    try:
        with urlopen(DASHBOARD_URL, timeout=5) as response:
            body = response.read(2_000_000).decode("utf-8", errors="ignore")
            data = json.loads(body)
    except Exception as exc:
        return Check("dashboard", False, f"{type(exc).__name__}: {exc}")
    projects = data.get("projects") or {}
    duty = data.get("duty_cycle") or {}
    good = bool(projects) and bool(duty.get("window_end_target_et"))
    return Check(
        "dashboard",
        good,
        f"status ok; projects={len(projects)}; duty_end={duty.get('window_end_target_et')}",
    )


def check_duty_deadline() -> Check:
    payload = read_json(DUTY_WINDOW_FILE)
    end = str(payload.get("shift_end_target_et") or "")
    note = str(payload.get("note") or "")
    source = str(payload.get("deadline_source") or "")
    good = bool(end) and "adaptive weather/resource" in note and "weather" in source
    return Check(
        "adaptive_duty_deadline",
        good,
        f"end={end}; source={source}; note={note}",
    )


def accelerated_loop_probe(rounds: int = 3) -> Check:
    starts: list[str] = []
    for _ in range(rounds):
        rc, output = run_ps(ENSURE_SCRIPT, timeout=90)
        if rc != 0 or "10M_PROGRESS:" not in output:
            return Check("accelerated_probe", False, output.replace("\n", " ")[:700])
        starts.append(output.replace("\r", " ").replace("\n", " ")[:300])
        time.sleep(2)
    return Check("accelerated_probe", True, f"{rounds} ensure cycles passed; latest={starts[-1]}")


def main() -> int:
    checks: list[Check] = []
    checks.append(check_automation())
    ensure_check, ensure_output = check_ensure()
    checks.append(ensure_check)
    checks.append(check_turn_close())
    checks.append(check_dashboard())
    checks.append(check_duty_deadline())
    checks.append(accelerated_loop_probe())

    passed = sum(1 for item in checks if item.passed)
    total = len(checks)
    ok = passed == total
    now = datetime.now().isoformat(timespec="seconds")
    report = {
        "updated_at": now,
        "status": "PASS" if ok else "FAIL",
        "passed": passed,
        "total": total,
        "checks": [item.__dict__ for item in checks],
        "latest_ensure_excerpt": ensure_output.replace("\r", " ").replace("\n", " ")[:1200],
    }
    out_dir = PROJECT_ROOT / "Reports"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "OPENCLAW_CONTINUATION_ACCEPTANCE_latest.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    status_line = f"CONTINUATION_ACCEPTANCE {report['status']} {passed}/{total}: "
    status_line += "; ".join(f"{item.name}={'OK' if item.passed else 'FAIL'}" for item in checks)
    print(status_line)
    print(f"report={out_path}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
