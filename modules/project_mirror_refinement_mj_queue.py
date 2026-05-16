"""Build a draft-grid Midjourney queue for Project Mirror refinement winners.

This is a no-publish/no-upscale bridge. It converts the production refinement
plan into the same dispatch schema used by the existing MJ dispatcher so the
monthly loop can continue from "good research result" to "reviewable draft
grids" without touching Printify, Etsy, eBay, or MJ upscale.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
REVIEW_DIR = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"

REFINEMENT_CSV = DATABASE_DIR / "Project_Mirror_Production_Refinement_Queue.csv"
OUT_CSV = DATABASE_DIR / "Project_Mirror_Refinement_MJ_Dispatch_Queue.csv"
OUT_MD = REVIEW_DIR / "PROJECT_MIRROR_REFINEMENT_MJ_DISPATCH_QUEUE.md"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"

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
    "Grid_Message_ID",
]

PRESERVE_FIELDS = {
    "Dispatch_Status",
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
    "Grid_Message_ID",
}


def now_et() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\n", " ").replace("\r", " ").split()).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def existing_by_sku() -> dict[str, dict[str, str]]:
    return {clean(row.get("Internal_SKU")): row for row in read_csv(OUT_CSV) if clean(row.get("Internal_SKU"))}


def build_rows(limit: int | None = None) -> list[dict[str, str]]:
    existing = existing_by_sku()
    rows: list[dict[str, str]] = []
    for item in read_csv(REFINEMENT_CSV):
        if limit is not None and len(rows) >= limit:
            break
        status = clean(item.get("Status"))
        if status != "READY_FOR_CONTROLLED_DRAFT_GRID_NO_UPSCALE":
            continue
        refine_id = clean(item.get("Refinement_ID"))
        sku = f"{refine_id}-PROJECT_MIRROR_REFINED"
        carrier = clean(item.get("Carrier"))
        blueprint = clean(item.get("Blueprint_ID"))
        prior = existing.get(sku, {})
        row = {
            "Internal_SKU": sku,
            "Dispatch_Status": "READY_FOR_MJ",
            "Batch": "Project Mirror Production Refinement",
            "Concept_Name": clean(item.get("Title")),
            "Product_Type": "Premium Decor Refinement",
            "Recommended_Format": f"{carrier} / Blueprint {blueprint}",
            "MJ_Master_Prompt": clean(item.get("MJ_Refinement_Prompt")),
            "QA_Gate": clean(item.get("QA_Gates")),
            "Output_Folder": str(PROJECT_ROOT / "Output" / "Project_Mirror_Refinement" / refine_id),
            "Review_Note": (
                f"{refine_id}; no Printify creation, no marketplace publish, no upscale. "
                f"Target retail {clean(item.get('Target_Retail'))}; mockup need: {clean(item.get('Mockup_Need'))}"
            ),
            "Dispatched_At_ET": "",
            "Dispatch_Response_Status": "",
            "Dispatch_Confirm_Message_ID": "",
            "Dispatch_Error": "",
            "Harvest_Status": "",
            "Grid_File": "",
            "U1_File": "",
            "U2_File": "",
            "U3_File": "",
            "U4_File": "",
            "Last_Harvest_ET": "",
            "Harvest_Error": "",
            "Grid_Wait_First_ET": "",
            "Grid_Wait_Attempts": "",
            "Visual_QA_Status": "",
            "Visual_QA_Best_File": "",
            "Visual_QA_Flags": "",
            "Upscale_Policy": "NO_UPSCALE_DRAFT_GRID_ONLY",
            "Grid_Message_ID": "",
        }
        for field in PRESERVE_FIELDS:
            if clean(prior.get(field)):
                row[field] = prior[field]
        rows.append(row)
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    ready = sum(1 for row in rows if row["Dispatch_Status"] == "READY_FOR_MJ")
    submitted = sum(1 for row in rows if row["Dispatch_Status"] == "MJ_SUBMITTED")
    found = sum(1 for row in rows if clean(row.get("Harvest_Status")) == "GRID_FOUND")
    lines = [
        "# Project Mirror Refinement MJ Dispatch Queue",
        "",
        f"Generated: {now_et().strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        f"- Rows: {len(rows)}",
        f"- READY_FOR_MJ: {ready}",
        f"- MJ_SUBMITTED: {submitted}",
        f"- GRID_FOUND: {found}",
        "- Policy: draft grids only; no upscale; no Printify creation; no marketplace publishing.",
        "",
        "| SKU | Carrier | Status |",
        "| --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['Internal_SKU']} | {row['Recommended_Format']} | {row['Dispatch_Status']} |")
    lines.append("")
    for row in rows[:3]:
        lines.extend(["## " + row["Internal_SKU"], "```text", row["MJ_Master_Prompt"], "```", ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    ready = sum(1 for row in rows if row["Dispatch_Status"] == "READY_FOR_MJ")
    submitted = sum(1 for row in rows if row["Dispatch_Status"] == "MJ_SUBMITTED")
    found = sum(1 for row in rows if clean(row.get("Harvest_Status")) == "GRID_FOUND")
    msg = (
        f"\n## {now_et().strftime('%Y-%m-%d %H:%M ET')} - Project Mirror refinement MJ queue\n"
        f"- Built/updated {len(rows)} controlled refinement MJ rows: READY={ready}, SUBMITTED={submitted}, GRID_FOUND={found}.\n"
        f"- Queue: `Database\\Project_Mirror_Refinement_MJ_Dispatch_Queue.csv`.\n"
        "- Policy remains draft-grid only; no upscale, publish, or fee.\n"
    )
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(msg)


def main() -> int:
    rows = build_rows()
    write_csv(rows)
    write_md(rows)
    append_progress(rows)
    ready = sum(1 for row in rows if row["Dispatch_Status"] == "READY_FOR_MJ")
    print(f"[PROJECT-MIRROR-REFINE-MJ] rows={len(rows)} ready={ready} csv={OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
