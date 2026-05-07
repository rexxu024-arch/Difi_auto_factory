from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.system_resource_allocator import sample_resources


DATABASE_DIR = PROJECT_ROOT / "Database"
STATE_PATH = DATABASE_DIR / "Hardware_Heartbeat_State.json"
LOG_PATH = DATABASE_DIR / "Hardware_Heartbeat.csv"
NY = ZoneInfo("America/New_York")


@dataclass
class Heartbeat:
    timestamp: str
    cpu_load_pct: float | None
    memory_used_pct: float | None
    temperature_c: float | None
    temperature_status: str
    fan_rpm: float | None
    fan_status: str
    gpu_util_pct: float | None
    battery_percent: float | None
    power_status: str
    health_state: str
    reason: str


def _run_powershell(script: str, timeout=20) -> str:
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return completed.stdout.strip() or completed.stderr.strip()


def _first_float(value):
    try:
        if value in {None, ""}:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def sample_fan():
    script = r"""
$ErrorActionPreference='SilentlyContinue'
$fan=$null
$status='UNAVAILABLE'
try {
  $item=Get-CimInstance Win32_Fan | Select-Object -First 1
  if($item){
    $fan=[double]$item.DesiredSpeed
    if(-not $fan -or $fan -lt 1){ $fan=[double]$item.VariableSpeed }
    $status='OK_WIN32_FAN'
  }
} catch { $status='DENIED_OR_UNAVAILABLE' }
[pscustomobject]@{ FanRPM=$fan; FanStatus=$status } | ConvertTo-Json
"""
    try:
        data = json.loads(_run_powershell(script))
        return _first_float(data.get("FanRPM")), str(data.get("FanStatus") or "UNKNOWN")
    except Exception as exc:
        return None, f"FAN_SAMPLE_ERROR:{type(exc).__name__}:{exc}"


def classify(snapshot, fan_rpm, fan_status):
    reasons = []
    health = "OK"
    if snapshot.temperature_c is not None:
        if snapshot.temperature_c >= 90:
            return "CRITICAL", f"temperature critical {snapshot.temperature_c:.1f}C"
        if snapshot.temperature_c >= 85:
            health = "COOLDOWN"
            reasons.append(f"temperature hot {snapshot.temperature_c:.1f}C")
        elif snapshot.temperature_c >= 80:
            health = "WARM"
            reasons.append(f"temperature warm {snapshot.temperature_c:.1f}C")
    else:
        reasons.append(f"temperature {snapshot.temperature_status}")

    if snapshot.cpu_load_pct is not None:
        if snapshot.cpu_load_pct >= 90:
            health = "COOLDOWN" if health != "CRITICAL" else health
            reasons.append(f"cpu {snapshot.cpu_load_pct:.1f}%")
        elif snapshot.cpu_load_pct >= 75 and health == "OK":
            health = "WARM"
            reasons.append(f"cpu elevated {snapshot.cpu_load_pct:.1f}%")
    if snapshot.memory_used_pct is not None:
        if snapshot.memory_used_pct >= 92:
            health = "COOLDOWN" if health != "CRITICAL" else health
            reasons.append(f"memory {snapshot.memory_used_pct:.1f}%")
        elif snapshot.memory_used_pct >= 82 and health == "OK":
            health = "WARM"
            reasons.append(f"memory elevated {snapshot.memory_used_pct:.1f}%")
    if fan_rpm is None:
        reasons.append(f"fan {fan_status}")
    if not reasons:
        reasons.append("within guardrail")
    return health, "; ".join(reasons)


def sample_heartbeat():
    snapshot = sample_resources()
    fan_rpm, fan_status = sample_fan()
    health, reason = classify(snapshot, fan_rpm, fan_status)
    return Heartbeat(
        timestamp=datetime.now(NY).isoformat(timespec="seconds"),
        cpu_load_pct=snapshot.cpu_load_pct,
        memory_used_pct=snapshot.memory_used_pct,
        temperature_c=snapshot.temperature_c,
        temperature_status=snapshot.temperature_status,
        fan_rpm=fan_rpm,
        fan_status=fan_status,
        gpu_util_pct=snapshot.gpu_util_pct,
        battery_percent=snapshot.battery_percent,
        power_status=snapshot.power_status,
        health_state=health,
        reason=reason,
    )


def write_heartbeat(heartbeat: Heartbeat):
    DATABASE_DIR.mkdir(exist_ok=True)
    STATE_PATH.write_text(json.dumps(asdict(heartbeat), indent=2), encoding="utf-8")
    exists = LOG_PATH.exists()
    with LOG_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(heartbeat).keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(asdict(heartbeat))


def main():
    parser = argparse.ArgumentParser(description="Hardware heartbeat monitor for OpenClaw cruise factory.")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--interval-seconds", type=int, default=300)
    parser.add_argument("--iterations", type=int, default=0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    iteration = 0
    while True:
        heartbeat = sample_heartbeat()
        write_heartbeat(heartbeat)
        if args.json:
            print(json.dumps(asdict(heartbeat), indent=2))
        else:
            print(
                f"[HEARTBEAT] health={heartbeat.health_state} cpu={heartbeat.cpu_load_pct} "
                f"mem={heartbeat.memory_used_pct} temp={heartbeat.temperature_c} "
                f"fan={heartbeat.fan_rpm} reason={heartbeat.reason}"
            )
        if args.once or not args.watch:
            break
        iteration += 1
        if args.iterations and iteration >= args.iterations:
            break
        time.sleep(max(10, args.interval_seconds))


if __name__ == "__main__":
    main()
