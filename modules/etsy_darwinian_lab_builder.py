"""Build the V7 Etsy Darwinian Lab experiment queue.

This is a planning/staging module. It creates the six 10-listing test pools
requested by Rex without publishing listings or spending Etsy listing fees.
Each row becomes a candidate production job for later asset generation, QA, and
fee-guarded Etsy launch.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "Database"
REVIEW = ROOT / "Review_Packets"
NY_TZ = ZoneInfo("America/New_York")

QUEUE_CSV = DATABASE / "Etsy_Darwinian_Lab_V7_Queue.csv"
PLAN_MD = REVIEW / "OPERATION_SHOCK_AND_AWE_V7_DARWINIAN_LAB_PLAN.md"


@dataclass(frozen=True)
class Pool:
    pool_id: str
    name: str
    theme: str
    format_name: str
    price: str
    constraint_profile: str
    suffix: str
    qa: str
    buyer: str
    search_angle: str


POOLS = [
    Pool(
        "POOL05",
        "Junk Journal & Ephemera",
        "dark academia relic paper, apothecary labels, gothic archive fragments",
        "Digital ephemera mega bundle",
        "9.99",
        "Ephemera_Pack",
        "vintage paper texture, antique ink, isolated collectible sheet, printable collage asset, no readable modern text --ar 4:5 --v 6.1 --style raw --no watermark, logo, modern typography",
        "No real readable copyrighted text; coherent paper set; printable contrast; no muddy edges.",
        "junk journal buyers, scrapbook makers, dark academia stationery users",
        "junk journal kit, dark academia ephemera, printable collage paper",
    ),
    Pool(
        "POOL07",
        "Laser/CNC Files",
        "closed-line ornament panels, gothic scholar frames, celestial relief plates",
        "SVG/DXF vector file pack",
        "6.99",
        "Laser_CNC_Vector",
        "flat vector blueprint, clean closed outlines, single-color cut paths, no gradients, no shading, pure white background --ar 1:1 --v 6.1 --style raw --no text, letters, watermark, mockup, photo",
        "Must be vectorizable, closed contours, no tiny floating noise, no gradients, no fake engraving text.",
        "laser cutter hobbyists, Cricut/Silhouette users, craft sellers",
        "laser cut file, svg dxf ornament, gothic frame svg",
    ),
    Pool(
        "POOL04",
        "Streetwear Graphics",
        "original cyber relic graphics, acid design symbols, non-IP graphic tee fronts",
        "PNG streetwear graphic pack",
        "8.99",
        "Streetwear_Graphic",
        "centered streetwear graphic, bold silhouette, high contrast, screenprint-ready, transparent-background intent, original symbol only --ar 4:5 --v 6.1 --style raw --no brand logo, celebrity, known character, trademark, text",
        "No recognizable IP; strong silhouette; works at small thumbnail; limited palette preferred.",
        "DIY apparel sellers, students, print-on-demand makers",
        "streetwear png, cyber graphic tee, y2k apparel design",
    ),
    Pool(
        "POOL08",
        "Maximalist Seamless Patterns",
        "baroque cyber jade pattern, dark floral archive, maximalist room decor surface design",
        "Seamless pattern mega bundle",
        "7.99",
        "Maximalist_Seamless",
        "hyper-detailed, edge-to-edge pattern, seamless repeating surface design, ornamental density, premium wallpaper textile style --tile --ar 1:1 --v 6.1 --style raw --no text, letters, watermark, logo",
        "Tile repeat must not show obvious seams; thumbnail must read as rich, not noisy.",
        "digital paper buyers, surface pattern designers, wallpaper/craft users",
        "seamless pattern, maximalist digital paper, gothic floral pattern",
    ),
    Pool(
        "POOL09",
        "Niche Planners",
        "roleplay grimoire planners, reading ritual pages, gothic productivity inserts",
        "Printable planner PDF bundle",
        "9.99",
        "Niche_Planner",
        "empty space in the middle for writing, ornate border, planner insert design, printable page, atmospheric but functional --ar 2:3 --v 6.1 --style raw --no text, typography, letters, watermark",
        "Writable center must remain clear; no AI pseudo-text; border cannot crowd utility area.",
        "planner users, fantasy readers, students, dark academia productivity buyers",
        "printable planner, grimoire planner, reading journal pages",
    ),
    Pool(
        "POOL10",
        "Esoteric Tattoo Flash",
        "black ink occult ornaments, scholar talismans, clean symbolic flash sheets",
        "Tattoo flash printable sheet",
        "5.99",
        "Tattoo_Flash",
        "clean line art, black ink only, pure white background, tattoo flash sheet, crisp negative space --ar 3:4 --v 6.1 --style raw --no shading, color, gradient, grey, text, watermark",
        "Pure black/white only; no grey shading; no fake letters; linework must be clean.",
        "tattoo inspiration buyers, flash collectors, stationery/craft users",
        "tattoo flash, occult line art, black ink printable",
    ),
]


CONCEPT_BANK = {
    "POOL05": [
        "Obsidian Library Receipt Scraps",
        "Apothecary Moon Ledger Fragments",
        "Gothic Herbarium Relic Cards",
        "Victorian Alchemist Bottle Labels",
        "Celestial Archive Cabinet Papers",
        "Raven Scholar Field Notes",
        "Antique Observatory Ticket Stubs",
        "Quiet Relic Correspondence Set",
        "Museum Specimen Tag Bundle",
        "Old Chapel Wax-Seal Papers",
    ],
    "POOL07": [
        "Celestial Gothic Mirror Frame",
        "Scholar Sunburst Ornament Plate",
        "Runic Door Corner Brackets",
        "Apothecary Label Cut Frame",
        "Library Arch Bookmark File",
        "Astrolabe Wall Medallion",
        "Gothic Herbarium Frame",
        "Quiet Relic Keyhole Plate",
        "Moon Gate Layered Ornament",
        "Cathedral Window Desk Panel",
    ],
    "POOL04": [
        "Cyber Obsidian Shrine Graphic",
        "Acid Jade Relic Emblem",
        "Neon Archive Skull-Free Crest",
        "Chrome Bonsai Signal Mark",
        "Industrial Oracle Symbol",
        "Black Titanium Halo Graphic",
        "Data Shrine Street Emblem",
        "Molten Circuit Sigil",
        "Nocturne Racing Relic",
        "Digital Monk Hand Symbol",
    ],
    "POOL08": [
        "Baroque Jade Circuit Damask",
        "Dark Academia Floral Archive",
        "Cyber Rococo Wallpaper Tile",
        "Smoky Emerald Cabinet Pattern",
        "Obsidian Botanical Overgrowth",
        "Gothic Library Carpet Repeat",
        "Maximalist Alchemy Surface",
        "Midnight Brass Vine Pattern",
        "Celestial Greenhouse Repeat",
        "Victorian Neon Relic Pattern",
    ],
    "POOL09": [
        "Reading Nook Ritual Planner",
        "Apothecary Habit Tracker Page",
        "Fantasy Study Weekly Insert",
        "Dark Academia Assignment Log",
        "Grimoire Meal and Mood Page",
        "Library Focus Sprint Sheet",
        "Moon Phase Reading Tracker",
        "Scholar Budget Ritual Page",
        "Potion Inventory Planner",
        "Quiet Work Deep Focus Sheet",
    ],
    "POOL10": [
        "Astrolabe Talisman Flash",
        "Gothic Key and Laurel Sheet",
        "Black Ink Apothecary Symbols",
        "Moon Gate Minimal Flash",
        "Ravenless Scholar Sigils",
        "Alchemical Vessel Line Sheet",
        "Obsidian Halo Flash Set",
        "Library Candle Tattoo Sheet",
        "Celestial Compass Ink Set",
        "Quiet Relic Symbol Board",
    ],
}


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %z")


def build_prompt(pool: Pool, concept: str) -> str:
    subject = f"{concept}, {pool.theme}"
    return f"{subject}, {pool.suffix}"


def title_for(pool: Pool, concept: str) -> str:
    title_templates = {
        "POOL05": f"{concept} Printable Ephemera Kit, Dark Academia Junk Journal Pages, Vintage Collage Paper",
        "POOL07": f"{concept} SVG DXF Laser Cut File, Gothic Ornament Digital Download for Cricut and Glowforge",
        "POOL04": f"{concept} Streetwear PNG Graphic, Cyber Relic Shirt Design, Y2K Apparel Art Download",
        "POOL08": f"{concept} Seamless Pattern Pack, Maximalist Digital Paper, Gothic Wallpaper Texture",
        "POOL09": f"{concept} Printable Planner Pages, Dark Academia Reading Journal, Grimoire Study Inserts",
        "POOL10": f"{concept} Tattoo Flash Sheet, Black Ink Occult Line Art, Printable Esoteric Design",
    }
    return title_templates[pool.pool_id][:140]


def tags_for(pool: Pool, concept: str) -> str:
    tag_map = {
        "POOL05": [
            "junk journal",
            "ephemera kit",
            "dark academia",
            "printable paper",
            "collage sheet",
            "vintage labels",
            "scrapbook paper",
            "gothic journal",
            "digital download",
            "apothecary art",
            "library decor",
            "paper crafting",
            "journal supplies",
        ],
        "POOL07": [
            "laser cut file",
            "svg dxf",
            "cricut file",
            "glowforge svg",
            "gothic ornament",
            "digital download",
            "cnc pattern",
            "craft file",
            "vector design",
            "bookmark svg",
            "wall decor svg",
            "cutting file",
            "instant download",
        ],
        "POOL04": [
            "streetwear png",
            "shirt design",
            "cyberpunk art",
            "y2k graphic",
            "apparel design",
            "png download",
            "tee graphic",
            "digital artwork",
            "cyber relic",
            "alt fashion",
            "print on demand",
            "edgy design",
            "instant download",
        ],
        "POOL08": [
            "seamless pattern",
            "digital paper",
            "maximalist decor",
            "gothic floral",
            "wallpaper pattern",
            "scrapbook paper",
            "surface pattern",
            "printable paper",
            "dark academia",
            "baroque pattern",
            "craft paper",
            "digital download",
            "pattern bundle",
        ],
        "POOL09": [
            "printable planner",
            "reading journal",
            "grimoire planner",
            "study planner",
            "dark academia",
            "planner insert",
            "journal pages",
            "book lover gift",
            "digital planner",
            "productivity page",
            "fantasy planner",
            "instant download",
            "printable pages",
        ],
        "POOL10": [
            "tattoo flash",
            "line art",
            "black ink",
            "occult art",
            "flash sheet",
            "tattoo design",
            "printable art",
            "esoteric design",
            "minimal tattoo",
            "symbol art",
            "instant download",
            "white background",
            "ink drawing",
        ],
    }
    return ", ".join(tag_map[pool.pool_id])


def description_for(pool: Pool, concept: str) -> str:
    lead = {
        "POOL05": "A printable paper set for journals, collage pages, scrapbooks, and moody desk rituals.",
        "POOL07": "A clean digital craft file concept for laser/CNC/Cricut style makers who want ornament without generic clipart.",
        "POOL04": "A digital streetwear graphic concept for apparel experiments, mockups, and print-on-demand idea testing.",
        "POOL08": "A maximalist digital paper concept for pattern lovers, wallpaper mood boards, packaging tests, and craft projects.",
        "POOL09": "A printable planner concept built around atmosphere and usefulness: decorative borders, clear writing space, and a room-use story.",
        "POOL10": "A black-ink flash concept for tattoo inspiration boards, stationery, and clean occult line-art collecting.",
    }[pool.pool_id]
    return (
        f"{concept} belongs to the OpenClaw Darwinian Lab: a small Etsy-native digital experiment built to test real buyer interest in a specific aesthetic/use case.\n\n"
        f"{lead}\n\n"
        f"Format: {pool.format_name}\n"
        f"Buyer use case: {pool.buyer}\n"
        f"Style direction: {pool.search_angle}\n\n"
        "This is a DIGITAL DOWNLOAD concept. No physical item is shipped. Final published files must pass the OpenClaw QA gate before launch.\n\n"
        "AI disclosure: artwork in this experimental line may be created with AI assistance and then curated, formatted, and quality-checked for the intended digital product format."
    )


def build_rows() -> list[dict[str, str]]:
    created = now_text()
    rows: list[dict[str, str]] = []
    for pool in POOLS:
        for index, concept in enumerate(CONCEPT_BANK[pool.pool_id], start=1):
            sku = f"OC-ETSY-{pool.pool_id}-{index:02d}"
            rows.append(
                {
                    "SKU": sku,
                    "Track": "Track B - Etsy Darwinian Lab",
                    "Pool_ID": pool.pool_id,
                    "Pool_Name": pool.name,
                    "Concept_Name": concept,
                    "Listing_Type": "Digital Download",
                    "Format": pool.format_name,
                    "Target_Buyer": pool.buyer,
                    "Search_Angle": pool.search_angle,
                    "Price_USD": pool.price,
                    "Etsy_Title": title_for(pool, concept),
                    "Etsy_Tags": tags_for(pool, concept),
                    "Etsy_Description": description_for(pool, concept),
                    "Constraint_Profile": pool.constraint_profile,
                    "MJ_Master_Prompt": build_prompt(pool, concept),
                    "QA_Requirements": pool.qa,
                    "Asset_Status": "STAGED_CONCEPT_ONLY",
                    "Publish_Status": "NOT_PUBLISHED_FEE_GUARD_REQUIRED",
                    "Kill_Rule": "After 14 days: Fav/Visit < 1.0% and 0 carts/orders = kill or archive.",
                    "Scale_Rule": "Natural order or Fav/Visit > 3.0% = scale into larger bundle family.",
                    "Created_At_ET": created,
                }
            )
    return rows


def write_queue(rows: list[dict[str, str]]) -> None:
    DATABASE.mkdir(exist_ok=True)
    fields = list(rows[0].keys())
    with QUEUE_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_plan(rows: list[dict[str, str]]) -> None:
    REVIEW.mkdir(exist_ok=True)
    lines = [
        "# Operation Shock and Awe V7 - Etsy Darwinian Lab",
        "",
        f"Generated: {now_text()}",
        "",
        "Purpose: Track B public-market experiment queue. These are Etsy digital product experiments, not private partner-demo products.",
        "",
        "Guardrails:",
        "- Do not publish until asset generation, QA, metadata, fee guard, and duplicate checks pass.",
        "- Batch launch remains capped by Etsy_Fee_Kill_Switch.json.",
        "- The first goal is market signal, not perfect brand mythology.",
        "- Etsy copy is not eBay copy: prioritize giftability, craft use case, room/persona language, and natural 13-tag coverage.",
        "- Each pool starts with 10 listings; winners scale, weak pools get killed.",
        "",
        "## Pool Summary",
        "",
        "| Pool | Format | Price | Buyer | Search Angle |",
        "|---|---|---:|---|---|",
    ]
    for pool in POOLS:
        lines.append(f"| {pool.pool_id} {pool.name} | {pool.format_name} | ${pool.price} | {pool.buyer} | {pool.search_angle} |")
    lines.extend(["", "## First 60 Concepts", ""])
    for row in rows:
        lines.append(f"### {row['SKU']} - {row['Concept_Name']}")
        lines.append(f"- Pool: {row['Pool_ID']} / {row['Pool_Name']}")
        lines.append(f"- Format: {row['Format']} at ${row['Price_USD']}")
        lines.append(f"- Etsy title: {row['Etsy_Title']}")
        lines.append(f"- Etsy tags: {row['Etsy_Tags']}")
        lines.append(f"- Search angle: {row['Search_Angle']}")
        lines.append(f"- Prompt: `{row['MJ_Master_Prompt']}`")
        lines.append(f"- QA: {row['QA_Requirements']}")
        lines.append("")
    PLAN_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    rows = build_rows()
    write_queue(rows)
    write_plan(rows)
    print(f"[ETSY-DARWINIAN] rows={len(rows)} csv={QUEUE_CSV}")
    print(f"[ETSY-DARWINIAN] plan={PLAN_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
