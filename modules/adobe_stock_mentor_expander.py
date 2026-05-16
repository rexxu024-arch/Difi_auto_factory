"""Expand Adobe Stock mentor DNA into a daily production queue.

This is the Adobe equivalent of Mentor Hub -> Production Line, but it stays
physically separate from Printify/Etsy/eBay. The output is still no-upload:
it creates stock-safe prompt and metadata candidates for later image generation,
QA, and Adobe Contributor submission.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from adobe_stock_isolation import assert_adobe_write_paths
from adobe_stock_quality_policy import macro_prompt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

MENTOR_HUB = DATABASE / "Adobe_Stock_Mentor_Hub.csv"
EXPANDED_DNA = DATABASE / "Adobe_Stock_Mentor_DNA_Expanded.csv"
DAILY_QUEUE = DATABASE / "Adobe_Stock_Daily_Production_Queue.csv"
REPORT = REVIEW / "Adobe_Stock_Mentor_Expansion_latest.md"

EXPANDED_HEADERS = [
    "Expanded_DNA_ID",
    "Timestamp_ET",
    "Source_DNA_ID",
    "Family",
    "Product_Type",
    "Reference_Intent",
    "Material_Modifier",
    "Lighting_Modifier",
    "Composition_Modifier",
    "Camera_Protocol",
    "Prompt_Fragment",
    "Title_Fragment",
    "Keyword_Additions",
    "Negative_Prompt",
    "Risk_Guard",
    "Visual_DNA_Version",
    "Status",
]

DAILY_HEADERS = [
    "Queue_ID",
    "Timestamp_ET",
    "Expanded_DNA_ID",
    "Family",
    "Product_Type",
    "MJ_Prompt",
    "Target_Filename",
    "Adobe_Title",
    "Adobe_Keywords",
    "Adobe_Category",
    "Created_Using_AI",
    "Release_Required",
    "Required_Upscale",
    "Production_Eligibility",
    "Visual_DNA_Version",
    "QA_Status",
    "Upload_Status",
    "Status",
]

PRODUCT_TYPE_CYCLE = [
    "Macro_Material_Background",
    "Macro_Texture_Surface",
    "Macro_Commercial_Backdrop",
    "Macro_Material_Detail",
]

REFERENCE_INTENTS = [
    "premium interior design background",
    "brand presentation backdrop",
    "luxury packaging surface",
    "architectural mood board material",
    "editorial layout negative space",
    "social media product background",
    "website hero background",
    "printable decorative paper",
    "commercial texture overlay",
    "minimal desktop wallpaper",
]

MATERIAL_MODIFIERS = [
    "micro surface pores",
    "subtle anisotropic reflection",
    "restrained mineral veining",
    "soft matte finish",
    "fine tactile grain",
    "low-noise premium surface",
    "clean edge-to-edge field",
    "physically plausible roughness",
    "thin tonal variation",
    "quiet luxury restraint",
]

LIGHTING_MODIFIERS = [
    "dramatic studio side-lighting with controlled shadow falloff",
    "raking side light revealing micro relief",
    "low-key gallery light with tactile highlights",
    "single softbox side reflection with crisp texture contrast",
    "grazing light across raised material ridges",
    "cool executive studio light with high local contrast",
    "warm oblique studio light and clean specular edges",
    "chiaroscuro macro lighting without clipping",
    "directional side light with rich shadow rolloff",
    "commercial macro studio lighting with depth",
]

COMPOSITION_MODIFIERS = [
    "usable copy space at center",
    "edge-to-edge commercial background",
    "balanced asymmetry for layouts",
    "seamless repeat-friendly structure",
    "macro close crop with no object silhouette",
    "clean surface plate",
    "subtle diagonal movement",
    "quiet grid rhythm",
    "large negative-space band",
    "minimal pattern density",
]

CAMERA_PROTOCOLS = [
    "shot on 100mm macro lens, f/8, ultra-sharp focus",
    "100mm macro product photography, full material depth",
    "commercial macro capture, f/8, high micro-contrast",
    "100mm macro lens, controlled studio side-lighting",
    "ultra-photorealistic macro product surface capture",
]

PUBLIC_BAN_TERMS = {
    "openclaw",
    "rex",
    "grey",
    "gemini",
    "codex",
    "midjourney",
    "claude",
    "deepseek",
    "dify",
    "first audit",
    "etsy",
    "ebay",
    "printify",
    "sweatshop",
}

GENERIC_KEYWORD_TAIL = [
    "commercial use",
    "design resource",
    "digital background",
    "high resolution",
    "stock image",
    "graphic resource",
    "surface design",
    "abstract texture",
    "premium background",
    "editorial layout",
    "presentation background",
    "web banner",
    "packaging design",
    "copy space",
    "creative asset",
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def today_slug() -> str:
    return datetime.now(NY_TZ).strftime("%Y%m%d")


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


def clean_public_text(value: str) -> str:
    lowered = value.lower()
    for term in PUBLIC_BAN_TERMS:
        if term in lowered:
            raise ValueError(f"blocked public term in Adobe text: {term}")
    return " ".join(value.replace(",", " ").split())


def compact_slug(value: str) -> str:
    out = "".join(ch.lower() if ch.isalnum() else "_" for ch in value)
    while "__" in out:
        out = out.replace("__", "_")
    return out.strip("_")[:18] or "adobe"


def short_hash(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()[:8]


def unique_keywords(*parts: str, limit: int = 50) -> str:
    out: list[str] = []
    for part in parts:
        for raw in part.replace(";", ",").split(","):
            keyword = clean_public_text(raw.strip().lower())
            if not keyword or keyword in out:
                continue
            out.append(keyword)
    return ",".join(out[:limit])


def round_robin_by_family(rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    """Keep each daily Adobe batch broad enough to avoid similar-content risk."""
    buckets: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        family = row.get("Family", "").strip() or "unknown"
        buckets.setdefault(family, []).append(row)

    selected: list[dict[str, str]] = []
    while buckets and len(selected) < limit:
        progressed = False
        for family in sorted(list(buckets)):
            bucket = buckets.get(family, [])
            if not bucket:
                buckets.pop(family, None)
                continue
            selected.append(bucket.pop(0))
            progressed = True
            if len(selected) >= limit:
                break
            if not bucket:
                buckets.pop(family, None)
        if not progressed:
            break
    return selected


def product_type_for(index: int, family: str, asset_type: str) -> str:
    text = f"{family} {asset_type}".lower()
    if any(word in text for word in ("paper", "vellum", "background", "gradient")):
        preferred = ["Macro_Commercial_Backdrop", "Macro_Material_Background", "Macro_Texture_Surface", "Macro_Commercial_Backdrop"]
    elif any(word in text for word in ("metal", "wood", "stone", "mineral", "glass", "concrete", "fiber", "marble")):
        preferred = ["Macro_Texture_Surface", "Macro_Material_Detail", "Macro_Texture_Surface", "Macro_Material_Background"]
    else:
        preferred = PRODUCT_TYPE_CYCLE
    return preferred[index % len(preferred)]


def build_expanded(limit_per_family: int) -> list[dict[str, str]]:
    mentor_rows = read_csv(MENTOR_HUB)
    rows: list[dict[str, str]] = []
    for mentor in mentor_rows:
        source_id = mentor.get("DNA_ID", "")
        family = mentor.get("Family", "")
        base_dna = mentor.get("Gold_Visual_DNA", "")
        asset_type = mentor.get("Asset_Type", "")
        negative = mentor.get("Negative_Prompt", "")
        risk = mentor.get("Adobe_Risk_Guard", "")
        for index in range(1, limit_per_family + 1):
            intent = REFERENCE_INTENTS[(index - 1) % len(REFERENCE_INTENTS)]
            material = MATERIAL_MODIFIERS[(index + len(family)) % len(MATERIAL_MODIFIERS)]
            lighting = LIGHTING_MODIFIERS[(index * 2 + len(family)) % len(LIGHTING_MODIFIERS)]
            composition = COMPOSITION_MODIFIERS[(index * 3 + len(family)) % len(COMPOSITION_MODIFIERS)]
            camera = CAMERA_PROTOCOLS[(index + len(source_id)) % len(CAMERA_PROTOCOLS)]
            product_type = product_type_for(index, family, asset_type)
            expanded_id = f"{source_id}-V{index:02d}"
            material_type = f"{family} {asset_type} with {base_dna}, {intent}, {material}, {composition}, {lighting}, {camera}"
            prompt = clean_public_text(macro_prompt(material_type))
            title_fragment = clean_public_text(f"{family} {intent.title()} {material.title()}")[:70].strip()
            keyword_additions = unique_keywords(
                family,
                asset_type,
                intent,
                material,
                lighting,
                composition,
                ",".join(GENERIC_KEYWORD_TAIL),
            )
            rows.append(
                {
                    "Expanded_DNA_ID": expanded_id,
                    "Timestamp_ET": now_text(),
                    "Source_DNA_ID": source_id,
                    "Family": family,
                    "Product_Type": product_type,
                    "Reference_Intent": intent,
                    "Material_Modifier": material,
                    "Lighting_Modifier": lighting,
                    "Composition_Modifier": composition,
                    "Camera_Protocol": camera,
                    "Prompt_Fragment": prompt,
                    "Title_Fragment": title_fragment,
                    "Keyword_Additions": keyword_additions,
                    "Negative_Prompt": negative or "no people, no logo, no text, no watermark",
                    "Risk_Guard": risk,
                    "Visual_DNA_Version": "ADOBE_MACRO_PHOTO_V2",
                    "Status": "READY_FOR_MJ_GRID_NO_UPLOAD",
                }
            )
    return rows


def build_daily_queue(expanded_rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    balanced_rows = round_robin_by_family(expanded_rows, limit)
    for index, row in enumerate(balanced_rows, start=1):
        family_slug = compact_slug(row["Family"])
        filename = f"ad_{family_slug}_{today_slug()}_{index:03d}.jpg"
        # Adobe CSV filename max is 30 chars including extension.
        if len(filename) > 30:
            filename = f"ad_{family_slug[:8]}_{index:03d}_{short_hash(row['Expanded_DNA_ID'])}.jpg"
        title = clean_public_text(row["Title_Fragment"])[:70].strip()
        rows.append(
            {
                "Queue_ID": f"ADOBE-DAILY-{today_slug()}-{index:03d}",
                "Timestamp_ET": now_text(),
                "Expanded_DNA_ID": row["Expanded_DNA_ID"],
                "Family": row["Family"],
                "Product_Type": row["Product_Type"],
                "MJ_Prompt": row["Prompt_Fragment"],
                "Target_Filename": filename,
                "Adobe_Title": title,
                "Adobe_Keywords": row["Keyword_Additions"],
                "Adobe_Category": "8",
                "Created_Using_AI": "true",
                "Release_Required": "false",
                "Required_Upscale": "MIDJOURNEY_U_BUTTON_OR_2X_UPSCALE_REQUIRED",
                "Production_Eligibility": "BLOCKED_UNTIL_REAL_MJ_UPSCALE_SOURCE",
                "Visual_DNA_Version": row.get("Visual_DNA_Version", "ADOBE_MACRO_PHOTO_V2"),
                "QA_Status": "PENDING_IMAGE_GENERATION",
                "Upload_Status": "BLOCKED_UNTIL_IMAGE_AND_METADATA_QA",
                "Status": "READY_FOR_GENERATION_NO_UPLOAD",
            }
        )
    return rows


def write_report(expanded_rows: list[dict[str, str]], daily_rows: list[dict[str, str]]) -> None:
    families = sorted({row["Family"] for row in expanded_rows})
    product_counts: dict[str, int] = {}
    for row in daily_rows:
        product_counts[row["Product_Type"]] = product_counts.get(row["Product_Type"], 0) + 1
    lines = [
        "# Adobe Stock Mentor Expansion",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Mentor families: {len(families)}",
        f"- Expanded DNA rows: {len(expanded_rows)}",
        f"- Daily production queue rows: {len(daily_rows)}",
        f"- Expanded CSV: `{EXPANDED_DNA.relative_to(PROJECT_ROOT)}`",
        f"- Daily queue CSV: `{DAILY_QUEUE.relative_to(PROJECT_ROOT)}`",
        "",
        "## Production Mix",
        "",
    ]
    for key, value in sorted(product_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Discipline",
            "",
            "- These are stock bricks, not Etsy/eBay finished products.",
            "- No upload happens here; image generation and QA must pass first.",
            "- Public metadata is screened for internal OpenClaw/project words.",
            "",
            "## Next 10 Queue Rows",
            "",
        ]
    )
    for row in daily_rows[:10]:
        lines.append(f"- {row['Queue_ID']} | {row['Family']} | {row['Product_Type']} | {row['Adobe_Title']}")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def append_progress(expanded_count: int, daily_count: int) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock Mentor expansion built; expanded_dna={expanded_count}; "
            f"daily_queue={daily_count}; no upload/spend.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-family", type=int, default=20)
    parser.add_argument("--daily-limit", type=int, default=50)
    args = parser.parse_args()
    assert_adobe_write_paths((EXPANDED_DNA, DAILY_QUEUE, REPORT))
    expanded_rows = build_expanded(args.per_family)
    daily_rows = build_daily_queue(expanded_rows, args.daily_limit)
    write_csv(EXPANDED_DNA, expanded_rows, EXPANDED_HEADERS)
    write_csv(DAILY_QUEUE, daily_rows, DAILY_HEADERS)
    write_report(expanded_rows, daily_rows)
    append_progress(len(expanded_rows), len(daily_rows))
    print(f"[ADOBE-MENTOR-EXPAND] expanded={len(expanded_rows)} daily_queue={len(daily_rows)} report={REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
