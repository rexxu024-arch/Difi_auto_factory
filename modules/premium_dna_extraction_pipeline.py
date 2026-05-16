from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "Database"
REVIEW = ROOT / "Review_Packets" / "Project_Mirror"
REPORT = REVIEW / "PREMIUM_DNA_EXTRACTION_V1.md"
SOURCE_QUEUE = DB / "Premium_DNA_Source_Queue.csv"
MENTOR_HUB = DB / "Premium_Mentor_Hub.csv"
AB_MATRIX = DB / "Premium_DNA_AB_Comparison.csv"
STATE = DB / "Premium_DNA_State.json"
PROGRESS_LOG = ROOT / "PROGRESS_LOG.md"


@dataclass(frozen=True)
class PremiumDnaSet:
    dna_id: str
    lane: str
    product_tier: str
    source_family: str
    source_url: str
    source_use: str
    requires_vision_api: str
    old_logic_fit: str
    vision_target: str
    codex_curated_fit: str
    current_winner: str
    material_parameters: str
    lighting_matrix: str
    composition_rules: str
    buyer_intent_words: str
    negative_guards: str
    mj_prompt_stem: str
    qa_gate: str
    notes: str


def rows() -> list[PremiumDnaSet]:
    return [
        PremiumDnaSet(
            dna_id="PMD-001",
            lane="NYC Luxury Executive Office",
            product_tier="$48-$98 entrance poster / $128 acrylic",
            source_family="RH gallery language, Manhattan penthouse, private design studio",
            source_url="https://rh.com/content/rh/it/en/galleries",
            source_use="Extract only room scale, restraint, walnut/stone/black-metal palette, and gallery pacing.",
            requires_vision_api="Optional for entrance products; required before First Audit or $128+ hero use.",
            old_logic_fit="Good enough for routine executive desk poster titles and simple acrylic tests.",
            vision_target="Measure negative space, furniture scale, warm-neutral light falloff, and gallery symmetry.",
            codex_curated_fit="Use as the default safe commercial lane for Etsy/eBay premium POD.",
            current_winner="C for mid-tier now; B+C for high-end.",
            material_parameters="dark walnut, smoked glass, honed stone, brushed blackened steel, low-sheen acrylic reflection",
            lighting_matrix="warm overhead fill, soft window bounce, low contrast shadows, no theatrical neon",
            composition_rules="single dominant object, generous negative space, desk or console horizon line, gallery-like restraint",
            buyer_intent_words="executive office gift; quiet luxury desk decor; minimalist boss decor; architecture lover gift",
            negative_guards="no clutter, no cheap gold, no casino neon, no generic AI office, no visible brand furniture",
            mj_prompt_stem=(
                "quiet luxury executive office object, smoky jade and brushed black metal, dark walnut console, "
                "restrained Manhattan gallery interior, warm architectural lighting, exact product-preserving mockup"
            ),
            qa_gate="Reject if it looks like stock office decor or if the object loses product identity.",
            notes="Best lane for public POD because it sells use case before concept.",
        ),
        PremiumDnaSet(
            dna_id="PMD-002",
            lane="European Dark Academia Archive",
            product_tier="$48 archival print / digital archive support only",
            source_family="Oxford/Cambridge libraries, museum plates, old manuscript rooms",
            source_url="https://en.wikipedia.org/wiki/Wren_Library",
            source_use="Extract shelving density, amber paper, black oak, brass instruments, and archival order.",
            requires_vision_api="Optional for planner/digital; recommended for premium poster hero composition.",
            old_logic_fit="Good for low/mid digital bundles and planner inserts.",
            vision_target="Detect page border width, text-free writing space, paper tone, and object arrangement hierarchy.",
            codex_curated_fit="Keep for Etsy archive and selected premium posters; avoid overusing gothic cliches.",
            current_winner="A+C for archive products; B for premium poster scenes.",
            material_parameters="vellum paper, oxidized brass, black oak, cracked leather, smoke-stained ivory margins",
            lighting_matrix="candle-warm side light, deep shelf shadows, narrow highlight on paper edge",
            composition_rules="flat-lay or library wall, strong central writing field for printables, border ornament kept thin",
            buyer_intent_words="dark academia journal pages; grimoire study inserts; reading nook wall art; archival library decor",
            negative_guards="no readable text, no fake Latin, no skull spam, no over-busy borders, no low-res parchment",
            mj_prompt_stem=(
                "European archive study object, black oak library, oxidized brass instruments, vellum paper, "
                "chiaroscuro side light, clean central field, no readable text"
            ),
            qa_gate="Reject if text appears, if border eats writing space, or if it becomes Halloween costume decor.",
            notes="This is one of the few digital-friendly lanes, but it should not dominate the store.",
        ),
        PremiumDnaSet(
            dna_id="PMD-003",
            lane="Imperial Kintsugi Material Field",
            product_tier="$128 acrylic / $295 anchor candidate",
            source_family="museum jade, bronze patina, kintsugi repair, mineral fracture fields",
            source_url="https://en.wikipedia.org/wiki/Kintsugi",
            source_use="Extract repair-line philosophy, fractured surface rhythm, matte stone, and restrained metallic seams.",
            requires_vision_api="Required for high-end use. Old prompt logic overproduces cheap gold cracks.",
            old_logic_fit="Risky; okay only for background material tests.",
            vision_target="Quantify crack spacing, seam thickness, stone translucency, and gold restraint.",
            codex_curated_fit="Strongest current OpenClaw material language when kept quiet and physical.",
            current_winner="B+C.",
            material_parameters="unpolished smoky jade, oxidized bronze, hairline kintsugi seams, mineral inclusions, heavy optical acrylic",
            lighting_matrix="grazing light across cracks, tiny metallic glints, cool black background, no high saturation",
            composition_rules="macro material field or single relic object; seams must guide the eye without becoming pattern wallpaper",
            buyer_intent_words="smoky jade acrylic block; kintsugi office gift; quiet luxury relic; collectible desk object",
            negative_guards="no bright yellow gold, no dragon, no temple, no lucky-cat cliche, no plastic toy shine",
            mj_prompt_stem=(
                "unpolished smoky jade relic with restrained hairline kintsugi, oxidized bronze undertone, "
                "heavy optical acrylic depth, grazing museum light, black velvet negative space"
            ),
            qa_gate="Reject if seams become loud clipart or if jade turns plastic/candy green.",
            notes="This should feed First Audit and the $128/$295 studio line.",
        ),
        PremiumDnaSet(
            dna_id="PMD-004",
            lane="Contemporary Sculpture Gallery",
            product_tier="$98 premium print / $128 acrylic",
            source_family="Artsy/Bowman/Contini sculpture exhibitions, bronze/marble/steel in white-box gallery",
            source_url="https://www.artsy.net/viewing-room/contini-art-gallery-pablo-atchugarry",
            source_use="Extract form-light-space relationship, marble/bronze restraint, and gallery object isolation.",
            requires_vision_api="Required before copying any composition logic into First Audit; optional for POD.",
            old_logic_fit="Weak; tends to generate generic museum statue language.",
            vision_target="Measure object silhouette, plinth scale, shadow softness, wall distance, and material specularity.",
            codex_curated_fit="Use for high-end acrylic objects and gallery mockups, not digital bundles.",
            current_winner="B+C.",
            material_parameters="honed marble, patinated bronze, brushed steel, thick gallery plinth, matte wall paint",
            lighting_matrix="overhead gallery track light, crisp object shadow, clean wall bounce, restrained contrast",
            composition_rules="isolated sculptural mass, clear plinth, human-height negative space, no crowded props",
            buyer_intent_words="gallery desk sculpture; art collector gift; modern relic decor; architectural office accent",
            negative_guards="no celebrity likeness, no direct artist style, no museum label text, no fake famous sculpture copy",
            mj_prompt_stem=(
                "contemporary sculptural relic, honed marble and patinated bronze, isolated on gallery plinth, "
                "track light shadow geometry, collector-grade object photography"
            ),
            qa_gate="Reject if it resembles a known artist's signature object too closely.",
            notes="Strong for private/demo line, needs IP distance.",
        ),
        PremiumDnaSet(
            dna_id="PMD-005",
            lane="Brutalist Penthouse Artifact",
            product_tier="$149 bundle / $295 anchor",
            source_family="1stDibs high-end decorative objects, black marble, bronze, architectural fragments",
            source_url="https://www.1stdibs.com/furniture/decorative-objects/sculptures/",
            source_use="Extract object-value cues: plinth, provenance feel, material gravity, collector photography.",
            requires_vision_api="Required for anchor products and bundle hero; optional for title/price tests.",
            old_logic_fit="Not enough for anchor pricing; useful only as seed phrase.",
            vision_target="Analyze luxury-product photography crop, specular highlights, surface imperfections, and scale cues.",
            codex_curated_fit="Use sparingly as the 'expensive object' lane, especially for private clients.",
            current_winner="B+C.",
            material_parameters="black marble, patinated bronze, smoky resin, beveled optical acrylic, hairline scratches",
            lighting_matrix="single softbox reflection, black-to-warm gradient falloff, small edge highlights",
            composition_rules="object fills 55-70 percent frame, low camera angle, heavy base, no decorative clutter",
            buyer_intent_words="collector desk object; luxury office artifact; penthouse decor; founder gift",
            negative_guards="no mass-market statue, no gold trophy, no fantasy creature, no logo, no fake auction label",
            mj_prompt_stem=(
                "brutalist collector artifact, black marble base, patinated bronze and smoky acrylic, "
                "penthouse object photography, heavy mass, low camera angle, premium catalog lighting"
            ),
            qa_gate="Reject if it reads as fantasy game prop instead of collector-grade design object.",
            notes="Best for $149 bundle and $295 anchor, not for cheap marketplace inventory.",
        ),
    ]


def write_csv(path: Path, records: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)


def build_report(items: list[PremiumDnaSet]) -> str:
    lines: list[str] = []
    lines.append("# Premium DNA Extraction V1")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("## Decision")
    lines.append("")
    lines.append(
        "Use a tiered routing model. Routine Etsy/eBay POD can use old OpenClaw experience plus Codex curation. "
        "Mid-tier products should mix Premium DNA. First Audit, cousin demos, $128 acrylic, $149 bundles, and $295 anchors "
        "must use source-derived DNA plus human/Codex judgment before upscale or public release."
    )
    lines.append("")
    lines.append("## A/B/C Experiment Model")
    lines.append("")
    lines.append("- A / Old logic: Claude-or-Codex imagination from existing OpenClaw patterns.")
    lines.append("- B / Source-derived vision: top-platform references parsed into material, lighting, composition, and buyer-intent DNA.")
    lines.append("- C / Codex/Rex standard: practical taste filter learned from Rex feedback and marketplace product fit.")
    lines.append("")
    lines.append("Promotion rule: low-risk POD may ship with C+A; premium public POD needs C+B; First Audit and private demos require B+C and Rex visual review.")
    lines.append("")
    lines.append("## Five Seed DNA Sets")
    lines.append("")
    for item in items:
        lines.append(f"### {item.dna_id} - {item.lane}")
        lines.append("")
        lines.append(f"- Product tier: {item.product_tier}")
        lines.append(f"- Source family: {item.source_family}")
        lines.append(f"- Source URL: {item.source_url}")
        lines.append(f"- Source use: {item.source_use}")
        lines.append(f"- Requires Vision API: {item.requires_vision_api}")
        lines.append(f"- Current winner: {item.current_winner}")
        lines.append(f"- Material parameters: {item.material_parameters}")
        lines.append(f"- Lighting matrix: {item.lighting_matrix}")
        lines.append(f"- Composition rules: {item.composition_rules}")
        lines.append(f"- Buyer-intent words: {item.buyer_intent_words}")
        lines.append(f"- Negative guards: {item.negative_guards}")
        lines.append(f"- MJ prompt stem: `{item.mj_prompt_stem}`")
        lines.append(f"- QA gate: {item.qa_gate}")
        lines.append(f"- Notes: {item.notes}")
        lines.append("")
    lines.append("## Immediate Use")
    lines.append("")
    lines.append("1. Apply PMD-001 and PMD-003 to the next Etsy POD acrylic/poster drip.")
    lines.append("2. Apply PMD-003, PMD-004, and PMD-005 to First Audit / cousin demo only after visual reference parsing.")
    lines.append("3. Keep PMD-002 as Etsy archive/digital support; do not let it dominate the shop.")
    lines.append("4. Do not copy or redistribute source images. Sources are reference anchors for abstracted DNA only.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    items = rows()
    records = [asdict(item) for item in items]

    write_csv(SOURCE_QUEUE, records)
    write_csv(MENTOR_HUB, records)
    write_csv(AB_MATRIX, records)
    REVIEW.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(build_report(items), encoding="utf-8")

    STATE.write_text(
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "dna_sets": len(items),
                "ab_tracks": ["old_logic", "source_vision", "codex_curated"],
                "premium_rule": "First Audit and $128+ acrylic use source-derived DNA plus Codex/Rex review.",
                "next_action": "Run a tiny image-vision sample on accepted references, then compare against existing Project Mirror grids.",
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    with PROGRESS_LOG.open("a", encoding="utf-8") as f:
        f.write(
            "\n\n## Premium DNA extraction seed - "
            + datetime.now().isoformat(timespec="seconds")
            + "\n"
        )
        f.write(
            "- Built 5 source-derived premium DNA seed sets and A/B/C routing matrix for Project Mirror / First Audit.\n"
        )
        f.write(f"- Report: `{REPORT}`\n")
        f.write(f"- Mentor hub CSV: `{MENTOR_HUB}`\n")
        f.write("- No marketplace publish, no upscale, no paid API call in this seed pass.\n")

    print(f"Wrote {len(items)} premium DNA sets")
    print(REPORT)
    print(MENTOR_HUB)
    print(AB_MATRIX)


if __name__ == "__main__":
    main()
