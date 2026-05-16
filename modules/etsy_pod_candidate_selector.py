"""Select the next Etsy POD candidates from the local launch plan.

This is a local-only step. It does not call Etsy, eBay, Printify, or spend fees.
It exists so the monthly loop can continue real product work after the previous
POD ready queue is exhausted or held by mockup/reconcile guards.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"

LAUNCH_PLAN = DATABASE / "Etsy_launch_plan.csv"
LAUNCH_LOG = DATABASE / "Etsy_Printify_Launch_Log.csv"
OUTPUT = DATABASE / "Etsy_POD_Next_Batch_Candidates.csv"
REPORT = REVIEW / "ETSY_POD_NEXT_BATCH_CANDIDATES.md"

SUPPORTED_TYPES = {"Poster", "Acrylic"}
HANDLED_STATUSES = {
    "PUBLISHED",
    "PUBLISHED_EXTERNAL_PENDING",
    "PUBLISHED_EXTERNAL_CONFIRMED",
    "EXTERNAL_STILL_PENDING_NEEDS_RECONCILE",
    "HOLD_DUPLICATE_MOCKUPS",
    "HOLD_MOCKUP_INSUFFICIENT",
    "FAILED",
}

HIGH_INTENT_TERMS = {
    "quiet luxury": 16,
    "reading nook": 14,
    "deep work": 14,
    "apartment": 10,
    "collector": 10,
    "study": 8,
    "desk": 8,
    "shelf": 8,
    "jade": 8,
    "dark academia": 8,
    "wabi sabi": 8,
    "zen": 6,
    "wall art": 6,
    "gallery": 6,
}


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def et_now() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def mockup_count(source_status: str) -> int:
    match = re.search(r"Mockups(\d+)", source_status or "")
    return int(match.group(1)) if match else 0


def file_exists(path_text: str) -> bool:
    text = clean(path_text)
    return bool(text) and Path(text).exists()


def gallery_count(row: dict[str, str]) -> int:
    return sum(1 for i in range(1, 5) if file_exists(clean(row.get(f"Gallery_U{i}_Path"))))


def latest_log_by_id() -> dict[str, dict[str, str]]:
    latest: dict[str, dict[str, str]] = {}
    for row in read_csv(LAUNCH_LOG):
        item_id = clean(row.get("ID"))
        if item_id:
            latest[item_id] = row
    return latest


def score_row(row: dict[str, str]) -> tuple[int, list[str]]:
    notes: list[str] = []
    score = 0
    product_type = clean(row.get("Product_Type"))
    source_status = clean(row.get("Source_Status"))
    title = clean(row.get("Etsy_Title")).lower()
    tags = clean(row.get("Etsy_Tags")).lower()
    text = f"{title} {tags}"
    count = mockup_count(source_status)
    galleries = gallery_count(row)

    if product_type == "Acrylic":
        score += 26
        notes.append("acrylic_high_margin")
    elif product_type == "Poster":
        score += 18
        notes.append("poster_mid_tier")

    if count >= 8:
        score += 42
        notes.append("official_mockups_8")
    elif count >= 6:
        score += 30
        notes.append("official_mockups_6")
    elif count >= 4:
        score += 16
        notes.append("official_mockups_4")
    else:
        score -= 80
        notes.append("mockup_count_low")

    score += galleries * 6
    if galleries >= 3:
        notes.append(f"gallery_assets_{galleries}")
    else:
        notes.append(f"gallery_assets_low_{galleries}")

    for term, weight in HIGH_INTENT_TERMS.items():
        if term in text:
            score += weight
            notes.append(f"intent:{term}")

    title_len = len(clean(row.get("Etsy_Title")))
    if 70 <= title_len <= 140:
        score += 8
        notes.append("title_length_ok")
    else:
        score -= 10
        notes.append(f"title_length_{title_len}")

    if not file_exists(clean(row.get("Production_Path"))):
        score -= 100
        notes.append("production_missing")
    if not file_exists(clean(row.get("Cover_Path"))):
        score -= 100
        notes.append("cover_missing")

    return score, notes


def select_candidates(limit: int) -> tuple[list[dict[str, str]], dict[str, int]]:
    plan_rows = read_csv(LAUNCH_PLAN)
    latest_logs = latest_log_by_id()
    excluded: Counter = Counter()
    scored: list[tuple[int, dict[str, str], list[str]]] = []

    for row in plan_rows:
        item_id = clean(row.get("ID"))
        product_type = clean(row.get("Product_Type"))
        launch_status = clean(row.get("Launch_Status"))
        source_status = clean(row.get("Source_Status"))
        latest_status = clean(latest_logs.get(item_id, {}).get("Status"))

        if not item_id:
            excluded["missing_id"] += 1
            continue
        if product_type not in SUPPORTED_TYPES:
            excluded["unsupported_or_sticker"] += 1
            continue
        if latest_status in HANDLED_STATUSES:
            excluded[f"handled_{latest_status}"] += 1
            continue
        if not launch_status.startswith("Draft_Prepared"):
            excluded["not_draft_prepared"] += 1
            continue
        if mockup_count(source_status) < 4:
            excluded["mockup_count_below_4"] += 1
            continue

        score, notes = score_row(row)
        if score < 35:
            excluded["score_below_floor"] += 1
            continue
        scored.append((score, row, notes))

    scored.sort(key=lambda item: item[0], reverse=True)

    # Keep the first wave mixed enough to learn, while still favoring quality.
    selected: list[tuple[int, dict[str, str], list[str]]] = []
    by_type: defaultdict[str, int] = defaultdict(int)
    for item in scored:
        product_type = clean(item[1].get("Product_Type"))
        if limit >= 4 and by_type[product_type] >= max(2, limit - 3):
            continue
        selected.append(item)
        by_type[product_type] += 1
        if len(selected) >= limit:
            break

    if len(selected) < limit:
        selected_ids = {clean(row.get("ID")) for _, row, _ in selected}
        for item in scored:
            if clean(item[1].get("ID")) in selected_ids:
                continue
            selected.append(item)
            if len(selected) >= limit:
                break

    rows: list[dict[str, str]] = []
    for score, row, notes in selected:
        rows.append(
            {
                "ID": clean(row.get("ID")),
                "Product_Type": clean(row.get("Product_Type")),
                "Category": clean(row.get("Category")),
                "Etsy_Title": clean(row.get("Etsy_Title")),
                "Price": clean(row.get("Price")),
                "Source_Status": clean(row.get("Source_Status")),
                "Launch_Status": clean(row.get("Launch_Status")),
                "_score": str(score),
                "_gallery_count": str(gallery_count(row)),
                "Production_Path": clean(row.get("Production_Path")),
                "Cover_Path": clean(row.get("Cover_Path")),
                "Etsy_Tags": clean(row.get("Etsy_Tags")),
                "Selection_Rationale": "; ".join(notes[:18]),
            }
        )
    return rows, dict(excluded)


def run(limit: int) -> None:
    rows, excluded = select_candidates(limit)
    fields = [
        "ID",
        "Product_Type",
        "Category",
        "Etsy_Title",
        "Price",
        "Source_Status",
        "Launch_Status",
        "_score",
        "_gallery_count",
        "Production_Path",
        "Cover_Path",
        "Etsy_Tags",
        "Selection_Rationale",
    ]
    write_csv(OUTPUT, rows, fields)
    by_type = Counter(row["Product_Type"] for row in rows)
    lines = [
        "# Etsy POD Next Batch Candidates",
        "",
        f"Generated: {et_now()}",
        f"Selected: {len(rows)}",
        f"Selected by type: {dict(by_type)}",
        f"Excluded summary: {excluded}",
        "",
        "Policy: local-only candidate selection. No Etsy/Printify publish and no fee spend.",
        "",
        "## Selected",
        "",
    ]
    if rows:
        for row in rows:
            lines.append(
                f"- {row['ID']} | {row['Product_Type']} | score {row['_score']} | "
                f"{row['Source_Status']} | galleries {row['_gallery_count']} | {row['Etsy_Title'][:110]}"
            )
    else:
        lines.append("- None. The selector found no unhandled Poster/Acrylic rows above the quality floor.")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Etsy POD selector: selected={len(rows)} by_type={dict(by_type)}")
    print(f"excluded={excluded}")
    print(f"output={OUTPUT}")
    print(f"report={REPORT}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    run(max(1, args.limit))


if __name__ == "__main__":
    main()
