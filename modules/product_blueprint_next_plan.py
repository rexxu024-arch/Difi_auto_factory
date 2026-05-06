"""Build the next Printify product R&D test plan from official probe outputs."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
DETAILS = DATABASE_DIR / "Product_Blueprint_Official_Details.csv"
MUG_DETAILS = DATABASE_DIR / "Product_Blueprint_Mug_Details.csv"
OUT_CSV = DATABASE_DIR / "Product_Blueprint_Next_Test_Plan.csv"
OUT_MD = DATABASE_DIR / "Product_Blueprint_Next_Test_Plan.md"

HEADERS = [
    "Priority",
    "Product_Type",
    "Blueprint_ID",
    "Blueprint_Title",
    "Provider_ID",
    "Provider_Title",
    "Variant_ID",
    "Variant_Title",
    "Print_Area",
    "US_Shipping_First_Cents",
    "Recommended_Test_Size",
    "Why",
    "Must_Verify_Before_Publish",
    "Decision",
]

TARGETS = [
    {
        "priority": 1,
        "product_type": "Canvas",
        "blueprint_id": "1936",
        "variant_contains": "12″ x 18″",
        "why": "Closest rectangular premium expansion from existing 12x18 poster art; buyer understands wall-art use case.",
        "test_size": "2-3 private/staged samples first",
        "verify": "Production cost via create-product/readback or UI; live mockup count/default cover; edge wrap crop.",
        "decision": "Next premium wall-art test after current cover gate is stable.",
    },
    {
        "priority": 2,
        "product_type": "Framed Poster",
        "blueprint_id": "1236",
        "variant_contains": "12″ x 18″",
        "why": "Ready-to-hang premium decor; keeps the same vertical print area and increases perceived value.",
        "test_size": "1-2 samples",
        "verify": "Frame color, exact variant, cost, shipping, and mockup reliability before public publish.",
        "decision": "Etsy-first premium test; eBay only if margin and mockups are clean.",
    },
    {
        "priority": 3,
        "product_type": "Notebook/Journal",
        "blueprint_id": "5634",
        "variant_contains": "5.5",
        "why": "Practical student/writer product that fits dark academia and zen study personas better than another pure decor item.",
        "test_size": "4-6 designs",
        "verify": "Front/back cover template, spine/edge crop, production cost, and whether simple art-object covers read clearly in thumbnails.",
        "decision": "Strong conversion experiment after image QA scripts are generalized.",
    },
    {
        "priority": 4,
        "product_type": "Mug",
        "blueprint_id": "478",
        "variant_contains": "11oz",
        "why": "Large gift market, but needs new panoramic/wrap design rather than reusing vertical Poster/Acrylic art.",
        "test_size": "2-3 wrap-specific designs",
        "verify": "Wrap template, handle-safe composition, readable thumbnails, production cost, and shipping.",
        "decision": "Defer until wrap mockup builder exists.",
    },
    {
        "priority": 5,
        "product_type": "Metal",
        "blueprint_id": "1206",
        "variant_contains": "14",
        "why": "Premium decor angle, but niche and return expectation is higher than canvas/poster.",
        "test_size": "1 high-end sample only",
        "verify": "Cost, shipping, reflectivity/color reproduction, and whether buyer demand justifies price.",
        "decision": "Optional later premium test.",
    },
]


def now_text() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")


def clean(value: object) -> str:
    return str(value or "").strip()


def read_details() -> list[dict[str, str]]:
    rows = []
    for path in (DETAILS, MUG_DETAILS):
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows.extend(csv.DictReader(handle))
    return rows


def pick_variant(rows: list[dict[str, str]], target: dict[str, object]) -> dict[str, str]:
    blueprint = str(target["blueprint_id"])
    needle = str(target["variant_contains"]).lower()
    candidates = [row for row in rows if clean(row.get("Blueprint_ID")) == blueprint]
    for row in candidates:
        if needle in clean(row.get("Variant_Title")).lower():
            return row
    return candidates[0] if candidates else {}


def build_rows() -> list[dict[str, str]]:
    details = read_details()
    rows = []
    for target in TARGETS:
        match = pick_variant(details, target)
        rows.append(
            {
                "Priority": target["priority"],
                "Product_Type": target["product_type"],
                "Blueprint_ID": clean(match.get("Blueprint_ID")) or target["blueprint_id"],
                "Blueprint_Title": clean(match.get("Blueprint_Title")),
                "Provider_ID": clean(match.get("Provider_ID")),
                "Provider_Title": clean(match.get("Provider_Title")),
                "Variant_ID": clean(match.get("Variant_ID")),
                "Variant_Title": clean(match.get("Variant_Title")),
                "Print_Area": clean(match.get("Print_Area")),
                "US_Shipping_First_Cents": clean(match.get("US_Shipping_First_Cents")),
                "Recommended_Test_Size": target["test_size"],
                "Why": target["why"],
                "Must_Verify_Before_Publish": target["verify"],
                "Decision": target["decision"],
            }
        )
    return rows


def write_outputs(rows: list[dict[str, str]]) -> None:
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "# Product Blueprint Next Test Plan",
        "",
        f"Generated: {now_text()} America/New_York",
        "",
        "Use this as the Scholar verification packet before coding a new product type at scale.",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## P{row['Priority']} {row['Product_Type']} - Blueprint {row['Blueprint_ID']}",
                f"- Title/provider: {row['Blueprint_Title']} / {row['Provider_ID']} {row['Provider_Title']}",
                f"- Variant: {row['Variant_ID']} {row['Variant_Title']}",
                f"- Print area: {row['Print_Area']}",
                f"- US shipping first: {row['US_Shipping_First_Cents']} cents",
                f"- Test size: {row['Recommended_Test_Size']}",
                f"- Why: {row['Why']}",
                f"- Must verify: {row['Must_Verify_Before_Publish']}",
                f"- Decision: {row['Decision']}",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_outputs(rows)
    print(f"[BLUEPRINT-NEXT-PLAN] rows={len(rows)} csv={OUT_CSV}")
    for row in rows:
        print(f"[BLUEPRINT-NEXT-PLAN] P{row['Priority']} {row['Product_Type']} blueprint={row['Blueprint_ID']} variant={row['Variant_ID']}")


if __name__ == "__main__":
    main()
