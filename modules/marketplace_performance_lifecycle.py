"""Build a safe marketplace performance lifecycle report.

This is read-only. It turns existing Etsy/eBay snapshots into concrete
scale/hold/repair/retire candidates without touching marketplace state.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REPORTS = PROJECT_ROOT / "Reports"
REVIEW = PROJECT_ROOT / "Review_Packets"
GEMINI = REVIEW / "Gemini_Bridge"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

EBAY_EXPERIMENT = DATABASE / "eBay_Traffic_Experiment_Report.csv"
EBAY_DIAGNOSIS = DATABASE / "eBay_Traffic_Diagnosis.csv"
ETSY_LIVE = DATABASE / "Etsy_Digital_Live_Audit.csv"
ETSY_POD_LOG = DATABASE / "Etsy_Printify_Launch_Log.csv"
ETSY_FEE = DATABASE / "Etsy_Fee_Ledger.csv"

OUT_CSV = DATABASE / "Marketplace_Performance_Lifecycle.csv"
OUT_MD = REPORTS / "Marketplace_Performance_Lifecycle.md"
GEMINI_MD = GEMINI / "MARKETPLACE_PERFORMANCE_LIFECYCLE_latest.md"

FIELDS = [
    "Platform",
    "Item_ID",
    "Title",
    "Product_Type",
    "Signal_Summary",
    "Action",
    "Priority",
    "Rationale",
    "Next_Safe_Step",
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\n", " ").replace("\r", " ").split()).strip()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def to_int(value: object) -> int:
    try:
        return int(float(clean(value) or "0"))
    except ValueError:
        return 0


def price_float(value: object) -> float:
    raw = clean(value).replace("$", "").replace(",", "")
    try:
        return float(raw)
    except ValueError:
        return 0.0


def product_type_from_id(item_id: str, title: str = "") -> str:
    blob = f"{item_id} {title}".lower()
    if "acrylic" in blob:
        return "Acrylic"
    if "poster" in blob or "print" in blob:
        return "Poster"
    if "sticker" in blob:
        return "Sticker"
    if "digital" in blob or "download" in blob:
        return "Digital"
    return "Unknown"


def ebay_rows() -> tuple[list[dict[str, str]], dict[str, int], list[str]]:
    rows: list[dict[str, str]] = []
    group_stats: dict[str, dict[str, int]] = defaultdict(lambda: {"rows": 0, "views": 0, "moved": 0})
    for row in read_rows(EBAY_EXPERIMENT):
        item_id = clean(row.get("ID"))
        latest = to_int(row.get("Latest_Views_30_Days"))
        delta = to_int(row.get("Delta"))
        group = clean(row.get("Group")) or "UNKNOWN"
        product = product_type_from_id(item_id)
        group_stats[group]["rows"] += 1
        group_stats[group]["views"] += latest
        group_stats[group]["moved"] += 1 if delta > 0 else 0
        if delta >= 2:
            action = "SCALE_DNA_VARIATION"
            priority = "80"
            step = "Clone buyer-intent title angle into 2-3 Poster/Acrylic variants after cost and gallery QA."
            rationale = "This listing moved above baseline while most eBay tests remained flat."
        elif latest == 0 and delta == 0:
            action = "HOLD_OR_RETIRE_AFTER_WINDOW"
            priority = "55"
            step = "Do not rewrite daily; keep in loser queue and retire/replace if still flat after the measurement window."
            rationale = "Zero views and no movement; likely weak buyer intent or weak product-market fit."
        else:
            action = "MONITOR"
            priority = "60"
            step = "Let the experiment run; avoid churn until 48-72h readback."
            rationale = "Some visibility exists but not enough to call a winner."
        rows.append(
            {
                "Platform": "eBay",
                "Item_ID": item_id,
                "Title": "",
                "Product_Type": product,
                "Signal_Summary": f"group={group}; latest_views_30d={latest}; delta={delta}",
                "Action": action,
                "Priority": priority,
                "Rationale": rationale,
                "Next_Safe_Step": step,
            }
        )
    flat_stats = {key: value["moved"] for key, value in group_stats.items()}
    summary = [
        f"{group}: rows={stats['rows']} views={stats['views']} moved={stats['moved']}"
        for group, stats in sorted(group_stats.items())
    ]
    return rows, flat_stats, summary


def etsy_rows() -> tuple[list[dict[str, str]], list[str]]:
    rows: list[dict[str, str]] = []
    live = read_rows(ETSY_LIVE)
    latest_by_listing: dict[str, dict[str, str]] = {}
    for row in live:
        listing_id = clean(row.get("Etsy_Listing_ID"))
        if listing_id:
            latest_by_listing[listing_id] = row
    status_counts = Counter(clean(row.get("Status")) for row in latest_by_listing.values())
    digital_count = sum(1 for row in latest_by_listing.values() if clean(row.get("Digital_Signal")).upper() == "YES")
    physical_count = len(latest_by_listing) - digital_count

    for row in latest_by_listing.values():
        title = clean(row.get("Title"))
        listing_id = clean(row.get("Etsy_Listing_ID"))
        image_count = to_int(row.get("Image_Count"))
        price = price_float(row.get("Price_Text"))
        digital = clean(row.get("Digital_Signal")).upper() == "YES"
        product = product_type_from_id(clean(row.get("ID")), title)
        if digital and price < 15:
            action = "KEEP_AS_LIMITED_SENSOR_OR_RETIRE"
            priority = "45"
            step = "Do not expand low-price digital volume until real views/favorites/orders are captured."
            rationale = "Etsy active data is readable, but local snapshot lacks conversion counters; low-price digital should not dominate."
        elif image_count < 5:
            action = "REPAIR_PHOTO_STACK"
            priority = "65"
            step = "Add/verify at least 5 useful images before expecting search lift."
            rationale = "Etsy seller UI flagged photo count as a visibility factor; weak image stack suppresses listing quality."
        else:
            action = "MONITOR_NEEDS_TRAFFIC_COUNTERS"
            priority = "50"
            step = "Fetch Etsy stats/favorites/orders before scale/retire decisions."
            rationale = "Listing shell is readable, but performance counters are not yet structured locally."
        rows.append(
            {
                "Platform": "Etsy",
                "Item_ID": listing_id,
                "Title": title[:120],
                "Product_Type": product,
                "Signal_Summary": f"status={clean(row.get('Status'))}; price={clean(row.get('Price_Text'))}; digital={digital}; images={image_count}",
                "Action": action,
                "Priority": priority,
                "Rationale": rationale,
                "Next_Safe_Step": step,
            }
        )
    summary = [
        f"readable_listings={len(latest_by_listing)}",
        f"digital={digital_count}",
        f"physical_or_unknown={physical_count}",
        f"statuses={dict(status_counts)}",
    ]
    return rows, summary


def pod_summary() -> list[str]:
    rows = read_rows(ETSY_POD_LOG)
    status_counts = Counter(clean(row.get("Status")) for row in rows)
    published = [row for row in rows if clean(row.get("External_ID"))]
    return [
        f"printify_log_rows={len(rows)}",
        f"external_id_rows={len(published)}",
        f"status_counts={dict(status_counts.most_common(8))}",
    ]


def fee_summary() -> list[str]:
    spent = 0.0
    rows = read_rows(ETSY_FEE)
    for row in rows:
        if clean(row.get("Status")).upper().startswith(("CONFIRMED", "ADOBE")) or clean(row.get("Confirmed_Spent_USD")):
            spent += price_float(row.get("Confirmed_Spent_USD"))
    return [f"etsy_fee_rows={len(rows)}", f"confirmed_spend_approx=${spent:.2f}"]


def write_report(rows: list[dict[str, str]], ebay_summary: list[str], etsy_summary: list[str]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    GEMINI.mkdir(parents=True, exist_ok=True)
    by_action = Counter(row["Action"] for row in rows)
    top = sorted(rows, key=lambda row: int(row.get("Priority") or "0"), reverse=True)[:20]
    lines = [
        "# Marketplace Performance Lifecycle",
        "",
        f"Generated: {now_text()}",
        "",
        "## Executive Read",
        "",
        "- This is read-only: no listing edits, deletes, spend, or publish actions.",
        "- eBay has enough local traffic data to rank weak/winner groups.",
        "- Etsy currently needs structured stats/favorites/orders ingestion before automatic scale/retire.",
        "- Near-term public-market product mix should stay tilted toward high-quality POD Poster/Acrylic, while Adobe remains the 3-day P0.",
        "",
        "## eBay Signal",
        "",
    ]
    lines.extend(f"- {item}" for item in ebay_summary)
    lines.extend(["", "## Etsy Signal", ""])
    lines.extend(f"- {item}" for item in etsy_summary)
    lines.extend(f"- {item}" for item in pod_summary())
    lines.extend(f"- {item}" for item in fee_summary())
    lines.extend(["", "## Action Mix", ""])
    lines.extend(f"- {action}: {count}" for action, count in by_action.most_common())
    lines.extend(["", "## Highest Priority Candidates", ""])
    for row in top:
        lines.append(
            f"- P{row['Priority']} {row['Platform']} {row['Item_ID']} [{row['Product_Type']}] "
            f"=> {row['Action']}: {row['Signal_Summary']} | {row['Next_Safe_Step']}"
        )
    lines.extend(
        [
            "",
            "## Next Engineering Step",
            "",
            "1. Add official Etsy stats/favorites/orders readback or a safe Seller UI export parser.",
            "2. Add eBay item-level active listing join so Printify-origin live items can be safely matched to traffic.",
            "3. Convert this report into a daily queue: scale winners, repair photo/title candidates, and retire losers after the measurement window.",
        ]
    )
    text = "\n".join(lines) + "\n"
    OUT_MD.write_text(text, encoding="utf-8")
    GEMINI_MD.write_text(text, encoding="utf-8")


def append_progress(total_rows: int) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Marketplace performance lifecycle report rebuilt; "
            f"read_only_candidates={total_rows}; outputs={OUT_CSV.relative_to(PROJECT_ROOT)}, {OUT_MD.relative_to(PROJECT_ROOT)}.\n"
        )


def main() -> int:
    ebay, _flat, ebay_summary = ebay_rows()
    etsy, etsy_summary = etsy_rows()
    rows = sorted(ebay + etsy, key=lambda row: int(row.get("Priority") or "0"), reverse=True)
    write_csv(OUT_CSV, rows)
    write_report(rows, ebay_summary, etsy_summary)
    append_progress(len(rows))
    print(f"[MARKETPLACE-LIFECYCLE] candidates={len(rows)} csv={OUT_CSV} report={OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
