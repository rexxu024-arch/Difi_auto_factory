import csv
import sys
from pathlib import Path

from openpyxl import Workbook

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
OUTPUT_CSV = DATABASE_DIR / "Product_Blueprint_RnD.csv"
OUTPUT_XLSX = DATABASE_DIR / "Product_Blueprint_RnD.xlsx"

HEADERS = [
    "Candidate",
    "Target_Channel",
    "Buyer_Use_Case",
    "Design_Fit",
    "Likely_DNA",
    "Price_Band",
    "Operational_Complexity_1_Low_5_High",
    "Mockup_Risk_1_Low_5_High",
    "Margin_Potential_1_Low_5_High",
    "Demand_Potential_1_Low_5_High",
    "Account_Diversification_1_Low_5_High",
    "Recommended_Test_Size",
    "Blueprint_ID",
    "Provider_ID",
    "Variant_ID",
    "Official_Print_Area",
    "Official_Cost",
    "Official_Shipping",
    "Score",
    "Decision",
    "Notes",
]

CANDIDATES = [
    {
        "Candidate": "Canvas Gallery Wrap",
        "Target_Channel": "Etsy first, eBay selective",
        "Buyer_Use_Case": "premium wall art, room decor, giftable study-room centerpiece",
        "Design_Fit": "full-frame Poster DNA; strong for Zen landscapes and dark academia interiors",
        "Likely_DNA": "Zen-Celestial_Gate, Academia-Astrological_Globe, Wabi_Sabi_Garden",
        "Price_Band": "$49-$89",
        "Operational_Complexity_1_Low_5_High": 3,
        "Mockup_Risk_1_Low_5_High": 2,
        "Margin_Potential_1_Low_5_High": 4,
        "Demand_Potential_1_Low_5_High": 4,
        "Account_Diversification_1_Low_5_High": 5,
        "Recommended_Test_Size": 10,
        "Blueprint_ID": "937 / 1159 / 1226 / 1238 / 1297 / 1936",
        "Notes": "Most natural expansion from Poster; buyer already understands rectangular artwork.",
    },
    {
        "Candidate": "Framed Poster / Framed Print",
        "Target_Channel": "Etsy first",
        "Buyer_Use_Case": "higher-ticket ready-to-hang decor",
        "Design_Fit": "full-frame Poster DNA; best for minimal negative-space art",
        "Likely_DNA": "Zen Scholar Study, Dark Academia Blueprint, Celestial Gate",
        "Price_Band": "$59-$129",
        "Operational_Complexity_1_Low_5_High": 4,
        "Mockup_Risk_1_Low_5_High": 3,
        "Margin_Potential_1_Low_5_High": 4,
        "Demand_Potential_1_Low_5_High": 4,
        "Account_Diversification_1_Low_5_High": 5,
        "Recommended_Test_Size": 6,
        "Blueprint_ID": "492 / 540 / 764 / 1130 / 1140 / 1236 / 1275 / 1502",
        "Notes": "Premium but shipping/returns risk higher; test after Etsy shop shell is credible.",
    },
    {
        "Candidate": "Spiral Notebook / Journal",
        "Target_Channel": "eBay and Etsy",
        "Buyer_Use_Case": "student, writer, journal, book-lover gift",
        "Design_Fit": "isolated object or full cover art; excellent for academia/zen study niche",
        "Likely_DNA": "Silent_Guqin, Astrological_Globe, Relic Instrument",
        "Price_Band": "$17-$27",
        "Operational_Complexity_1_Low_5_High": 3,
        "Mockup_Risk_1_Low_5_High": 3,
        "Margin_Potential_1_Low_5_High": 3,
        "Demand_Potential_1_Low_5_High": 5,
        "Account_Diversification_1_Low_5_High": 4,
        "Recommended_Test_Size": 12,
        "Blueprint_ID": "74 / 75 / 76 / 485 / 486 / 514 / 515 / 1041 / 1193 / 1194 / 1404 / 1481 / 5634",
        "Notes": "More practical than wall art; may convert better for students if mockups are clear.",
    },
    {
        "Candidate": "Ceramic Mug",
        "Target_Channel": "eBay and Etsy",
        "Buyer_Use_Case": "gift, desk ritual, study drinkware",
        "Design_Fit": "needs seamless/panoramic adaptation; not same as Poster/Acrylic single image",
        "Likely_DNA": "Alchemy symbols, Zen tea room, Dark Academia library motifs",
        "Price_Band": "$18-$29",
        "Operational_Complexity_1_Low_5_High": 4,
        "Mockup_Risk_1_Low_5_High": 4,
        "Margin_Potential_1_Low_5_High": 3,
        "Demand_Potential_1_Low_5_High": 5,
        "Account_Diversification_1_Low_5_High": 4,
        "Recommended_Test_Size": 6,
        "Blueprint_ID": "68 / 289 / 425 / 478 / 479 / 503 / 535 / 583 / 595 / 618 / 628 / 635 / 827 / 930 / 985 / 1016 / 1017 / 1018 / 1126 / 1151 / 1152 / 1156 / 1244 / 1301 / 1302 / 1680 / 1682 / 2692 / 2693",
        "Notes": "Good market but requires new design prompt and wrap QA; do not reuse vertical art directly.",
    },
    {
        "Candidate": "Phone Case",
        "Target_Channel": "Etsy selective",
        "Buyer_Use_Case": "personal accessory, style signal",
        "Design_Fit": "vertical full-frame art can fit, but device variants complicate SKU management",
        "Likely_DNA": "Jade Alchemy, Cosmic Academia, Zen Relic",
        "Price_Band": "$24-$39",
        "Operational_Complexity_1_Low_5_High": 5,
        "Mockup_Risk_1_Low_5_High": 4,
        "Margin_Potential_1_Low_5_High": 3,
        "Demand_Potential_1_Low_5_High": 4,
        "Account_Diversification_1_Low_5_High": 3,
        "Recommended_Test_Size": 4,
        "Blueprint_ID": "268 / 269 / 370 / 371 / 421 / 477 / 529 / 841 / 849 / 886 / 1022 / 1230 / 1273 / 1487 / 1521 / 1658 / 2000",
        "Notes": "Potentially hot, but variation complexity and fit QA are not ideal during weak-network phase.",
    },
    {
        "Candidate": "Metal Print",
        "Target_Channel": "Etsy premium",
        "Buyer_Use_Case": "high-end glossy wall art, modern decor",
        "Design_Fit": "bioluminescent/jade/cosmic art could look strong",
        "Likely_DNA": "Bioluminescent Garden, Cosmic Academia Vault",
        "Price_Band": "$69-$149",
        "Operational_Complexity_1_Low_5_High": 4,
        "Mockup_Risk_1_Low_5_High": 3,
        "Margin_Potential_1_Low_5_High": 5,
        "Demand_Potential_1_Low_5_High": 3,
        "Account_Diversification_1_Low_5_High": 5,
        "Recommended_Test_Size": 4,
        "Blueprint_ID": "1206",
        "Notes": "Premium test only after official Printify cost/shipping and print area are verified.",
    },
]


def _score(row):
    return (
        row["Margin_Potential_1_Low_5_High"] * 2
        + row["Demand_Potential_1_Low_5_High"] * 2
        + row["Account_Diversification_1_Low_5_High"]
        - row["Operational_Complexity_1_Low_5_High"]
        - row["Mockup_Risk_1_Low_5_High"]
    )


def _decision(score):
    if score >= 12:
        return "Priority Test"
    if score >= 9:
        return "Secondary Test"
    return "Defer"


def build_rows():
    rows = []
    for item in CANDIDATES:
        row = {header: "" for header in HEADERS}
        row.update(item)
        score = _score(item)
        row["Score"] = score
        row["Decision"] = _decision(score)
        rows.append(row)
    rows.sort(key=lambda row: (-row["Score"], row["Candidate"]))
    return rows


def write_outputs(rows):
    DATABASE_DIR.mkdir(exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    wb = Workbook()
    ws = wb.active
    ws.title = "Blueprint RnD"
    ws.append(HEADERS)
    for row in rows:
        ws.append([row.get(header, "") for header in HEADERS])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for column, width in {
        "A": 24,
        "B": 22,
        "C": 46,
        "D": 52,
        "E": 44,
        "F": 14,
        "L": 16,
        "P": 22,
        "U": 70,
    }.items():
        ws.column_dimensions[column].width = width
    wb.save(OUTPUT_XLSX)
    wb.close()


def main():
    rows = build_rows()
    write_outputs(rows)
    print(f"[BLUEPRINT-RND] rows={len(rows)} csv={OUTPUT_CSV}")
    for row in rows:
        print(f"[BLUEPRINT-RND] {row['Decision']} score={row['Score']} {row['Candidate']}")


if __name__ == "__main__":
    sys.exit(main())
