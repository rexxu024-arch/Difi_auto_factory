"""Build a product matrix from promoted Project Mirror DNA.

The matrix is a no-spend bridge between visual research and actual production:
it recommends carrier, blueprint, price lane, QA gate, and next action without
creating any Printify/Etsy/eBay product.
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
REVIEW_DIR = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"
SOURCE_CSV = DATABASE_DIR / "Project_Mirror_Promoted_DNA.csv"
OUT_CSV = DATABASE_DIR / "Project_Mirror_Product_Matrix.csv"
OUT_MD = REVIEW_DIR / "PROJECT_MIRROR_PRODUCT_MATRIX.md"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"

HEADERS = [
    "Rank",
    "Promoted_ID",
    "Pair_ID",
    "Title",
    "Carrier",
    "Blueprint_ID",
    "Provider_Preference",
    "Price_Lane",
    "Target_Retail",
    "Rationale",
    "Production_Status",
    "Next_Action",
]


def now_et() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def score_float(value: object) -> float:
    try:
        return float(clean(value))
    except ValueError:
        return 0.0


def carrier_for(row: dict[str, str], rank: int) -> tuple[str, str, str, str, str]:
    category = clean(row.get("Category"))
    score = score_float(row.get("Score"))
    product_fit = clean(row.get("Product_Fit"))

    if rank <= 3 or "Executive" in category:
        return (
            "Acrylic Block 5x7",
            "1471",
            "Printify acrylic photo block provider 104; vertical 5x7",
            "Core",
            "$128",
        )
    if "Poster" in product_fit and score < 80:
        return (
            "Premium Matte Poster 12x18",
            "282",
            "Printify Choice provider 99; vertical 12x18",
            "Entrance",
            "$48",
        )
    return (
        "Framed/Archival Poster Candidate",
        "540",
        "Framed vertical poster; confirm final variant before publish",
        "Entrance/Core Test",
        "$68-$98",
    )


def build_rows() -> list[dict[str, str]]:
    promoted = sorted(read_csv(SOURCE_CSV), key=lambda row: score_float(row.get("Score")), reverse=True)
    rows: list[dict[str, str]] = []
    for rank, row in enumerate(promoted, start=1):
        carrier, blueprint, provider, lane, retail = carrier_for(row, rank)
        if lane == "Core":
            rationale = "Best scoring luxury/executive DNA deserves acrylic depth and higher perceived gift value."
        elif lane == "Entrance":
            rationale = "Use lower-friction poster price to test demand without cheapening the Studio line."
        else:
            rationale = "Promising but needs framed-poster variant verification before public launch."
        rows.append(
            {
                "Rank": str(rank),
                "Promoted_ID": clean(row.get("Promoted_ID")),
                "Pair_ID": clean(row.get("Pair_ID")),
                "Title": clean(row.get("Title")),
                "Carrier": carrier,
                "Blueprint_ID": blueprint,
                "Provider_Preference": provider,
                "Price_Lane": lane,
                "Target_Retail": retail,
                "Rationale": rationale,
                "Production_Status": "LOCAL_MATRIX_READY_NO_PUBLISH",
                "Next_Action": "Rex/Gemini visual review or controlled MJ refinement before any Printify product creation.",
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    counts = Counter(row["Carrier"] for row in rows)
    lines = [
        "# Project Mirror Product Matrix",
        "",
        f"Generated: {now_et().strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        "- No Printify product was created.",
        "- No Etsy/eBay listing was created.",
        "- No MJ upscale was triggered.",
        "",
        f"Carrier mix: {dict(counts)}",
        "",
        "| Rank | Promoted DNA | Carrier | Blueprint | Target Retail |",
        "| ---: | --- | --- | --- | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['Rank']} | {row['Promoted_ID']} | {row['Carrier']} | "
            f"{row['Blueprint_ID']} | {row['Target_Retail']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    counts = Counter(row["Carrier"] for row in rows)
    msg = (
        f"\n## {now_et().strftime('%Y-%m-%d %H:%M ET')} - Project Mirror product matrix\n"
        f"- Converted {len(rows)} promoted DNA rows into product-carrier candidates: {dict(counts)}.\n"
        f"- Output: `Database\\Project_Mirror_Product_Matrix.csv`; review: `Review_Packets\\Project_Mirror\\PROJECT_MIRROR_PRODUCT_MATRIX.md`.\n"
        "- No publish, fee, or upscale action was taken.\n"
    )
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(msg)


def main() -> int:
    rows = build_rows()
    write_csv(rows)
    write_md(rows)
    append_progress(rows)
    print(f"[PROJECT-MIRROR-MATRIX] rows={len(rows)} csv={OUT_CSV}")
    print(f"[PROJECT-MIRROR-MATRIX] carriers={dict(Counter(row['Carrier'] for row in rows))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
