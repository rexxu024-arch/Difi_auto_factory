from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
WEATHER_PATH = DATABASE_DIR / "Ambient_Weather_State.json"
SCHEDULE_PATH = DATABASE_DIR / "Thermal_Task_Schedule.json"
NY = ZoneInfo("America/New_York")

LATITUDE = 40.7243
LONGITUDE = -74.0793
LOCATION_LABEL = "Lincoln Park / Jersey City, NJ"
COOL_HEAVY_THRESHOLD_F = 80.0
DUTY_STOP_THRESHOLD_F = 85.0


def et_now() -> datetime:
    return datetime.now(NY)


def parse_hour(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=NY)
    return parsed.astimezone(NY)


def fetch_open_meteo() -> dict:
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "temperature_2m",
        "temperature_unit": "fahrenheit",
        "forecast_days": 3,
        "timezone": "America/New_York",
    }
    url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def build_windows(hours: list[dict], threshold_f: float, min_len: int = 2) -> list[dict]:
    windows = []
    current: list[dict] = []
    for hour in hours:
        if hour["temperature_f"] < threshold_f:
            current.append(hour)
        else:
            if len(current) >= min_len:
                windows.append(
                    {
                        "start_et": current[0]["time_et"],
                        "end_et": (parse_hour(current[-1]["time_et"]) + timedelta(hours=1)).isoformat(timespec="seconds"),
                        "hours": len(current),
                        "min_f": min(item["temperature_f"] for item in current),
                        "max_f": max(item["temperature_f"] for item in current),
                    }
                )
            current = []
    if len(current) >= min_len:
        windows.append(
            {
                "start_et": current[0]["time_et"],
                "end_et": (parse_hour(current[-1]["time_et"]) + timedelta(hours=1)).isoformat(timespec="seconds"),
                "hours": len(current),
                "min_f": min(item["temperature_f"] for item in current),
                "max_f": max(item["temperature_f"] for item in current),
            }
        )
    return windows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--max-age-hours", type=float, default=3.0)
    args = parser.parse_args()

    DATABASE_DIR.mkdir(exist_ok=True)
    if WEATHER_PATH.exists():
        try:
            existing = json.loads(WEATHER_PATH.read_text(encoding="utf-8"))
            updated = datetime.fromisoformat(str(existing.get("updated_at_et") or ""))
            if updated.tzinfo is None:
                updated = updated.replace(tzinfo=NY)
            if et_now() - updated < timedelta(hours=args.max_age_hours):
                if not args.quiet:
                    print(f"Weather cache fresh: {WEATHER_PATH}")
                return 0
        except Exception:
            pass

    raw = fetch_open_meteo()
    times = raw.get("hourly", {}).get("time", [])
    temps = raw.get("hourly", {}).get("temperature_2m", [])
    now_et = et_now()
    horizon = now_et + timedelta(hours=48)
    hours: list[dict] = []
    for time_text, temp in zip(times, temps):
        stamp = parse_hour(str(time_text))
        if now_et - timedelta(hours=1) <= stamp <= horizon:
            hours.append(
                {
                    "time_et": stamp.isoformat(timespec="seconds"),
                    "temperature_f": round(float(temp), 1),
                    "heavy_allowed": float(temp) < COOL_HEAVY_THRESHOLD_F,
                }
            )

    if not hours:
        raise RuntimeError("Open-Meteo returned no usable hourly forecast rows.")

    nearest = min(hours, key=lambda item: abs((parse_hour(item["time_et"]) - now_et).total_seconds()))
    today = [item for item in hours if parse_hour(item["time_et"]).date() == now_et.date()]
    today_high = max(item["temperature_f"] for item in today) if today else nearest["temperature_f"]
    cool_windows = build_windows(hours, COOL_HEAVY_THRESHOLD_F)
    duty_windows = build_windows(hours, DUTY_STOP_THRESHOLD_F)
    next_cool = next((window for window in cool_windows if parse_hour(window["end_et"]) > now_et), None)

    state = {
        "location": LOCATION_LABEL,
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "source": "open-meteo",
        "updated_at_et": now_et.isoformat(timespec="seconds"),
        "observed_at_et": now_et.isoformat(timespec="seconds"),
        "current_f": nearest["temperature_f"],
        "today_high_f": today_high,
        "heavy_threshold_f": COOL_HEAVY_THRESHOLD_F,
        "duty_stop_threshold_f": DUTY_STOP_THRESHOLD_F,
        "heavy_allowed_now_by_weather": nearest["temperature_f"] < COOL_HEAVY_THRESHOLD_F,
        "light_work_allowed_now_by_weather": nearest["temperature_f"] < DUTY_STOP_THRESHOLD_F,
        "next_cool_heavy_window_et": next_cool["start_et"] if next_cool else None,
        "next_48h_hours": hours,
        "cool_windows": cool_windows,
        "duty_work_windows": duty_windows,
        "note": "Heavy image/upscale/local processing is eligible only when hourly ambient forecast is below 80F, subject to CPU/memory/temperature guards.",
    }
    WEATHER_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")

    schedule = {
        "updated_at_et": state["updated_at_et"],
        "location": LOCATION_LABEL,
        "heavy_threshold_f": COOL_HEAVY_THRESHOLD_F,
        "duty_stop_threshold_f": DUTY_STOP_THRESHOLD_F,
        "cool_heavy_windows": cool_windows,
        "duty_work_windows": duty_windows,
        "current_heavy_allowed": state["heavy_allowed_now_by_weather"],
        "current_light_work_allowed": state["light_work_allowed_now_by_weather"],
        "current_f": state["current_f"],
        "today_high_f": state["today_high_f"],
        "note": "Use cool_heavy_windows for GPU/image work and duty_work_windows for the overall workday. 80-85F is light-work-only, not idle.",
    }
    SCHEDULE_PATH.write_text(json.dumps(schedule, indent=2), encoding="utf-8")

    if not args.quiet:
        allowed = "allowed" if state["heavy_allowed_now_by_weather"] else "deferred"
        next_text = state["next_cool_heavy_window_et"] or "none in 48h"
        print(
            f"Weather updated: {state['current_f']}F now, high {state['today_high_f']}F, "
            f"heavy={allowed}, next cool window={next_text}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
