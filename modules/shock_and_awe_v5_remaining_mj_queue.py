from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
SOURCE = DATABASE / "Shock_And_Awe_V5_Zones1_3_Printify_Private_Queue.csv"
QUEUE = DATABASE / "Shock_And_Awe_V5_Zones1_3_MJ_Dispatch_Queue.csv"

FIELDS = [
    "Internal_SKU",
    "Dispatch_Status",
    "Batch",
    "Concept_Name",
    "Product_Type",
    "Recommended_Format",
    "MJ_Master_Prompt",
    "QA_Gate",
    "Output_Folder",
    "Review_Note",
    "Dispatched_At_ET",
    "Dispatch_Error",
    "Harvest_Status",
    "Grid_Message_ID",
    "Grid_File",
    "U1_File",
    "U2_File",
    "U3_File",
    "U4_File",
    "Last_Harvest_ET",
    "Harvest_Error",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    source = read_csv(SOURCE)
    existing = {row.get("Internal_SKU", ""): row for row in read_csv(QUEUE)}
    rows: list[dict[str, str]] = []
    for row in source:
        sku = row["Internal_SKU"]
        old = existing.get(sku, {})
        status = row.get("Status", "")
        if status != "READY_FOR_MJ":
            dispatch_status = "HOLD_PROMPT_QUALITY_REVIEW"
        else:
            dispatch_status = old.get("Dispatch_Status") or "READY_FOR_MJ"
        rows.append(
            {
                "Internal_SKU": sku,
                "Dispatch_Status": dispatch_status,
                "Batch": row.get("Battlefield", ""),
                "Concept_Name": row.get("Concept_Name", ""),
                "Product_Type": row.get("Product_Type", ""),
                "Recommended_Format": row.get("Variant", ""),
                "MJ_Master_Prompt": row.get("MJ_Master_Prompt", ""),
                "QA_Gate": "NO_TEXT_NO_LOGO_NO_IP_MATCH; PREMIUM_MATERIAL_ILLUSION; CORRECT_AR; REVIEWABLE_FOR_PARTNER_DEMO",
                "Output_Folder": f"Output/Shock_And_Awe/V5/Zones1_3/{sku}",
                "Review_Note": "Generate v1 visual for Rex/Gemini review before Printify private draft creation.",
                "Dispatched_At_ET": old.get("Dispatched_At_ET", ""),
                "Dispatch_Error": old.get("Dispatch_Error", ""),
                "Harvest_Status": old.get("Harvest_Status", ""),
                "Grid_Message_ID": old.get("Grid_Message_ID", ""),
                "Grid_File": old.get("Grid_File", ""),
                "U1_File": old.get("U1_File", ""),
                "U2_File": old.get("U2_File", ""),
                "U3_File": old.get("U3_File", ""),
                "U4_File": old.get("U4_File", ""),
                "Last_Harvest_ET": old.get("Last_Harvest_ET", ""),
                "Harvest_Error": old.get("Harvest_Error", ""),
            }
        )
    write_csv(QUEUE, rows)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["Dispatch_Status"]] = counts.get(row["Dispatch_Status"], 0) + 1
    print(f"[SHOCK-V5-REMAINING-MJ-QUEUE] rows={len(rows)} counts={counts} queue={QUEUE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
