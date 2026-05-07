from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.etsy_digital_gray_launch import qa_zip


DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
METADATA_PATH = DATABASE / "Digital_Etsy_Metadata.csv"
PLAN_PATH = DATABASE / "Multi_Track_Experiment_Plan.csv"
OUTPUT_CSV = DATABASE / "Etsy_Digital_Next_Batch_Candidates.csv"
OUTPUT_STATE = DATABASE / "Etsy_Digital_Next_Batch_State.json"
OUTPUT_REPORT = REVIEW / "ETSY_DIGITAL_NEXT_BATCH_CANDIDATES.md"
NY = ZoneInfo("America/New_York")


FIELDS = [
    "Timestamp",
    "Rank",
    "ID",
    "Title",
    "Price",
    "SEO_Mode",
    "Primary_Search_Intent",
    "Secondary_Keywords",
    "Zip_MB",
    "Image_Count",
    "Readme_Present",
    "QA_Status",
    "QA_Reason",
    "Decision",
]


def now_text() -> str:
    return datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S %z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\n", " ").replace("\r", " ").split())


def plan_by_id() -> dict[str, dict[str, str]]:
    result = {}
    for row in read_csv(PLAN_PATH):
        if row.get("Track") != "C_DIGITAL_PURE_PROFIT":
            continue
        result[clean(row.get("ID"))] = row
    return result


def score(row: dict[str, str], plan: dict[str, str]) -> tuple[int, str]:
    title = clean(row.get("Title")).lower()
    intent = clean(plan.get("Primary_Search_Intent")).lower()
    secondary = clean(plan.get("Secondary_Keywords")).lower()
    points = 0
    reasons: list[str] = []
    for token in ["reading nook", "study", "dark academia", "printable", "digital", "wall art"]:
        if token in title or token in intent or token in secondary:
            points += 4
            reasons.append(token)
    if "zen" in title or "meditation" in title or "meditation" in intent:
        points += 3
        reasons.append("zen/meditation")
    if "poster" in title:
        points += 2
    if "digital" in title and "download" in title:
        points += 3
    return points, ", ".join(reasons[:5])


def select(limit: int) -> dict[str, object]:
    plans = plan_by_id()
    rows = []
    for meta in read_csv(METADATA_PATH):
        if meta.get("Status") != "READY_FOR_ETSY_DRAFT":
            continue
        item_id = clean(meta.get("ID"))
        plan = plans.get(item_id, {})
        points, reason = score(meta, plan)
        rows.append((points, reason, meta, plan))
    rows.sort(key=lambda item: (-item[0], item[2].get("ID", "")))

    output: list[dict[str, object]] = []
    timestamp = now_text()
    for rank, (points, reason, meta, plan) in enumerate(rows[:limit], start=1):
        qa = qa_zip(meta)
        decision = "READY_FOR_NEXT_PAID_GRAY_BATCH" if qa.status.startswith("PASS") else "HOLD_QA"
        output.append(
            {
                "Timestamp": timestamp,
                "Rank": rank,
                "ID": meta.get("ID", ""),
                "Title": meta.get("Title", ""),
                "Price": meta.get("Price", ""),
                "SEO_Mode": plan.get("SEO_Mode", ""),
                "Primary_Search_Intent": plan.get("Primary_Search_Intent", reason),
                "Secondary_Keywords": plan.get("Secondary_Keywords", ""),
                "Zip_MB": f"{qa.zip_mb:.2f}",
                "Image_Count": qa.image_count,
                "Readme_Present": qa.readme_present,
                "QA_Status": qa.status,
                "QA_Reason": qa.reason,
                "Decision": decision,
            }
        )
    write_csv(OUTPUT_CSV, output, FIELDS)
    ready = sum(1 for row in output if row["Decision"] == "READY_FOR_NEXT_PAID_GRAY_BATCH")
    state = {
        "timestamp": timestamp,
        "selected": len(output),
        "ready": ready,
        "hold": len(output) - ready,
        "projected_fee_if_published_usd": round(ready * 0.20, 2),
        "spend_now": 0.0,
        "csv": str(OUTPUT_CSV),
        "report": str(OUTPUT_REPORT),
    }
    OUTPUT_STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    write_report(output, state)
    return state


def write_report(rows: list[dict[str, object]], state: dict[str, object]) -> None:
    REVIEW.mkdir(exist_ok=True)
    lines = [
        "# Etsy Digital Next Batch Candidates",
        "",
        f"Generated: {state['timestamp']}",
        "",
        "This is a no-spend selector. It does not reserve or publish Etsy listings.",
        "",
        f"- Selected: {state['selected']}",
        f"- Ready: {state['ready']}",
        f"- Hold: {state['hold']}",
        f"- Projected fee if published later: ${state['projected_fee_if_published_usd']:.2f}",
        "",
        "| Rank | ID | QA | Intent | Decision |",
        "|---:|---|---|---|---|",
    ]
    for row in rows:
        intent = clean(row.get("Primary_Search_Intent"))[:46]
        lines.append(f"| {row['Rank']} | {row['ID']} | {row['QA_Status']} | {intent} | {row['Decision']} |")
    OUTPUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Select the next Etsy Digital gray batch without fee reservation.")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    state = select(limit=args.limit)
    if args.json:
        print(json.dumps(state, indent=2, ensure_ascii=False))
    else:
        print(f"[ETSY-NEXT] selected={state['selected']} ready={state['ready']} csv={OUTPUT_CSV}")


if __name__ == "__main__":
    main()
