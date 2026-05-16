from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
POLICY_PATH = DATABASE_DIR / "System_Resource_Policy.json"
STATE_PATH = DATABASE_DIR / "System_Resource_State.json"
LOG_PATH = DATABASE_DIR / "System_Resource_Allocation.csv"
COOLDOWN_PATH = DATABASE_DIR / "Hardware_Cooldown_State.json"
AMBIENT_WEATHER_PATH = DATABASE_DIR / "Ambient_Weather_State.json"
RED_ALERT_PATH = DATABASE_DIR / "Thermal_Red_Alert.json"
NY = ZoneInfo("America/New_York")


DEFAULT_POLICY = {
    "timezone": "America/New_York",
    "location": {
        "label": "Lincoln Park / Jersey City, NJ",
        "weather_mode": "forecast_aware",
        "hot_day_high_f": 88,
        "extreme_day_high_f": 92,
        "forecast_note": "On hot Jersey City days, shift heavy work into 20:00-08:00 and keep 12:00-20:00 low-power.",
    },
    "sensor_policy": {
        "temperature_preferred": True,
        "temperature_missing_mode": "proxy_by_cpu_memory",
        "temperature_missing_note": "If Windows denies thermal sensors, use sustained CPU/memory pressure as heat proxy.",
    },
    "temperature_celsius": {
        "ideal_max": 75,
        "warm_reduce": 80,
        "hot_cooldown": 85,
        "critical_pause": 90,
        "cooldown_minutes": 20,
    },
    "load_thresholds": {
        "cpu_reduce_pct": 75,
        "cpu_cooldown_pct": 88,
        "cruise_cpu_target_min_pct": 40,
        "cruise_cpu_target_max_pct": 50,
        "memory_reduce_pct": 82,
        "memory_cooldown_pct": 92,
        "hot_streak_required": 3,
    },
    "windows": [
        {
            "name": "night_heavy_production",
            "start": "00:00",
            "end": "05:30",
            "preferred_classes": ["image_batch", "asset_build", "qa_batch", "market_research", "bulk_download", "api_read"],
            "max_parallel": 1,
            "batch_size": 5,
            "target_cpu_pct": "45-65",
        },
        {
            "name": "pre_shutdown_winddown",
            "start": "05:30",
            "end": "06:00",
            "preferred_classes": ["hardware_heartbeat", "memory_cleanup", "report_batch", "queue_planning", "git_checkpoint", "rest_maintenance"],
            "max_parallel": 1,
            "batch_size": 1,
            "protected_actions": [
                "no_new_marketplace_writes",
                "no_new_browser_ui_tasks",
                "finish_or_stop_by_0550",
                "prepare_for_0600_shutdown"
            ],
        },
        {
            "name": "morning_heavy_production",
            "start": "06:00",
            "end": "08:00",
            "preferred_classes": ["image_batch", "asset_build", "qa_batch", "market_research", "bulk_download", "api_read"],
            "max_parallel": 2,
            "batch_size": 5,
            "target_cpu_pct": "45-65",
        },
        {
            "name": "morning_qa_briefing",
            "start": "08:00",
            "end": "12:00",
            "preferred_classes": ["qa_packaging", "api_read", "local_light", "queue_planning", "memory_cleanup", "hardware_heartbeat"],
            "max_parallel": 1,
            "batch_size": 2,
            "protect_user_interactivity": True,
        },
        {
            "name": "thermal_siesta",
            "start": "12:00",
            "end": "20:00",
            "preferred_classes": ["api_read", "local_light", "queue_planning", "report_batch", "memory_cleanup", "hardware_heartbeat", "sticker_zip_packaging", "pinterest_posting"],
            "max_parallel": 1,
            "batch_size": 2,
            "protect_user_interactivity": True,
            "defer_classes": ["local_heavy", "image_batch", "asset_build", "single_browser_task", "bulk_download", "upscale_batch"],
            "protected_actions": [
                "no_image_generation_batches",
                "no_midjourney_generation",
                "no_fast_upscale",
                "no_heavy_local_image_processing",
                "no_large_preview_builds",
                "no_marketplace_publish_bursts",
                "no_browser_ui_tasks_unless_rex_requests",
                "prefer_api_reads_csv_packaging_reports",
                "move_visual_qa_to_needs_rex_qa"
            ],
        },
        {
            "name": "evening_heavy_production",
            "start": "20:00",
            "end": "23:00",
            "preferred_classes": ["image_batch", "asset_build", "upscale_batch", "market_research", "bulk_download", "qa_batch", "api_read"],
            "max_parallel": 2,
            "batch_size": 4,
            "protect_user_interactivity": True,
        },
        {
            "name": "preflight_checkpoint",
            "start": "23:00",
            "end": "24:00",
            "preferred_classes": ["report_batch", "git_checkpoint", "queue_planning", "local_light"],
            "max_parallel": 1,
            "batch_size": 3,
        },
    ],
    "resource_classes": {
        "local_heavy": {"base_parallel": 2, "base_batch": 8, "public_write": False},
        "image_batch": {"base_parallel": 2, "base_batch": 6, "public_write": False},
        "upscale_batch": {"base_parallel": 1, "base_batch": 3, "public_write": False},
        "qa_batch": {"base_parallel": 2, "base_batch": 10, "public_write": False},
        "qa_packaging": {"base_parallel": 1, "base_batch": 8, "public_write": False},
        "asset_build": {"base_parallel": 2, "base_batch": 6, "public_write": False},
        "bulk_download": {"base_parallel": 1, "base_batch": 8, "public_write": False},
        "sticker_zip_packaging": {"base_parallel": 1, "base_batch": 4, "public_write": False},
        "pinterest_posting": {"base_parallel": 1, "base_batch": 2, "public_write": True},
        "report_batch": {"base_parallel": 2, "base_batch": 8, "public_write": False},
        "market_research": {"base_parallel": 2, "base_batch": 5, "public_write": False},
        "api_read": {"base_parallel": 3, "base_batch": 12, "public_write": False},
        "online_publish_safe": {"base_parallel": 1, "base_batch": 3, "public_write": True},
        "single_browser_task": {"base_parallel": 1, "base_batch": 1, "public_write": True},
        "local_light": {"base_parallel": 1, "base_batch": 5, "public_write": False},
        "git_checkpoint": {"base_parallel": 1, "base_batch": 1, "public_write": False},
        "queue_planning": {"base_parallel": 1, "base_batch": 10, "public_write": False},
        "hardware_heartbeat": {"base_parallel": 1, "base_batch": 1, "public_write": False},
        "memory_cleanup": {"base_parallel": 1, "base_batch": 1, "public_write": False},
        "rest_maintenance": {"base_parallel": 1, "base_batch": 1, "public_write": False},
    },
}


@dataclass
class ResourceSnapshot:
    timestamp: str
    cpu_load_pct: float | None
    memory_used_pct: float | None
    memory_total_gb: float | None
    memory_free_gb: float | None
    temperature_c: float | None
    temperature_status: str
    gpu_util_pct: float | None
    battery_percent: float | None
    power_status: str
    top_processes: list[dict]


@dataclass
class Allocation:
    timestamp: str
    window: str
    task_class: str
    priority: int
    decision: str
    reason: str
    max_parallel: int
    batch_size: int
    cooldown_minutes: int
    cpu_load_pct: float | None
    memory_used_pct: float | None
    temperature_c: float | None
    power_status: str


def now():
    return datetime.now(NY)


def _run_powershell(script: str, timeout=30) -> str:
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
    return completed.stdout.strip()


def _first_float(value):
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _read_cpu_temp_psutil():
    try:
        import psutil  # type: ignore
    except Exception:
        return None, "PSUTIL_NOT_AVAILABLE"
    try:
        sensors = getattr(psutil, "sensors_temperatures", lambda: {})()
    except Exception as exc:
        return None, f"PSUTIL_TEMP_ERROR:{type(exc).__name__}"
    values = []
    for entries in (sensors or {}).values():
        for entry in entries:
            current = _first_float(getattr(entry, "current", None))
            if current is not None and -20 <= current <= 120:
                values.append(current)
    if not values:
        return None, "PSUTIL_TEMP_UNAVAILABLE"
    return max(values), "OK_PSUTIL"


def ensure_policy():
    DATABASE_DIR.mkdir(exist_ok=True)
    if not POLICY_PATH.exists():
        POLICY_PATH.write_text(json.dumps(DEFAULT_POLICY, indent=2), encoding="utf-8")
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def sample_resources() -> ResourceSnapshot:
    script = r"""
$ErrorActionPreference='SilentlyContinue'
$cpu=(Get-CimInstance Win32_Processor | Select-Object -First 1)
$os=Get-CimInstance Win32_OperatingSystem
$total=[math]::Round($os.TotalVisibleMemorySize/1MB,2)
$free=[math]::Round($os.FreePhysicalMemory/1MB,2)
$usedPct=[math]::Round((($total-$free)/$total)*100,1)
$temp=$null
$tempStatus='UNAVAILABLE'
try {
  $tz=Get-CimInstance -Namespace root/wmi -Class MSAcpi_ThermalZoneTemperature -ErrorAction Stop | Select-Object -First 1
  if($tz){ $temp=[math]::Round(($tz.CurrentTemperature/10)-273.15,1); $tempStatus='OK' }
} catch { $tempStatus='DENIED_OR_UNAVAILABLE' }
$gpu=$null
try {
  $samples=(Get-Counter '\GPU Engine(*)\Utilization Percentage' -ErrorAction Stop).CounterSamples |
    Where-Object { $_.InstanceName -match 'engtype_3d|engtype_compute' }
  if($samples){ $gpu=[math]::Round(($samples | Measure-Object CookedValue -Sum).Sum,1) }
} catch {}
$battery=Get-CimInstance Win32_Battery | Select-Object -First 1
$batteryPct=$null
$power='AC_OR_NO_BATTERY'
if($battery){
  $batteryPct=[double]$battery.EstimatedChargeRemaining
  $power = switch ($battery.BatteryStatus) {
    1 {'BATTERY_DISCHARGING'}
    2 {'AC_CHARGING'}
    3 {'FULLY_CHARGED'}
    6 {'CHARGING'}
    7 {'CHARGING_HIGH'}
    8 {'CHARGING_LOW'}
    9 {'CHARGING_CRITICAL'}
    default {'BATTERY_STATUS_' + $battery.BatteryStatus}
  }
}
$top=Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 8 ProcessName,Id,@{n='WorkingSetMB';e={[math]::Round($_.WorkingSet64/1MB,1)}},CPU
[pscustomobject]@{
  CpuLoadPct=[double]$cpu.LoadPercentage
  MemoryUsedPct=[double]$usedPct
  MemoryTotalGB=[double]$total
  MemoryFreeGB=[double]$free
  TemperatureC=$temp
  TemperatureStatus=$tempStatus
  GpuUtilPct=$gpu
  BatteryPercent=$batteryPct
  PowerStatus=$power
  TopProcesses=$top
} | ConvertTo-Json -Depth 5
"""
    try:
        data = json.loads(_run_powershell(script))
    except Exception as exc:
        data = {
            "CpuLoadPct": None,
            "MemoryUsedPct": None,
            "MemoryTotalGB": None,
            "MemoryFreeGB": None,
            "TemperatureC": None,
            "TemperatureStatus": f"SAMPLE_ERROR:{type(exc).__name__}:{exc}",
            "GpuUtilPct": None,
            "BatteryPercent": None,
            "PowerStatus": "UNKNOWN",
            "TopProcesses": [],
        }
    if _first_float(data.get("TemperatureC")) is None:
        psutil_temp, psutil_status = _read_cpu_temp_psutil()
        if psutil_temp is not None:
            data["TemperatureC"] = psutil_temp
            data["TemperatureStatus"] = psutil_status
        else:
            data["TemperatureStatus"] = f"{data.get('TemperatureStatus') or 'UNKNOWN'}|{psutil_status}"
    top = data.get("TopProcesses") or []
    if isinstance(top, dict):
        top = [top]
    return ResourceSnapshot(
        timestamp=now().isoformat(timespec="seconds"),
        cpu_load_pct=_first_float(data.get("CpuLoadPct")),
        memory_used_pct=_first_float(data.get("MemoryUsedPct")),
        memory_total_gb=_first_float(data.get("MemoryTotalGB")),
        memory_free_gb=_first_float(data.get("MemoryFreeGB")),
        temperature_c=_first_float(data.get("TemperatureC")),
        temperature_status=str(data.get("TemperatureStatus") or "UNKNOWN"),
        gpu_util_pct=_first_float(data.get("GpuUtilPct")),
        battery_percent=_first_float(data.get("BatteryPercent")),
        power_status=str(data.get("PowerStatus") or "UNKNOWN"),
        top_processes=top,
    )


def _minutes(text):
    hour, minute = text.split(":")
    return int(hour) * 60 + int(minute)


def active_window(policy, at=None):
    at = at or now()
    current = at.hour * 60 + at.minute
    for window in policy["windows"]:
        start = _minutes(window["start"])
        end = _minutes(window["end"])
        if start <= current < end:
            return window
    return policy["windows"][-1]


def _load_state():
    if not STATE_PATH.exists():
        return {"hot_streak": 0, "last_decision": ""}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"hot_streak": 0, "last_decision": "STATE_READ_ERROR"}


def _active_cooldown():
    if not COOLDOWN_PATH.exists():
        return None
    try:
        data = json.loads(COOLDOWN_PATH.read_text(encoding="utf-8"))
        if not data.get("active"):
            return None
        until_text = str(data.get("cooldown_until") or "")
        until = datetime.fromisoformat(until_text)
        if until.tzinfo is None:
            until = until.replace(tzinfo=NY)
        if until <= now():
            return None
        return data
    except Exception:
        return None


def _load_ambient_weather():
    if not AMBIENT_WEATHER_PATH.exists():
        return {}
    try:
        data = json.loads(AMBIENT_WEATHER_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    try:
        stamp = datetime.fromisoformat(str(data.get("observed_at_et") or data.get("updated_at_et") or ""))
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=NY)
        if now() - stamp > timedelta(hours=8):
            data["stale"] = True
    except Exception:
        data["stale"] = True
    return data


def _write_state(state):
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _append_log(allocation: Allocation):
    exists = LOG_PATH.exists()
    with LOG_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(allocation).keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(asdict(allocation))


def _write_cooldown(allocation: Allocation, snapshot: ResourceSnapshot):
    if allocation.decision != "PAUSE_COOLDOWN" or allocation.cooldown_minutes <= 0:
        return
    cooldown_until = now() + timedelta(minutes=allocation.cooldown_minutes)
    payload = {
        "active": True,
        "updated_at_et": allocation.timestamp,
        "cooldown_until": cooldown_until.isoformat(timespec="seconds"),
        "reason": allocation.reason,
        "temperature_c": allocation.temperature_c,
        "cpu_load_pct": allocation.cpu_load_pct,
        "memory_used_pct": allocation.memory_used_pct,
        "snapshot": asdict(snapshot),
    }
    COOLDOWN_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_red_alert(allocation: Allocation, snapshot: ResourceSnapshot):
    if snapshot.temperature_c is None or snapshot.temperature_c < 90:
        return
    payload = {
        "active": True,
        "severity": "RED",
        "updated_at_et": allocation.timestamp,
        "message": "CPU temperature exceeded 90C. Heavy operational tasks must stop; run only lightweight polling/text/DB work until cooldown.",
        "allocation": asdict(allocation),
        "snapshot": asdict(snapshot),
    }
    RED_ALERT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def choose_allocation(task_class="auto", priority=50, snapshot=None, policy=None, write_state=True):
    policy = policy or ensure_policy()
    snapshot = snapshot or sample_resources()
    window = active_window(policy)
    if task_class == "auto":
        task_class = (window.get("preferred_classes") or ["local_light"])[0]
    classes = policy["resource_classes"]
    class_policy = classes.get(task_class) or classes["local_light"]
    base_parallel = min(int(class_policy["base_parallel"]), int(window.get("max_parallel", 1)))
    base_batch = min(int(class_policy["base_batch"]), int(window.get("batch_size", 1)))

    thresholds = policy["load_thresholds"]
    temps = policy["temperature_celsius"]
    reasons = []
    decision = "RUN"
    cooldown = 0
    cooldown_state = _active_cooldown()

    temp = snapshot.temperature_c
    cpu = snapshot.cpu_load_pct
    mem = snapshot.memory_used_pct
    hot_now = False
    ambient = _load_ambient_weather()
    current_f = _first_float(ambient.get("current_f"))
    today_high_f = _first_float(ambient.get("today_high_f"))
    hot_day_f = _first_float(policy.get("location", {}).get("hot_day_high_f")) or 88
    extreme_day_f = _first_float(policy.get("location", {}).get("extreme_day_high_f")) or 92
    hot_ambient_day = False
    extreme_ambient_day = False
    weather_heavy_allowed = None
    next_cool_window = None
    if not ambient.get("stale"):
        hot_ambient_day = (today_high_f is not None and today_high_f >= hot_day_f) or (current_f is not None and current_f >= hot_day_f)
        extreme_ambient_day = (today_high_f is not None and today_high_f >= extreme_day_f) or (current_f is not None and current_f >= extreme_day_f)
        weather_heavy_allowed = ambient.get("heavy_allowed_now_by_weather")
        next_cool_window = ambient.get("next_cool_heavy_window_et")
        reasons.append(f"ambient Jersey City current={current_f}F high={today_high_f}F")
    elif ambient:
        reasons.append("ambient weather stale; using local resource proxy only")

    if temp is not None:
        if temp >= temps["critical_pause"]:
            decision = "PAUSE_COOLDOWN"
            cooldown = max(cooldown, temps["cooldown_minutes"])
            reasons.append(f"temperature critical {temp:.1f}C")
        elif temp >= temps["hot_cooldown"]:
            decision = "PAUSE_COOLDOWN"
            cooldown = max(cooldown, temps["cooldown_minutes"])
            reasons.append(f"temperature hot {temp:.1f}C")
        elif temp >= temps["warm_reduce"]:
            decision = "RUN_CONSERVATIVE"
            reasons.append(f"temperature warm {temp:.1f}C")
    else:
        reasons.append(f"temperature sensor {snapshot.temperature_status}; using CPU/memory proxy")

    if cpu is not None and cpu >= thresholds["cpu_cooldown_pct"]:
        hot_now = True
        reasons.append(f"cpu high {cpu:.1f}%")
    elif cpu is not None and cpu >= thresholds["cpu_reduce_pct"] and decision == "RUN":
        decision = "RUN_CONSERVATIVE"
        reasons.append(f"cpu elevated {cpu:.1f}%")
    if mem is not None and mem >= thresholds["memory_cooldown_pct"]:
        hot_now = True
        if task_class == "memory_cleanup":
            decision = "RUN_CONSERVATIVE"
            reasons.append(f"memory high {mem:.1f}%; run cleanup before any pause")
        else:
            reasons.append(f"memory high {mem:.1f}%")
    elif mem is not None and mem >= thresholds["memory_reduce_pct"] and decision == "RUN":
        decision = "RUN_CONSERVATIVE"
        reasons.append(f"memory elevated {mem:.1f}%")

    state = _load_state()
    hot_streak = int(state.get("hot_streak") or 0)
    hot_streak = hot_streak + 1 if hot_now else 0
    if hot_streak >= thresholds["hot_streak_required"]:
        decision = "PAUSE_COOLDOWN"
        cooldown = max(cooldown, temps["cooldown_minutes"])
        reasons.append(f"proxy hot streak {hot_streak}")

    if snapshot.power_status == "BATTERY_DISCHARGING" and task_class in {"local_heavy", "image_batch", "asset_build", "online_publish_safe"}:
        decision = "RUN_CONSERVATIVE" if decision == "RUN" else decision
        reasons.append("battery discharging; avoid heavy/background drains")

    heavy_deferred_by_window = task_class in set(window.get("defer_classes") or [])
    if heavy_deferred_by_window:
        cpu_hot = cpu is not None and cpu >= thresholds["cpu_reduce_pct"]
        mem_hot = mem is not None and mem >= thresholds["memory_reduce_pct"]
        if (
            window.get("name") == "thermal_siesta"
            and not hot_ambient_day
            and not cpu_hot
            and not mem_hot
            and weather_heavy_allowed is not False
        ):
            if decision == "RUN":
                decision = "RUN_CONSERVATIVE"
            reasons.append(f"{task_class} allowed conservative in cool thermal window")
        else:
            decision = "DEFER_TO_NIGHT"
            reasons.append(f"{task_class} deferred by {window.get('name')} heat window")
    if extreme_ambient_day and task_class in {"image_batch", "asset_build", "upscale_batch", "bulk_download", "local_heavy"}:
        decision = "DEFER_TO_NIGHT"
        reasons.append(f"{task_class} deferred by extreme ambient heat forecast")
    if (
        not ambient.get("stale")
        and task_class in {"image_batch", "asset_build", "upscale_batch", "bulk_download", "local_heavy"}
        and weather_heavy_allowed is False
    ):
        decision = "DEFER_TO_NIGHT"
        reasons.append(f"{task_class} deferred by hourly forecast >=80F; next cool window={next_cool_window or 'unknown'}")
    if window.get("name") == "thermal_siesta" and task_class in {
        "online_publish_safe",
        "single_browser_task",
        "market_research",
    }:
        if hot_ambient_day or (cpu is not None and cpu >= thresholds["cpu_reduce_pct"]):
            decision = "DEFER_TO_NIGHT"
            reasons.append(f"{task_class} deferred by thermal siesta account-safety/heat window")
        elif decision == "RUN":
            decision = "RUN_CONSERVATIVE"
            reasons.append(f"{task_class} allowed conservative in cool thermal window")
    if window.get("protect_user_interactivity") and task_class in {"local_heavy", "image_batch", "asset_build"} and priority < 90:
        decision = "DEFER_TO_NIGHT"
        reasons.append("interactive window protects Rex foreground use")
    if window.get("name") == "cruise" and cpu is not None and cpu >= thresholds["cruise_cpu_target_max_pct"]:
        decision = "RUN_CONSERVATIVE" if decision == "RUN" else decision
        reasons.append(f"cruise target CPU 40-50%; current {cpu:.1f}%")

    if cooldown_state:
        remaining = int((datetime.fromisoformat(cooldown_state["cooldown_until"]) - now()).total_seconds() / 60)
        cooling_allowed = task_class in {
            "hardware_heartbeat",
            "report_batch",
            "local_light",
            "queue_planning",
            "api_read",
            "online_publish_safe",
            "memory_cleanup",
        }
        reasons.append(f"hardware cooldown active {max(1, remaining)}m: {cooldown_state.get('reason', '')}")
        if cooling_allowed and decision == "RUN":
            decision = "RUN_CONSERVATIVE"
        elif not cooling_allowed:
            decision = "PAUSE_COOLDOWN"
            cooldown = max(cooldown, max(1, remaining))

    if decision == "RUN_CONSERVATIVE":
        base_parallel = 1
        base_batch = max(1, min(base_batch, 2))
    elif decision in {"PAUSE_COOLDOWN", "DEFER_TO_NIGHT"}:
        base_parallel = 0
        base_batch = 0

    if not reasons:
        reasons.append("resource envelope healthy")

    allocation = Allocation(
        timestamp=now().isoformat(timespec="seconds"),
        window=str(window.get("name")),
        task_class=task_class,
        priority=priority,
        decision=decision,
        reason="; ".join(reasons),
        max_parallel=base_parallel,
        batch_size=base_batch,
        cooldown_minutes=cooldown,
        cpu_load_pct=cpu,
        memory_used_pct=mem,
        temperature_c=temp,
        power_status=snapshot.power_status,
    )
    if write_state:
        state.update(
            {
                "updated_at": allocation.timestamp,
                "hot_streak": hot_streak,
                "last_decision": allocation.decision,
                "last_reason": allocation.reason,
                "last_snapshot": asdict(snapshot),
                "last_allocation": asdict(allocation),
            }
        )
        _write_state(state)
        _append_log(allocation)
        _write_cooldown(allocation, snapshot)
        _write_red_alert(allocation, snapshot)
    return allocation, snapshot


def main():
    parser = argparse.ArgumentParser(description="OpenClaw local system resource allocator.")
    parser.add_argument("--task-class", default="auto")
    parser.add_argument("--priority", type=int, default=50)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--interval-seconds", type=int, default=300)
    parser.add_argument("--iterations", type=int, default=0, help="0 means run forever in --watch mode.")
    args = parser.parse_args()

    ensure_policy()
    iteration = 0
    while True:
        allocation, snapshot = choose_allocation(task_class=args.task_class, priority=args.priority)
        payload = {"allocation": asdict(allocation), "snapshot": asdict(snapshot)}
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(
                f"[RESOURCE] window={allocation.window} task={allocation.task_class} "
                f"decision={allocation.decision} parallel={allocation.max_parallel} "
                f"batch={allocation.batch_size} cooldown={allocation.cooldown_minutes}m "
                f"reason={allocation.reason}"
            )
        if not args.watch:
            break
        iteration += 1
        if args.iterations and iteration >= args.iterations:
            break
        time.sleep(max(10, args.interval_seconds))


if __name__ == "__main__":
    main()
