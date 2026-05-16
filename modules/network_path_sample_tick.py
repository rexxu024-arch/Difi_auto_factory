"""Timed 48-hour Ethernet/Wi-Fi sampling wrapper.

This is deliberately separate from Codex heartbeats. It records the physical
network path in the background so Rex can decide whether the USB Ethernet
adapter is unstable without needing manual spot checks.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import network_path_monitor as npm


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
CONFIG_PATH = DATABASE / "Network_Path_Sampling_Config.json"
TASK_NAME = "OpenClaw Network Path Sampler"
NY_TZ = ZoneInfo("America/New_York")


def now_et() -> datetime:
    return datetime.now(NY_TZ)


def read_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_config(config: dict) -> None:
    DATABASE.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")


def init_config(hours: float, interval_minutes: int, expected_alias: str) -> dict:
    started = now_et()
    config = {
        "enabled": True,
        "started_at": started.isoformat(timespec="seconds"),
        "ends_at": (started + timedelta(hours=hours)).isoformat(timespec="seconds"),
        "duration_hours": hours,
        "interval_minutes": interval_minutes,
        "expected_alias": expected_alias,
        "task_name": TASK_NAME,
        "purpose": "48h Ethernet stability sampling; alert only if active path leaves Ethernet or Ethernet drops.",
    }
    write_config(config)
    return config


def parse_dt(text: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=NY_TZ)
        return parsed.astimezone(NY_TZ)
    except Exception:
        return None


def disable_task_quietly(task_name: str) -> None:
    try:
        subprocess.run(
            ["schtasks", "/Change", "/TN", task_name, "/DISABLE"],
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )
    except Exception:
        pass


def sample_once(config: dict) -> dict:
    previous = npm.read_state()
    current = npm.snapshot()
    expected_alias = str(config.get("expected_alias") or "Ethernet 3")
    current["alert"] = npm.classify_alert(current, previous, expected_alias)
    npm.append_csv(npm.LOG_PATH, current)
    if current["alert"]:
        npm.append_csv(npm.ALERT_PATH, current)
    npm.STATE_PATH.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")
    return current


def tick() -> dict:
    config = read_config()
    if not config.get("enabled"):
        return {"status": "DISABLED", "config": config}
    end_at = parse_dt(str(config.get("ends_at") or ""))
    if end_at and now_et() > end_at:
        config["enabled"] = False
        config["completed_at"] = now_et().isoformat(timespec="seconds")
        write_config(config)
        disable_task_quietly(str(config.get("task_name") or TASK_NAME))
        return {"status": "COMPLETED_WINDOW", "config": config}
    current = sample_once(config)
    current["status"] = "SAMPLED"
    return current


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenClaw network sampling tick.")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--hours", type=float, default=48)
    parser.add_argument("--interval-minutes", type=int, default=10)
    parser.add_argument("--expected-alias", default="Ethernet 3")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.init:
        result = init_config(args.hours, args.interval_minutes, args.expected_alias)
        result["status"] = "INITIALIZED"
    else:
        result = tick()

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result.get('status')} active={result.get('active_alias', '')} alert={result.get('alert', '')}")


if __name__ == "__main__":
    main()
