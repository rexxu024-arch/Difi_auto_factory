from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "Database"
REVIEW = ROOT / "Review_Packets"
SOURCE = DB / "Adobe_Stock_Market_Sample_MJ_Queue.csv"
OUT = DB / "Adobe_Stock_Market_Sample_MJ_Dispatch_Queue.csv"
REPORT = REVIEW / "Adobe_Stock_Market_Sample_MJ_Dispatch_Queue_latest.md"
ET = ZoneInfo("America/New_York")

HEADERS = [
    "Internal_SKU",
    "Source_Queue_ID",
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
    "Adobe_Category",
    "Created_Using_AI",
    "Release_Required",
]

PRIORITY_LANES = [
    "Carbon Fiber / Technical Weave",
    "Nero Marble / Luxury Stone",
    "Kintsugi Marble / Gold Repair Stone",
    "Brushed Titanium / Chrome Silver",
    "Walnut Burl / Executive Wood",
    "Clean Architectural Concrete / Plaster",
    "Archival Vellum / Premium Paper",
]


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\r", " ").replace("\n", " ").split()).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in HEADERS})


def priority(row: dict[str, str]) -> tuple[int, str]:
    lane = clean(row.get("Lane"))
    try:
        idx = PRIORITY_LANES.index(lane)
    except ValueError:
        idx = 99
    return idx, clean(row.get("Queue_ID"))


def ensure_relax(prompt: str) -> str:
    prompt = clean(prompt)
    if "--relax" not in prompt:
        prompt = f"{prompt} --relax"
    return prompt


def main() -> None:
    source_rows = sorted(read_csv(SOURCE), key=priority)
    existing = {clean(row.get("Internal_SKU")): row for row in read_csv(OUT)}
    out_rows: list[dict[str, str]] = []
    for source in source_rows:
        queue_id = clean(source.get("Queue_ID"))
        sku = queue_id.replace("ADOBE-MARKET-SAMPLE-", "ADOBE-MARKET-")
        prior = existing.get(sku, {})
        status = clean(prior.get("Dispatch_Status")) or "READY_FOR_MJ"
        lane = clean(source.get("Lane"))
        prompt = ensure_relax(clean(source.get("Prompt")))
        row = {field: clean(prior.get(field)) for field in HEADERS}
        row.update(
            {
                "Internal_SKU": sku,
                "Source_Queue_ID": queue_id,
                "Dispatch_Status": status,
                "Batch": "Adobe Stock Market Training Samples",
                "Concept_Name": f"{lane} / {clean(source.get('Variant'))}",
                "Product_Type": "Adobe Stock material training sample",
                "Recommended_Format": "MJ relaxed draft grid only; U images only after Rex visual pass; no Fast, no upload.",
                "MJ_Master_Prompt": prompt,
                "QA_Gate": "REX_TRAINING_SAMPLE; DEEP_FOCUS_BROAD_SHARP_TEXTURE_REQUIRED; NO_FAST; NO_UPLOAD",
                "Output_Folder": f"Output/Adobe_Stock/Market_Samples/{queue_id}",
                "Review_Note": clean(source.get("Rex_QA_Note")),
                "Upscale_Policy": "NO_FAST; RELAXED_GRID_THEN_SELECTED_U_ONLY; LOCAL_4MP_FIX_AFTER_QA",
                "Adobe_Title": clean(source.get("Title_Pattern")),
                "Adobe_Keywords": clean(source.get("First_10_Keywords")),
                "Adobe_Category": "8",
                "Created_Using_AI": "true",
                "Release_Required": "false",
            }
        )
        out_rows.append(row)
    write_csv(OUT, out_rows)
    counts: dict[str, int] = {}
    ready = 0
    for row in out_rows:
        lane = clean(row.get("Concept_Name")).split(" / ")[0]
        counts[lane] = counts.get(lane, 0) + 1
        if clean(row.get("Dispatch_Status")) == "READY_FOR_MJ":
            ready += 1
    lines = [
        "# Adobe Stock Market Sample Dispatch Queue",
        "",
        f"Generated: {datetime.now(ET).strftime('%Y-%m-%d %H:%M:%S %Z')}",
        "",
        f"- Rows: {len(out_rows)}",
        f"- READY_FOR_MJ: {ready}",
        "- Policy: relaxed draft samples only; no Fast, no upload.",
        "",
        "## Counts",
        "",
    ]
    for lane, count in counts.items():
        lines.append(f"- {lane}: {count}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[ADOBE-MARKET-SAMPLE-DISPATCH] rows={len(out_rows)} ready={ready} out={OUT}")


if __name__ == "__main__":
    main()
