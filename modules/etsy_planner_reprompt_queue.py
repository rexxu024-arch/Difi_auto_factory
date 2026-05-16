from __future__ import annotations

import csv
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATABASE = ROOT / "Database"
REPORTS = ROOT / "Review_Packets"
PACKET = DATABASE / "Etsy_Darwinian_Lab_V7_Listing_Packet.csv"
MJ_QUEUE = DATABASE / "Etsy_Darwinian_Lab_V7_MJ_Dispatch_Queue.csv"
OUT_QUEUE = DATABASE / "Etsy_Darwinian_Lab_V7_Planner_Reprompt_MJ_Queue.csv"
OUT_MD = REPORTS / "ETSY_V7_PLANNER_REPROMPT_QUEUE.md"
NY = ZoneInfo("America/New_York")

FIELDS = [
    "Internal_SKU",
    "Source_SKU",
    "Track",
    "Pool_ID",
    "Pool_Name",
    "Concept_Name",
    "Listing_Type",
    "Format",
    "Price_USD",
    "Etsy_Title",
    "Etsy_Tags",
    "Etsy_Description",
    "Constraint_Profile",
    "MJ_Master_Prompt",
    "QA_Requirements",
    "Output_Folder",
    "Dispatch_Status",
    "Dispatched_At_ET",
    "Dispatch_Error",
    "Harvest_Status",
    "Harvest_Error",
    "Grid_Message_ID",
    "Grid_File",
    "U1_File",
    "U2_File",
    "U3_File",
    "U4_File",
    "Last_Harvest_ET",
    "Visual_QA_Status",
    "Publish_Status",
    "Created_At_ET",
    "Reprompt_Reason",
]


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\n", " ").replace("\r", " ").split()).strip()


def now() -> str:
    return datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S %z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def improved_prompt(concept: str) -> str:
    subject = clean(concept)
    return (
        f"{subject}, printable dark academia planner page, 70 percent empty clean central writing area, "
        "large blank parchment center with no decoration inside the writing zone, ornate gothic border only around outer edges, "
        "subtle corner ornaments, faint paper grain, functional planner insert layout, balanced margins, scan-ready design, "
        "high contrast printable PDF page --ar 2:3 --v 6.1 --style raw "
        "--no text, typography, letters, words, watermark, logo, cluttered center, busy middle, pseudo text"
    )


def main() -> int:
    packet_rows = read_csv(PACKET)
    mj_rows = read_csv(MJ_QUEUE)
    by_sku = {clean(row.get("Internal_SKU")): row for row in mj_rows}
    out: list[dict[str, str]] = []
    for row in packet_rows:
        if clean(row.get("Launch_Readiness")) != "HOLD_REPROMPT_LAYOUT":
            continue
        source_sku = clean(row.get("Internal_SKU"))
        source = by_sku.get(source_sku, {})
        new_sku = f"{source_sku}-R1"
        concept = clean(source.get("Concept_Name") or row.get("Concept_Name") or source_sku)
        out.append(
            {
                "Internal_SKU": new_sku,
                "Source_SKU": source_sku,
                "Track": clean(source.get("Track") or "Track B - Etsy Darwinian Lab"),
                "Pool_ID": "POOL09",
                "Pool_Name": clean(source.get("Pool_Name") or "Niche Planners"),
                "Concept_Name": concept,
                "Listing_Type": clean(source.get("Listing_Type") or "Digital Download"),
                "Format": clean(source.get("Format") or "Printable planner PDF bundle"),
                "Price_USD": clean(source.get("Price_USD") or "9.99"),
                "Etsy_Title": clean(source.get("Etsy_Title")),
                "Etsy_Tags": clean(source.get("Etsy_Tags")),
                "Etsy_Description": clean(source.get("Etsy_Description")),
                "Constraint_Profile": "Niche_Planner_R1_Clear_Center",
                "MJ_Master_Prompt": improved_prompt(concept),
                "QA_Requirements": "Must show a mostly blank central writing area; border cannot crowd the center; no pseudo-text anywhere.",
                "Output_Folder": f"Output/Etsy/Darwinian_Lab/V7/{new_sku}",
                "Dispatch_Status": "READY_FOR_MJ",
                "Dispatched_At_ET": "",
                "Dispatch_Error": "",
                "Harvest_Status": "",
                "Harvest_Error": "",
                "Grid_Message_ID": "",
                "Grid_File": "",
                "U1_File": "",
                "U2_File": "",
                "U3_File": "",
                "U4_File": "",
                "Last_Harvest_ET": "",
                "Visual_QA_Status": "PENDING_IMAGE_GENERATION",
                "Publish_Status": "NOT_PUBLISHED_NO_FEE_SPENT",
                "Created_At_ET": now(),
                "Reprompt_Reason": clean(row.get("Readiness_Note") or "Planner center area too crowded"),
            }
        )
    write_csv(OUT_QUEUE, out)
    lines = [
        "# Etsy V7 Planner Reprompt Queue",
        "",
        f"- Created: {now()}",
        f"- Rows: {len(out)}",
        "- Purpose: recover POOL09 planner products that failed the central-writing-space QA gate.",
        "",
    ]
    for item in out:
        lines.append(f"## {item['Internal_SKU']}")
        lines.append(f"- Source: {item['Source_SKU']}")
        lines.append(f"- Reason: {item['Reprompt_Reason']}")
        lines.append(f"- Prompt: `{item['MJ_Master_Prompt']}`")
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"[ETSY-PLANNER-REPROMPT] rows={len(out)} csv={OUT_QUEUE}")
    print(f"[ETSY-PLANNER-REPROMPT] report={OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
