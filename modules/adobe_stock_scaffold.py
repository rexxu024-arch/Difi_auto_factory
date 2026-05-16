"""Prepare Adobe Stock passive-fortress scaffold.

No upload happens here. This script creates a reusable metadata and keyword
pack for low-risk texture/background assets so the later FTP worker has a clean
input contract.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from adobe_stock_isolation import assert_adobe_write_paths
from adobe_stock_quality_policy import macro_prompt
from adobe_stock_two_layer_schema import reconcile_two_layer_tables


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
OUT_KEYWORDS = DATABASE / "Adobe_Stock_Keyword_Pack.csv"
OUT_SCHEMA = DATABASE / "Adobe_Stock_Metadata_Schema.csv"
OUT_MD = REVIEW / "Adobe_Stock_Passive_Fortress_Scaffold.md"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

KEYWORD_HEADERS = [
    "Family",
    "Asset_Type",
    "Prompt_Stem",
    "Title_Template",
    "Keyword_Seed",
    "Risk_Guard",
    "Production_Spec",
]

KEYWORD_ROWS = [
    {
        "Family": "Manhattan Order",
        "Asset_Type": "abstract architecture background",
        "Prompt_Stem": "4K seamless abstract material background with urban Art Deco stone geometry, brushed brass lines, quiet luxury grid, no logo, no text",
        "Title_Template": "Quiet Luxury Art Deco Stone and Brass Background",
        "Keyword_Seed": "art deco; abstract background; luxury texture; brass; stone; geometric; urban; architecture; interior design; premium; minimal; wallpaper; business; elegant; neutral",
        "Risk_Guard": "No recognizable skyline, brand, signage, or building facade.",
        "Production_Spec": "4K, 8-bit sRGB, Created using AI tools checked, no people, no text.",
    },
    {
        "Family": "Smoky Jade",
        "Asset_Type": "mineral texture",
        "Prompt_Stem": "4K macro mineral texture, smoky jade translucency, subtle veining, deep green gray, luxury stone background, physically plausible roughness",
        "Title_Template": "Smoky Jade Mineral Texture with Subtle Luxury Veining",
        "Keyword_Seed": "jade; mineral; texture; green; smoky; stone; luxury; macro; background; veining; translucent; abstract; natural; elegant; premium",
        "Risk_Guard": "Avoid figurative symbols, dragons, characters, and any cultural iconography.",
        "Production_Spec": "4K, sRGB, low noise, edge-to-edge usable background.",
    },
    {
        "Family": "Kintsugi Marble",
        "Asset_Type": "stone repair texture",
        "Prompt_Stem": "4K cracked marble background with restrained kintsugi gold repair lines, museum stone texture, matte surface, balanced negative space",
        "Title_Template": "Kintsugi Marble Texture with Subtle Gold Repair Lines",
        "Keyword_Seed": "kintsugi; marble; gold; cracked; repair; texture; stone; background; wabi sabi; luxury; abstract; neutral; elegant; design; surface",
        "Risk_Guard": "No readable symbols, no pottery trademark forms, no ornamental overload.",
        "Production_Spec": "4K, 8-bit sRGB, tile-safe variant optional.",
    },
    {
        "Family": "Brushed Titanium",
        "Asset_Type": "metal surface",
        "Prompt_Stem": "4K brushed titanium surface, micro scratches, cool gray industrial luxury, soft studio reflection, clean high-end material background",
        "Title_Template": "Brushed Titanium Industrial Luxury Metal Texture",
        "Keyword_Seed": "titanium; metal; brushed; industrial; gray; texture; background; modern; luxury; micro scratches; technology; design; surface; premium; clean",
        "Risk_Guard": "No device silhouettes, no logos, no futuristic UI elements.",
        "Production_Spec": "4K, sRGB, usable as product background or overlay.",
    },
    {
        "Family": "Archival Vellum",
        "Asset_Type": "paper texture",
        "Prompt_Stem": "4K archival vellum paper texture, subtle fibers, warm museum conservation tone, blank surface, no writing",
        "Title_Template": "Blank Archival Vellum Paper Texture with Subtle Fibers",
        "Keyword_Seed": "vellum; paper; texture; archival; blank; fibers; parchment; museum; warm; background; stationery; vintage; neutral; design; printable",
        "Risk_Guard": "No handwriting, no letters, no printed marks.",
        "Production_Spec": "4K, sRGB, high detail, copy-space safe.",
    },
    {
        "Family": "Obsidian Glass",
        "Asset_Type": "dark reflective background",
        "Prompt_Stem": "4K black obsidian glass texture, deep reflection, subtle smoke, luxury gallery surface, no object, no text",
        "Title_Template": "Black Obsidian Glass Luxury Reflective Background",
        "Keyword_Seed": "obsidian; black; glass; texture; reflective; dark; luxury; background; smoke; elegant; premium; abstract; modern; surface; dramatic",
        "Risk_Guard": "No occult symbols, no faces, no readable elements.",
        "Production_Spec": "4K, sRGB, contrast checked, not clipped.",
    },
    {
        "Family": "Nero Marble",
        "Asset_Type": "black stone texture",
        "Prompt_Stem": "4K nero marble slab texture, black stone, ivory mineral veins, gallery-grade luxury surface, realistic polished depth",
        "Title_Template": "Black Nero Marble Texture with Ivory Stone Veining",
        "Keyword_Seed": "black marble; nero marble; stone texture; luxury background; ivory veins; polished stone; interior design; premium surface; dark texture; elegant; architecture; slab; natural material; graphic resource; backdrop",
        "Risk_Guard": "No recognizable object, brand, lettering, face, or religious/occult symbol.",
        "Production_Spec": "4K, 8-bit sRGB, commercial stone texture, no clipped highlights.",
    },
    {
        "Family": "Travertine Plaster",
        "Asset_Type": "warm limestone plaster texture",
        "Prompt_Stem": "4K warm travertine plaster wall texture, limestone pores, quiet luxury neutral beige, hand-troweled matte surface",
        "Title_Template": "Warm Travertine Plaster Wall Texture Neutral Background",
        "Keyword_Seed": "travertine; plaster; limestone; wall texture; beige background; neutral; interior design; quiet luxury; matte surface; trowel; mineral; natural stone; warm minimal; architecture; design resource",
        "Risk_Guard": "No building facade, no brand, no graffiti, no readable marks.",
        "Production_Spec": "4K, sRGB, negative-space friendly, useful for branding and interior mockups.",
    },
    {
        "Family": "Walnut Burl",
        "Asset_Type": "dark wood grain texture",
        "Prompt_Stem": "4K dark walnut burl wood grain texture, executive desk warmth, organic rings, satin finish, luxury furniture surface",
        "Title_Template": "Dark Walnut Burl Wood Grain Texture Executive Surface",
        "Keyword_Seed": "walnut; burl wood; wood grain; dark wood; furniture texture; executive desk; luxury interior; organic pattern; satin finish; brown background; natural material; premium surface; carpentry; design resource; backdrop",
        "Risk_Guard": "No furniture silhouette, no brand mark, no recognizable manufactured product.",
        "Production_Spec": "4K, sRGB, high-detail grain without moire artifacts.",
    },
    {
        "Family": "Aged Bronze Patina",
        "Asset_Type": "oxidized metal texture",
        "Prompt_Stem": "4K aged bronze patina metal texture, museum oxidized surface, teal verdigris, warm brass undertone, macro material field",
        "Title_Template": "Aged Bronze Patina Metal Texture with Verdigris Surface",
        "Keyword_Seed": "bronze; patina; verdigris; oxidized metal; teal; brass; antique texture; museum surface; metal background; aged material; luxury texture; macro; industrial design; graphic resource; premium",
        "Risk_Guard": "No statue, no coin, no artifact shape, no cultural object, no text.",
        "Production_Spec": "4K, sRGB, material-only plate, no protected artifact reference.",
    },
    {
        "Family": "Linen Canvas",
        "Asset_Type": "woven textile texture",
        "Prompt_Stem": "4K natural linen canvas weave texture, off-white fibers, tactile gallery fabric, matte textile background",
        "Title_Template": "Natural Linen Canvas Weave Texture Off White Background",
        "Keyword_Seed": "linen; canvas; fabric texture; textile; weave; off white; natural fibers; background; craft; neutral; tactile; matte; design resource; editorial layout; printable texture",
        "Risk_Guard": "No clothing item, no logo, no embroidery, no readable label.",
        "Production_Spec": "4K, sRGB, sharp weave detail without harsh aliasing.",
    },
    {
        "Family": "Architectural Concrete",
        "Asset_Type": "minimal concrete texture",
        "Prompt_Stem": "4K architectural concrete texture, cool gray micro pores, brutalist minimal wall surface, soft studio gradient",
        "Title_Template": "Minimal Architectural Concrete Texture Cool Gray Background",
        "Keyword_Seed": "concrete; gray background; architectural texture; brutalist; wall surface; minimal; cement; micro pores; industrial; modern design; neutral backdrop; construction material; graphic resource; premium surface; copy space",
        "Risk_Guard": "No recognizable building, no signage, no graffiti, no cracks forming readable marks.",
        "Production_Spec": "4K, sRGB, clean commercial backdrop with copy-space variants.",
    },
    {
        "Family": "Carbon Fiber",
        "Asset_Type": "woven technical material texture",
        "Prompt_Stem": "4K carbon fiber weave texture, dark graphite technical material, subtle anisotropic reflection, premium performance surface",
        "Title_Template": "Dark Carbon Fiber Weave Texture Premium Graphite Background",
        "Keyword_Seed": "carbon fiber; graphite; weave texture; technical material; dark background; performance; automotive; aerospace; pattern; modern; industrial design; premium; black texture; composite; design resource",
        "Risk_Guard": "No vehicle parts, no logo, no dashboard, no brandable product silhouette.",
        "Production_Spec": "4K, sRGB, repeat-friendly technical texture, no moire.",
    },
    {
        "Family": "Champagne Frosted Glass",
        "Asset_Type": "soft luxury gradient background",
        "Prompt_Stem": "4K champagne frosted glass background, soft translucent gradient, premium product backdrop, subtle studio caustics",
        "Title_Template": "Champagne Frosted Glass Gradient Luxury Background",
        "Keyword_Seed": "champagne; frosted glass; gradient background; luxury backdrop; translucent; soft light; product background; premium; warm neutral; glass texture; studio; elegant; abstract; design resource; copy space",
        "Risk_Guard": "No bottle, no alcohol branding, no logo, no readable label, no luxury brand reference.",
        "Production_Spec": "4K, sRGB, smooth commercial gradient with subtle texture, copy-space friendly.",
    },
]

SCHEMA_ROWS = [
    {"Field": "filename", "Rule": "Stable ASCII filename, 30 chars or fewer including extension."},
    {"Field": "title", "Rule": "Simple commercial stock title, 70 chars or fewer, no comma, no brand or protected style name."},
    {"Field": "keywords", "Rule": "35-49 keywords ordered by search value; title concepts must appear in the top 10."},
    {"Field": "category", "Rule": "Use Adobe category 8, Graphic Resources, for backgrounds and textures."},
    {"Field": "created_using_ai", "Rule": "Always true internally; manually check Created using generative AI tools in Contributor portal."},
    {"Field": "release_required", "Rule": "False unless people/property marks appear; QA should block those before upload."},
    {"Field": "color_space", "Rule": "sRGB 8-bit."},
    {"Field": "resolution", "Rule": "Minimum 4K long edge; no upscale artifacts or watermark remnants."},
]

for row in KEYWORD_ROWS:
    # Rex rejected the old flat stock-texture direction on 2026-05-16.
    # Keep the family/SEO scaffold, but force every prompt stem through the
    # macro-photography production contract so this module cannot re-seed
    # low-value orthographic/flat assets.
    row["Prompt_Stem"] = macro_prompt(row["Family"])
    row["Production_Spec"] = (
        "MJ U-button or 2x-upscaled macro-photography source; 8-bit sRGB; "
        "OpenClaw gate >=8MP and short edge >=2200px; no flat grid slices."
    )


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def write_table(path: Path, rows: list[dict[str, str]], headers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def write_report() -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Adobe Stock Passive Fortress Scaffold",
        "",
        f"Generated: {now_text()}",
        "",
        "This scaffold is intentionally no-upload. It prepares the stock-image worker for texture/background assets, not finished OpenClaw hero art.",
        "",
        "## Production Discipline",
        "",
        "- Produce bricks, not temples: textures, backgrounds, material fields.",
        "- Do not reuse Etsy/First Audit hero assets.",
        "- Always mark Created using AI tools.",
        "- Block brands, landmarks, readable text, faces, and protected artist references.",
        "- Keep output suitable for 4K 8-bit sRGB stock submission.",
        "",
        "## Families",
        "",
    ]
    for row in KEYWORD_ROWS:
        lines.extend(
            [
                f"### {row['Family']}",
                "",
                f"- Asset type: {row['Asset_Type']}",
                f"- Title template: {row['Title_Template']}",
                f"- Prompt stem: `{row['Prompt_Stem']}`",
                f"- Keywords: {row['Keyword_Seed']}",
                f"- Guard: {row['Risk_Guard']}",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def append_progress() -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Built Adobe Stock scaffold; families={len(KEYWORD_ROWS)}; "
            f"keywords={OUT_KEYWORDS.relative_to(PROJECT_ROOT)}; schema={OUT_SCHEMA.relative_to(PROJECT_ROOT)}.\n"
        )


def main() -> None:
    assert_adobe_write_paths((OUT_KEYWORDS, OUT_SCHEMA, OUT_MD))
    write_table(OUT_KEYWORDS, KEYWORD_ROWS, KEYWORD_HEADERS)
    write_table(OUT_SCHEMA, SCHEMA_ROWS, ["Field", "Rule"])
    write_report()
    mentor_count, production_count = reconcile_two_layer_tables(write_progress=False)
    append_progress()
    print(f"[ADOBE-SCAFFOLD] families={len(KEYWORD_ROWS)} keywords={OUT_KEYWORDS}")
    print(f"[ADOBE-SCAFFOLD] schema={OUT_SCHEMA}")
    print(f"[ADOBE-SCAFFOLD] packet={OUT_MD}")
    print(f"[ADOBE-SCAFFOLD] two_layer mentor={mentor_count} production={production_count}")


if __name__ == "__main__":
    main()
