from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
SOURCE_QUEUE = DATABASE / "Shock_And_Awe_V5_Zone2_Printify_Private_Queue.csv"
MJ_QUEUE = DATABASE / "Shock_And_Awe_V5_MJ_Dispatch_Queue.csv"
DEMO_INDEX = REVIEW / "OPERATION_SHOCK_AND_AWE_V5_PARTNER_DEMO_INDEX_20260509.md"
NY = ZoneInfo("America/New_York")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing source queue: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise RuntimeError("No rows to write")
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def existing_by_sku() -> dict[str, dict[str, str]]:
    if not MJ_QUEUE.exists():
        return {}
    return {row.get("Internal_SKU", ""): row for row in read_csv(MJ_QUEUE)}


def build() -> None:
    REVIEW.mkdir(exist_ok=True)
    rows = []
    existing = existing_by_sku()
    for source in read_csv(SOURCE_QUEUE):
        prior = existing.get(source["Internal_SKU"], {})
        dispatch_status = prior.get("Dispatch_Status") or "READY_FOR_MJ"
        if dispatch_status == "READY_FOR_MJ" and prior.get("Dispatched_At_ET"):
            dispatch_status = "MJ_SUBMITTED"
        rows.append(
            {
                "Internal_SKU": source["Internal_SKU"],
                "Dispatch_Status": dispatch_status,
                "Batch": source["Battlefield"],
                "Concept_Name": source["Concept_Name"],
                "Product_Type": source["Product_Type"],
                "Recommended_Format": source["Variant"],
                "MJ_Master_Prompt": source["MJ_Master_Prompt"],
                "QA_Gate": "NO_TEXT_NO_LOGO_NO_IP_MATCH; PREMIUM_MATERIAL_ILLUSION; CORRECT_AR; REVIEWABLE_FOR_PARTNER_DEMO",
                "Output_Folder": f"Output/Shock_And_Awe/V5/Zone2/{source['Internal_SKU']}",
                "Review_Note": prior.get("Review_Note") or "Generate v1 visual for Rex/Gemini review before Printify private draft creation.",
                "Dispatched_At_ET": prior.get("Dispatched_At_ET", ""),
                "Dispatch_Error": prior.get("Dispatch_Error", ""),
            }
        )
    write_csv(MJ_QUEUE, rows)

    lines = [
        "# Operation Shock and Awe V5 - Partner Demo Index",
        "",
        f"Generated: {datetime.now(NY).strftime('%Y-%m-%d %H:%M:%S %z')}",
        "",
        "Purpose: impress Rex's partner with a finished-looking private traffic product system: visual idea, cultural story, emotional value, private DM pitch, and Printify fulfillment anchor.",
        "",
        "Rules:",
        "- The partner is not required to co-design at this stage.",
        "- Do not sync these products to eBay or Etsy.",
        "- Generate reviewable v1 images first; iterate 1-3 rounds before treating any item as final.",
        "- Sell story, identity signal, cultural depth, room aura, and social talking value. The physical object is the fulfillment carrier.",
        "- Information is decoupled: Block B is short broker copy for WeChat/朋友圈; Block C is dense studio authority copy for serious buyers.",
        "",
    ]
    for row in read_csv(SOURCE_QUEUE):
        lines.extend(
            [
                f"## {row['Internal_SKU']} - {row['Concept_Name']}",
                f"- Product: {row['Product_Type']} / {row['Variant']}",
                "### Block A: Midjourney Master Prompt",
                f"`{row['MJ_Master_Prompt']}`",
                "",
                "### Block B: The Broker's Hook",
                row["Broker_Hook"],
                "",
                "### Block C: The Studio Spec Sheet",
                f"- Cultural Anchor: {row['Cultural_Anchor']}",
                f"- Material Illusion: {row['Emotional_Value']} {row['Private_Copy']}",
                f"- Spatial Recommendation: {row['Placement_Scene']}",
                f"- Objection Handling: {row['Objection_Reply']} 纽约排期满，走 Printify 全球供应链打样预计需 10-14 天。",
                "",
                "### Block D: Printify Production Vector",
                f"- Printify Anchor: blueprint {row['Blueprint_ID']} / provider {row['Provider_ID']} / variant {row['Variant_ID']}",
                f"- RRP: {row['Recommended_Retail_USD']}",
                "",
            ]
        )
    DEMO_INDEX.write_text("\n".join(lines), encoding="utf-8-sig")
    print(f"[SHOCK-MJ-QUEUE] rows={len(rows)} csv={MJ_QUEUE}")
    print(f"[SHOCK-MJ-QUEUE] demo_index={DEMO_INDEX}")


if __name__ == "__main__":
    build()
