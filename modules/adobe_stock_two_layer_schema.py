"""Maintain the Adobe Stock Mentor Hub / Production Line split.

The Adobe Stock fallback line may reuse OpenClaw execution patterns, but its
state must stay physically separate from Printify, Etsy, and eBay. This module
keeps the two canonical CSVs:

- Adobe_Stock_Mentor_Hub.csv: high-level visual DNA, later owned by Claude.
- Adobe_Stock_Production_Line.csv: stock-ready prompt/metadata rows, later
  owned by DeepSeek-style expansion.

Existing keyword and pilot queue CSVs remain derived execution artifacts.
"""

from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from adobe_stock_isolation import assert_adobe_write_paths


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

KEYWORD_PACK = DATABASE / "Adobe_Stock_Keyword_Pack.csv"
PILOT_QUEUE = DATABASE / "Adobe_Stock_Pilot_Queue.csv"
MENTOR_HUB = DATABASE / "Adobe_Stock_Mentor_Hub.csv"
PRODUCTION_LINE = DATABASE / "Adobe_Stock_Production_Line.csv"
REPORT = REVIEW / "Adobe_Stock_Two_Layer_Pipeline.md"

MENTOR_HEADERS = [
    "DNA_ID",
    "Timestamp_ET",
    "Generation_Source",
    "Family",
    "Stock_Niche",
    "Asset_Type",
    "Logic_Protocol",
    "Gold_Visual_DNA",
    "Material_Keywords",
    "Lighting_Protocol",
    "Composition_Protocol",
    "Negative_Prompt",
    "Adobe_Risk_Guard",
    "Production_Spec",
    "Design_Count",
    "Status",
]

PRODUCTION_HEADERS = [
    "Asset_ID",
    "Timestamp_ET",
    "DNA_ID",
    "Family",
    "Product_Type",
    "Variant_Label",
    "Stock_Category",
    "MJ_Prompt",
    "Target_Filename",
    "Adobe_Title",
    "Adobe_Keywords",
    "Adobe_Category",
    "Created_Using_AI",
    "Release_Required",
    "Source_Path",
    "QA_Status",
    "Upload_Status",
    "Status",
    "Notes",
]

STOCK_PRODUCT_TYPES = {
    "Stock_Texture": "4K+ material texture or surface plate for commercial design use.",
    "Stock_Background": "4K+ premium background/backdrop with copy-safe negative space.",
    "Stock_Seamless_Pattern": "4K+ tileable pattern or wallpaper-ready repeat asset.",
    "Stock_Isolated_Material": "4K+ isolated premium material object or slab on clean background.",
}


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], headers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


def stable_slug(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").upper()
    return re.sub(r"_+", "_", text) or "FAMILY"


def family_to_dna_id(family: str, index: int) -> str:
    slug = stable_slug(family)
    parts = slug.split("_")
    initials = "".join(part[:1] for part in parts)[:4] or "DNA"
    return f"ADOBE-DNA-{initials}-{index:04d}"


def extract_material_keywords(prompt: str, seed: str) -> str:
    hints = [
        "jade",
        "brass",
        "stone",
        "marble",
        "gold",
        "titanium",
        "vellum",
        "obsidian",
        "glass",
        "paper",
        "metal",
        "mineral",
        "nero",
        "travertine",
        "plaster",
        "walnut",
        "burl",
        "wood",
        "bronze",
        "patina",
        "verdigris",
        "linen",
        "canvas",
        "concrete",
        "carbon",
        "fiber",
        "champagne",
    ]
    text = f"{prompt} {seed}".lower()
    found = [hint.title() for hint in hints if re.search(rf"\b{re.escape(hint)}\b", text)]
    return ", ".join(dict.fromkeys(found))


def classify_stock_product_type(row: dict[str, str], previous: dict[str, str]) -> str:
    """Keep Adobe Stock Product_Type intentionally small and stock-native."""
    existing = previous.get("Product_Type", "").strip()
    if existing in STOCK_PRODUCT_TYPES and "MANUAL_PRODUCT_TYPE_LOCK" in previous.get("Notes", ""):
        return existing

    text = " ".join(
        [
            row.get("Asset_Type", ""),
            row.get("Family", ""),
            row.get("Prompt", ""),
            row.get("Adobe_Title", ""),
            row.get("Adobe_Keywords", ""),
        ]
    ).lower()
    if re.search(r"\b(pattern|seamless|tile|repeat)\b", text):
        return "Stock_Seamless_Pattern"
    if re.search(r"\b(texture|surface|marble|jade|titanium|vellum|glass|stone|mineral|metal|paper)\b", text):
        return "Stock_Texture"
    if re.search(r"\b(background|backdrop|wallpaper|negative space|architecture)\b", text):
        return "Stock_Background"
    return "Stock_Isolated_Material"


def build_mentor_rows(existing: dict[str, dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, str]]:
    keyword_rows = read_csv(KEYWORD_PACK)
    rows: list[dict[str, str]] = []
    family_map: dict[str, str] = {}
    for index, row in enumerate(keyword_rows, start=1):
        family = row.get("Family", "").strip()
        if not family:
            continue
        dna_id = family_to_dna_id(family, index)
        family_map[family] = dna_id
        previous = existing.get(dna_id, {})
        prompt_stem = row.get("Prompt_Stem", "").strip()
        keyword_seed = row.get("Keyword_Seed", "").strip()
        previous_source = previous.get("Generation_Source", "")
        material_keywords = previous.get("Material_Keywords") or extract_material_keywords(prompt_stem, keyword_seed)
        if previous_source.startswith("FOUNDATION_SCAFFOLD"):
            material_keywords = extract_material_keywords(prompt_stem, keyword_seed)
        rows.append(
            {
                "DNA_ID": dna_id,
                "Timestamp_ET": previous.get("Timestamp_ET") or now_text(),
                "Generation_Source": previous_source or "FOUNDATION_SCAFFOLD; CLAUDE_EXPANSION_PENDING",
                "Family": family,
                "Stock_Niche": previous.get("Stock_Niche") or row.get("Family", ""),
                "Asset_Type": row.get("Asset_Type", ""),
                "Logic_Protocol": previous.get("Logic_Protocol") or row.get("Risk_Guard", ""),
                "Gold_Visual_DNA": previous.get("Gold_Visual_DNA") or prompt_stem,
                "Material_Keywords": material_keywords,
                "Lighting_Protocol": previous.get("Lighting_Protocol") or "stock-clean studio light; no theatrical hero-art treatment",
                "Composition_Protocol": previous.get("Composition_Protocol") or "edge-to-edge material field; background/texture usable by designers",
                "Negative_Prompt": previous.get("Negative_Prompt") or "no people, no faces, no brand, no logo, no text, no watermark, no protected IP",
                "Adobe_Risk_Guard": previous.get("Adobe_Risk_Guard") or row.get("Risk_Guard", ""),
                "Production_Spec": previous.get("Production_Spec") or row.get("Production_Spec", ""),
                "Design_Count": previous.get("Design_Count") or "0",
                "Status": previous.get("Status") or "READY_FOR_CLAUDE_20_DNA_EXPANSION",
            }
        )
    return rows, family_map


def build_production_rows(existing: dict[str, dict[str, str]], family_map: dict[str, str]) -> list[dict[str, str]]:
    pilot_rows = read_csv(PILOT_QUEUE)
    rows: list[dict[str, str]] = []
    for index, row in enumerate(pilot_rows, start=1):
        asset_id = row.get("ID") or f"ADOBE-ASSET-{index:04d}"
        family = row.get("Family", "").strip()
        previous = existing.get(asset_id, {})
        previous_status = previous.get("Status", "")
        status = previous_status or "BLOCKED_UNTIL_MENTOR_DNA_APPROVED_THEN_DEEPSEEK_EXPANSION"
        if previous_status == "READY_FOR_DEEPSEEK_METADATA_EXPANSION":
            status = "BLOCKED_UNTIL_MENTOR_DNA_APPROVED_THEN_DEEPSEEK_EXPANSION"
        rows.append(
            {
                "Asset_ID": asset_id,
                "Timestamp_ET": previous.get("Timestamp_ET") or now_text(),
                "DNA_ID": previous.get("DNA_ID") or family_map.get(family, ""),
                "Family": family,
                "Product_Type": classify_stock_product_type(row, previous),
                "Variant_Label": previous.get("Variant_Label") or row.get("Status", ""),
                "Stock_Category": previous.get("Stock_Category") or row.get("Asset_Type", ""),
                "MJ_Prompt": previous.get("MJ_Prompt") or row.get("Prompt", ""),
                "Target_Filename": row.get("Target_Filename", ""),
                "Adobe_Title": row.get("Adobe_Title", ""),
                "Adobe_Keywords": row.get("Adobe_Keywords", ""),
                "Adobe_Category": row.get("Adobe_Category", ""),
                "Created_Using_AI": row.get("Created_Using_AI", "true"),
                "Release_Required": row.get("Release_Required", "false"),
                "Source_Path": previous.get("Source_Path") or row.get("Source_Path", ""),
                "QA_Status": previous.get("QA_Status") or row.get("QA_Status", "PENDING_IMAGE"),
                "Upload_Status": previous.get("Upload_Status") or row.get("Upload_Status", "BLOCKED_UNTIL_IMAGE_QA"),
                "Status": status,
                "Notes": previous.get("Notes") or "Derived from Adobe_Stock_Pilot_Queue; public metadata must stay store-agnostic.",
            }
        )
    return rows


def write_report(mentor_count: int, production_count: int) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Adobe Stock Two-Layer Pipeline",
        "",
        f"Generated: {now_text()}",
        "",
        "## Canonical Tables",
        "",
        f"- Mentor Hub CSV: `{MENTOR_HUB.relative_to(PROJECT_ROOT)}`",
        f"- Production Line CSV: `{PRODUCTION_LINE.relative_to(PROJECT_ROOT)}`",
        "",
        "## Contract",
        "",
        "- Mentor Hub owns visual DNA only: Claude should expand each stock family into 20 high-quality DNA variants.",
        "- Production Line owns stock-ready execution: DeepSeek-style compiler expands DNA into prompts, Adobe titles, and 35-49 keywords.",
        "- DeepSeek-only mode is not accepted for final production; it may format and clean, but it must not replace the Mentor DNA layer.",
        "- Pilot queue and upload metadata CSVs are derived artifacts, not the canonical memory layer.",
        "- No Etsy/eBay/Printify/First Audit copy may leak into Adobe public metadata.",
        "- Production Line Product_Type is locked to a small stock-native taxonomy: "
        + ", ".join(STOCK_PRODUCT_TYPES),
        "",
        "## Current Counts",
        "",
        f"- Mentor DNA rows: {mentor_count}",
        f"- Production rows: {production_count}",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def append_progress(mentor_count: int, production_count: int) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock two-layer schema reconciled; "
            f"mentor_rows={mentor_count}; production_rows={production_count}; canonical CSVs separated.\n"
        )


def reconcile_two_layer_tables(*, write_progress: bool = True) -> tuple[int, int]:
    assert_adobe_write_paths((MENTOR_HUB, PRODUCTION_LINE, REPORT))
    existing_mentor = {row.get("DNA_ID", ""): row for row in read_csv(MENTOR_HUB)}
    existing_production = {row.get("Asset_ID", ""): row for row in read_csv(PRODUCTION_LINE)}
    mentor_rows, family_map = build_mentor_rows(existing_mentor)
    production_rows = build_production_rows(existing_production, family_map)
    write_csv(MENTOR_HUB, mentor_rows, MENTOR_HEADERS)
    write_csv(PRODUCTION_LINE, production_rows, PRODUCTION_HEADERS)
    write_report(len(mentor_rows), len(production_rows))
    if write_progress:
        append_progress(len(mentor_rows), len(production_rows))
    return len(mentor_rows), len(production_rows)


def main() -> int:
    mentor_count, production_count = reconcile_two_layer_tables()
    print(
        f"[ADOBE-TWO-LAYER] mentor_rows={mentor_count} production_rows={production_count} "
        f"mentor={MENTOR_HUB} production={PRODUCTION_LINE}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
