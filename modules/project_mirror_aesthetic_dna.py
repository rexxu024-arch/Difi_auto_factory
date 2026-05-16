"""Scaffold Project Mirror aesthetic DNA sampling and distillation.

This module does not scrape or publish. It creates the durable local
structure needed to collect high-end visual references, distill them into
Mentor-Hub-style DNA metadata, and compare old prompt logic against
reference-derived prompt logic.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
POOL_ROOT = DATABASE_DIR / "Aesthetic_DNA_Pool"
REVIEW_DIR = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"
INDEX_CSV = DATABASE_DIR / "Aesthetic_DNA_Pool_Index.csv"
DNA_SCHEMA_CSV = DATABASE_DIR / "Aesthetic_DNA_Distillation_Schema.csv"
SOURCE_CANDIDATES_CSV = DATABASE_DIR / "Aesthetic_DNA_Source_Candidates.csv"
STATE_JSON = DATABASE_DIR / "Project_Mirror_State.json"
PLAN_MD = REVIEW_DIR / "PROJECT_MIRROR_DNA_PIPELINE.md"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"


@dataclass(frozen=True)
class Niche:
    key: str
    label: str
    target_count: int
    source_targets: tuple[str, ...]
    visual_intent: str
    forbid: str


NICHES = (
    Niche(
        key="NYC_Luxury",
        label="NYC Luxury / Manhattan order",
        target_count=15,
        source_targets=(
            "official luxury interior brand lookbooks",
            "architectural digest style penthouse photography",
            "museum-grade furniture and material photography",
            "Manhattan hotel lobby / executive office photography",
        ),
        visual_intent=(
            "quiet luxury, walnut desks, brushed metal, smoked glass, "
            "controlled neutral palette, large-window city light"
        ),
        forbid="Pinterest collage spam, low-res realtor photos, obvious AI renders",
    ),
    Niche(
        key="European_Dark_Academia",
        label="European Dark Academia / library authority",
        target_count=15,
        source_targets=(
            "Oxford and Cambridge library architecture",
            "public-domain museum natural-history plates",
            "19th-century scientific instruments and manuscripts",
            "European museum reading-room interiors",
        ),
        visual_intent=(
            "aged paper, carved oak, brass instruments, dusted chiaroscuro, "
            "archival ink, scholarly visual hierarchy"
        ),
        forbid="fantasy cosplay, cheap skull motifs, text-heavy poster spam",
    ),
    Niche(
        key="Imperial_Kintsugi",
        label="Imperial Kintsugi / museum relic material",
        target_count=15,
        source_targets=(
            "museum jade and bronze artifact catalog photography",
            "high-end kintsugi repair close-ups",
            "Japanese craft exhibition macro material studies",
            "ceramic and metal conservation detail photography",
        ),
        visual_intent=(
            "smoky jade, unpolished ceramic, gold repair seams, oxidized bronze, "
            "refractive cracks, tactile imperfection"
        ),
        forbid="generic dragon/phoenix mythology, souvenir-shop Asian decor",
    ),
)


INDEX_HEADERS = [
    "Niche",
    "Sample_ID",
    "Status",
    "Source_Target",
    "Source_URL",
    "Local_File",
    "Quality_Gate",
    "Rights_Note",
    "Vision_Status",
    "Distilled_DNA_ID",
    "Notes",
]

DNA_HEADERS = [
    "DNA_ID",
    "Niche",
    "Source_Sample_IDs",
    "Physical_Material_Parameters",
    "Light_Distribution_Matrix",
    "Composition_Rules",
    "Purchase_Intent_Word_Cluster",
    "Negative_Prompt_Cluster",
    "Mentor_Hub_DNA_Style",
    "MJ_Test_Prompt_A_OldLogic",
    "MJ_Test_Prompt_B_ReferenceDerived",
    "QA_Status",
]

SOURCE_HEADERS = [
    "Niche",
    "Source_Title",
    "Source_URL",
    "Source_Type",
    "Use_Mode",
    "Why_Useful",
    "Do_Not_Do",
]

SOURCE_CANDIDATES = (
    {
        "Niche": "NYC_Luxury",
        "Source_Title": "Architectural Digest Manhattan penthouse archive",
        "Source_URL": "https://www.architecturaldigest.com/gallery/look-inside-this-sun-splashed-manhattan-penthouse",
        "Source_Type": "editorial interior reference",
        "Use_Mode": "visual DNA only",
        "Why_Useful": "Manhattan penthouse light, walnut tables, quiet luxury room hierarchy",
        "Do_Not_Do": "do not copy layout or redistribute images",
    },
    {
        "Niche": "NYC_Luxury",
        "Source_Title": "Architectural Digest Art Deco NYC penthouse",
        "Source_URL": "https://www.architecturaldigest.com/gallery/inside-a-soaring-new-york-city-penthouse-thats-infused-with-art-deco-charm",
        "Source_Type": "editorial interior reference",
        "Use_Mode": "visual DNA only",
        "Why_Useful": "Art Deco, antique walnut, brass, Verde marble, executive decor cues",
        "Do_Not_Do": "do not use publication images as marketplace assets",
    },
    {
        "Niche": "NYC_Luxury",
        "Source_Title": "RH gallery press archive",
        "Source_URL": "https://images.restorationhardware.com/media/press/World_of_RH_May_2022/SanFranciscoRelease_Final.pdf",
        "Source_Type": "brand press PDF",
        "Use_Mode": "material and spatial vocabulary only",
        "Why_Useful": "gallery/atelier staging, premium furniture material language",
        "Do_Not_Do": "do not scrape brand product photos for reuse",
    },
    {
        "Niche": "European_Dark_Academia",
        "Source_Title": "Radcliffe Camera architecture reference",
        "Source_URL": "https://en.wikipedia.org/wiki/Radcliffe_Camera",
        "Source_Type": "public architecture reference",
        "Use_Mode": "composition/history anchor",
        "Why_Useful": "Baroque geometry, scholarly prestige, reading room aura",
        "Do_Not_Do": "do not overfit to a single building facade",
    },
    {
        "Niche": "European_Dark_Academia",
        "Source_Title": "Wren Library architecture reference",
        "Source_URL": "https://en.wikipedia.org/wiki/Wren_Library",
        "Source_Type": "public architecture reference",
        "Use_Mode": "composition/history anchor",
        "Why_Useful": "proportion, carved shelving, classical library authority",
        "Do_Not_Do": "do not generate branded university merchandise",
    },
    {
        "Niche": "European_Dark_Academia",
        "Source_Title": "All Souls College library architecture PDF",
        "Source_URL": "https://www.asc.ox.ac.uk/sites/default/files/2022-10/Scrn3_Arch_edit1.pdf",
        "Source_Type": "institutional PDF",
        "Use_Mode": "architecture structure notes",
        "Why_Useful": "continuous gallery logic and scholarly spatial rhythm",
        "Do_Not_Do": "do not reuse photography directly",
    },
    {
        "Niche": "Imperial_Kintsugi",
        "Source_Title": "Nanyue King Museum jade artifact reference",
        "Source_URL": "https://en.wikipedia.org/wiki/Nanyue_King_Museum",
        "Source_Type": "museum artifact reference",
        "Use_Mode": "material craft anchor",
        "Why_Useful": "jade techniques, relief carving, drilling, openwork, ancient material prestige",
        "Do_Not_Do": "do not make fake museum claims in listings",
    },
    {
        "Niche": "Imperial_Kintsugi",
        "Source_Title": "Kintsugi conservation discussion seed",
        "Source_URL": "https://www.reddit.com/r/kintsugi/comments/1l4qk36",
        "Source_Type": "craft/community discussion",
        "Use_Mode": "concept language sanity check",
        "Why_Useful": "distinguishes visible repair from conservation concealment",
        "Do_Not_Do": "do not treat forum opinion as authoritative museum policy",
    },
    {
        "Niche": "Imperial_Kintsugi",
        "Source_Title": "Bronze conservation material study",
        "Source_URL": "https://arxiv.org/abs/2601.10265",
        "Source_Type": "research material reference",
        "Use_Mode": "material degradation vocabulary",
        "Why_Useful": "corrosion, fragment assembly, conservation traces",
        "Do_Not_Do": "do not cite as product provenance",
    },
)


def now_et() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def now_text() -> str:
    return now_et().strftime("%Y-%m-%d %H:%M:%S %z")


def ensure_dirs() -> None:
    DATABASE_DIR.mkdir(exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for niche in NICHES:
        for child in ("raw", "accepted", "rejected", "distilled"):
            (POOL_ROOT / niche.key / child).mkdir(parents=True, exist_ok=True)


def write_index(force: bool = False) -> int:
    existing_keys: set[tuple[str, str]] = set()
    rows: list[dict[str, str]] = []
    if INDEX_CSV.exists() and not force:
        with INDEX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                rows.append(row)
                existing_keys.add((row.get("Niche", ""), row.get("Sample_ID", "")))

    added = 0
    for niche in NICHES:
        for i in range(1, niche.target_count + 1):
            sample_id = f"{niche.key}-{i:02d}"
            key = (niche.key, sample_id)
            if key in existing_keys:
                continue
            target = niche.source_targets[(i - 1) % len(niche.source_targets)]
            rows.append(
                {
                    "Niche": niche.key,
                    "Sample_ID": sample_id,
                    "Status": "SOURCE_NEEDED",
                    "Source_Target": target,
                    "Source_URL": "",
                    "Local_File": "",
                    "Quality_Gate": (
                        "accept only high-resolution real-world or museum/catalog imagery; "
                        f"reject: {niche.forbid}"
                    ),
                    "Rights_Note": "reference/DNA distillation only; do not redistribute source image",
                    "Vision_Status": "WAITING_SOURCE",
                    "Distilled_DNA_ID": "",
                    "Notes": niche.visual_intent,
                }
            )
            added += 1

    with INDEX_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=INDEX_HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in INDEX_HEADERS})
    return added


def write_schema() -> None:
    rows = []
    for niche in NICHES:
        rows.append(
            {
                "DNA_ID": f"PM-{niche.key}-001",
                "Niche": niche.key,
                "Source_Sample_IDs": "",
                "Physical_Material_Parameters": (
                    "roughness, translucency, metallic edge behavior, texture frequency, "
                    "surface wear, refractive depth"
                ),
                "Light_Distribution_Matrix": (
                    "key light angle, color temperature, fill ratio, shadow decay, "
                    "specular highlight placement"
                ),
                "Composition_Rules": (
                    "dominant silhouette, negative space, depth layers, object scale, "
                    "buyer-use context"
                ),
                "Purchase_Intent_Word_Cluster": niche.visual_intent,
                "Negative_Prompt_Cluster": niche.forbid,
                "Mentor_Hub_DNA_Style": (
                    "Convert source DNA into a Mentor-Hub Gold_Prompt_DNA row, not a copy. "
                    "The result must be original, product-compatible, and platform-safe."
                ),
                "MJ_Test_Prompt_A_OldLogic": "",
                "MJ_Test_Prompt_B_ReferenceDerived": "",
                "QA_Status": "SCHEMA_READY",
            }
        )

    with DNA_SCHEMA_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=DNA_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def write_source_candidates() -> None:
    with SOURCE_CANDIDATES_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SOURCE_HEADERS)
        writer.writeheader()
        for row in SOURCE_CANDIDATES:
            writer.writerow({header: row.get(header, "") for header in SOURCE_HEADERS})


def write_plan() -> None:
    lines = [
        "# Project Mirror - Aesthetic DNA Pipeline",
        "",
        f"Generated: {now_text()}",
        "",
        "Purpose: build a reference-derived high-end aesthetic DNA layer that can upgrade Mentor Hub prompts without copying any source image.",
        "",
        "## Guardrails",
        "",
        "- Use reference images only for material, lighting, composition, and buyer-intent extraction.",
        "- Do not redistribute downloaded source images.",
        "- Avoid direct artist/style-name copying for living artists or protected IP.",
        "- Distilled prompts must create original OpenClaw product assets for Printify/Etsy/eBay/private Studio.",
        "- Reject low-resolution, collage, watermark, marketplace spam, and obvious AI render samples.",
        "",
        "## Niches",
        "",
    ]
    for niche in NICHES:
        lines.extend(
            [
                f"### {niche.key}",
                f"- Target count: {niche.target_count}",
                f"- Label: {niche.label}",
                f"- Visual intent: {niche.visual_intent}",
                f"- Reject: {niche.forbid}",
                "- Source target families:",
            ]
        )
        lines.extend([f"  - {target}" for target in niche.source_targets])
        lines.append("")

    lines.extend(
        [
            "## Distillation Output",
            "",
            "Each accepted sample should produce:",
            "",
            "- material parameters: roughness, translucency, metal behavior, texture frequency",
            "- light matrix: key angle, color temperature, fill ratio, shadow decay",
            "- composition rules: silhouette, negative space, depth, product context",
            "- purchase-intent word cluster: high-income buyer language",
            "- Mentor-Hub-compatible DNA: original Gold_Prompt_DNA, material keywords, and product fit",
            "",
            "## Next Execution Slice",
            "",
            "1. Start from `Database/Aesthetic_DNA_Source_Candidates.csv`, then fill 10-15 accepted source URLs per niche in `Database/Aesthetic_DNA_Pool_Index.csv`.",
            "2. Download or manually save only acceptable reference images into each niche `raw` folder.",
            "3. Run a future vision distiller against accepted samples.",
            "4. Build A/B MJ prompts: old logic vs reference-derived DNA.",
            "5. Compare outputs for premium feel, product feasibility, and conversion story.",
        ]
    )
    PLAN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_state(added: int) -> None:
    state = {
        "updated_at": now_text(),
        "pool_root": str(POOL_ROOT),
        "index_csv": str(INDEX_CSV),
        "dna_schema_csv": str(DNA_SCHEMA_CSV),
        "source_candidates_csv": str(SOURCE_CANDIDATES_CSV),
        "plan_md": str(PLAN_MD),
        "niches": {n.key: {"target_count": n.target_count, "label": n.label} for n in NICHES},
        "new_index_rows_added": added,
        "status": "SCAFFOLD_READY_SOURCE_COLLECTION_NEXT",
    }
    STATE_JSON.write_text(json.dumps(state, indent=2), encoding="utf-8")


def append_progress(added: int) -> None:
    msg = (
        f"\n## {now_et().strftime('%Y-%m-%d %H:%M ET')} - Project Mirror Aesthetic DNA Scaffold\n"
        f"- Created/validated aesthetic DNA pool folders under `{POOL_ROOT}`.\n"
        f"- Seeded `{INDEX_CSV.name}` with {added} new source slots across NYC Luxury, European Dark Academia, and Imperial Kintsugi.\n"
        f"- Wrote starter source candidates to `{SOURCE_CANDIDATES_CSV.name}` for DNA-only reference research.\n"
        f"- Wrote distillation schema `{DNA_SCHEMA_CSV.name}` and review plan `{PLAN_MD}`.\n"
        "- No marketplace publish, fee spend, or source-image redistribution occurred.\n"
    )
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(msg)


def main() -> int:
    ensure_dirs()
    added = write_index()
    write_schema()
    write_source_candidates()
    write_plan()
    write_state(added)
    append_progress(added)
    print(json.dumps(json.loads(STATE_JSON.read_text(encoding="utf-8")), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
