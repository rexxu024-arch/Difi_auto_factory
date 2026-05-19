"""Convert Adobe Stock Codex A/B/C prompts into the standard MJ dispatch schema.

This is draft-grid only: no upscale, no Adobe upload, no marketplace action.
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
SOURCE = DB / "Adobe_Stock_Codex_AB_Review_Queue.csv"
OUT = DB / "Adobe_Stock_Codex_AB_MJ_Dispatch_Queue.csv"
REPORT = REVIEW / "Adobe_Stock_Codex_AB_MJ_Dispatch_Queue.md"
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
    "Adobe_Title",
    "Adobe_Keywords",
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


def build_rows() -> list[dict[str, str]]:
    existing = {clean(row.get("Internal_SKU")): row for row in read_csv(OUT)}
    rows: list[dict[str, str]] = []
    for source in read_csv(SOURCE):
        sku = clean(source.get("Review_ID"))
        prior = existing.get(sku, {})
        status = clean(prior.get("Dispatch_Status")) or clean(source.get("Dispatch_Status"))
        if status == "READY_FOR_MJ_RELAXED_DRAFT_NO_UPLOAD":
            status = "READY_FOR_MJ"
        row = {field: clean(prior.get(field)) for field in HEADERS}
        row.update(
            {
                "Internal_SKU": sku,
                "Dispatch_Status": status,
                "Batch": "Adobe Stock Codex A/B/C",
                "Concept_Name": f"{clean(source.get('Family'))} / Arm {clean(source.get('Arm'))}",
                "Product_Type": "Adobe Stock material background",
                "Recommended_Format": "JPEG 3:2, MJ relaxed draft grid first, selected U-button full-res only after QA approval",
                "MJ_Master_Prompt": clean(source.get("MJ_Prompt")),
                "QA_Gate": "NO_TEXT_NO_LOGO_NO_PEOPLE; DEEP_FOCUS_BROAD_SHARP_TEXTURE_REQUIRED; SHALLOW_DOF_HELD; 4MP_MIN_AFTER_UPSCALE; ADOBE_AI_DISCLOSURE_REQUIRED",
                "Output_Folder": f"Output/Adobe_Stock/Codex_AB/{sku}",
                "Review_Note": clean(source.get("Strategy")),
                "Upscale_Policy": "NO_FAST_NO_CREATIVE_UPSCALE; DRAFT_GRID_ONLY_UNTIL_REX_APPROVES_U_BUTTON",
                "Adobe_Title": clean(source.get("Adobe_Title")),
                "Adobe_Keywords": clean(source.get("Adobe_Keywords")),
            }
        )
        rows.append(row)
    return rows


def write_report(rows: list[dict[str, str]]) -> None:
    counts = Counter(row["Dispatch_Status"] for row in rows)
    lines = [
        "# Adobe Stock Codex A/B/C MJ Dispatch Queue",
        "",
        f"Generated: {now_et()}",
        f"Rows: {len(rows)}",
        f"Status: {dict(counts)}",
        "",
        "Policy: MJ relaxed draft grids only. No upscale, no Adobe upload, no fee.",
        "",
    ]
    for row in rows:
        lines.append(f"- {row['Internal_SKU']}: {row['Concept_Name']} / {row['Dispatch_Status']} / {row['Review_Note']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {now_et()} - Adobe Stock Codex A/B/C MJ Dispatch Adapter\n"
            f"- Converted {len(rows)} Codex-led Adobe A/B/C prompts to `{OUT}`.\n"
            "- Policy: relaxed draft grids only; no upscale, no upload, no marketplace fee.\n"
        )


def main() -> int:
    rows = build_rows()
    write_csv(OUT, rows)
    write_report(rows)
    append_progress(rows)
    print(f"[ADOBE-AB-MJ] rows={len(rows)} status={dict(Counter(row['Dispatch_Status'] for row in rows))} csv={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
