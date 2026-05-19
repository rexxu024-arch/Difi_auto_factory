"""Convert the Adobe Stock daily production queue into MJ dispatch rows.

This is deliberately thin infrastructure: the mentor expander owns stock DNA
and metadata, while this adapter only exposes today's 50 rows to the existing
Midjourney dispatcher. Adobe Stock uses relaxed draft grids first. Upload is
blocked until a selected U-button/full-resolution image passes local QA.
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
SOURCE = DATABASE / "Adobe_Stock_Daily_Production_Queue.csv"
OUT = DATABASE / "Adobe_Stock_Daily_MJ_Dispatch_Queue.csv"
REPORT = REVIEW / "Adobe_Stock_Daily_MJ_Dispatch_Queue_latest.md"
NY_TZ = ZoneInfo("America/New_York")

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

PUBLIC_BAN_TERMS = {
    "openclaw",
    "first audit",
    "sweatshop",
    "etsy",
    "ebay",
    "printify",
    "midjourney",
    "claude",
    "codex",
    "gemini",
    "deepseek",
    "dify",
}

TITLE_USE_CASES = {
    "Macro_Material_Background": "texture background with copy space",
    "Macro_Texture_Surface": "texture background",
    "Macro_Commercial_Backdrop": "background for product design",
    "Macro_Material_Detail": "macro texture background",
}

TITLE_FAMILY_ALIASES = {
    "Manhattan Order": "abstract art deco stone",
    "Kintsugi Marble": "kintsugi marble",
    "Smoky Jade": "green jade stone",
    "Walnut Burl": "walnut wood",
    "Aged Bronze Patina": "aged bronze patina",
    "Nero Marble": "black marble",
    "Brushed Titanium": "brushed metal",
    "Architectural Concrete": "concrete wall",
    "Archival Vellum": "vintage paper",
}


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


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
        writer = csv.DictWriter(handle, fieldnames=HEADERS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in HEADERS})


def validate_public_text(*values: str) -> None:
    text = " ".join(values).lower()
    for term in PUBLIC_BAN_TERMS:
        if term in text:
            raise ValueError(f"blocked public Adobe metadata term: {term}")


def stock_title(family: str, product_type: str, prior_title: str) -> str:
    subject = TITLE_FAMILY_ALIASES.get(family, family)
    use_case = TITLE_USE_CASES.get(product_type, "Texture Background for Design Projects")
    title = clean(f"{subject} {use_case}").lower()
    if 10 <= len(title) <= 70:
        return title[:1].upper() + title[1:]
    prior = clean(prior_title)
    return prior[:70].rstrip() if prior else title[:70].rstrip()


def ensure_relax(prompt: str) -> str:
    prompt = clean(prompt)
    if "--relax" in prompt:
        return prompt
    return f"{prompt} --relax"


def sku_from_row(row: dict[str, str]) -> str:
    queue_id = clean(row.get("Queue_ID"))
    return queue_id.replace("ADOBE-DAILY-", "ADOBE-STOCK-")


def build_rows() -> list[dict[str, str]]:
    existing = {clean(row.get("Internal_SKU")): row for row in read_csv(OUT)}
    rows: list[dict[str, str]] = []
    for source in read_csv(SOURCE):
        source_status = clean(source.get("Status"))
        queue_id = clean(source.get("Queue_ID"))
        sku = sku_from_row(source)
        prior = existing.get(sku, {})
        status = clean(prior.get("Dispatch_Status"))
        if not status:
            status = "READY_FOR_MJ" if source_status == "READY_FOR_GENERATION_NO_UPLOAD" else "MJ_DISPATCH_HOLD"
        family = clean(source.get("Family"))
        product_type = clean(source.get("Product_Type"))
        title = stock_title(family, product_type, clean(source.get("Adobe_Title")))
        keywords = clean(source.get("Adobe_Keywords"))
        prompt = ensure_relax(source.get("MJ_Prompt") or "")
        validate_public_text(title, keywords)
        output_folder = f"Output/Adobe_Stock/Daily_Production/{queue_id}"
        row = {field: clean(prior.get(field)) for field in HEADERS}
        row.update(
            {
                "Internal_SKU": sku,
                "Source_Queue_ID": queue_id,
                "Dispatch_Status": status,
                "Batch": "Adobe Stock Daily 50",
                "Concept_Name": f"{family} / {product_type}",
                "Product_Type": "Adobe Stock material / background",
                "Recommended_Format": "MJ relaxed draft grid first; selected U-button full-res JPEG/PNG only; no Fast or creative upscale",
                "MJ_Master_Prompt": prompt,
                "QA_Gate": "NO_TEXT_NO_LOGO_NO_PEOPLE; DEEP_FOCUS_BROAD_SHARP_TEXTURE_REQUIRED; SHALLOW_DOF_HELD; 4MP_MIN; SELECTED_U_FULL_RES_REQUIRED; ADOBE_AI_DISCLOSURE_REQUIRED; SIMILAR_CONTENT_SPACING",
                "Output_Folder": output_folder,
                "Review_Note": "Stock brick: useful commercial background/material, not an Etsy/First Audit finished product.",
                "Upscale_Policy": "NO_FAST_NO_CREATIVE_UPSCALE; GRID_DRAFT_THEN_SELECTED_U_BUTTON_ONLY",
                "Adobe_Title": title,
                "Adobe_Keywords": keywords,
                "Adobe_Category": clean(source.get("Adobe_Category")) or "8",
                "Created_Using_AI": clean(source.get("Created_Using_AI")) or "true",
                "Release_Required": clean(source.get("Release_Required")) or "false",
            }
        )
        rows.append(row)
    return rows


def write_report(rows: list[dict[str, str]]) -> None:
    counts = Counter(row.get("Dispatch_Status", "") for row in rows)
    families = Counter(row.get("Concept_Name", "").split(" / ", 1)[0] for row in rows)
    lines = [
        "# Adobe Stock Daily 50 MJ Dispatch Queue",
        "",
        f"Generated: {now_text()}",
        f"Rows: {len(rows)}",
        f"Dispatch status: {dict(counts)}",
        "",
        "## Policy",
        "",
        "- No Midjourney Fast hours.",
        "- No Creative/Subtle upscale for stock.",
        "- Generate relaxed draft grids first, then only selected U-button full-res images may enter QA.",
        "- No Adobe upload until image QA + metadata QA pass.",
        "",
        "## Family Mix",
        "",
    ]
    for family, count in families.most_common():
        lines.append(f"- {family}: {count}")
    lines.append("")
    lines.append("## First 12 Rows")
    lines.append("")
    for row in rows[:12]:
        lines.append(f"- {row['Internal_SKU']} | {row['Concept_Name']} | {row['Dispatch_Status']} | {row['Adobe_Title']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock daily MJ dispatch queue built; "
            f"rows={len(rows)}; no Fast/no creative upscale; selected U-button full-res required before QA/upload.\n"
        )


def main() -> int:
    rows = build_rows()
    write_csv(OUT, rows)
    write_report(rows)
    append_progress(rows)
    print(f"[ADOBE-DAILY-MJ] rows={len(rows)} status={dict(Counter(row['Dispatch_Status'] for row in rows))} csv={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
