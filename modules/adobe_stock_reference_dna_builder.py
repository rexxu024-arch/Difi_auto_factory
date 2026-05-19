"""Build a reference-driven Adobe Stock material DNA packet.

Public Adobe Stock pages do not expose reliable download counts. Until Rex
adds a paid market-data source, use high-relevance public search examples,
official contributor rules, and texture-market pages as proxy evidence. The
goal is to extract reusable structure, not copy images or clone exact assets.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
OUT_CSV = DATABASE / "Adobe_Stock_Reference_DNA.csv"
OUT_REPORT = REVIEW / "Adobe_Stock_Reference_DNA_latest.md"
NY_TZ = ZoneInfo("America/New_York")


FIELDS = [
    "Reference_ID",
    "Source_URL",
    "Proxy_Signal",
    "Visible_Title_Pattern",
    "Visible_Dimensions",
    "Category",
    "Author_or_Source",
    "Keyword_Cluster",
    "Visual_Commonality",
    "Usable_DNA",
    "OpenClaw_Adaptation",
    "Do_Not_Copy",
]


REFERENCE_ROWS = [
    {
        "Reference_ID": "ADS-REF-BRONZE-001",
        "Source_URL": "https://stock.adobe.com/ar/images/seamless-rusted-copper-metal-patina-texture-background-vintage-bronze-tileable-antique-pattern-backdrop/493697674",
        "Proxy_Signal": "Adobe Stock search result; 8192x4096 JPEG; graphic resources; keyword-rich texture asset",
        "Visible_Title_Pattern": "Seamless rusted copper metal patina texture background. Vintage bronze tileable antique pattern backdrop.",
        "Visible_Dimensions": "8192 x 4096 px",
        "Category": "Graphic Resources",
        "Author_or_Source": "Unleashed Design",
        "Keyword_Cluster": "seamless,copper,metal,patina,texture,background,vintage,bronze,antique,pattern,grunge,old,brass,iron,material,rust",
        "Visual_Commonality": "high resolution, tile-friendly, material-first title, vintage patina terms, clear commercial texture use",
        "Usable_DNA": "oxidized bronze/copper surface, teal-green verdigris over warm brown metal, edge-to-edge field, no object silhouette",
        "OpenClaw_Adaptation": "aged bronze patina macro texture background; keep bronze/verdigris terms early; avoid finished sculpture or brand cues",
        "Do_Not_Copy": "Do not copy source image; extract only metadata structure and material behavior",
    },
    {
        "Reference_ID": "ADS-REF-KINTSUGI-001",
        "Source_URL": "https://stock.adobe.com/pl/images/abstract-black-marble-background-with-golden-veins-japanese-kintsugi-technique-fake-painted-artificial-stone-texture-marbled-surface-digital-marbling-illustration/351851710",
        "Proxy_Signal": "Adobe Stock search result; 6000x4000 JPEG; graphic resources; direct keyword cluster for marble/kintsugi",
        "Visible_Title_Pattern": "abstract black marble background with golden veins, japanese kintsugi technique, fake painted artificial stone texture, marbled surface",
        "Visible_Dimensions": "6000 x 4000 px",
        "Category": "Graphic Resources",
        "Author_or_Source": "wacomka",
        "Keyword_Cluster": "abstract,marble,background,texture,black,gold,veins,crack,granite,luxury,modern,minimal,stone,surface,pattern,wallpaper,interior",
        "Visual_Commonality": "dark stone base, gold vein contrast, large background field, title states exact subject and style",
        "Usable_DNA": "black marble field, controlled gold kintsugi cracks, macro stone grain, enough open area for layout",
        "OpenClaw_Adaptation": "black marble macro texture background; kintsugi marble texture background; keep 'japanese culture' optional and not overused",
        "Do_Not_Copy": "Do not clone crack layout; generate new mineral veining and abstract repair paths",
    },
    {
        "Reference_ID": "ADS-REF-KINTSUGI-002",
        "Source_URL": "https://stock.adobe.com/images/seamless-luxury-kintsugi-pattern-n-golden-cracks-on-white-marble-texture/1841615919",
        "Proxy_Signal": "Adobe Stock search result; vector/JPEG; seamless luxury kintsugi phrase",
        "Visible_Title_Pattern": "Seamless Luxury Kintsugi Pattern - Golden Cracks on White Marble Texture",
        "Visible_Dimensions": "SVG and JPEG",
        "Category": "Graphic Resources",
        "Author_or_Source": "Farjana",
        "Keyword_Cluster": "seamless pattern,japanese culture,kintsugi,golden cracks,white marble,texture,luxury,background",
        "Visual_Commonality": "simple title, seamless pattern promise, luxury material keyword, high buyer clarity",
        "Usable_DNA": "white/cream stone plane with gold repair lines; repeat-friendly; not too painterly",
        "OpenClaw_Adaptation": "cream kintsugi marble texture background; use as safer light variant against dark kintsugi",
        "Do_Not_Copy": "Do not use identical white-marble/gold-crack layout",
    },
    {
        "Reference_ID": "ADS-REF-MARBLE-001",
        "Source_URL": "https://www.everypixel.com/image-6582928415042533978",
        "Proxy_Signal": "Stock aggregator keyword page; useful broad buyer keyword cluster for black marble",
        "Visible_Title_Pattern": "Black marble texture background High resolution.",
        "Visible_Dimensions": "not provided in snippet",
        "Category": "Stock Image",
        "Author_or_Source": "Everypixel index",
        "Keyword_Cluster": "copy space,backdrop,stone material,architecture,flooring,decor,abstract,material,backgrounds,wallpaper,design,luxury,marble,smooth,dark,black marble texture,marble pattern",
        "Visual_Commonality": "buyer terms include decor, architecture, flooring, wallpaper, copy space, design",
        "Usable_DNA": "dark marble surface, natural veins, polished/smooth surface, flexible interior/design use",
        "OpenClaw_Adaptation": "black marble texture background; include architecture/decor/design/copy space secondary terms",
        "Do_Not_Copy": "Use keyword structure only",
    },
    {
        "Reference_ID": "ADS-REF-WOOD-001",
        "Source_URL": "https://elements.envato.com/textured-wooden-background-collection-TYGFTBN",
        "Proxy_Signal": "Commercial texture collection; high-resolution pack language; buyer-use framing",
        "Visible_Title_Pattern": "Textured Wooden Background collection, backgrounds, textures, patterns",
        "Visible_Dimensions": "8256 x 5504 px collection note",
        "Category": "Texture Pack",
        "Author_or_Source": "Envato Elements listing",
        "Keyword_Cluster": "wood grain,veneer,background,texture,pattern,high resolution,photographs,scans,photoshop,layer effects",
        "Visual_Commonality": "collection framing, real photo/scan credibility, high resolution stated, flexible editing use",
        "Usable_DNA": "wood grain macro, veneer sheet, continuous surface, directional fibers, warm/cool variants",
        "OpenClaw_Adaptation": "walnut wood texture background; walnut burl macro; keep practical design-use terms",
        "Do_Not_Copy": "No source image copying; only use pack-positioning logic",
    },
    {
        "Reference_ID": "ADS-REF-PBR-001",
        "Source_URL": "https://www.poliigon.com/texture/patina-metal-texture-worn-bronze/7158",
        "Proxy_Signal": "Premium PBR texture market; 1K-8K resolutions; material realism requirements",
        "Visible_Title_Pattern": "Worn Patina Metal Texture",
        "Visible_Dimensions": "1K, 2K, 4K, 8K texture set",
        "Category": "PBR Texture",
        "Author_or_Source": "Poliigon",
        "Keyword_Cluster": "worn bronze,patina metal,architectural visualization,industrial scenes,realistic,high resolution,3D metal material,displacement,normals,reflection",
        "Visual_Commonality": "serious texture buyers care about realism, maps, scale, patina layering, not decorative slogans",
        "Usable_DNA": "layered oxidized bronze, realistic roughness, high-frequency surface variation, believable metal aging",
        "OpenClaw_Adaptation": "aged bronze patina macro texture background; emphasize real material depth and oxidation layers",
        "Do_Not_Copy": "Extract realism requirements only",
    },
    {
        "Reference_ID": "ADS-REF-LINEN-001",
        "Source_URL": "https://stock.adobe.com/images/high-resolution-linen-canvas-texture-background/38073490",
        "Proxy_Signal": "Adobe Stock search result; 5492x3662 JPEG; direct 'high resolution linen canvas texture background' buyer wording",
        "Visible_Title_Pattern": "High resolution linen canvas texture background",
        "Visible_Dimensions": "5492 x 3662 px",
        "Category": "Fabrics and Canvas Textures",
        "Author_or_Source": "Ekaterina Lin",
        "Keyword_Cluster": "linen,canvas,textile,background,pattern,texture,white,material,woven,beige,fiber,fabric,cotton,empty,macro,blank,rough,full frame,copy space",
        "Visual_Commonality": "flat commercial utility, high resolution claim, fabric/canvas front-loaded, copy-space and blank-use terms",
        "Usable_DNA": "woven fabric field, visible fibers, beige/white natural tone, continuous surface, no decorative subject",
        "OpenClaw_Adaptation": "linen canvas texture background; generate warm and cool variants as stock-safe neutral backgrounds",
        "Do_Not_Copy": "No source image copying; preserve only texture-market title/keyword logic",
    },
    {
        "Reference_ID": "ADS-REF-CARBON-001",
        "Source_URL": "https://stock.adobe.com/pl/images/black-carbon-fiber-macro-texture-pattern-of-textile-fibres-material-light-carbon-fibre-fabric-seamless-dark-vector-background/192085570",
        "Proxy_Signal": "Adobe Stock search result; vector/JPEG; high buyer clarity for tech material backgrounds",
        "Visible_Title_Pattern": "Black carbon fiber macro texture. Pattern of textile fibres material. Light carbon fibre fabric seamless dark vector background",
        "Visible_Dimensions": "AI/EPS and JPEG",
        "Category": "Graphic Resources",
        "Author_or_Source": "fim.design",
        "Keyword_Cluster": "carbon,fiber,pattern,seamless,texture,fabric,black,background,material,surface,strong,industrial,dark,metal,composite,light,macro,technology,rough",
        "Visual_Commonality": "macro woven pattern, dark industrial palette, technology/industrial secondary keywords, seamless promise",
        "Usable_DNA": "black woven carbon fiber plane, specular edge highlights, diagonal textile pattern, continuous surface",
        "OpenClaw_Adaptation": "carbon fiber macro texture background; keep black/fiber/technology/material keywords early",
        "Do_Not_Copy": "Do not clone weave orientation or image; use material physics only",
    },
    {
        "Reference_ID": "ADS-REF-PAPER-001",
        "Source_URL": "https://www.freepik.com/premium-photo/vintage-paper-texture-background-with-copy-space-space-text_16110051.htm",
        "Proxy_Signal": "Commercial stock result; explicit copy-space buyer phrase and broad paper keyword cluster",
        "Visible_Title_Pattern": "Vintage paper texture background with copy space and space for text",
        "Visible_Dimensions": "not provided in snippet",
        "Category": "Stock Image",
        "Author_or_Source": "Freepik premium photo",
        "Keyword_Cluster": "vintage,paper,texture,background,copy space,parchment,cardboard,grunge,brown,material,rough,grain,old,surface,page,blank",
        "Visual_Commonality": "copy-space title, simple aged paper subject, design/invitation/scrapbook utility rather than art object",
        "Usable_DNA": "aged parchment surface, subtle stains, fiber grain, usable blank central area, warm neutral palette",
        "OpenClaw_Adaptation": "vintage paper texture background with copy space; useful as lower-risk high-volume stock family",
        "Do_Not_Copy": "Do not reproduce layout/stain map; use buyer-intent vocabulary and blank-space structure",
    },
    {
        "Reference_ID": "ADS-REF-CONCRETE-001",
        "Source_URL": "https://www.everypixel.com/search?q=concrete+wall+texture+background",
        "Proxy_Signal": "Stock aggregator keyword pattern for concrete/wall/background usage",
        "Visible_Title_Pattern": "Concrete wall texture background / gray concrete surface",
        "Visible_Dimensions": "varies by indexed source",
        "Category": "Stock Image",
        "Author_or_Source": "Everypixel index",
        "Keyword_Cluster": "concrete,wall,texture,background,gray,cement,surface,rough,grunge,industrial,architecture,material,copy space,abstract,blank",
        "Visual_Commonality": "generic but highly usable architecture material terms; strongest when flat enough for overlays",
        "Usable_DNA": "matte gray cement plane, small pits and trowel marks, soft side light, open usable field",
        "OpenClaw_Adaptation": "concrete wall macro texture background; avoid object-like sculptural closeups unless clearly background usable",
        "Do_Not_Copy": "Use keyword cluster and material constraints only",
    },
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def write_csv() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(REFERENCE_ROWS)


def write_report() -> None:
    lines = [
        "# Adobe Stock Reference DNA",
        "",
        f"Generated: {now_text()}",
        "",
        "## Interpretation",
        "",
        "- Adobe public pages rarely expose true download counts, so this packet uses high-relevance public stock results and commercial texture listings as proxy evidence.",
        "- Use these references to copy metadata structure and buyer intent, not source images or exact compositions.",
        "- Immediate lesson: winners are practical material/background bricks with direct titles, useful keywords, high resolution, and clear commercial use cases.",
        "",
        "## Extracted DNA Families",
        "",
    ]
    for row in REFERENCE_ROWS:
        lines.extend(
            [
                f"### {row['Reference_ID']}",
                "",
                f"- Source: {row['Source_URL']}",
                f"- Proxy signal: {row['Proxy_Signal']}",
                f"- Title pattern: {row['Visible_Title_Pattern']}",
                f"- Keywords: {row['Keyword_Cluster']}",
                f"- Usable DNA: {row['Usable_DNA']}",
                f"- OpenClaw adaptation: {row['OpenClaw_Adaptation']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Rules Applied To Queue",
            "",
            "- Do not invent from a blank page.",
            "- Titles: material + texture/background + use case.",
            "- Keywords: first 10 must contain title concepts; keep 25-35 strong terms.",
            "- Image outputs: relaxed MJ grids, then selected U-button/full-res assets only.",
            "- Upload only after image QA and metadata QA pass.",
        ]
    )
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress() -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock reference-driven DNA packet rebuilt; "
            f"references={len(REFERENCE_ROWS)}; no upload/spend.\n"
        )


def main() -> int:
    write_csv()
    write_report()
    append_progress()
    print(f"[ADOBE-REFERENCE-DNA] rows={len(REFERENCE_ROWS)} csv={OUT_CSV} report={OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
