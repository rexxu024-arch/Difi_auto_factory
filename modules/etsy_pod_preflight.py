"""Preflight Etsy POD candidates before paid/API launch.

This selects high-quality Printify-backed physical products for Etsy while
keeping Digital as a limited sensing pool. It is read-only against marketplaces:
no product creation, no publishing, and no fees.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.risk_guard import RiskBlocked, assert_no_first_audit_public_assets


DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
INPUT = DATABASE / "Etsy_POD_Next_Batch_Candidates.csv"
QA_CSV = DATABASE / "Etsy_POD_Preflight_QA.csv"
READY_CSV = DATABASE / "Etsy_POD_Printify_Launch_Ready.csv"
READY_FULL_CSV = DATABASE / "Etsy_POD_Printify_Launch_Ready_Full.csv"
LAUNCH_PLAN = DATABASE / "Etsy_launch_plan.csv"
LAUNCH_LOG = DATABASE / "Etsy_Printify_Launch_Log.csv"
REPORT = REVIEW / "ETSY_POD_PREFLIGHT_QA.md"

PRODUCT_COSTS = {
    # Printify catalog truth captured earlier in project notes.
    "poster": {"product": 6.00, "shipping": 5.99, "min_long_edge": 3000, "target_price": 34.99},
    "acrylic": {"product": 35.43, "shipping": 15.99, "min_long_edge": 1500, "target_price": 89.99},
}

ETSY_LISTING_FEE = 0.20
ETSY_TRANSACTION_RATE = 0.065
PAYMENT_RATE = 0.03
PAYMENT_FIXED = 0.25
TEST_AD_RATE = 0.12
MIN_MARGIN = {
    "poster": 8.00,
    "acrylic": 18.00,
}


@dataclass
class ImageInfo:
    exists: bool
    width: int = 0
    height: int = 0
    mode: str = ""
    error: str = ""


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def money(value: object) -> float:
    match = re.search(r"\d+(?:\.\d{1,2})?", clean(value))
    return float(match.group(0)) if match else 0.0


def et_now() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def launched_ids() -> set[str]:
    if not LAUNCH_LOG.exists():
        return set()
    launched_statuses = {
        "CREATED",
        "PUBLISHED",
        "PUBLISHED_EXTERNAL_PENDING",
        "PUBLISHED_EXTERNAL_CONFIRMED",
    }
    ids: set[str] = set()
    for row in read_csv(LAUNCH_LOG):
        if clean(row.get("Status")) in launched_statuses:
            item_id = clean(row.get("ID"))
            if item_id:
                ids.add(item_id)
    return ids


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def image_info(path_text: str) -> ImageInfo:
    path = Path(path_text)
    if not path.exists():
        return ImageInfo(False, error="missing")
    try:
        with Image.open(path) as img:
            img.load()
            return ImageInfo(True, img.width, img.height, img.mode)
    except Exception as exc:  # noqa: BLE001
        return ImageInfo(False, error=str(exc)[:120])


def tags_ok(tags_text: str) -> tuple[bool, int, str]:
    tags = [tag.strip() for tag in tags_text.split(",") if tag.strip()]
    if not (8 <= len(tags) <= 13):
        return False, len(tags), f"tag_count={len(tags)}"
    too_long = [tag for tag in tags if len(tag) > 20]
    if too_long:
        return False, len(tags), f"tags_over_20={too_long[:3]}"
    return True, len(tags), "ok"


def estimate_margin(product_type: str, price: float) -> tuple[float, float]:
    costs = PRODUCT_COSTS[product_type]
    platform = price * (ETSY_TRANSACTION_RATE + PAYMENT_RATE + TEST_AD_RATE) + PAYMENT_FIXED + ETSY_LISTING_FEE
    total_cost = costs["product"] + costs["shipping"] + platform
    return price - total_cost, total_cost


def qa_row(row: dict[str, str]) -> dict[str, str]:
    product_type = clean(row.get("Product_Type")).lower()
    if product_type.startswith("poster"):
        product_type = "poster"
    elif product_type.startswith("acry"):
        product_type = "acrylic"
    else:
        product_type = "unsupported"

    result = {
        "ID": clean(row.get("ID")),
        "Product_Type": clean(row.get("Product_Type")),
        "Category": clean(row.get("Category")),
        "Price": clean(row.get("Price")),
        "Decision": "HOLD",
        "Reasons": "",
        "Recommended_Action": "",
        "Estimated_Total_Cost_USD": "",
        "Estimated_Margin_USD": "",
        "Title_Length": str(len(clean(row.get("Etsy_Title")))),
        "Tag_Count": "0",
        "Production_Size": "",
        "Cover_Size": "",
    }
    reasons: list[str] = []

    if product_type == "unsupported":
        reasons.append("unsupported_product_type")

    title = clean(row.get("Etsy_Title"))
    if not (70 <= len(title) <= 140):
        reasons.append(f"title_length={len(title)}")
    if len(set(title.lower().split())) < 7:
        reasons.append("title_too_repetitive")

    ok_tags, tag_count, tag_note = tags_ok(clean(row.get("Etsy_Tags")))
    result["Tag_Count"] = str(tag_count)
    if not ok_tags:
        reasons.append(tag_note)

    prod = image_info(clean(row.get("Production_Path")))
    cover = image_info(clean(row.get("Cover_Path")))
    result["Production_Size"] = f"{prod.width}x{prod.height}" if prod.exists else prod.error
    result["Cover_Size"] = f"{cover.width}x{cover.height}" if cover.exists else cover.error
    if not prod.exists:
        reasons.append("production_missing")
    if not cover.exists:
        reasons.append("cover_missing")
    if prod.exists and product_type in PRODUCT_COSTS:
        if max(prod.width, prod.height) < PRODUCT_COSTS[product_type]["min_long_edge"]:
            reasons.append("production_resolution_low")
    if cover.exists and min(cover.width, cover.height) < 900:
        reasons.append("cover_resolution_low")

    try:
        assert_no_first_audit_public_assets(row, context=f"Etsy POD preflight {result['ID']}")
    except RiskBlocked as exc:
        reasons.append(f"first_audit_blocked={exc}")

    price = money(row.get("Price"))
    if product_type in PRODUCT_COSTS:
        margin, total_cost = estimate_margin(product_type, price)
        result["Estimated_Total_Cost_USD"] = f"{total_cost:.2f}"
        result["Estimated_Margin_USD"] = f"{margin:.2f}"
        if margin < MIN_MARGIN[product_type]:
            reasons.append(f"margin_too_low={margin:.2f}")

    if reasons:
        result["Reasons"] = "; ".join(reasons)
        result["Recommended_Action"] = "repair_before_launch"
    else:
        result["Decision"] = "READY_FOR_SMALL_BATCH_POD_TEST"
        result["Recommended_Action"] = "eligible_for_1_to_3_item_drip_launch_after_account_guard"
    return result


def run(limit: int = 0) -> None:
    done_ids = launched_ids()
    rows = [row for row in read_csv(INPUT) if clean(row.get("ID")) not in done_ids]
    if limit:
        rows = rows[:limit]
    qa_rows = [qa_row(row) for row in rows]
    fields = [
        "ID",
        "Product_Type",
        "Category",
        "Price",
        "Decision",
        "Reasons",
        "Recommended_Action",
        "Estimated_Total_Cost_USD",
        "Estimated_Margin_USD",
        "Title_Length",
        "Tag_Count",
        "Production_Size",
        "Cover_Size",
    ]
    write_csv(QA_CSV, qa_rows, fields)
    ready_ids = {row["ID"] for row in qa_rows if row["Decision"] == "READY_FOR_SMALL_BATCH_POD_TEST"}
    ready_source = [row for row in rows if clean(row.get("ID")) in ready_ids]
    if ready_source:
        write_csv(READY_CSV, ready_source, list(ready_source[0].keys()))
    else:
        write_csv(READY_CSV, [], list(rows[0].keys()) if rows else ["ID"])

    launch_rows = read_csv(LAUNCH_PLAN) if LAUNCH_PLAN.exists() else []
    full_ready = [row for row in launch_rows if clean(row.get("ID")) in ready_ids]
    if full_ready:
        write_csv(READY_FULL_CSV, full_ready, list(full_ready[0].keys()))
    else:
        write_csv(READY_FULL_CSV, [], list(launch_rows[0].keys()) if launch_rows else ["ID"])

    ready_count = len(ready_source)
    hold_count = len(qa_rows) - ready_count
    by_type: dict[str, int] = {}
    for row in ready_source:
        by_type[clean(row.get("Product_Type"))] = by_type.get(clean(row.get("Product_Type")), 0) + 1

    lines = [
        "# Etsy POD Preflight QA",
        "",
        f"Generated: {et_now()}",
        f"Candidates checked: {len(qa_rows)}",
        f"Already launched/excluded: {len(done_ids)}",
        f"Ready for small-batch POD test: {ready_count}",
        f"Hold/repair: {hold_count}",
        f"Ready by type: {by_type}",
        "",
        "Policy: no marketplace write, no fee spend. Digital remains a limited sensing pool; Etsy physical expansion should favor QA-passed Printify-backed POD.",
        "",
        "## Ready Candidates",
        "",
    ]
    if ready_source:
        for row in ready_source[:20]:
            qa = next(q for q in qa_rows if q["ID"] == clean(row.get("ID")))
            lines.append(
                f"- {qa['ID']} ({qa['Product_Type']}) price {qa['Price']}, margin ${qa['Estimated_Margin_USD']}, title length {qa['Title_Length']}"
            )
    else:
        lines.append("- None.")
    lines.extend(["", "## Holds", ""])
    for qa in qa_rows:
        if qa["Decision"] != "READY_FOR_SMALL_BATCH_POD_TEST":
            lines.append(f"- {qa['ID']}: {qa['Reasons']}")
    lines.extend([
        "",
        "Outputs:",
        f"- {QA_CSV.relative_to(PROJECT_ROOT)}",
        f"- {READY_CSV.relative_to(PROJECT_ROOT)}",
        f"- {READY_FULL_CSV.relative_to(PROJECT_ROOT)}",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Etsy POD preflight: checked={len(qa_rows)} ready={ready_count} hold={hold_count}")
    print(f"qa={QA_CSV}")
    print(f"ready={READY_CSV}")
    print(f"ready_full={READY_FULL_CSV}")
    print(f"report={REPORT}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    run(args.limit)


if __name__ == "__main__":
    main()
