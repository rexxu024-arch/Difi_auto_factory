from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "Database"
REVIEW = ROOT / "Review_Packets"
SOURCE = DB / "Adobe_Stock_Market_Sample_MJ_Queue.csv"
REPORT = REVIEW / "Adobe_Stock_Market_Sample_Expander_latest.md"
ET = ZoneInfo("America/New_York")

FIELDS = [
    "Queue_ID",
    "Lane",
    "Variant",
    "Prompt",
    "Title_Pattern",
    "First_10_Keywords",
    "Status",
    "Rex_QA_Note",
]

STYLE_RULE = (
    "extreme macro photography, deep focus across the whole material plane, "
    "broad crop-safe sharp texture coverage, commercial stock background, "
    "controlled studio side lighting, 100mm macro lens, f/11, ultra photorealistic, "
    "no shallow depth of field, no bokeh, no blurred foreground, no blurred background, "
    "no text, no logo, no people, no object, no clutter"
)


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\r", " ").replace("\n", " ").split()).strip()


def read_rows() -> list[dict[str, str]]:
    if not SOURCE.exists():
        return []
    with SOURCE.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(rows: list[dict[str, str]]) -> None:
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    with SOURCE.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def prompt(material: str, variant: str, negative: str) -> str:
    return (
        f"Extreme macro photography of {material} texture background, {variant}, "
        f"{STYLE_RULE} --ar 3:2 --style raw --v 6.1 --chaos 10 --no {negative}"
    )


def candidate_rows(start: int) -> list[dict[str, str]]:
    specs = [
        (
            "Nero Marble / Luxury Stone",
            "Black marble texture background with ivory veins",
            "black, marble, texture, background, stone, luxury, ivory veins, slab, polished, surface",
            "random lightning veins, muddy cracks, yellow stain, text, logo, blurry edges",
            [
                "gallery black marble slab, sparse ivory veins, realistic mineral grain",
                "quiet luxury black stone plane, thin controlled veins, copy-space friendly",
                "polished nero marble macro, clean white veins, high contrast but restrained",
                "black marble surface, diagonal ivory vein network, premium interior backdrop",
                "deep black stone, few elegant mineral veins, broad sharp surface",
                "minimal black marble, realistic subsurface speckles, luxury product background",
            ],
        ),
        (
            "Kintsugi Marble / Gold Repair Stone",
            "Kintsugi marble texture background with gold veins",
            "kintsugi, marble, texture, background, gold, stone, repair, luxury, mineral, surface",
            "ornamental clutter, gold overload, messy cracks, text, logo, blurry edges",
            [
                "cream marble with sparse gold repair lines, clean negative space",
                "black marble with restrained gold kintsugi seams, realistic mineral grain",
                "warm white stone with thin gold repair paths, premium design background",
                "gray marble with delicate gold lines, low crack density, elegant surface",
                "minimal kintsugi stone plane, thin metallic seams, copy-space friendly",
                "ivory marble with controlled gold fissures, luxury packaging backdrop",
            ],
        ),
        (
            "Smoky Jade / Green Stone",
            "Green jade stone texture background",
            "jade, green, stone, texture, background, mineral, translucent, luxury, surface, abstract",
            "cartoon crystal, fantasy object, muddy green, text, logo, blurry edges",
            [
                "smoky green jade slab, translucent mineral bands, sharp natural texture",
                "deep emerald jade surface, cloudy stone layers, clean commercial background",
                "green mineral texture, subtle white inclusions, premium interior backdrop",
                "polished smoky jade macro, layered stone veins, broad sharp focus",
                "dark green jade plane, soft internal glow, realistic mineral structure",
                "clean jade stone background, elegant banding, copy-space friendly crop",
            ],
        ),
        (
            "Walnut Burl / Executive Wood",
            "Dark walnut burl wood grain texture background",
            "walnut, wood, texture, background, burl, grain, veneer, dark, luxury, surface",
            "plank seams, furniture object, orange oversaturation, muddy grain, text, logo, blur",
            [
                "dark walnut burl veneer, swirling grain, satin executive desk finish",
                "premium wood burl macro, tight organic rings, controlled warm highlights",
                "luxury walnut surface, clean continuous veneer, deep brown grain detail",
                "dark wood grain background, elegant burl pattern, broad sharp focus",
                "walnut burl slab, refined satin sheen, product design background",
                "minimal dark walnut copy-space, realistic pores and fine grain",
            ],
        ),
        (
            "Brushed Titanium / Chrome Silver",
            "Brushed metal texture background",
            "brushed metal, titanium, texture, background, silver, chrome, industrial, surface, metallic, grain",
            "pure gradient, plastic shine, logo, text, object, blur, fingerprints",
            [
                "horizontal brushed titanium, visible fine grain, cool silver surface",
                "dark brushed metal plane, subtle linear scratches, industrial luxury backdrop",
                "satin chrome texture, crisp directional grain, clean product background",
                "brushed silver metal macro, tactile micro scratches, no reflections",
                "gunmetal titanium surface, refined parallel grain, premium tech background",
                "clean aluminum brush texture, edge-to-edge sharp lines, copy-space friendly",
            ],
        ),
        (
            "Clean Travertine / Plaster",
            "Warm travertine plaster texture background",
            "travertine, plaster, texture, background, wall, stone, beige, minimal, surface, copy space",
            "dirty stains, grunge, graffiti, broken wall, text, logo, blur",
            [
                "warm travertine plaster wall, clean pores, quiet luxury background",
                "minimal limestone plaster texture, subtle mineral speckles, copy space",
                "soft beige stone wall, refined natural pores, broad sharp focus",
                "clean architectural plaster surface, warm studio side light, stock background",
                "travertine stone plane, elegant pale bands, minimal design backdrop",
                "matte plaster texture, smooth premium wall surface, clear micro detail",
            ],
        ),
        (
            "Obsidian Glass / Dark Reflective Stone",
            "Black obsidian glass texture background",
            "obsidian, black glass, texture, background, dark, reflective, stone, luxury, surface, abstract",
            "mirror object, sharp glare, lens flare, text, logo, blur, fantasy crystal",
            [
                "black obsidian glass surface, subtle smoky reflections, premium dark background",
                "polished volcanic glass texture, controlled highlights, clean abstract surface",
                "dark reflective stone plane, fine mineral haze, elegant product backdrop",
                "smoky black glass macro, restrained specular lines, broad sharp focus",
                "obsidian slab background, deep black layers, minimal luxury texture",
                "dark glass stone texture, subtle gray reflections, crop-safe surface",
            ],
        ),
    ]
    rows: list[dict[str, str]] = []
    idx = start
    for lane, title, keywords, negative, variants in specs:
        note = "PASS only if clean, useful, broad sharp, and stock-background ready; reject muddy, blurry, or meaningless variants."
        if "Kintsugi" in lane:
            note = "Reject if gold lines exceed about 20%, look decorative, or turn into random lightning."
        elif "Travertine" in lane:
            note = "Reject if dirty or flat; only clean warm wall/plaster surfaces pass."
        elif "Brushed" in lane:
            note = "Reject if it becomes a pure gradient without visible tactile grain."
        for variant in variants:
            rows.append(
                {
                    "Queue_ID": f"ADOBE-MARKET-SAMPLE-{idx:03d}",
                    "Lane": lane,
                    "Variant": variant,
                    "Prompt": prompt(lane.split(" / ")[0].lower(), variant, negative),
                    "Title_Pattern": title,
                    "First_10_Keywords": keywords,
                    "Status": "READY_FOR_MJ_RELAXED_WHEN_THERMAL_OK",
                    "Rex_QA_Note": note,
                }
            )
            idx += 1
    return rows


def main() -> int:
    existing = read_rows()
    existing_ids = {clean(row.get("Queue_ID")) for row in existing}
    additions = [row for row in candidate_rows(34) if row["Queue_ID"] not in existing_ids]
    write_rows(existing + additions)
    lines = [
        "# Adobe Stock Market Sample Expander",
        "",
        f"Generated: {datetime.now(ET).strftime('%Y-%m-%d %H:%M:%S %Z')}",
        f"- Existing before append: {len(existing)}",
        f"- Added: {len(additions)}",
        f"- Total: {len(existing) + len(additions)}",
        "",
        "New lanes prioritize Rex-passed clean material/background DNA and avoid shallow blur.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[ADOBE-MARKET-EXPAND] added={len(additions)} total={len(existing)+len(additions)} source={SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
