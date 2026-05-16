from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW_PACKETS = PROJECT_ROOT / "Review_Packets"


def now_et() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def money(value: str) -> str:
    try:
        return f"${float(value):.2f}"
    except (TypeError, ValueError):
        return "$0.00"


def row_line(row: dict[str, str], zone: str) -> str:
    sku = row.get("Final_SKU") or row.get("SKU") or ""
    title = row.get("Printify_Title") or row.get("Concept_Name") or ""
    vector = row.get("Product_Vector") or ""
    pid = row.get("Printify_Product_ID") or ""
    rrp = money(row.get("RRP_USD") or "")
    status = row.get("Draft_Status") or row.get("Final_Status") or ""
    return f"| {zone} | {sku} | {title} | {vector} | {rrp} | {status} | {pid} |"


def build_report() -> str:
    zone2 = read_csv(DATABASE / "Shock_And_Awe_V5_Printify_Private_Drafts.csv")
    zones13 = read_csv(DATABASE / "Shock_And_Awe_V5_Zones1_3_Printify_Private_Drafts.csv")
    selection = read_csv(DATABASE / "Shock_And_Awe_V5_Zones1_3_Final_Selection.csv")
    report_time = now_et().strftime("%Y-%m-%d %H:%M:%S %z")

    all_drafts = zone2 + zones13
    draft_count = sum(1 for row in all_drafts if row.get("Draft_Status") == "PRINTIFY_DRAFT_CREATED")
    vector_counts = Counter(row.get("Product_Vector") or "UNKNOWN" for row in all_drafts)
    hold_rows = [row for row in selection if str(row.get("Final_Status") or "").startswith("HOLD")]

    lines = [
        "# Shock & Awe Private Showcase Status",
        "",
        f"Generated: {report_time} America/New_York",
        "",
        "## Executive Snapshot",
        "",
        f"- Private Printify drafts: {draft_count}/30",
        f"- Zone 2 drafts: {sum(1 for row in zone2 if row.get('Draft_Status') == 'PRINTIFY_DRAFT_CREATED')}/10",
        f"- Zone 1/3 drafts: {sum(1 for row in zones13 if row.get('Draft_Status') == 'PRINTIFY_DRAFT_CREATED')}/20",
        f"- Remaining holds: {len(hold_rows)}/30",
        "- Publish policy: PRIVATE_DRAFT_ONLY_DO_NOT_PUBLISH",
        "- MJ payment status: cleared by Rex; remaining MJ gaps are submission/session/payload issues, not billing.",
        "",
        "## Product Mix",
        "",
    ]
    for vector, count in sorted(vector_counts.items()):
        lines.append(f"- {vector}: {count}")

    lines.extend(
        [
            "",
            "## Draft Inventory",
            "",
            "| Zone | SKU | Title | Product Vector | RRP | Status | Printify Product ID |",
            "|---|---|---|---|---:|---|---|",
        ]
    )
    for row in zone2:
        lines.append(row_line(row, "Zone2"))
    for row in zones13:
        lines.append(row_line(row, "Zone1/3"))

    lines.extend(
        [
            "",
            "## Holds",
            "",
        ]
    )
    if not hold_rows:
        lines.append("- None.")
    else:
        for row in hold_rows:
            lines.append(
                f"- {row.get('Final_SKU')}: {row.get('Final_Status')} - {row.get('QA_Note')}"
            )

    lines.extend(
        [
            "",
            "## Next Safe Actions",
            "",
            "1. Replace 4 ghosted MJ submissions through a verified browser/UI Midjourney path or fresh Discord session capture.",
            "2. Reprompt 2 redline concepts as still-life/object designs only.",
            "3. After visual QA, create the final 6 private Printify drafts and regenerate this report.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    REVIEW_PACKETS.mkdir(parents=True, exist_ok=True)
    report = build_report()
    latest = REVIEW_PACKETS / "OPERATION_SHOCK_AND_AWE_PRIVATE_SHOWCASE_STATUS_latest.md"
    stamped = REVIEW_PACKETS / f"OPERATION_SHOCK_AND_AWE_PRIVATE_SHOWCASE_STATUS_{now_et():%Y%m%d_%H%M%S}.md"
    latest.write_text(report, encoding="utf-8")
    stamped.write_text(report, encoding="utf-8")
    print(latest)


if __name__ == "__main__":
    main()
