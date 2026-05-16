from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
ALLOC_LOG = DATABASE_DIR / "System_Resource_Allocation.csv"
STATE_PATH = DATABASE_DIR / "System_Resource_State.json"
WEATHER_PATH = DATABASE_DIR / "Ambient_Weather_State.json"
OUT_PATH = DATABASE_DIR / "Thermal_Efficiency_Report.md"
ET = ZoneInfo("America/New_York")


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    except OSError:
        return []


def parse_stamp(value: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value)
    except Exception:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=ET)
    return parsed.astimezone(ET)


def fnum(value) -> float | None:
    try:
        if value in (None, ""):
            return None
        return float(value)
    except Exception:
        return None


def window_counts(rows: list[dict]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for row in rows:
        window = row.get("window") or "unknown"
        decision = row.get("decision") or "UNKNOWN"
        counts.setdefault(window, {})
        counts[window][decision] = counts[window].get(decision, 0) + 1
    return counts


def avg(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 1)


def main() -> int:
    now = datetime.now(ET)
    cutoff = now - timedelta(hours=48)
    rows = []
    for row in read_rows(ALLOC_LOG):
        stamp = parse_stamp(row.get("timestamp", ""))
        if stamp and stamp >= cutoff:
            rows.append(row)

    cpus = [x for x in (fnum(row.get("cpu_load_pct")) for row in rows) if x is not None]
    mems = [x for x in (fnum(row.get("memory_used_pct")) for row in rows) if x is not None]
    decisions = {}
    for row in rows:
        decisions[row.get("decision") or "UNKNOWN"] = decisions.get(row.get("decision") or "UNKNOWN", 0) + 1

    state = load_json(STATE_PATH, {})
    weather = load_json(WEATHER_PATH, {})
    current_f = weather.get("current_f")
    high_f = weather.get("today_high_f")
    heavy_allowed_now = weather.get("heavy_allowed_now_by_weather")
    next_cool = weather.get("next_cool_heavy_window_et")

    counts = window_counts(rows)
    hot_pause = decisions.get("PAUSE_COOLDOWN", 0)
    deferred = decisions.get("DEFER_TO_NIGHT", 0)
    conservative = decisions.get("RUN_CONSERVATIVE", 0)
    run = decisions.get("RUN", 0)

    recommendation = "Normal schedule: continue mixed work."
    if heavy_allowed_now is False:
        recommendation = (
            "Heat-aware schedule: defer image/upscale/heavy local work until the next <80F window "
            f"({next_cool or 'unknown'}); keep lightweight API/CSV/SEO/QA work active now."
        )
    elif high_f and float(high_f) >= 92:
        recommendation = "Hot-day schedule: run heavy work before 08:00 ET or after 20:00 ET; keep 12:00-20:00 light."
    elif high_f and float(high_f) >= 88:
        recommendation = "Warm-day schedule: allow only conservative heavy work when CPU < 65% and memory < 80%; otherwise defer to night."
    elif avg(cpus) is not None and avg(cpus) >= 75:
        recommendation = "CPU-heavy day: keep image/upscale tasks conservative until CPU average falls below 65%."
    else:
        recommendation = "Cool-day schedule: conservative heavy work is acceptable during daytime if CPU/memory stay stable."

    lines = [
        "# Thermal Efficiency Report",
        "",
        f"- generated_at_et: {now.isoformat(timespec='seconds')}",
        f"- location_basis: Lincoln Park / Jersey City, NJ",
        f"- ambient_current_f: {current_f}",
        f"- ambient_today_high_f: {high_f}",
        f"- heavy_allowed_now_by_weather: {heavy_allowed_now}",
        f"- next_cool_heavy_window_et: {next_cool}",
        f"- samples_48h: {len(rows)}",
        f"- avg_cpu_pct_48h: {avg(cpus)}",
        f"- avg_memory_pct_48h: {avg(mems)}",
        f"- decisions_48h: RUN={run}, RUN_CONSERVATIVE={conservative}, DEFER_TO_NIGHT={deferred}, PAUSE_COOLDOWN={hot_pause}",
        f"- last_allocator_decision: {state.get('last_decision', '')}",
        f"- last_allocator_reason: {state.get('last_reason', '')}",
        "",
        "## Window Counts",
    ]
    for window, decision_counts in sorted(counts.items()):
        detail = ", ".join(f"{k}={v}" for k, v in sorted(decision_counts.items()))
        lines.append(f"- {window}: {detail}")
    lines += ["", "## Recommendation", f"- {recommendation}", ""]
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"{recommendation} Report: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
