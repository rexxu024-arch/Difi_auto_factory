"""Summarize eBay traffic experiment groups from the latest performance snapshot."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
EXPERIMENT_CSV = DATABASE_DIR / "eBay_Traffic_Experiment.csv"
PERFORMANCE_CSV = DATABASE_DIR / "Performance_Log.csv"
OUTPUT_CSV = DATABASE_DIR / "eBay_Traffic_Experiment_Report.csv"
OUTPUT_MD = DATABASE_DIR / "eBay_Traffic_Experiment_Report.md"


def clean(value) -> str:
    return str(value or "").strip()


def load_experiment() -> list[dict]:
    with EXPERIMENT_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_latest_performance() -> tuple[str, dict[str, int]]:
    if not PERFORMANCE_CSV.exists():
        return "", {}
    with PERFORMANCE_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return "", {}
    latest = max(clean(row.get("Snapshot_Timestamp")) for row in rows)
    views = {}
    for row in rows:
        if clean(row.get("Snapshot_Timestamp")) != latest:
            continue
        item_id = clean(row.get("Item_ID"))
        if not item_id:
            continue
        raw = clean(row.get("Views_30_Days"))
        try:
            views[item_id] = int("".join(ch for ch in raw if ch.isdigit()) or "0")
        except ValueError:
            views[item_id] = 0
    return latest, views


def build() -> list[dict]:
    latest, views = load_latest_performance()
    rows = []
    for row in load_experiment():
        item_id = clean(row.get("eBay_Item_ID"))
        latest_views = views.get(item_id, 0)
        baseline = int(clean(row.get("Views_30_Days")) or "0")
        rows.append(
            {
                "Snapshot_Timestamp": latest,
                "ID": clean(row.get("ID")),
                "Group": clean(row.get("Group")),
                "eBay_Item_ID": item_id,
                "Baseline_Views_30_Days": baseline,
                "Latest_Views_30_Days": latest_views,
                "Delta": latest_views - baseline,
                "Action": clean(row.get("Action")),
            }
        )
    return rows


def write(rows: list[dict]) -> None:
    headers = [
        "Snapshot_Timestamp",
        "ID",
        "Group",
        "eBay_Item_ID",
        "Baseline_Views_30_Days",
        "Latest_Views_30_Days",
        "Delta",
        "Action",
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    groups = defaultdict(lambda: {"count": 0, "views": 0, "delta": 0, "moved": 0})
    for row in rows:
        g = groups[row["Group"]]
        g["count"] += 1
        g["views"] += int(row["Latest_Views_30_Days"])
        g["delta"] += int(row["Delta"])
        if int(row["Delta"]) > 0:
            g["moved"] += 1
    md = ["# eBay Traffic Experiment Report", ""]
    for group, data in sorted(groups.items()):
        md.extend(
            [
                f"## {group}",
                f"- Listings: {data['count']}",
                f"- Latest total views: {data['views']}",
                f"- Delta since baseline: {data['delta']}",
                f"- Listings with movement: {data['moved']}",
                "",
            ]
        )
    OUTPUT_MD.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    rows = build()
    write(rows)
    print(f"[EXPERIMENT-REPORT] rows={len(rows)} csv={OUTPUT_CSV}")


if __name__ == "__main__":
    main()
