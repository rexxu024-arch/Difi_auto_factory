from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "Database" / "Adobe_Stock_Market_Sample_MJ_Dispatch_Queue.csv"


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


TRAINING_VARIANTS = [
    ("Nero Marble", "deep black marble with sparse ivory veining, broad sharp commercial surface, elegant negative space", "Black marble texture background with sparse ivory veins", "black marble, marble texture, texture background, luxury stone, ivory veins, polished surface, interior design, product background, abstract, material"),
    ("Nero Marble", "charcoal stone slab, restrained gray-white mineral veins, clean edge-to-edge designer backdrop", "Charcoal marble texture background with mineral veins", "charcoal marble, stone texture, texture background, gray veins, luxury surface, abstract background, design resource, interior, polished stone, material"),
    ("Nero Marble", "minimal black marble copy-space field, one diagonal ivory mineral path, high-end editorial layout background", "Minimal black marble copy space background", "black marble, copy space, texture background, luxury background, stone surface, editorial backdrop, marble veins, design, abstract, material"),
    ("Kintsugi Marble", "cream marble with thin gold repair lines, sparse crack density, clean luxury packaging background", "Cream kintsugi marble texture with gold veins", "kintsugi marble, cream marble, gold veins, texture background, luxury stone, abstract background, packaging, repair lines, design resource, material"),
    ("Kintsugi Marble", "black kintsugi stone, controlled gold seams, realistic mineral grain, no ornament clutter", "Black kintsugi stone texture with gold seams", "black kintsugi, kintsugi texture, gold seams, stone background, luxury texture, abstract, material surface, design resource, marble, background"),
    ("Kintsugi Marble", "gray kintsugi marble slab, subtle gold mineral repair paths, broad sharp surface for stock buyers", "Gray kintsugi marble texture background", "gray marble, kintsugi, gold veins, texture background, stone surface, luxury design, abstract background, material, commercial use, macro"),
    ("Walnut Burl", "dark walnut burl veneer, satin finish, swirling rings, clean premium desk-surface background", "Dark walnut burl wood grain texture background", "walnut burl, wood grain, wood texture, texture background, dark wood, veneer, luxury surface, executive desk, material, background"),
    ("Walnut Burl", "cool brown walnut burl, continuous veneer sheet, organic figure without muddy noise", "Cool walnut burl veneer texture background", "walnut veneer, burl wood, wood texture, background, grain, luxury wood, dark brown, material surface, interior design, texture"),
    ("Walnut Burl", "high contrast walnut burl macro, golden brown figure, broad sharp usable surface", "Walnut burl macro wood texture background", "walnut burl, macro wood, wood grain, texture background, brown, luxury material, veneer, design resource, surface, abstract"),
    ("Carbon Fiber", "black carbon fiber twill, crisp technical weave, satin highlights, full-frame sharpness", "Black carbon fiber twill texture background", "carbon fiber, twill weave, texture background, black graphite, technical texture, material, surface, pattern, automotive, design"),
    ("Carbon Fiber", "matte graphite basket weave, subtle blue-black rim light, no blur, clean product background", "Graphite carbon fiber weave texture background", "carbon fiber texture, graphite weave, texture background, black, technical material, product background, pattern, surface, composite, macro"),
    ("Carbon Fiber", "large scale carbon composite fabric, clean diagonal pattern, sharp weave detail across the frame", "Carbon composite fabric texture background", "carbon composite, carbon fiber, fabric texture, weave background, technical surface, black texture, material, pattern, design resource, macro"),
    ("Brushed Titanium", "horizontal brushed titanium sheet, fine micro scratches, tactile metal grain, not a flat gradient", "Brushed titanium metal texture background", "brushed titanium, metal texture, texture background, silver metal, micro scratches, industrial surface, material, steel, design resource, macro"),
    ("Brushed Titanium", "dark graphite titanium metal, diagonal brushing, controlled studio reflection, premium hardware surface", "Dark brushed titanium texture background", "dark titanium, brushed metal, metal texture, graphite, texture background, industrial, premium surface, material, macro, design"),
    ("Brushed Titanium", "cool silver brushed metal, crisp directional grain, product mockup background, broad sharp focus", "Silver brushed metal texture background", "silver brushed metal, metal texture, texture background, chrome, steel, industrial surface, material, design resource, macro, abstract"),
    ("Smoky Jade", "flat smoky jade slab, translucent green mineral depth, crisp veins, broad commercial background", "Smoky jade stone texture background", "smoky jade, jade texture, green stone, texture background, mineral surface, luxury material, abstract, design resource, macro, background"),
    ("Smoky Jade", "dark green jade mineral plane, cloudy depth, clean sharp surface without crystal object silhouette", "Dark green jade mineral texture background", "green jade, jade stone, mineral texture, texture background, dark green, luxury surface, abstract, material, macro, design"),
    ("Smoky Jade", "soft celadon jade slab, subtle internal veins, clean product backdrop, not silk or fog", "Celadon jade stone texture background", "celadon jade, jade texture, stone background, green mineral, texture, surface, luxury material, abstract background, macro, design"),
    ("Architectural Plaster", "clean warm limewash plaster wall, subtle trowel texture, large copy space, no stains", "Warm limewash plaster wall texture background", "limewash plaster, wall texture, texture background, warm neutral, copy space, plaster surface, interior design, minimal, material, background"),
    ("Architectural Plaster", "cool gray microcement wall, fine pores, brutalist minimal background, clean commercial surface", "Gray microcement wall texture background", "microcement, concrete wall, wall texture, texture background, gray plaster, minimal, copy space, cement surface, interior, design"),
    ("Architectural Plaster", "travertine plaster wall, quiet beige mineral texture, high-end interior backdrop, broad sharpness", "Travertine plaster texture background", "travertine plaster, plaster texture, texture background, beige wall, interior design, mineral surface, copy space, luxury wall, material, background"),
    ("Archival Paper", "clean off-white cotton paper, visible fibers, blank center field, museum conservation surface", "Off white cotton paper texture background", "cotton paper, paper texture, texture background, off white, fibers, blank paper, copy space, archival paper, material, design"),
    ("Archival Paper", "warm vellum paper, subtle translucent fiber texture, clean stationery mockup background", "Warm vellum paper texture background", "vellum paper, paper texture, texture background, warm white, stationery, fibers, blank background, material surface, copy space, design"),
    ("Archival Paper", "handmade watercolor paper, fine tooth texture, clean white field, no stains or writing", "White watercolor paper texture background", "watercolor paper, paper texture, white paper, texture background, fine tooth, fibers, blank, art paper, material, copy space"),
    ("Obsidian Glass", "black obsidian glass surface, smoky reflections, subtle mineral inclusions, clean dark luxury background", "Black obsidian glass texture background", "obsidian glass, black glass, texture background, dark surface, luxury material, reflection, mineral texture, abstract, design, macro"),
    ("Onyx Stone", "honey onyx stone slab, translucent amber bands, polished mineral surface, broad sharp focus", "Honey onyx stone texture background", "onyx stone, honey onyx, stone texture, texture background, amber bands, mineral surface, luxury material, abstract, macro, design"),
    ("Terrazzo Stone", "premium black terrazzo surface, sparse white and brass chips, clean modern material background", "Black terrazzo stone texture background", "black terrazzo, terrazzo texture, texture background, stone chips, modern surface, material, interior design, abstract, macro, background"),
    ("Slate Stone", "dark slate stone surface, layered mineral striations, clean matte texture, product background", "Dark slate stone texture background", "slate stone, stone texture, texture background, dark slate, layered mineral, matte surface, material, design resource, macro, background"),
    ("Raw Silk", "ivory raw silk fabric, crisp woven slubs, broad sharp textile surface, luxury packaging background", "Ivory raw silk fabric texture background", "raw silk, silk texture, fabric texture, texture background, ivory fabric, textile, luxury material, woven surface, macro, design"),
    ("Linen Canvas", "natural linen canvas, visible woven threads, clean neutral copy-space surface, no wrinkles", "Natural linen canvas texture background", "linen canvas, fabric texture, linen texture, texture background, natural textile, woven surface, neutral background, material, design, macro"),
    ("Frosted Glass", "frosted glass surface, soft diffused light, fine etched micro texture, clean commercial backdrop", "Frosted glass texture background", "frosted glass, glass texture, texture background, translucent surface, diffused light, material, abstract, design resource, macro, background"),
    ("Smoked Acrylic", "smoked gray acrylic sheet, subtle internal reflections, premium translucent plastic material, broad sharp surface", "Smoked acrylic sheet texture background", "smoked acrylic, acrylic texture, texture background, translucent plastic, gray surface, reflection, material, design resource, macro, background"),
    ("Pearlescent Shell", "mother of pearl nacre surface, iridescent bands, clean organic luxury material background", "Mother of pearl nacre texture background", "mother of pearl, nacre texture, pearlescent, texture background, iridescent surface, shell, luxury material, abstract, macro, design"),
    ("Holographic Foil", "subtle holographic foil surface, controlled rainbow refraction, crisp commercial packaging background", "Holographic foil texture background", "holographic foil, foil texture, texture background, iridescent, rainbow reflection, packaging, material, abstract, design resource, macro"),
    ("Black Leather", "black pebbled leather grain, clean premium texture, matte highlights, broad sharp surface", "Black pebbled leather texture background", "black leather, leather texture, texture background, pebbled leather, material surface, luxury texture, fashion background, macro, design, abstract"),
    ("Saffiano Leather", "saffiano leather crosshatch texture, dark oxblood tone, premium fashion material background", "Oxblood saffiano leather texture background", "saffiano leather, leather texture, oxblood, texture background, crosshatch, fashion material, luxury surface, macro, design, abstract"),
    ("Copper Patina", "verdigris copper patina, controlled turquoise oxidation, clean metal surface without dirt", "Verdigris copper patina texture background", "copper patina, verdigris, metal texture, texture background, oxidized copper, turquoise surface, material, abstract, design resource, macro"),
    ("Basalt Stone", "black basalt stone surface, fine volcanic pores, matte mineral texture, clean product background", "Black basalt stone texture background", "basalt stone, black stone, stone texture, texture background, volcanic rock, matte surface, mineral, material, macro, design"),
    ("Travertine Stone", "warm travertine stone slab, subtle linear pores, beige luxury interior material background", "Travertine stone texture background", "travertine, stone texture, texture background, beige stone, interior design, natural pores, luxury material, surface, macro, background"),
    ("Sandstone", "minimal beige sandstone surface, fine sediment lines, warm neutral copy-space texture", "Beige sandstone texture background", "sandstone, stone texture, texture background, beige surface, sediment lines, natural material, neutral background, design resource, macro, copy space"),
    ("Cork Board", "clean natural cork texture, fine granules, warm craft material background, no pins", "Natural cork texture background", "cork texture, cork background, texture background, natural material, granules, craft surface, warm background, design resource, macro, abstract"),
    ("Recycled Paper", "premium recycled paper texture, subtle fibers and flecks, clean neutral background", "Recycled paper texture background", "recycled paper, paper texture, texture background, fibers, flecks, neutral background, sustainable material, stationery, macro, design"),
    ("Woven Wool", "dark woven wool textile, crisp threads, clean premium fabric texture background", "Dark woven wool fabric texture background", "woven wool, wool texture, fabric texture, texture background, dark textile, threads, material surface, macro, design, abstract"),
    ("Boucle Fabric", "cream boucle fabric texture, tactile loops, broad sharp textile surface, clean interior background", "Cream boucle fabric texture background", "boucle fabric, fabric texture, cream textile, texture background, looped fabric, interior design, material, macro, design, background"),
    ("Ribbed Glass", "ribbed fluted glass texture, vertical refractive lines, clean architectural material background", "Ribbed glass texture background", "ribbed glass, fluted glass, glass texture, texture background, refractive lines, architectural material, surface, macro, design"),
    ("Liquid Chrome", "liquid chrome surface, smooth mirror waves, abstract silver metal background, controlled highlights", "Liquid chrome abstract metal texture background", "liquid chrome, chrome texture, metal background, silver abstract, reflective surface, texture background, material, design resource, macro"),
    ("Dark Granite", "dark granite stone surface, fine mineral speckles, sharp commercial countertop texture", "Dark granite stone texture background", "dark granite, granite texture, stone background, texture background, mineral speckles, countertop, material, interior design, macro, surface"),
    ("White Ceramic", "white glazed ceramic surface, subtle crackle glaze, clean bright material background", "White ceramic crackle glaze texture background", "white ceramic, ceramic texture, crackle glaze, texture background, material surface, clean background, pottery glaze, macro, design"),
    ("Blue Limestone", "blue gray limestone surface, fossil-like mineral flecks, clean architectural stone texture", "Blue gray limestone texture background", "limestone, stone texture, blue gray, texture background, architectural stone, mineral flecks, material, surface, macro, design"),
    ("Matte Rubber", "matte black rubber surface, fine micro texture, clean industrial product background", "Matte black rubber texture background", "black rubber, rubber texture, texture background, matte surface, industrial material, product background, macro, design, abstract"),
]

HIGH_CONFIDENCE_REX_VARIANTS = [
    ("Nero Marble", "premium black marble slab with broad clean negative space, sparse ivory veins, crisp polished mineral detail, no random lightning cracks", "Premium black marble texture with ivory veins", "black marble, marble texture, luxury stone, ivory veins, texture background, polished surface, premium background, interior design, abstract, material"),
    ("Nero Marble", "black and charcoal marble surface, controlled diagonal white veining, designer stock backdrop, sharp edge-to-edge stone grain", "Charcoal black marble texture background", "black marble, charcoal marble, white veins, stone texture, texture background, luxury surface, abstract background, design resource, material, polished"),
    ("Kintsugi Marble", "white marble with thin metallic gold kintsugi seams, clean luxury packaging background, sparse elegant cracks, broad sharp surface", "White kintsugi marble texture with gold seams", "kintsugi marble, white marble, gold seams, marble texture, texture background, luxury stone, packaging background, abstract, material, polished"),
    ("Kintsugi Marble", "cream stone with restrained gold repair lines, museum-clean mineral surface, elegant copy-space, no ornament clutter", "Cream kintsugi stone texture background", "kintsugi, cream stone, gold veins, texture background, luxury material, marble surface, copy space, abstract background, design resource, mineral"),
    ("Carbon Fiber", "premium carbon fiber weave texture, symmetrical twill pattern, crisp black graphite strands, broad sharp commercial background", "Premium carbon fiber weave texture background", "carbon fiber, carbon texture, weave pattern, black graphite, texture background, technical material, surface, automotive, product background, macro"),
    ("Carbon Fiber", "blue black carbon composite fabric, clean diagonal weave, satin studio highlights, no depth blur, sharp full-frame textile detail", "Blue black carbon fiber texture background", "carbon fiber, blue black, weave texture, texture background, composite fabric, technical surface, material, pattern, macro, design"),
    ("Brushed Titanium", "brushed titanium sheet with crisp linear grain, realistic micro scratches, cool silver industrial surface, broad sharp focus", "Brushed titanium sheet texture background", "brushed titanium, titanium texture, metal texture, silver metal, texture background, micro scratches, industrial surface, material, product background, macro"),
    ("Brushed Titanium", "dark gunmetal brushed metal, diagonal grain, subtle studio reflection, premium hardware background, not a soft gradient", "Dark gunmetal brushed metal texture", "gunmetal, brushed metal, metal texture, dark metal, texture background, industrial material, surface, hardware, macro, design"),
    ("Walnut Burl", "dark walnut burl veneer, elegant swirling figure, polished executive desk surface, sharp continuous wood grain", "Dark walnut burl veneer texture background", "walnut burl, wood texture, burl veneer, wood grain, texture background, dark wood, luxury surface, executive desk, material, interior"),
    ("Walnut Burl", "black walnut wood grain, clean linear figure, satin furniture finish, premium natural material background", "Black walnut wood grain texture background", "black walnut, wood grain, wood texture, texture background, dark wood, furniture finish, natural material, interior design, surface, background"),
    ("Onyx Stone", "honey onyx translucent stone slab, amber mineral bands, polished luxury surface, sharp commercial material background", "Honey onyx stone texture background", "honey onyx, onyx stone, stone texture, amber bands, texture background, mineral surface, luxury material, abstract, polished, macro"),
    ("Onyx Stone", "black onyx stone with subtle gold-brown mineral ribbons, clean high contrast luxury slab, edge-to-edge sharpness", "Black onyx stone texture background", "black onyx, onyx texture, stone background, gold veins, luxury stone, texture background, mineral surface, abstract, material, polished"),
    ("Travertine Stone", "warm beige travertine slab, subtle linear pores, clean architectural surface, broad sharp interior design background", "Beige travertine stone texture background", "travertine, beige stone, stone texture, texture background, interior design, architectural surface, natural pores, luxury material, macro, background"),
    ("Slate Stone", "dark slate stone with fine layered striations, matte clean mineral texture, product mockup background", "Dark slate stone texture background", "slate stone, dark slate, stone texture, texture background, layered mineral, matte surface, material, product background, macro, design"),
    ("Linen Canvas", "black linen canvas texture, crisp woven threads, premium textile background, clean full-frame surface", "Black linen fabric texture background", "black linen, linen texture, fabric texture, texture background, woven threads, textile surface, material, macro, design, abstract"),
    ("Linen Canvas", "warm natural linen fabric, visible weave, clean neutral copy-space textile background, no wrinkles or dirt", "Natural linen fabric texture background", "linen texture, natural linen, fabric texture, texture background, woven fabric, neutral background, textile, material, macro, copy space"),
    ("Archival Paper", "clean black handmade paper texture, visible fibers, premium stationery background, sharp matte surface", "Black handmade paper texture background", "black paper, handmade paper, paper texture, texture background, fibers, stationery, matte surface, material, design resource, macro"),
    ("Archival Paper", "warm ivory cotton paper, subtle fiber tooth, blank center copy-space, clean archival stationery texture", "Ivory cotton paper texture background", "cotton paper, ivory paper, paper texture, texture background, copy space, stationery, fibers, archival paper, material, design"),
    ("Architectural Plaster", "warm gray limewash plaster wall, subtle trowel marks, clean editorial copy-space, no stains or cracks", "Gray limewash plaster wall texture", "limewash, plaster texture, wall texture, texture background, gray wall, copy space, interior design, minimal background, material, surface"),
    ("Architectural Plaster", "clean microcement wall surface, soft gray mineral texture, brutalist interior backdrop, broad sharp commercial background", "Gray microcement wall texture background", "microcement, concrete wall, wall texture, texture background, gray plaster, interior design, minimal surface, material, copy space, background"),
    ("Obsidian Glass", "black obsidian glass slab, subtle smoky reflection, crisp mineral inclusions, clean dark luxury texture background", "Black obsidian glass texture background", "obsidian glass, black glass, texture background, dark surface, reflection, luxury material, mineral texture, abstract, macro, design"),
    ("Frosted Glass", "frosted architectural glass, fine etched grain, soft diffused studio light, sharp translucent material surface", "Frosted glass texture background", "frosted glass, glass texture, texture background, translucent surface, etched glass, architectural material, diffused light, macro, design, background"),
    ("Pearlescent Shell", "mother of pearl nacre, clean iridescent bands, sharp organic luxury surface, commercial texture background", "Mother of pearl nacre texture background", "mother of pearl, nacre texture, pearlescent, texture background, iridescent surface, shell texture, luxury material, macro, abstract, design"),
    ("Holographic Foil", "subtle holographic foil sheet, controlled rainbow refraction, crisp packaging material background, no chaotic glare", "Subtle holographic foil texture background", "holographic foil, foil texture, texture background, iridescent, packaging material, rainbow reflection, abstract surface, design resource, macro, background"),
]


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\r", " ").replace("\n", " ").split()).strip()


def read_rows() -> tuple[list[dict[str, str]], list[str]]:
    with QUEUE.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or HEADERS)


def next_number(rows: list[dict[str, str]]) -> int:
    found = []
    for row in rows:
        match = re.search(r"ADOBE-MARKET-(\d+)", row.get("Internal_SKU", ""))
        if match:
            found.append(int(match.group(1)))
    return max(found or [0]) + 1


def prompt_for(family: str, variant: str) -> str:
    return (
        f"Extreme macro photography of {variant}, safe commercial stock material background, "
        "broad sharp texture coverage across the whole image, deep focus across the material plane, "
        "crisp micro detail, realistic physical surface, useful for product mockups, packaging, web banners, "
        "and interior design mood boards, 100mm macro lens, f/11, ultra photorealistic, no shallow depth of field, "
        "no blurred foreground, no bokeh, no logo, no text, no watermark, no people, no product object, "
        "--ar 3:2 --style raw --v 6.1 --relax"
    )


def main() -> int:
    rows, fields = read_rows()
    for field in HEADERS:
        if field not in fields:
            fields.append(field)
    existing_concepts = {clean(row.get("Concept_Name")) for row in rows}
    n = next_number(rows)
    added = 0
    for family, variant, title, keywords in [*TRAINING_VARIANTS, *HIGH_CONFIDENCE_REX_VARIANTS]:
        concept = f"{family} / {variant}"
        if concept in existing_concepts:
            continue
        sku = f"ADOBE-MARKET-{n:03d}"
        source = f"ADOBE-MARKET-SAMPLE-{n:03d}"
        rows.append(
            {
                "Internal_SKU": sku,
                "Source_Queue_ID": source,
                "Dispatch_Status": "READY_FOR_MJ",
                "Batch": "Adobe Stock Rex Training Expansion",
                "Concept_Name": concept,
                "Product_Type": "Adobe Stock material training sample",
                "Recommended_Format": "MJ relaxed draft grid only; U images only after Rex visual pass; no Fast, no upload.",
                "MJ_Master_Prompt": prompt_for(family, variant),
                "QA_Gate": "REX_TRAINING_SAMPLE; DEEP_FOCUS_BROAD_SHARP_TEXTURE_REQUIRED; NO_FAST; NO_UPLOAD",
                "Output_Folder": f"Output/Adobe_Stock/Market_Samples/{source}",
                "Review_Note": "PASS if broad-sharp, commercially useful, clean, and not muddy/blurred/repetitive.",
                "Upscale_Policy": "NO_FAST; RELAXED_GRID_THEN_SELECTED_U_ONLY; LOCAL_4MP_FIX_AFTER_QA",
                "Adobe_Title": title,
                "Adobe_Keywords": keywords,
                "Adobe_Category": "8",
                "Created_Using_AI": "true",
                "Release_Required": "false",
            }
        )
        existing_concepts.add(concept)
        n += 1
        added += 1
    with QUEUE.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})
    print(f"[ADOBE-TRAINING-POOL-EXPAND] added={added} total={len(rows)} queue={QUEUE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
