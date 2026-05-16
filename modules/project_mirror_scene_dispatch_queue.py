"""Convert Project Mirror identity-locked mockup prompts to MJ dispatch rows.

The output is compatible with `mj_reference_image_uploader.py`,
`shock_and_awe_mj_dispatcher.py`, and `shock_and_awe_mj_harvester.py`.
It deliberately keeps every row draft-grid only: no upscale, no publish, no fee.
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
SOURCE = DATABASE / "Project_Mirror_Identity_Locked_Mockup_Queue.csv"
OUT = DATABASE / "Project_Mirror_Identity_Locked_Scene_Dispatch_Queue.csv"
REPORT = REVIEW / "PROJECT_MIRROR_IDENTITY_LOCKED_SCENE_DISPATCH_QUEUE.md"
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
    "Grid_Message_ID",
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
    "Reference_Image_Path",
    "Reference_Image_URL",
    "Reference_Upload_Message_ID",
    "Reference_Uploaded_At_ET",
    "Reference_Upload_Error",
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
    prior = existing_by_sku()
    rows: list[dict[str, str]] = []
    for source in read_csv(SOURCE):
        sku = clean(source.get("Queue_ID"))
        old = prior.get(sku, {})
        status = clean(old.get("Dispatch_Status")) or "READY_FOR_MJ"
        row = {field: clean(old.get(field)) for field in HEADERS}
        candidate = clean(source.get("Candidate_File"))
        prompt = clean(source.get("Prompt")).replace("[UPLOAD_SOURCE_IMAGE_TO_DISCORD_AND_PLACE_CDN_URL_FIRST]", candidate)
        product_type = "Acrylic Scene" if "acrylic" in prompt.lower() else "Framed Poster Scene"
        row.update(
            {
                "Internal_SKU": sku,
                "Dispatch_Status": status,
                "Batch": "Project Mirror Identity-Locked Scene",
                "Concept_Name": f"{clean(source.get('DNA_ID'))} {clean(source.get('Scene_Type'))}",
                "Product_Type": product_type,
                "Recommended_Format": clean(source.get("Scene_Type")),
                "MJ_Master_Prompt": prompt,
                "QA_Gate": clean(source.get("QA_Gate")),
                "Output_Folder": str(PROJECT_ROOT / "Output" / "Project_Mirror_Scene_Mockups" / sku),
                "Review_Note": (
                    f"{clean(source.get('Source_SKU'))}; {clean(source.get('Scene_Type'))}; "
                    "draft only; original image must remain visually identical"
                ),
                "Upscale_Policy": "NO_UPSCALE_DRAFT_GRID_ONLY",
                "Reference_Image_Path": clean(old.get("Reference_Image_Path")) or candidate,
            }
        )
        rows.append(row)
    return rows


def write_report(rows: list[dict[str, str]]) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    counts = Counter(row["Dispatch_Status"] for row in rows)
    lines = [
        "# Project Mirror Identity-Locked Scene Dispatch Queue",
        "",
        f"- Generated: {now_et()}",
        f"- Rows: {len(rows)}",
        f"- Status: {dict(counts)}",
        f"- CSV: `{OUT}`",
        "- Policy: draft grids only; no upscale, no publish, no fee.",
        "- Required bridge: run `mj_reference_image_uploader.py --queue ...` before dispatch so Midjourney receives a real image URL.",
        "",
    ]
    for row in rows:
        lines.append(f"- {row['Internal_SKU']}: {row['Dispatch_Status']} / {row['Review_Note']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    counts = Counter(row["Dispatch_Status"] for row in rows)
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {now_et()} - Project Mirror scene dispatch adapter\n"
            f"- Converted {len(rows)} identity-locked scene prompts into standard MJ dispatch rows: {dict(counts)}.\n"
            f"- Output: `{OUT}`; review packet: `{REPORT}`.\n"
            "- Draft-grid only. No upscale, publish, Printify creation, or fee action was taken.\n"
        )


def main() -> int:
    rows = build_rows()
    if not rows:
        print("[PROJECT-MIRROR-SCENE-DISPATCH] no scene rows")
        return 1
    write_csv(OUT, rows)
    write_report(rows)
    append_progress(rows)
    print(f"[PROJECT-MIRROR-SCENE-DISPATCH] rows={len(rows)} status={dict(Counter(row['Dispatch_Status'] for row in rows))} csv={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
