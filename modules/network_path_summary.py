"""Summarize Ethernet stability samples for Rex's adapter decision."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REPORTS = PROJECT_ROOT / "Reports"
LOG_PATH = DATABASE / "Network_Path_Monitor.csv"
CONFIG_PATH = DATABASE / "Network_Path_Sampling_Config.json"
REPORT_PATH = REPORTS / "Network_Path_48h_Sampling_Report.md"
NY_TZ = ZoneInfo("America/New_York")


def read_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def parse_dt(text: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=NY_TZ)
        return parsed.astimezone(NY_TZ)
    except Exception:
        return None


def read_rows() -> list[dict[str, str]]:
    if not LOG_PATH.exists():
        return []
    with LOG_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def summarize(expected_alias: str = "Ethernet 3") -> dict:
    config = read_config()
    start = parse_dt(str(config.get("started_at") or ""))
    end = parse_dt(str(config.get("ends_at") or ""))
    rows = []
    for row in read_rows():
        ts = parse_dt(row.get("timestamp", ""))
        if not ts:
            continue
        if start and ts < start:
            continue
        if end and ts > end:
            continue
        row["_dt"] = ts.isoformat(timespec="seconds")
        rows.append(row)

    aliases = Counter(row.get("active_alias") or "NONE" for row in rows)
    alerts = Counter(row.get("alert") or "" for row in rows if row.get("alert"))
    not_expected = [row for row in rows if (row.get("active_alias") or "") != expected_alias]
    eth_not_up = [
        row
        for row in rows
        if (row.get("ethernet_status") or "").lower() != "up"
        or (row.get("ethernet_link_speed") or "").strip().lower() not in {"1 gbps", "1000 mbps"}
    ]
    path_changes = 0
    previous = ""
    for row in rows:
        alias = row.get("active_alias") or ""
        if previous and alias and alias != previous:
            path_changes += 1
        if alias:
            previous = alias

    return {
        "generated_at": datetime.now(NY_TZ).isoformat(timespec="seconds"),
        "window_started_at": config.get("started_at", ""),
        "window_ends_at": config.get("ends_at", ""),
        "sampling_enabled": bool(config.get("enabled")),
        "expected_alias": expected_alias,
        "sample_count": len(rows),
        "active_alias_counts": dict(aliases),
        "alert_counts": dict(alerts),
        "not_expected_count": len(not_expected),
        "ethernet_not_up_or_not_gigabit_count": len(eth_not_up),
        "path_change_count": path_changes,
        "first_sample": rows[0].get("_dt", "") if rows else "",
        "last_sample": rows[-1].get("_dt", "") if rows else "",
        "recommendation": recommendation(len(rows), len(not_expected), len(eth_not_up), path_changes),
    }


def recommendation(samples: int, not_expected: int, eth_bad: int, path_changes: int) -> str:
    if samples < 12:
        return "Too early. Keep sampling before buying hardware."
    bad = max(not_expected, eth_bad)
    ratio = bad / max(1, samples)
    if ratio >= 0.05 or path_changes >= 3:
        return "Likely adapter/cable/path instability. Buying a better Ethernet adapter or cable is justified."
    if ratio > 0 or path_changes:
        return "Minor instability observed. Continue sampling; replace adapter if repeats during work windows."
    return "Ethernet path appears stable so far. No adapter replacement justified yet."


def write_report(summary: dict) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Network Path 48h Sampling Report",
        "",
        f"Generated: {summary['generated_at']}",
        f"Window: {summary['window_started_at']} -> {summary['window_ends_at']}",
        f"Expected path: {summary['expected_alias']}",
        "",
        "## Counters",
        f"- Samples: {summary['sample_count']}",
        f"- Active alias counts: {summary['active_alias_counts']}",
        f"- Alerts: {summary['alert_counts']}",
        f"- Not expected path count: {summary['not_expected_count']}",
        f"- Ethernet not up / not gigabit count: {summary['ethernet_not_up_or_not_gigabit_count']}",
        f"- Path changes: {summary['path_change_count']}",
        "",
        "## Decision",
        summary["recommendation"],
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize OpenClaw network path samples.")
    parser.add_argument("--expected-alias", default="Ethernet 3")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    summary = summarize(args.expected_alias)
    write_report(summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2) if args.json else summary["recommendation"])


if __name__ == "__main__":
    main()
