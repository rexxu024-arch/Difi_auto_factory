"""Convert Project Mirror A/B prompts into the standard MJ dispatch schema.

This keeps Project Mirror compatible with the existing Shock/MJ dispatcher
without rewriting the Discord submission code. It is intentionally draft-grid
only: no upscale, no marketplace publish, no fee spend.
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"
SOURCE = DATABASE / "Project_Mirror_AB_MJ_Test_Queue.csv"
OUT = DATABASE / "Project_Mirror_MJ_Dispatch_Queue.csv"
REPORT = REVIEW / "PROJECT_MIRROR_MJ_DISPATCH_QUEUE.md"
PROGRESS = PROJECT_ROOT / "PROGRESS_LOG.md"

HEADERS = [
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
    "Dispatch_Response_Status",
    "Dispatch_Confirm_Message_ID",
    "Dispatch_Error",
    "Harvest_Status",
    "Grid_File",
    "U1_File",
    "U2_File",
    "U3_File",
    "U4_File",
    "Last_Harvest_ET",
    "Harvest_Error",
    "Grid_Wait_First_ET",
    "Grid_Wait_Attempts",
    "Visual_QA_Status",
    "Visual_QA_Best_File",
    "Visual_QA_Flags",
    "Upscale_Policy",
]


def now_et() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M ET")


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\r", " ").replace("\n", " ").split()).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def existing_by_sku() -> dict[str, dict[str, str]]:
    return {clean(row.get("Internal_SKU")): row for row in read_csv(OUT) if clean(row.get("Internal_SKU"))}


def build_rows() -> list[dict[str, str]]:
    existing = existing_by_sku()
    rows: list[dict[str, str]] = []
    for source in read_csv(SOURCE):
        sku = clean(source.get("Test_ID"))
        prior = existing.get(sku, {})
        status = clean(prior.get("Dispatch_Status")) or clean(source.get("Status"))
        if status == "READY_FOR_MJ_DRAFT_GRID":
            status = "READY_FOR_MJ"
        row = {field: clean(prior.get(field)) for field in HEADERS}
        row.update(
            {
                "Internal_SKU": sku,
                "Dispatch_Status": status,
                "Batch": "Project Mirror A/B",
                "Concept_Name": clean(source.get("Title")),
                "Product_Type": "Premium Decor A/B",
                "Recommended_Format": clean(source.get("Product_Fit")),
                "MJ_Master_Prompt": clean(source.get("MJ_Prompt")),
                "QA_Gate": clean(source.get("QA_Target")),
                "Output_Folder": clean(source.get("Output_Folder")),
                "Review_Note": f"{clean(source.get('Variant'))}; {clean(source.get('Notes'))}",
                "Upscale_Policy": "NO_UPSCALE_DRAFT_GRID_ONLY",
            }
        )
        rows.append(row)
    return rows


def write_report(rows: list[dict[str, str]]) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    counts = Counter(row["Dispatch_Status"] for row in rows)
    lines = [
        "# Project Mirror MJ Dispatch Queue",
        "",
        f"Generated: {now_et()}",
        f"Rows: {len(rows)}",
        f"Status: {dict(counts)}",
        "",
        "Policy: draft grids only. No upscale, no marketplace publish, no fee spend.",
        "",
    ]
    for row in rows[:12]:
        lines.append(f"- {row['Internal_SKU']}: {row['Dispatch_Status']} / {row['Review_Note']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    counts = Counter(row["Dispatch_Status"] for row in rows)
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {now_et()} - Project Mirror MJ Dispatch Adapter\n"
            f"- Built standard MJ dispatch queue `{OUT}` from Project Mirror A/B rows.\n"
            f"- Rows={len(rows)} status={dict(counts)}; policy remains draft-grid only, no upscale/publish/fee.\n"
        )


def main() -> int:
    rows = build_rows()
    write_csv(OUT, rows)
    write_report(rows)
    append_progress(rows)
    print({"rows": len(rows), "status": dict(Counter(row["Dispatch_Status"] for row in rows)), "csv": str(OUT)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
