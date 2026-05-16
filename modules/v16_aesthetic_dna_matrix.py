"""Build the V16 premium aesthetic DNA matrix.

This is a local-only replenishment task for the monthly cruise loop. It turns
Rex's current high-end direction into durable Mentor-Hub-style DNA rows that
can later feed DeepSeek/Claude/MJ without spending marketplace fees.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
OUT_CSV = DATABASE / "V16_Aesthetic_DNA_Matrix.csv"
OUT_MD = REVIEW / "V16_Aesthetic_DNA_Matrix.md"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

HEADERS = [
    "DNA_ID",
    "Track",
    "Buyer_Intent",
    "Classical_Anchor",
    "Material_Model",
    "Lighting_Model",
    "Composition_Model",
    "Product_Carrier",
    "Price_Lane",
    "MJ_Prompt_Stem",
    "Negative_Guard",
    "QA_Gate",
]


ROWS = [
    {
        "DNA_ID": "V16-NYC-001",
        "Track": "NYC Luxury",
        "Buyer_Intent": "executive office gift, quiet luxury desk decor, Manhattan apartment statement",
        "Classical_Anchor": "Art Deco lobby geometry and pre-war Manhattan brass elevator panels",
        "Material_Model": "smoky jade, brushed brass, optical acrylic refraction, black walnut shadow",
        "Lighting_Model": "low-angle gallery spotlight, warm brass rim light, soft city-window reflection",
        "Composition_Model": "vertical architectural symmetry, central monolith, negative space around object",
        "Product_Carrier": "5x7 acrylic block / 12x18 archival poster",
        "Price_Lane": "$48 entrance / $128 core",
        "MJ_Prompt_Stem": "a quiet luxury Art Deco monolith reconstructed from smoky jade and brushed brass, optical acrylic depth, Manhattan penthouse mood, gallery object photography, 85mm lens, f/8, ultra sharp",
        "Negative_Guard": "--no text, logo, watermark, cartoon, cheap plastic, blurry background, warped symmetry",
        "QA_Gate": "must read as expensive physical material; no decorative clipart; no flat AI gradient",
    },
    {
        "DNA_ID": "V16-NYC-002",
        "Track": "NYC Luxury",
        "Buyer_Intent": "tech founder desk set, minimalist boss decor, premium client gift",
        "Classical_Anchor": "Brooklyn Bridge cable rhythm and Bauhaus grid discipline",
        "Material_Model": "liquid chrome, cold jade glass, matte graphite, micro-scratched titanium",
        "Lighting_Model": "cool north-window light, controlled specular highlights, deep contact shadows",
        "Composition_Model": "diagonal cable tension, floating engineered artifact, wide matte border",
        "Product_Carrier": "acrylic block / framed poster",
        "Price_Lane": "$98 entrance / $149 bundle",
        "MJ_Prompt_Stem": "Brooklyn Bridge cable geometry transformed into a liquid chrome and cold jade executive desk artifact, Bauhaus precision, optical refraction, museum-grade product photo, 85mm lens, f/8",
        "Negative_Guard": "--no people, text, logo, tourist postcard, skyline cliche, soft focus",
        "QA_Gate": "bridge reference must be abstracted, not souvenir-like",
    },
    {
        "DNA_ID": "V16-EU-001",
        "Track": "European Dark Academia",
        "Buyer_Intent": "reading nook decor, professor office gift, old library wall art",
        "Classical_Anchor": "Oxford reading room vaults and 19th century natural-history copperplate plates",
        "Material_Model": "aged vellum, oxidized bronze, smoky amber glass, kintsugi hairlines",
        "Lighting_Model": "Rembrandt chiaroscuro, candle-warm bounce, controlled archival shadows",
        "Composition_Model": "specimen plate frame, central relic, marginal annotation space without text",
        "Product_Carrier": "12x18 archival poster / 5x7 acrylic block",
        "Price_Lane": "$48 entrance / $128 core",
        "MJ_Prompt_Stem": "an Oxford natural-history relic plate reimagined as oxidized bronze and smoky amber glass, Rembrandt chiaroscuro, dark academia museum archive, no readable text, ultra sharp paper grain",
        "Negative_Guard": "--no letters, typography, watermark, modern plastic, fantasy castle, messy clutter",
        "QA_Gate": "must feel like museum archive, not Halloween gothic",
    },
    {
        "DNA_ID": "V16-EU-002",
        "Track": "European Dark Academia",
        "Buyer_Intent": "heritage study decor, luxury reading room poster, intellectual gift",
        "Classical_Anchor": "Da Vinci mechanical notebook and astrolabe manuscript structure",
        "Material_Model": "dark parchment, brushed copper, obsidian ink, jade lensing",
        "Lighting_Model": "single desk-lamp cone, soft fog diffusion, crisp engraved shadows",
        "Composition_Model": "technical-diagram order, centered instrument, generous matte margin",
        "Product_Carrier": "framed poster / acrylic block",
        "Price_Lane": "$48 entrance / $149 bundle",
        "MJ_Prompt_Stem": "a Renaissance astrolabe study reconstructed as brushed copper, obsidian ink, and jade optical lenses, Da Vinci notebook discipline, museum conservation lighting, no readable labels, f/8 ultra sharp",
        "Negative_Guard": "--no text, letters, watermark, messy scribbles, steampunk costume, low detail",
        "QA_Gate": "geometry must be clean enough for premium print; avoid noisy fake handwriting",
    },
    {
        "DNA_ID": "V16-KIN-001",
        "Track": "Imperial Kintsugi",
        "Buyer_Intent": "luxury housewarming gift, refined entryway decor, collector desk object",
        "Classical_Anchor": "Kyoto kintsugi repair logic and museum bronze vessel fragments",
        "Material_Model": "unpolished jade, broken celadon glaze, antique bronze, thin gold repair veins",
        "Lighting_Model": "dappled temple sunlight, shallow fog diffusion, restrained gold glints",
        "Composition_Model": "single monumental fragment, asymmetric wabi-sabi void, low plinth",
        "Product_Carrier": "acrylic block / archival poster",
        "Price_Lane": "$128 core / $295 anchor",
        "MJ_Prompt_Stem": "a museum bronze vessel fragment repaired with hairline kintsugi and unpolished jade, Kyoto restraint, dappled sunlight through shoji, optical acrylic depth, 85mm lens, f/8",
        "Negative_Guard": "--no dragon, phoenix, cheap gold, oversaturated green, cartoon, text",
        "QA_Gate": "must avoid tourist orientalism; material should feel quiet and heavy",
    },
    {
        "DNA_ID": "V16-KIN-002",
        "Track": "Imperial Kintsugi",
        "Buyer_Intent": "executive gift, meditative office object, luxury recovery symbol",
        "Classical_Anchor": "Japanese lacquer repair and Roman ruin fragment display",
        "Material_Model": "black lacquer, smoky jade core, brushed titanium clamp, gold seam repair",
        "Lighting_Model": "gallery spot from upper left, hard contact shadow, reflective black floor",
        "Composition_Model": "ruin fragment held by precise metal clamp, object centered in void",
        "Product_Carrier": "5x7 acrylic block / 8x10 premium print",
        "Price_Lane": "$128 core",
        "MJ_Prompt_Stem": "a black lacquer ruin fragment clamped in brushed titanium, smoky jade core exposed through kintsugi seams, high-end gallery product photography, black reflective plinth, f/8, ultra sharp",
        "Negative_Guard": "--no text, logo, red lantern, cheap souvenir, fantasy weapon, blur",
        "QA_Gate": "object must look physically manufacturable as an image on acrylic/poster",
    },
    {
        "DNA_ID": "V16-CYBER-001",
        "Track": "Cyber-Renaissance",
        "Buyer_Intent": "founder office statement, AI era art, premium tech gift",
        "Classical_Anchor": "Babel tower composition translated into computational architecture",
        "Material_Model": "cold jade slabs, liquid chrome scaffolds, smoked glass, nano-engraved brass",
        "Lighting_Model": "cinematic fog diffusion, cold blue core glow, warm brass edge light",
        "Composition_Model": "towering vertical spiral, impossible scale, clear foreground plinth",
        "Product_Carrier": "large archival poster / acrylic block",
        "Price_Lane": "$98 entrance / $295 anchor",
        "MJ_Prompt_Stem": "the Tower of Babel re-engineered as cold jade slabs and liquid chrome scaffolds, cyber-renaissance architecture, cinematic fog diffusion, optical acrylic depth, ultra sharp f/8, no text",
        "Negative_Guard": "--no readable symbols, people, sci-fi spaceship, cheap neon, blurry haze",
        "QA_Gate": "classical composition must remain legible; cyber material cannot look like gaming poster",
    },
    {
        "DNA_ID": "V16-CYBER-002",
        "Track": "Cyber-Renaissance",
        "Buyer_Intent": "gallery-grade desk decor, private collector gift, AI civilization symbol",
        "Classical_Anchor": "classical bust silhouette and Renaissance chiaroscuro portrait structure",
        "Material_Model": "smoky jade marble, black titanium fractures, refractive glass halo",
        "Lighting_Model": "Rembrandt lighting, narrow rim light, deep black background",
        "Composition_Model": "three-quarter bust, empty identity, haloed material fracture",
        "Product_Carrier": "acrylic block / framed poster",
        "Price_Lane": "$128 core / $295 anchor",
        "MJ_Prompt_Stem": "an anonymous classical bust reconstructed from smoky jade marble, black titanium fracture lines and refractive glass halo, Rembrandt lighting, cyber-renaissance gallery portrait, 85mm lens, f/8",
        "Negative_Guard": "--no celebrity, living artist style, gore, text, watermark, anime, smooth plastic",
        "QA_Gate": "must be anonymous and non-IP; no recognizable real person",
    },
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def write_csv() -> None:
    DATABASE.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(ROWS)


def write_report() -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    lines = [
        "# V16 Aesthetic DNA Matrix",
        "",
        f"Generated: {now_text()}",
        "",
        "Purpose: replenish the monthly task pool with premium, reference-derived design DNA that can feed DeepSeek/Claude/MJ without touching marketplace accounts.",
        "",
        "## Operating Rule",
        "",
        "- Keep cheap sticker-style logic out of this matrix.",
        "- Use these rows as high-end prompt scaffolds, not as literal public listing copy.",
        "- No upscale, publish, or fee action is authorized by this artifact.",
        "",
        "## Rows",
        "",
    ]
    for row in ROWS:
        lines.extend(
            [
                f"### {row['DNA_ID']} - {row['Track']}",
                "",
                f"- Buyer intent: {row['Buyer_Intent']}",
                f"- Classical anchor: {row['Classical_Anchor']}",
                f"- Material model: {row['Material_Model']}",
                f"- Lighting: {row['Lighting_Model']}",
                f"- Product fit: {row['Product_Carrier']} ({row['Price_Lane']})",
                f"- Prompt stem: `{row['MJ_Prompt_Stem']} {row['Negative_Guard']} --v 6.1 --style raw`",
                f"- QA gate: {row['QA_Gate']}",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def append_progress() -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Built V16 aesthetic DNA matrix; rows={len(ROWS)}; "
            f"csv={OUT_CSV.relative_to(PROJECT_ROOT)}; packet={OUT_MD.relative_to(PROJECT_ROOT)}.\n"
        )


def main() -> None:
    write_csv()
    write_report()
    append_progress()
    print(f"[V16-DNA] rows={len(ROWS)} csv={OUT_CSV}")
    print(f"[V16-DNA] packet={OUT_MD}")


if __name__ == "__main__":
    main()
