from __future__ import annotations

import csv
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
BATCH = DATABASE / "Multi_Track_Copy_Batch.csv"
PERFORMANCE = DATABASE / "Performance_Log.csv"
OUT_CSV = DATABASE / "Multi_Track_Copy_Performance_Monitor.csv"
OUT_MD = REVIEW / f"MULTI_TRACK_COPY_MONITOR_{datetime.now():%Y%m%d}.md"
NY = ZoneInfo("America/New_York")


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        return list(csv.DictReader(handle))


def as_int(value: object) -> int | None:
    text = re.sub(r"[^0-9-]", "", clean(value))
    if text in {"", "-"}:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def latest_performance() -> dict[str, dict[str, str]]:
    by_item: dict[str, dict[str, str]] = {}
    for row in read_csv(PERFORMANCE):
        item_id = clean(row.get("Item_ID"))
        if item_id:
            by_item[item_id] = row
    return by_item


def build_rows() -> list[dict[str, str]]:
    performance = latest_performance()
    rows = []
    for batch in read_csv(BATCH):
        item_id = clean(batch.get("eBay_Item_ID"))
        perf = performance.get(item_id, {})
        latest_views = as_int(perf.get("Views_30_Days"))
        rows.append(
            {
                "Timestamp": datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S %z"),
                "ID": clean(batch.get("ID")),
                "Product_Type": clean(batch.get("Product_Type")),
                "Track": clean(batch.get("Track")),
                "Primary_Intent": clean(batch.get("Primary_Intent")),
                "Mockup_Mood": clean(batch.get("Mockup_Mood")),
                "eBay_Item_ID": item_id,
                "Apply_Status": clean(batch.get("Apply_Status")),
                "Sync_Result": clean(batch.get("Sync_Result")),
                "New_Title": clean(batch.get("New_Title")),
                "Latest_Views_30d": "" if latest_views is None else str(latest_views),
                "Latest_General_Status": clean(perf.get("General_Status")),
                "Latest_Priority_Status": clean(perf.get("Priority_Status")),
                "Read_Status": clean(perf.get("Read_Status")),
                "Monitor_Action": action(latest_views, batch, perf),
            }
        )
    return rows


def action(latest_views: int | None, batch: dict[str, str], perf: dict[str, str]) -> str:
    if clean(batch.get("Sync_Result")) != "OK":
        return "RECONCILE_SYNC_BEFORE_JUDGING_TRAFFIC"
    if not perf:
        return "WAIT_FOR_NEXT_SELLER_HUB_READ"
    if latest_views is None:
        return "READBACK_MISSING_VIEWS"
    if latest_views == 0:
        return "ZERO_VIEW_WAIT_48H_THEN_DOWNGRADE_OR_TRACK_C"
    if latest_views <= 2:
        return "NONZERO_TRAFFIC_MONITOR_CLICK_SIGNAL"
    return "HAS_TRAFFIC_CONSIDER_VARIATION"


def write_outputs(rows: list[dict[str, str]]) -> None:
    headers = [
        "Timestamp",
        "ID",
        "Product_Type",
        "Track",
        "Primary_Intent",
        "Mockup_Mood",
        "eBay_Item_ID",
        "Apply_Status",
        "Sync_Result",
        "New_Title",
        "Latest_Views_30d",
        "Latest_General_Status",
        "Latest_Priority_Status",
        "Read_Status",
        "Monitor_Action",
    ]
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    counts = defaultdict(int)
    for row in rows:
        counts[row["Monitor_Action"]] += 1
    lines = [
        "# Multi-Track Copy Monitor",
        "",
        f"Generated: {datetime.now(NY).strftime('%Y-%m-%d %H:%M:%S %z')}",
        "",
        "## Action Counts",
        "",
    ]
    for key, value in sorted(counts.items()):
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Rows", "", "| ID | Intent | Views | Action |", "|---|---|---:|---|"])
    for row in rows:
        lines.append(f"| {row['ID']} | {row['Primary_Intent']} | {row['Latest_Views_30d'] or 'n/a'} | {row['Monitor_Action']} |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_outputs(rows)
    print(f"[MULTI-MONITOR] rows={len(rows)} csv={OUT_CSV} report={OUT_MD}")


if __name__ == "__main__":
    main()
