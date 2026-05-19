"""Non-destructive continuity self-test for Rex's long monthly shift.

The test verifies the minimum viable contract:
1. A heartbeat exists to wake this thread and demand visible progress.
2. An AI work-block cron exists for real model participation.
3. The local long-shift process is alive or explicitly in thermal cooldown.
4. A work-proof log exists so progress is auditable rather than assumed.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tomllib
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = ROOT / "Database"
REPORTS_DIR = ROOT / "Reports"
AUTOMATION_DIR = Path(os.environ.get("USERPROFILE", "")) / ".codex" / "automations"
ET = ZoneInfo("America/New_York")

HEARTBEAT_ID = "openclaw-current-thread-work-bridge"
AI_WORKER_ID = "openclaw-ai-supervised-long-work-block"
DAILY_WORK_BLOCK_PATH = DATABASE_DIR / "Daily_Work_Blocks_Current.json"
STEER_ROUTE_PATH = DATABASE_DIR / "Chat_Model_Work_Route_Current.json"
STEER_ACCEPTANCE_PATH = DATABASE_DIR / "Steer_Continuation_Acceptance.json"


def read_toml(automation_id: str) -> dict:
    path = AUTOMATION_DIR / automation_id / "automation.toml"
    if not path.exists():
        return {}
    with path.open("rb") as handle:
        return tomllib.load(handle)


def pid_alive(pid_file: Path) -> tuple[bool, str]:
    if not pid_file.exists():
        return False, "pid-file-missing"
    try:
        pid = int(pid_file.read_text(encoding="utf-8").strip())
    except ValueError:
        return False, "pid-file-invalid"
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"Get-Process -Id {pid} -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=12,
        )
    except Exception as exc:  # pragma: no cover - defensive for desktop runtime
        return False, f"process-check-failed:{exc}"
    if str(pid) in result.stdout:
        return True, str(pid)
    return False, f"pid-not-running:{pid}"


def parse_latest_state_stamp(state_file: Path) -> tuple[str, str]:
    if not state_file.exists():
        return "", "state-file-missing"
    lines = state_file.read_text(encoding="utf-8", errors="ignore").splitlines()[-300:]
    stamp_re = re.compile(r"^- (?P<stamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) EDT \| (?P<event>START|END|THERMAL_GLOBAL_STOP|THERMAL_DEFER|THERMAL_CONSERVATIVE)")
    latest_stamp = ""
    latest_event = ""
    for line in lines:
        match = stamp_re.match(line)
        if match:
            latest_stamp = match.group("stamp")
            latest_event = match.group("event")
    return latest_stamp, latest_event


def minutes_old(stamp: str) -> float:
    if not stamp:
        return 99999.0
    try:
        dt = datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S").replace(tzinfo=ET)
    except ValueError:
        return 99999.0
    return (datetime.now(ET) - dt).total_seconds() / 60


def proof_age_minutes() -> float:
    path = DATABASE_DIR / "Work_Proof_Latest.json"
    if not path.exists():
        return 99999.0
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        stamp = str(data.get("recorded_at_et", ""))
        # PowerShell can emit 7 fractional digits, while Python accepts up to 6.
        if "." in stamp:
            head, tail = stamp.split(".", 1)
            frac = tail
            zone = ""
            for marker in ("+", "-", "Z"):
                if marker in tail:
                    frac, zone = tail.split(marker, 1)
                    zone = marker + zone
                    break
            stamp = head + "." + frac[:6] + zone
        dt = datetime.fromisoformat(stamp)
    except Exception:
        return 99999.0
    return (datetime.now(ET) - dt).total_seconds() / 60


def daily_work_block_status() -> tuple[bool, str]:
    if not DAILY_WORK_BLOCK_PATH.exists():
        return False, "daily-work-block-file-missing"
    try:
        payload = json.loads(DAILY_WORK_BLOCK_PATH.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return False, f"daily-work-block-json-error:{type(exc).__name__}"
    blocks = payload.get("blocks", [])
    leaked_test = [
        block.get("id", "")
        for block in blocks
        if "STEER_ACCEPTANCE" in str(block.get("title", "")) or "Test-only rescued steer" in str(block.get("objective", ""))
    ]
    if leaked_test:
        return False, f"test-steer-leaked ids={','.join(leaked_test[:3])}"
    current = next((block for block in blocks if block.get("status") in {"IN_PROGRESS", "PENDING"}), None)
    if not current:
        return False, f"no-current-block total={len(blocks)}"
    return True, f"current={current.get('id')} project={current.get('project')} total={len(blocks)}"


def steer_route_status() -> tuple[bool, str]:
    if not STEER_ROUTE_PATH.exists():
        return False, "steer-route-file-missing"
    try:
        payload = json.loads(STEER_ROUTE_PATH.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return False, f"steer-route-json-error:{type(exc).__name__}"
    blocks = payload.get("blocks", [])
    first = blocks[0] if blocks else {}
    ok = (
        payload.get("mode") == "chat_model_steer_equivalent_route"
        and bool(blocks)
        and str(first.get("id", "")).startswith("steer_")
        and "chat" in str(payload.get("policy", "")).lower()
        and "model" in str(payload.get("policy", "")).lower()
    )
    detail = f"blocks={len(blocks)} first={first.get('id')} shutdown={payload.get('thermal_summary', {}).get('shutdown_policy')}"
    return ok, detail


def steer_acceptance_status() -> tuple[bool, str]:
    if not STEER_ACCEPTANCE_PATH.exists():
        return False, "steer-acceptance-report-missing"
    try:
        payload = json.loads(STEER_ACCEPTANCE_PATH.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return False, f"steer-acceptance-json-error:{type(exc).__name__}"
    status = payload.get("status")
    checked_at = payload.get("checked_at_et", "")
    try:
        checked_dt = datetime.fromisoformat(checked_at)
        age_min = (datetime.now(ET) - checked_dt).total_seconds() / 60
    except Exception:
        age_min = 99999.0
    checks = payload.get("checks", [])
    failed = [item.get("name", "unknown") for item in checks if not item.get("ok")]
    ok = status == "PASS" and age_min < 24 * 60 and not failed
    detail = f"status={status} age_min={age_min:.1f}"
    if failed:
        detail += f" failed={','.join(failed)}"
    return ok, detail


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    checks: list[dict] = []

    hb = read_toml(HEARTBEAT_ID)
    hb_prompt = str(hb.get("prompt", ""))
    checks.append(
        {
            "name": "current-thread heartbeat",
            "ok": hb.get("status") == "ACTIVE"
            and hb.get("kind") == "heartbeat"
            and "VISIBLE" in hb_prompt
            and "Chat_Model_Work_Route_Current.json" in hb_prompt
            and "daily_steer_workblock_planner.py" in hb_prompt
            and ("work" in hb_prompt.lower() or "concrete" in hb_prompt.lower()),
            "detail": f"status={hb.get('status')} rrule={hb.get('rrule')}",
        }
    )

    worker = read_toml(AI_WORKER_ID)
    worker_prompt = str(worker.get("prompt", ""))
    checks.append(
        {
            "name": "AI model work-block cron",
            "ok": worker.get("status") == "ACTIVE"
            and worker.get("kind") == "cron"
            and worker.get("reasoning_effort") == "xhigh"
            and "concrete project work" in worker_prompt
            and "Chat_Model_Work_Route_Current.json" in worker_prompt
            and "Daily_Work_Blocks_Current.json" in worker_prompt,
            "detail": f"status={worker.get('status')} model={worker.get('model')} rrule={worker.get('rrule')}",
        }
    )

    block_ok, block_detail = daily_work_block_status()
    checks.append({"name": "daily work-block queue", "ok": block_ok, "detail": block_detail})

    route_ok, route_detail = steer_route_status()
    checks.append({"name": "Steer-equivalent route", "ok": route_ok, "detail": route_detail})

    steer_ok, steer_detail = steer_acceptance_status()
    checks.append({"name": "Steer continuation rescue acceptance", "ok": steer_ok, "detail": steer_detail})

    alive, pid_detail = pid_alive(DATABASE_DIR / "Monthly_Shift_Loop.pid")
    checks.append({"name": "local long-shift pid", "ok": alive, "detail": pid_detail})

    stamp, event = parse_latest_state_stamp(DATABASE_DIR / "Monthly_Shift_Loop_State.md")
    age = minutes_old(stamp)
    checks.append(
        {
            "name": "long-shift state freshness",
            "ok": age < 30 or event == "THERMAL_GLOBAL_STOP",
            "detail": f"latest={stamp or 'none'} event={event or 'none'} age_min={age:.1f}",
        }
    )

    proof_age = proof_age_minutes()
    checks.append(
        {
            "name": "auditable work proof",
            "ok": proof_age < 180,
            "detail": f"latest_age_min={proof_age:.1f}",
        }
    )

    ok_count = sum(1 for item in checks if item["ok"])
    all_ok = ok_count == len(checks)
    data = {
        "checked_at_et": datetime.now(ET).isoformat(timespec="seconds"),
        "status": "PASS" if all_ok else "WARN",
        "checks": checks,
    }
    (DATABASE_DIR / "Monthly_Shift_Continuity_Selftest.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    lines = [
        "# Monthly Shift Continuity Selftest",
        "",
        f"- checked_at_et: `{data['checked_at_et']}`",
        f"- status: `{data['status']}`",
        "",
    ]
    for item in checks:
        mark = "PASS" if item["ok"] else "WARN"
        lines.append(f"- {mark}: {item['name']} - {item['detail']}")
    lines.append("")
    report = "\n".join(lines)
    (REPORTS_DIR / "Monthly_Shift_Continuity_Selftest_latest.md").write_text(
        report,
        encoding="utf-8",
    )
    print(report)
    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
