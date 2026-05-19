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
REX_FEEDBACK_WEIGHTS = DATABASE / "Adobe_Stock_Rex_Feedback_Weights.csv"
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
    "shot on 100mm macro lens, f/8, ultra-sharp deep focus across the material plane",
    "100mm macro product photography, full material depth, broad crop-safe sharpness",
    "commercial macro capture, f/8, high micro-contrast, no shallow depth of field",
    "100mm macro lens, controlled studio side-lighting, foreground and background kept usable",
    "ultra-photorealistic macro product surface capture with wide sharp texture coverage",
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

# First real Adobe submit batch: use only families Rex has approved as clear,
# useful stock material/backdrop candidates. Weak families are not deleted; they
# are parked until cleaner DNA exists.
FIRST_SUBMIT_ALLOWED_FAMILIES = {
    "Kintsugi Marble",
    "Nero Marble",
    "Walnut Burl",
    "Smoky Jade",
    "Manhattan Order",
    "Clean Architectural Concrete",
    "Obsidian Glass",
}

FIRST_SUBMIT_DEFERRED_FAMILIES = {
    "Aged Bronze Patina",
    "Architectural Concrete",
    "Archival Vellum",
    "Brushed Titanium",
    "Carbon Fiber",
    "Linen Canvas",
    "Travertine Plaster",
    "Champagne Frosted Glass",
}

STOCK_USE_KEYWORDS = {
    "Macro_Material_Background": ["copy space", "blank background", "empty space", "template"],
    "Macro_Texture_Surface": ["surface", "material", "pattern", "wallpaper"],
    "Macro_Commercial_Backdrop": ["backdrop", "product design", "branding background", "mockup background"],
    "Macro_Material_Detail": ["macro", "close up", "detail", "surface"],
}

GENERIC_STOCK_KEYWORDS = [
    "abstract",
    "design",
    "decorative",
    "graphic resource",
    "high resolution",
    "commercial use",
    "packaging design",
    "web banner",
    "presentation background",
    "editorial layout",
]

REX_REMAKE_CLEANER_CLAUSE = (
    "clean controlled commercial surface, sharply resolved micro-detail, no muddy stains, "
    "no chaotic dirt, no clutter, no random artifacts, no painterly smearing, "
    "copy-space friendly, crisp material detail, stock-usable background"
)

REX_HOLD_REFINEMENT_CLAUSE = (
    "cleaner stock background, restrained texture density, clear micro-detail, "
    "less grime, less chaos, more usable negative space"
)

KEYWORD_STOPWORDS = {"and", "with", "for", "the", "space", "copy"}
KEYWORD_DROP_TERMS = {
    "premium interior",
    "quiet luxury",
    "dramatic studio",
    "controlled shadow",
    "physically plausible",
    "negative-space",
}


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


def stock_subject(family: str) -> str:
    return TITLE_FAMILY_ALIASES.get(family, family).lower()


def title_word_keywords(title: str) -> list[str]:
    words = [word for word in title.lower().split() if len(word) > 2 and word not in KEYWORD_STOPWORDS]
    out: list[str] = []
    for word in words:
        if word not in out:
            out.append(word)
    return out


def stock_title(family: str, product_type: str) -> str:
    subject = TITLE_FAMILY_ALIASES.get(family, family)
    use_case = TITLE_USE_CASES.get(product_type, "Texture Background for Design Projects")
    title = clean_public_text(f"{subject} {use_case}").lower()
    if len(title) <= 70:
        return title[:1].upper() + title[1:]
    fallback = clean_public_text(f"{subject} Texture Background")
    fallback = fallback.lower()[:70].rstrip()
    return fallback[:1].upper() + fallback[1:]


def unique_keywords(*parts: str, limit: int = 50) -> str:
    out: list[str] = []
    for part in parts:
        for raw in part.replace(";", ",").split(","):
            keyword = clean_public_text(raw.strip().lower())
            if any(term in keyword for term in KEYWORD_DROP_TERMS):
                continue
            if len(keyword) > 42:
                continue
            if not keyword or keyword in out:
                continue
            out.append(keyword)
    return ",".join(out[:limit])


def stock_keywords(family: str, asset_type: str, product_type: str, title: str, *modifiers: str) -> str:
    """Build Adobe-style keywords from observed stock texture patterns.

    The first 10 keywords must cover the title terms because Adobe's own
    guidance gives title concepts extra relevance when they appear early.
    """
    subject = stock_subject(family)
    title_terms = title_word_keywords(title)
    first_ten = [
        subject,
        f"{subject} texture",
        "texture background",
        "background",
        "texture",
        *title_terms,
    ]
    use_terms = STOCK_USE_KEYWORDS.get(product_type, [])
    candidate_parts = [
        ",".join(first_ten),
        asset_type,
        ",".join(use_terms),
        ",".join(GENERIC_STOCK_KEYWORDS),
        ",".join(modifiers),
    ]
    keywords = unique_keywords(*candidate_parts, limit=49)
    # Keep metadata concise: 25-35 strong keywords beat weak stuffing.
    return ",".join(keywords.split(",")[:32])


def load_rex_feedback_weights() -> dict[str, dict[str, str]]:
    """Load Rex visual feedback so generation follows approved aesthetics first."""
    rows = read_csv(REX_FEEDBACK_WEIGHTS)
    return {row.get("Family", "").strip(): row for row in rows if row.get("Family")}


def family_limit(base_limit: int, family: str, feedback: dict[str, dict[str, str]]) -> int:
    row = feedback.get(family, {})
    try:
        weight = float(row.get("Weight") or 1.0)
    except ValueError:
        weight = 1.0
    # More rows for approved families, fewer for rejected families, but do not ban
    # a material family solely from one weak batch.
    return max(4, min(40, int(round(base_limit * weight))))


def is_first_submit_safe_family(family: str, feedback: dict[str, dict[str, str]]) -> bool:
    """Hard gate for Adobe's first real submit batch."""
    if family in FIRST_SUBMIT_DEFERRED_FAMILIES:
        return False
    if family in FIRST_SUBMIT_ALLOWED_FAMILIES:
        return True
    action = (feedback.get(family, {}).get("Action") or "").upper()
    return action == "INCREASE_NIGHT_GENERATION"


def feedback_refinement_clause(family: str, feedback: dict[str, dict[str, str]]) -> str:
    action = (feedback.get(family, {}).get("Action") or "").upper()
    if action == "REMAKE_DNA_CLEANER_SHARPER_NOT_BANNED":
        return REX_REMAKE_CLEANER_CLAUSE
    if action == "HOLD_MORE_EVIDENCE":
        return REX_HOLD_REFINEMENT_CLAUSE
    return ""


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


def build_expanded(limit_per_family: int, strict_first_submit: bool = True) -> list[dict[str, str]]:
    mentor_rows = read_csv(MENTOR_HUB)
    feedback = load_rex_feedback_weights()
    rows: list[dict[str, str]] = []
    for mentor in mentor_rows:
        source_id = mentor.get("DNA_ID", "")
        family = mentor.get("Family", "")
        if strict_first_submit and not is_first_submit_safe_family(family, feedback):
            continue
        base_dna = mentor.get("Gold_Visual_DNA", "")
        asset_type = mentor.get("Asset_Type", "")
        negative = mentor.get("Negative_Prompt", "")
        risk = mentor.get("Adobe_Risk_Guard", "")
        adjusted_limit = family_limit(limit_per_family, family, feedback)
        rex_refinement = feedback_refinement_clause(family, feedback)
        for index in range(1, adjusted_limit + 1):
            intent = REFERENCE_INTENTS[(index - 1) % len(REFERENCE_INTENTS)]
            material = MATERIAL_MODIFIERS[(index + len(family)) % len(MATERIAL_MODIFIERS)]
            lighting = LIGHTING_MODIFIERS[(index * 2 + len(family)) % len(LIGHTING_MODIFIERS)]
            composition = COMPOSITION_MODIFIERS[(index * 3 + len(family)) % len(COMPOSITION_MODIFIERS)]
            camera = CAMERA_PROTOCOLS[(index + len(source_id)) % len(CAMERA_PROTOCOLS)]
            product_type = product_type_for(index, family, asset_type)
            expanded_id = f"{source_id}-V{index:02d}"
            variation_token = short_hash(f"{expanded_id}|{family}|{intent}|{material}|{lighting}|{composition}")
            material_type = f"{family} {asset_type} with {base_dna}, {intent}, {material}, {composition}, {lighting}, {camera}"
            material_type = (
                f"{material_type}, distinct non-repeating stock variation {variation_token}, "
                "unique vein layout and crop geometry, visibly different from sibling assets"
            )
            if rex_refinement:
                material_type = f"{material_type}, visual QA refinement: {rex_refinement}"
            prompt = clean_public_text(macro_prompt(material_type))
            title_fragment = stock_title(family, product_type)
            keyword_additions = stock_keywords(
                family,
                asset_type,
                product_type,
                title_fragment,
                intent,
                material,
                composition,
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
                    "Negative_Prompt": (
                        negative
                        or "no people, no logo, no text, no watermark, no bokeh, no shallow depth of field, no blurred foreground, no blurred background"
                    ),
                    "Risk_Guard": risk,
                    "Visual_DNA_Version": "ADOBE_MACRO_PHOTO_V4_DEEP_FOCUS_REX_WEIGHTED",
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
                "Required_Upscale": "NO_FAST_NO_CREATIVE_UPSCALE; SELECTED_MJ_U_BUTTON_FULL_RES_REQUIRED",
                "Production_Eligibility": "BLOCKED_UNTIL_SELECTED_U_FULL_RES_SOURCE",
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
            "- First-submit strict mode is active: weak/rejected families are deferred, not silently uploaded.",
            "- No upload happens here; image generation and QA must pass first.",
            "- Public metadata is screened for internal OpenClaw/project words.",
            "",
            "## Deferred Until Cleaner DNA",
            "",
        ]
    )
    for family in sorted(FIRST_SUBMIT_DEFERRED_FAMILIES):
        lines.append(f"- {family}")
    lines.extend(
        [
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
    parser.add_argument(
        "--include-deferred-families",
        action="store_true",
        help="Disable Rex first-submit hard gate; only use after weak families have cleaner approved DNA.",
    )
    args = parser.parse_args()
    assert_adobe_write_paths((EXPANDED_DNA, DAILY_QUEUE, REPORT))
    expanded_rows = build_expanded(args.per_family, strict_first_submit=not args.include_deferred_families)
    daily_rows = build_daily_queue(expanded_rows, args.daily_limit)
    write_csv(EXPANDED_DNA, expanded_rows, EXPANDED_HEADERS)
    write_csv(DAILY_QUEUE, daily_rows, DAILY_HEADERS)
    write_report(expanded_rows, daily_rows)
    append_progress(len(expanded_rows), len(daily_rows))
    print(f"[ADOBE-MENTOR-EXPAND] expanded={len(expanded_rows)} daily_queue={len(daily_rows)} report={REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
