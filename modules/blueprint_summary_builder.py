import csv
import sys
from collections import defaultdict
from pathlib import Path

from openpyxl import Workbook

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
DETAILS = DATABASE_DIR / "Product_Blueprint_Official_Details.csv"
EXTRA_DETAILS = DATABASE_DIR / "Product_Blueprint_Mug_Details.csv"
OUTPUT_CSV = DATABASE_DIR / "Product_Blueprint_Official_Summary.csv"
OUTPUT_XLSX = DATABASE_DIR / "Product_Blueprint_Official_Summary.xlsx"

HEADERS = [
    "Product_Family",
    "Blueprint_ID",
    "Blueprint_Title",
    "Provider_ID",
    "Provider_Title",
    "Variant_Count_Probed",
    "Sample_Variants",
    "Sample_Print_Areas",
    "Min_US_Shipping_First_Cents",
    "Max_US_Shipping_First_Cents",
    "Production_Cost_Source",
    "Recommended_Next_Test",
    "Risk_Note",
]


def _read(path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _int(value):
    try:
        return int(value)
    except Exception:
        return None


def _recommend(family, blueprint_id, title):
    if family == "Canvas" and blueprint_id in {"937", "1159", "1226"}:
        return "Build 2-3 sample listings after official cost is verified"
    if family == "Framed Poster" and blueprint_id in {"540", "1130", "1275"}:
        return "Build 1-2 premium samples after cost verification"
    if family == "Metal" and blueprint_id == "1206":
        return "Build 1 high-end sample only if cost/margin works"
    if family == "Notebook/Journal" and blueprint_id in {"74", "485", "514", "515", "5634"}:
        return "Strong practical-product test; design cover only, no inside-page complexity"
    if family == "Mug" and blueprint_id in {"478", "479", "618"}:
        return "Only after wrap-around design QA; do not reuse vertical art directly"
    return "Verify cost/provider first"


def _risk(family, blueprint_id):
    if family == "Mug":
        return "Requires wrap-around design and mug mockup QA; higher expectation risk than rectangular art."
    if family == "Notebook/Journal":
        return "Cover placement and back/inside placeholders may require product-specific templates."
    if family == "Framed Poster":
        return "Higher shipping/return expectation; verify frame color/size variants carefully."
    if family == "Canvas":
        return "Good fit for existing full-frame art; verify production cost before pricing."
    if family == "Metal":
        return "Premium but niche; test tiny batch only."
    return ""


def build():
    rows = _read(DETAILS) + _read(EXTRA_DETAILS)
    grouped = defaultdict(list)
    for row in rows:
        if row.get("Probe_Status") != "OK" or not row.get("Variant_ID"):
            continue
        key = (
            row["Product_Family"],
            row["Blueprint_ID"],
            row["Blueprint_Title"],
            row["Provider_ID"],
            row["Provider_Title"],
        )
        grouped[key].append(row)
    output = []
    for key, values in grouped.items():
        family, bid, title, provider_id, provider_title = key
        ships = [_int(row.get("US_Shipping_First_Cents")) for row in values]
        ships = [value for value in ships if value is not None]
        sample_variants = " | ".join(row.get("Variant_Title", "") for row in values[:4])
        sample_areas = " | ".join(row.get("Print_Area", "") for row in values[:3])
        output.append(
            {
                "Product_Family": family,
                "Blueprint_ID": bid,
                "Blueprint_Title": title,
                "Provider_ID": provider_id,
                "Provider_Title": provider_title,
                "Variant_Count_Probed": len(values),
                "Sample_Variants": sample_variants,
                "Sample_Print_Areas": sample_areas,
                "Min_US_Shipping_First_Cents": min(ships) if ships else "",
                "Max_US_Shipping_First_Cents": max(ships) if ships else "",
                "Production_Cost_Source": "Not exposed by queried Printify catalog variant endpoint; verify via UI/create-product readback before pricing.",
                "Recommended_Next_Test": _recommend(family, bid, title),
                "Risk_Note": _risk(family, bid),
            }
        )
    output.sort(key=lambda row: (row["Product_Family"], int(row["Blueprint_ID"])))
    return output


def write(rows):
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    wb = Workbook()
    ws = wb.active
    ws.title = "Official Summary"
    ws.append(HEADERS)
    for row in rows:
        ws.append([row.get(header, "") for header in HEADERS])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for col, width in {
        "A": 18,
        "B": 14,
        "C": 42,
        "D": 12,
        "E": 24,
        "G": 72,
        "H": 72,
        "K": 58,
        "L": 48,
        "M": 58,
    }.items():
        ws.column_dimensions[col].width = width
    wb.save(OUTPUT_XLSX)
    wb.close()


def main():
    rows = build()
    write(rows)
    print(f"[BLUEPRINT-SUMMARY] rows={len(rows)} csv={OUTPUT_CSV}")


if __name__ == "__main__":
    sys.exit(main())
