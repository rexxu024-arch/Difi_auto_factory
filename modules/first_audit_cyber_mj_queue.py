"""Build the First Audit Cyber-Renaissance MJ draft dispatch queue.

This converts the studio concept queue into the standard Midjourney dispatch
shape used by ``shock_and_awe_mj_dispatcher.py``. It deliberately prepares
draft grid jobs only. No upscale action is created here; Rex must explicitly
select a Top 1% candidate before any production upscale is allowed.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets" / "First_Audit_001"
SOURCE = DATABASE / "First_Audit_Cyber_Renaissance_Draft_Queue.csv"
MJ_QUEUE = DATABASE / "First_Audit_Cyber_Renaissance_MJ_Dispatch_Queue.csv"
REPORT = REVIEW / "FIRST_AUDIT_CYBER_RENAISSANCE_MJ_DISPATCH_PACKET.md"
NY = ZoneInfo("America/New_York")


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\n", " ").replace("\r", " ").split()).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise RuntimeError("No Cyber-Renaissance rows available for MJ queue")
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def existing_by_sku() -> dict[str, dict[str, str]]:
    return {row.get("Internal_SKU", ""): row for row in read_csv(MJ_QUEUE)}


def build(limit: int = 6) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    source_rows = [row for row in read_csv(SOURCE) if clean(row.get("status")).startswith("READY_FOR_MJ_DRAFT")]
    if not source_rows:
        raise RuntimeError(f"No READY_FOR_MJ_DRAFT rows in {SOURCE}")
    existing = existing_by_sku()
    rows: list[dict[str, str]] = []
    for source in source_rows:
        sku = clean(source.get("id"))
        prior = existing.get(sku, {})
        dispatch_status = clean(prior.get("Dispatch_Status")) or "READY_FOR_MJ"
        if dispatch_status == "READY_FOR_MJ" and prior.get("Dispatched_At_ET"):
            dispatch_status = "MJ_SUBMITTED"
        rows.append(
            {
                "Internal_SKU": sku,
                "Dispatch_Status": dispatch_status,
                "Batch": clean(source.get("battlefield")),
                "Concept_Name": clean(source.get("code_name_cn")),
                "Product_Type": clean(source.get("product_vector")),
                "Recommended_Format": clean(source.get("product_vector")),
                "MJ_Master_Prompt": clean(source.get("mj_prompt")),
                "QA_Gate": "DRAFT_GRID_ONLY; NO_UPSCALE; CYBER_RENAISSANCE; CLASSICAL_ANCHOR; MATERIAL_ILLUSION; NO_TEXT_NO_LOGO_NO_IP",
                "Output_Folder": f"Output/First_Audit/Cyber_Renaissance/{sku}",
                "Review_Note": prior.get("Review_Note") or "Generate initial grid only. Do not upscale until Rex approves Top 1%.",
                "Dispatched_At_ET": prior.get("Dispatched_At_ET", ""),
                "Dispatch_Response_Status": prior.get("Dispatch_Response_Status", ""),
                "Dispatch_Confirm_Message_ID": prior.get("Dispatch_Confirm_Message_ID", ""),
                "Dispatch_Error": prior.get("Dispatch_Error", ""),
                "Harvest_Status": prior.get("Harvest_Status", ""),
                "Grid_File": prior.get("Grid_File", ""),
                "Visual_QA_Status": prior.get("Visual_QA_Status", ""),
                "Visual_QA_Best_File": prior.get("Visual_QA_Best_File", ""),
                "Upscale_Policy": "NO_UPSCALE_UNTIL_REX_TOP1_APPROVAL",
            }
        )
    write_csv(MJ_QUEUE, rows)

    ready = [row for row in rows if row["Dispatch_Status"] == "READY_FOR_MJ"]
    preview = ready[: max(0, limit)]
    lines = [
        "# First Audit Cyber-Renaissance MJ Dispatch Packet",
        "",
        f"Generated: {datetime.now(NY).strftime('%Y-%m-%d %H:%M:%S %Z')}",
        "",
        f"Source concepts: {len(source_rows)}",
        f"Dispatch rows: {len(rows)}",
        f"Ready for draft-grid submit: {len(ready)}",
        "",
        "Guardrail: this queue creates Midjourney grid drafts only. Upscale is blocked until Rex chooses Top 1%.",
        "",
    ]
    for row in preview:
        prompt = row["MJ_Master_Prompt"]
        lines.extend(
            [
                f"## {row['Internal_SKU']} - {row['Concept_Name']}",
                f"- Product Vector: {row['Product_Type']}",
                f"- Cultural Frame: {row['Batch']}",
                f"- Prompt chars: {len(prompt)}",
                f"- Output: `{row['Output_Folder']}`",
                "",
                "```text",
                prompt,
                "```",
                "",
            ]
        )
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[FIRST-AUDIT-CYBER-MJ] rows={len(rows)} ready={len(ready)} csv={MJ_QUEUE}")
    print(f"[FIRST-AUDIT-CYBER-MJ] report={REPORT}")


if __name__ == "__main__":
    build()
