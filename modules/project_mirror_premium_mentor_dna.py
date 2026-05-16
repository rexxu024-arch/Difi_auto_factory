"""Compile promoted Project Mirror refinement drafts into premium Mentor DNA.

The output is a compact, high-aesthetic DNA layer for DeepSeek/Claude/MJ.
It intentionally avoids marketplace listing copy and does not spend, publish,
or upscale anything.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"
PRESELECT = DATABASE / "Project_Mirror_Refinement_Preselect.csv"
OUT_CSV = DATABASE / "Project_Mirror_Premium_Mentor_DNA.csv"
OUT_MD = REVIEW / "PROJECT_MIRROR_PREMIUM_MENTOR_DNA.md"
PROGRESS = PROJECT_ROOT / "PROGRESS_LOG.md"


HEADERS = [
    "DNA_ID",
    "Source_SKU",
    "Category",
    "Sub_Category",
    "Layout",
    "Title",
    "Gold_Prompt_DNA",
    "Material_Keywords",
    "Lighting_Composition",
    "Product_Fit",
    "Price_Tier",
    "Scene_Mockup_Directive",
    "Negative_Prompt",
    "Candidate_File",
    "QA_Status",
]


def clean(value: object) -> str:
    return str(value or "").strip()


def now_et() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M ET")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def dna_for(row: dict[str, str], idx: int) -> dict[str, str]:
    title = clean(row.get("Concept_Name"))
    source = clean(row.get("Internal_SKU"))
    candidate = clean(row.get("Candidate_File"))
    fmt = clean(row.get("Recommended_Format"))
    rationale = clean(row.get("Rationale"))
    score = clean(row.get("Score"))

    if "Jade Repair" in title or "Kintsugi" in title or "Bronze conservation" in title:
        category = "Relic-Kintsugi_Material"
        sub = "Smoky_Jade_Conservation"
        material = "smoky jade, kintsugi gold repair seams, oxidized bronze, unpolished mineral skin, conservation patina, hairline fracture networks"
        lighting = "museum conservation table lighting, low-angle grazing light, restrained chiaroscuro, tactile macro depth, no decorative clutter"
        subject = (
            "a museum-grade material study of smoky jade and gold repair seams, composed as a restrained relic surface rather than a souvenir object"
        )
        price = "$48 studio print / $128 acrylic material relic"
        fit = "Premium Matte Poster 12x18, Framed/Archival Poster, Acrylic Block 5x7"
        scene = (
            "Preserve exact jade-gold surface identity; place as a framed material study above walnut console, or as an acrylic object on executive desk. "
            "Do not redesign cracks, color, or material geometry."
        )
    elif "Scholarly" in title or "library" in title.lower() or "Radcliffe" in title:
        category = "Academia-Architectural_Relic"
        sub = "Scholarly_Stone_Gallery"
        material = "carved oak, dusted limestone, oxidized brass, archival paper warmth, museum glass, old library shadow gradients"
        lighting = "late-afternoon library light, long corridor perspective, controlled amber highlights, quiet negative space, credible architectural scale"
        subject = (
            "an old-world scholarly corridor distilled into a premium wall-art relic, using architecture as status signal rather than fantasy decor"
        )
        price = "$48 studio print / $68-$98 framed executive wall art"
        fit = "Premium Matte Poster 12x18, Framed Paper Poster"
        scene = (
            "Preserve exact corridor/library composition; show in executive office, reading nook, or private gallery hallway with neutral matting. "
            "No new ornaments, no people, no readable text."
        )
    else:
        category = "Luxury-Executive_Decor"
        sub = "Manhattan_Material_Order"
        material = "smoked glass, brushed brass, antique walnut, Belgian black stone, Verde marble, city-window reflections"
        lighting = "quiet Manhattan penthouse window light, hard-edged shadow, polished-but-not-glossy material response"
        subject = "a restrained Manhattan material-order composition designed for a high-income executive interior"
        price = "$128 acrylic block / $149 desk set candidate"
        fit = "Acrylic Block 5x7"
        scene = (
            "Preserve exact object silhouette and stone/glass colors; place on walnut executive desk or gallery shelf. "
            "Avoid real-estate photo drift."
        )

    negative = "no people, no readable text, no watermark, no logo, no low-resolution smear, no cheap souvenir styling, no fantasy cliché"
    gold = (
        f"{subject}, {material}, {lighting}, premium physical art product, executive office gift, quiet luxury apartment decor, "
        f"gallery-grade composition, tactile surface detail, ultra-sharp product-ready artwork, shot on 85mm lens, f/8, "
        f"controlled realistic material response --v 6.1 --ar 2:3 --style raw --stylize 250 --chaos 14 --no {negative.replace('no ', '')}"
    )
    return {
        "DNA_ID": f"PM-PREMIUM-{idx:03d}",
        "Source_SKU": source,
        "Category": category,
        "Sub_Category": sub,
        "Layout": "Full_Frame",
        "Title": title,
        "Gold_Prompt_DNA": gold,
        "Material_Keywords": material,
        "Lighting_Composition": lighting,
        "Product_Fit": fit or clean(row.get("Recommended_Format")),
        "Price_Tier": price,
        "Scene_Mockup_Directive": scene,
        "Negative_Prompt": negative,
        "Candidate_File": candidate,
        "QA_Status": f"PROMOTED_FROM_PROJECT_MIRROR_PRESELECT_SCORE_{score}; {rationale}",
    }


def build_rows() -> list[dict[str, str]]:
    preselect = read_csv(PRESELECT)
    accepted = [
        row
        for row in preselect
        if clean(row.get("Decision")) in {"PROMOTE_DRAFT", "PROMOTE_SECONDARY"}
    ]
    accepted.sort(key=lambda row: int(clean(row.get("Score")) or 0), reverse=True)
    return [dna_for(row, idx) for idx, row in enumerate(accepted, start=1)]


def write_md(rows: list[dict[str, str]]) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Project Mirror Premium Mentor DNA",
        "",
        f"- Generated: {now_et()}",
        f"- Source scorecard: `{PRESELECT}`",
        f"- Output CSV: `{OUT_CSV}`",
        "- Purpose: convert the best reference-derived drafts into compact Mentor-Hub DNA for high-end POD and Studio work.",
        "- Policy: no marketplace copy, no publish, no upscale, no fee.",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['DNA_ID']} - {row['Sub_Category']}",
                f"- Source: {row['Source_SKU']}",
                f"- Candidate crop: `{PROJECT_ROOT / row['Candidate_File']}`",
                f"- Product fit: {row['Product_Fit']}",
                f"- Price tier: {row['Price_Tier']}",
                f"- Materials: {row['Material_Keywords']}",
                f"- Lighting/composition: {row['Lighting_Composition']}",
                "",
                "### Gold Prompt DNA",
                "",
                row["Gold_Prompt_DNA"],
                "",
                "### Scene Mockup Directive",
                "",
                row["Scene_Mockup_Directive"],
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {now_et()} - Project Mirror premium Mentor DNA\n"
            f"- Compiled {len(rows)} promoted refinement candidates into high-end Mentor-Hub DNA rows.\n"
            f"- Output: `{OUT_CSV}`; review packet: `{OUT_MD}`.\n"
            "- No upscale, publish, Printify creation, or fee action was taken.\n"
        )


def main() -> int:
    rows = build_rows()
    if not rows:
        print("[PROJECT-MIRROR-PREMIUM-DNA] no promoted rows")
        return 1
    write_csv(OUT_CSV, rows)
    write_md(rows)
    append_progress(rows)
    print(f"[PROJECT-MIRROR-PREMIUM-DNA] rows={len(rows)} csv={OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
