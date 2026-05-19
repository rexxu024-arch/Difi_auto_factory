from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "Database"
REVIEW = ROOT / "Review_Packets"


SOURCES = [
    {
        "name": "Adobe 2026 Creative Trends",
        "url": "https://blog.adobe.com/en/publish/2026/01/08/how-creators-leveraging-adobe-2026-creative-trends",
        "signal": "Adobe says buyers want useful, relatable visuals with multi-sensory tactile depth; trends are derived from campaigns, communities, and search history.",
    },
    {
        "name": "Adobe Stock Textures Discover",
        "url": "https://stock.adobe.com/discover/textures",
        "signal": "Adobe Stock exposes texture categories as popular buyer paths: paper, wood, concrete, metal, stone, marble, canvas, glass, chrome, carbon fiber.",
    },
    {
        "name": "Adobe Stock Keyword Tutorial",
        "url": "https://helpx.adobe.com/stock/contributor/help/keyword-tutorial.html",
        "signal": "Adobe asks for natural titles up to 70 characters, main subject first, 15-25 relevant keywords, and no irrelevant or trademarked terms.",
    },
    {
        "name": "Adobe Stock Metadata Guide",
        "url": "https://stock.adobe.com/pages/artisthub/get-started/photo-video-metadata-stock-contributor-guide-pt-3",
        "signal": "Adobe emphasizes metadata quality and warns against lazy bulk keywording.",
    },
]


LANES = [
    {
        "lane": "Carbon Fiber / Technical Weave",
        "priority": 1,
        "market_evidence": "Adobe texture category includes Carbon Fiber; Rex pass rate 4/4 locally.",
        "low_competition_angle": "Avoid generic car-part imagery; use clean dark graphite weave for product backgrounds, tech decks, and performance branding.",
        "rex_fit": "Strong. Already passed Rex visual taste when broad, sharp, not shallow-DOF.",
        "dna": "edge-to-edge black graphite woven fiber, diagonal technical pattern, satin anisotropic highlights, broad deep-focus sharpness, no vehicle parts",
        "prompt_spine": "Extreme macro photography of dark graphite carbon fiber weave texture background, broad sharp material coverage, satin anisotropic highlights, clean technical surface, useful for product mockups and technology branding, deep focus across the material plane, 100mm macro lens, f/11, ultra photorealistic --ar 3:2 --style raw --v 6.1 --no shallow depth of field, bokeh, blurred foreground, car part, logo, text, watermark",
        "title_pattern": "Dark carbon fiber weave texture background",
        "first_keywords": "carbon fiber, texture, background, weave, graphite, black, technical, material, surface, pattern",
        "sample_plan": "Generate 6 relaxed grids: 3 diagonal weave, 2 straight basket weave, 1 subtle blue-black highlight.",
        "qa_rule": "PASS only if at least 70% of image is visibly sharp; HOLD cinematic blur variants.",
    },
    {
        "lane": "Nero Marble / Luxury Stone",
        "priority": 1,
        "market_evidence": "Adobe texture category includes Marble and Stone; Rex pass rate 4/4 locally; public stock references use black marble + luxury/interior keywords.",
        "low_competition_angle": "Use restrained ivory/gold veining and copy-space variants rather than chaotic AI marble.",
        "rex_fit": "Strong. Visual sophistication high and directly useful for stock backgrounds.",
        "dna": "black polished stone plane, ivory mineral veins, controlled negative space, gallery-grade contrast, realistic mineral grain",
        "prompt_spine": "Extreme macro photography of nero black marble slab texture background, restrained ivory mineral veins, polished stone depth, elegant copy space, luxury interior material surface, broad sharp focus, 100mm macro lens, f/11, ultra photorealistic --ar 3:2 --style raw --v 6.1 --no shallow depth of field, messy veins, text, logo, watermark",
        "title_pattern": "Black marble texture background with ivory veins",
        "first_keywords": "black marble, marble, texture, background, stone, luxury, veins, surface, interior, design",
        "sample_plan": "Generate 5 relaxed grids: 3 dark, 1 gray-black, 1 copy-space minimal.",
        "qa_rule": "Reject if veins look like random lightning or muddy cracks.",
    },
    {
        "lane": "Kintsugi Marble / Gold Repair Stone",
        "priority": 1,
        "market_evidence": "Public Adobe Stock references use kintsugi + marble + golden cracks wording; Rex pass rate 4/4 locally.",
        "low_competition_angle": "Blend kintsugi as abstract repair lines on stone, not pottery or cultural object; safer and more designer-useful.",
        "rex_fit": "Strong, but must avoid overdecorated/AI fantasy look.",
        "dna": "cream or black stone surface, restrained gold repair lines, matte mineral micrograin, balanced copy space",
        "prompt_spine": "Extreme macro photography of luxury kintsugi marble texture background, restrained gold repair veins across realistic stone, clean abstract material surface, balanced copy space, broad sharp focus, 100mm macro lens, f/11, ultra photorealistic --ar 3:2 --style raw --v 6.1 --no pottery, bowl, object, symbol, text, logo, shallow depth of field, messy cracks",
        "title_pattern": "Kintsugi marble texture background with gold veins",
        "first_keywords": "kintsugi, marble, texture, background, gold, veins, stone, luxury, abstract, pattern",
        "sample_plan": "Generate 6 relaxed grids: 3 dark kintsugi, 2 cream kintsugi, 1 gray stone kintsugi.",
        "qa_rule": "Reject if gold line density exceeds 20% or becomes ornamental clutter.",
    },
    {
        "lane": "Brushed Titanium / Chrome Silver",
        "priority": 2,
        "market_evidence": "Adobe texture categories include Metal, Silver, Steel, Chrome; Rex pass rate 3/4 locally.",
        "low_competition_angle": "Aim for premium hardware/product-background surfaces, not generic flat gradients.",
        "rex_fit": "Good. Needs more micro-scratches and less bland CG sheen.",
        "dna": "cool silver titanium sheet, directional brushing, micro scratches, controlled studio reflection, crop-safe surface",
        "prompt_spine": "Extreme macro photography of brushed titanium metal texture background, fine directional micro scratches, premium silver industrial surface, controlled studio reflection, broad sharp focus, 100mm macro lens, f/11, ultra photorealistic --ar 3:2 --style raw --v 6.1 --no shallow depth of field, device, logo, text, watermark, plastic CGI",
        "title_pattern": "Brushed titanium metal texture background",
        "first_keywords": "brushed metal, titanium, texture, background, silver, chrome, steel, surface, industrial, material",
        "sample_plan": "Generate 5 relaxed grids: 2 horizontal brush, 2 diagonal brush, 1 darker graphite metal.",
        "qa_rule": "Reject if it becomes pure gradient without tactile metal grain.",
    },
    {
        "lane": "Walnut Burl / Executive Wood",
        "priority": 2,
        "market_evidence": "Adobe popular texture paths include Wood; commercial texture packs sell high-resolution wood backgrounds; aligns with executive desk products.",
        "low_competition_angle": "Dark walnut burl as executive/luxury desk background instead of generic light wood plank.",
        "rex_fit": "Likely strong if clean and not muddy; useful bridge to Etsy/POD visual language.",
        "dna": "dark walnut burl grain, organic rings, satin finish, continuous veneer sheet, warm executive desk tone",
        "prompt_spine": "Extreme macro photography of dark walnut burl wood grain texture background, organic swirling rings, satin executive desk finish, continuous veneer sheet, broad sharp focus, 100mm macro lens, f/11, ultra photorealistic --ar 3:2 --style raw --v 6.1 --no furniture object, plank seams, logo, text, shallow depth of field, blur",
        "title_pattern": "Dark walnut burl wood grain texture background",
        "first_keywords": "walnut, wood, texture, background, burl, grain, veneer, dark, luxury, surface",
        "sample_plan": "Generate 5 relaxed grids: 3 dark burl, 1 cooler walnut, 1 copy-space desk-surface variant.",
        "qa_rule": "Reject if grain turns noisy, muddy, or too orange.",
    },
    {
        "lane": "Clean Architectural Concrete / Plaster",
        "priority": 3,
        "market_evidence": "Adobe popular texture paths include Concrete and Wall textures.",
        "low_competition_angle": "Clean brutalist/plaster wall with copy space, not dirty grunge.",
        "rex_fit": "Weak in prior batch, but salvageable if cleaner/sharper.",
        "dna": "matte cool gray concrete, subtle pores and trowel marks, large clean field, soft side light, designer copy space",
        "prompt_spine": "Extreme macro photography of clean architectural concrete wall texture background, subtle cement pores, minimal brutalist plaster surface, soft side lighting, large copy space, broad sharp focus, 100mm macro lens, f/11, ultra photorealistic --ar 3:2 --style raw --v 6.1 --no grunge dirt, stains, graffiti, cracks, shallow depth of field, text, logo",
        "title_pattern": "Clean concrete wall texture background with copy space",
        "first_keywords": "concrete, wall, texture, background, plaster, gray, cement, minimal, copy space, surface",
        "sample_plan": "Generate 3 test grids only; expand only after Rex pass.",
        "qa_rule": "Reject if dirty, chaotic, stained, or too flat.",
    },
    {
        "lane": "Archival Vellum / Premium Paper",
        "priority": 3,
        "market_evidence": "Adobe popular texture paths include Paper, Canvas, Parchment; Adobe keyword guidance supports main-subject-first titles.",
        "low_competition_angle": "Museum archival paper/vellum for stationery mockups, not old pirate-map parchment.",
        "rex_fit": "Prior output rejected; keep as low-volume remake lane.",
        "dna": "warm off-white vellum, subtle fibers, blank center copy space, clean museum conservation tone",
        "prompt_spine": "Extreme macro photography of clean archival vellum paper texture background, subtle natural fibers, warm off white museum paper surface, blank copy space, broad sharp focus, 100mm macro lens, f/11, ultra photorealistic --ar 3:2 --style raw --v 6.1 --no writing, stains, old map, burnt edges, shallow depth of field, logo, text",
        "title_pattern": "Archival vellum paper texture background",
        "first_keywords": "paper, vellum, texture, background, archival, fibers, blank, copy space, off white, material",
        "sample_plan": "Generate 3 test grids only; expand only after Rex pass.",
        "qa_rule": "Reject if it becomes dirty vintage paper or invisible texture.",
    },
]


def now_et() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "Priority",
        "Lane",
        "Market_Evidence",
        "Low_Competition_Angle",
        "Rex_Fit",
        "Reusable_DNA",
        "Prompt_Spine",
        "Title_Pattern",
        "First_10_Keywords",
        "Sample_Plan",
        "QA_Rule",
        "Status",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for lane in LANES:
            writer.writerow(
                {
                    "Priority": lane["priority"],
                    "Lane": lane["lane"],
                    "Market_Evidence": lane["market_evidence"],
                    "Low_Competition_Angle": lane["low_competition_angle"],
                    "Rex_Fit": lane["rex_fit"],
                    "Reusable_DNA": lane["dna"],
                    "Prompt_Spine": lane["prompt_spine"],
                    "Title_Pattern": lane["title_pattern"],
                    "First_10_Keywords": lane["first_keywords"],
                    "Sample_Plan": lane["sample_plan"],
                    "QA_Rule": lane["qa_rule"],
                    "Status": "READY_FOR_REX_TRAINING_SAMPLES"
                    if lane["priority"] <= 2
                    else "TEST_ONLY_AFTER_PRIMARY_LANES",
                }
            )


def write_md(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Adobe Stock Market DNA Scout")
    lines.append("")
    lines.append(f"Generated: {now_et()} ET")
    lines.append("")
    lines.append("## Bottom Line")
    lines.append("")
    lines.append(
        "Yes, the market/reference-learning lane is now active. The stronger version is not blind invention: start from official Adobe texture/trend/metadata signals, combine Rex QA weights, then generate narrow long-tail material families for review."
    )
    lines.append("")
    lines.append("## Evidence Sources")
    lines.append("")
    for source in SOURCES:
        lines.append(f"- [{source['name']}]({source['url']}): {source['signal']}")
    lines.append("")
    lines.append("## Priority Lanes")
    lines.append("")
    for lane in sorted(LANES, key=lambda item: item["priority"]):
        lines.append(f"### P{lane['priority']} - {lane['lane']}")
        lines.append("")
        lines.append(f"- Market evidence: {lane['market_evidence']}")
        lines.append(f"- Low-competition angle: {lane['low_competition_angle']}")
        lines.append(f"- Rex fit: {lane['rex_fit']}")
        lines.append(f"- DNA: {lane['dna']}")
        lines.append(f"- Title pattern: {lane['title_pattern']}")
        lines.append(f"- First 10 keywords: {lane['first_keywords']}")
        lines.append(f"- Sample plan: {lane['sample_plan']}")
        lines.append(f"- QA rule: {lane['qa_rule']}")
        lines.append("")
    lines.append("## Execution Order")
    lines.append("")
    lines.append("1. Generate more review samples for Carbon Fiber, Nero Marble, Kintsugi Marble, Brushed Titanium, and Walnut Burl.")
    lines.append("2. Keep Concrete and Vellum as low-volume remake lanes only; do not expand until Rex passes them.")
    lines.append("3. Use deep-focus broad-sharp material coverage only. Shallow depth-of-field images are not first-batch Adobe Stock upload candidates.")
    lines.append("4. Metadata rule: natural title under Adobe guidance, first 10 keywords mirror title concepts, 15-25 total relevant keywords.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sample_queue(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    variants = {
        "Carbon Fiber / Technical Weave": [
            "diagonal weave, blue black studio rim highlights",
            "straight basket weave, graphite gray material field",
            "tight premium weave, black-on-black subtle sheen",
            "large scale composite fabric, crisp edge-to-edge detail",
            "matte technical fiber, minimal reflection, copy-space friendly",
            "dark carbon twill, clean repeat-friendly surface",
        ],
        "Nero Marble / Luxury Stone": [
            "minimal ivory veins, black polished slab",
            "wide copy-space marble plane, restrained veins",
            "subtle gray-black stone, luxury interior backdrop",
            "high-contrast black marble, realistic mineral grain",
            "quiet gallery stone surface, few elegant veins",
        ],
        "Kintsugi Marble / Gold Repair Stone": [
            "black marble with restrained gold repair veins",
            "cream marble with sparse kintsugi lines",
            "gray stone with thin gold mineral repair paths",
            "copy-space kintsugi stone, minimal crack density",
            "luxury abstract marble repair pattern, realistic grain",
            "matte stone kintsugi, clean background use",
        ],
        "Brushed Titanium / Chrome Silver": [
            "horizontal brushed titanium, cool silver surface",
            "diagonal brushed metal, fine micro scratches",
            "dark graphite titanium, product backdrop finish",
            "soft studio reflection, steel gray satin metal",
            "silver chrome texture, tactile grain not gradient",
        ],
        "Walnut Burl / Executive Wood": [
            "dark walnut burl, satin executive desk finish",
            "cool brown veneer, swirling organic rings",
            "luxury wood grain, broad sharp surface",
            "minimal dark wood copy-space background",
            "walnut burl macro, controlled warm highlights",
        ],
        "Clean Architectural Concrete / Plaster": [
            "clean gray concrete, subtle pores, copy space",
            "warm travertine plaster, quiet luxury wall surface",
            "minimal cement background, matte studio side light",
        ],
        "Archival Vellum / Premium Paper": [
            "clean off-white vellum, subtle fibers",
            "museum paper texture, blank copy-space center",
            "warm archival paper, fine tactile grain",
        ],
    }
    fields = [
        "Queue_ID",
        "Lane",
        "Variant",
        "Prompt",
        "Title_Pattern",
        "First_10_Keywords",
        "Status",
        "Rex_QA_Note",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        n = 0
        for lane in sorted(LANES, key=lambda item: item["priority"]):
            for variant in variants[lane["lane"]]:
                n += 1
                prompt = lane["prompt_spine"].replace(
                    "texture background,", f"texture background, {variant},"
                )
                writer.writerow(
                    {
                        "Queue_ID": f"ADOBE-MARKET-SAMPLE-{n:03d}",
                        "Lane": lane["lane"],
                        "Variant": variant,
                        "Prompt": prompt,
                        "Title_Pattern": lane["title_pattern"],
                        "First_10_Keywords": lane["first_keywords"],
                        "Status": "READY_FOR_MJ_RELAXED_WHEN_THERMAL_OK",
                        "Rex_QA_Note": lane["qa_rule"],
                    }
                )


def write_sample_md(csv_path: Path, md_path: Path) -> None:
    by_lane: dict[str, int] = {}
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            by_lane[row["Lane"]] = by_lane.get(row["Lane"], 0) + 1
    lines = [
        "# Adobe Stock Market Sample MJ Queue",
        "",
        f"Generated: {now_et()} ET",
        "",
        "Purpose: market-backed relaxed draft samples for Rex visual training. No Fast, no upload, no marketplace spend.",
        "",
        "## Counts",
        "",
    ]
    for lane, count in by_lane.items():
        lines.append(f"- {lane}: {count} prompts")
    lines.extend(
        [
            "",
            "## Dispatch Rule",
            "",
            "- Use Midjourney relaxed only.",
            "- Use U images as source only after Rex/sample QA.",
            "- Do not use shallow depth-of-field variants for first upload candidates.",
            "- Do not submit any grid to Adobe unless a separate QA gate proves 4MP+ and broad sharpness.",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    csv_path = DB / "Adobe_Stock_Market_DNA_Scout.csv"
    md_path = REVIEW / "Adobe_Stock_Market_DNA_Scout_latest.md"
    sample_csv = DB / "Adobe_Stock_Market_Sample_MJ_Queue.csv"
    sample_md = REVIEW / "Adobe_Stock_Market_Sample_MJ_Queue_latest.md"
    write_csv(csv_path)
    write_md(md_path)
    write_sample_queue(sample_csv)
    # Keep Rex's post-feedback expanded market sample set durable. The base
    # scout intentionally stays small, then the expander appends the broader
    # clean material lanes that Rex asked to review overnight.
    from adobe_stock_market_sample_expander import main as expand_market_samples

    expand_market_samples()
    write_sample_md(sample_csv, sample_md)
    print(
        f"[ADOBE-MARKET-DNA-SCOUT] lanes={len(LANES)} csv={csv_path} report={md_path} samples={sample_csv}"
    )


if __name__ == "__main__":
    main()
