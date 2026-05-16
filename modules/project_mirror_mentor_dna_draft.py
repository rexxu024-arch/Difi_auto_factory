"""Create Mentor-Hub-style DNA drafts from Project Mirror source candidates.

This is an intermediate design layer. It converts high-end reference intent
into original OpenClaw DNA rows for later DeepSeek/Claude/MJ refinement.
It does not copy source images or claim provenance.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
REVIEW_DIR = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"
SOURCE_CANDIDATES_CSV = DATABASE_DIR / "Aesthetic_DNA_Source_Candidates.csv"
OUT_CSV = DATABASE_DIR / "Project_Mirror_Mentor_DNA_Draft.csv"
OUT_MD = REVIEW_DIR / "PROJECT_MIRROR_MENTOR_DNA_DRAFT.md"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"

HEADERS = [
    "DNA_ID",
    "Category",
    "Layout",
    "Title",
    "Gold_Prompt_DNA",
    "Material_Keywords",
    "Source_Inspiration",
    "Product_Fit",
    "AB_Test_A_OldLogic",
    "AB_Test_B_ProjectMirror",
    "QA_Status",
]

NICHE_RULES = {
    "NYC_Luxury": {
        "category": "Luxury-Executive_Decor",
        "layout": "Full_Frame",
        "materials": "smoked glass, brushed brass, antique walnut, Belgian black stone, Verde marble, soft city-window reflections",
        "fit": "Acrylic Block, Framed Poster, Archival Poster",
        "suffix": "executive office gift, quiet luxury apartment decor, Manhattan penthouse atmosphere",
        "negative": "no cheap hotel lobby, no generic luxury logo, no people, no text, no watermark",
    },
    "European_Dark_Academia": {
        "category": "Academia-Architectural_Relic",
        "layout": "Full_Frame",
        "materials": "carved oak, aged vellum, oxidized brass, archival ink, dusted stone, museum glass",
        "fit": "Framed Poster, Archival Poster, Acrylic Block",
        "suffix": "reading room decor, scholar office wall art, old-world study atmosphere",
        "negative": "no fantasy cosplay, no skull cliché, no readable text, no watermark",
    },
    "Imperial_Kintsugi": {
        "category": "Relic-Kintsugi_Material",
        "layout": "Full_Frame",
        "materials": "smoky jade, unpolished ceramic, kintsugi gold seams, oxidized bronze, refractive cracks, conservation patina",
        "fit": "Acrylic Block, Premium Poster, Framed Poster",
        "suffix": "curated desk object, material study decor, museum relic inspired gift",
        "negative": "no dragon, no phoenix, no souvenir-shop ornament, no text, no watermark",
    },
}


def now_et() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def clean(value: object) -> str:
    return str(value or "").strip()


def read_sources() -> list[dict[str, str]]:
    with SOURCE_CANDIDATES_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def make_title(niche: str, source_title: str) -> str:
    base = source_title.split(" reference")[0].split(" archive")[0].split(" PDF")[0]
    if niche == "NYC_Luxury":
        return f"Manhattan Material Order - {base}"
    if niche == "European_Dark_Academia":
        return f"Scholarly Stone Gallery - {base}"
    return f"Smoky Jade Repair Study - {base}"


def build_rows() -> list[dict[str, str]]:
    rows = []
    for idx, source in enumerate(read_sources(), start=1):
        niche = clean(source.get("Niche"))
        rule = NICHE_RULES[niche]
        title = make_title(niche, clean(source.get("Source_Title")))
        why = clean(source.get("Why_Useful"))
        dna_id = f"PM-{niche}-{idx:03d}"
        subject = (
            f"an original OpenClaw {title.lower()} composition, inspired only by the abstract material and spatial DNA of {why}, "
            f"never copying the source image, built as a premium physical art product"
        )
        gold = (
            f"{subject}, {rule['materials']}, layered depth, restrained high-income composition, "
            f"cinematic but realistic lighting, tactile surface detail, gallery-grade framing logic, "
            f"{rule['suffix']}, ultra-sharp product-ready artwork, --v 6.1 --ar 2:3 --style raw --no {rule['negative'].replace('no ', '')}"
        )
        old_logic = (
            f"{title}, premium decor object, jade and brass, dramatic lighting, beautiful wall art --v 6.1 --ar 2:3 --style raw"
        )
        project_mirror = gold
        rows.append(
            {
                "DNA_ID": dna_id,
                "Category": rule["category"],
                "Layout": rule["layout"],
                "Title": title,
                "Gold_Prompt_DNA": gold,
                "Material_Keywords": rule["materials"],
                "Source_Inspiration": f"{source.get('Source_Title')} | {source.get('Source_URL')}",
                "Product_Fit": rule["fit"],
                "AB_Test_A_OldLogic": old_logic,
                "AB_Test_B_ProjectMirror": project_mirror,
                "QA_Status": "DRAFT_READY_FOR_DEEPSEEK_OR_CLAUDE_REFINEMENT",
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Project Mirror Mentor DNA Draft",
        "",
        f"Generated: {now_et().strftime('%Y-%m-%d %H:%M %z')}",
        "",
        "Purpose: translate curated high-end references into original OpenClaw Mentor-Hub DNA drafts. These are not source copies and should be refined before production.",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['DNA_ID']} - {row['Title']}",
                f"- Category: {row['Category']}",
                f"- Product fit: {row['Product_Fit']}",
                f"- Materials: {row['Material_Keywords']}",
                f"- Source inspiration: {row['Source_Inspiration']}",
                "",
                "### Project Mirror Prompt",
                "",
                row["AB_Test_B_ProjectMirror"],
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["Category"]] = counts.get(row["Category"], 0) + 1
    msg = (
        f"\n## {now_et().strftime('%Y-%m-%d %H:%M ET')} - Project Mirror Mentor DNA Drafts\n"
        f"- Built {len(rows)} high-end Mentor-Hub-style DNA drafts from Project Mirror source candidates.\n"
        f"- Category mix: {counts}.\n"
        f"- Output CSV: `{OUT_CSV}`; review packet: `{OUT_MD}`.\n"
        "- These are original prompt/DNA drafts for later DeepSeek/Claude refinement; no source images were copied.\n"
    )
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(msg)


def main() -> int:
    rows = build_rows()
    write_csv(rows)
    write_md(rows)
    append_progress(rows)
    print({"rows": len(rows), "csv": str(OUT_CSV), "review": str(OUT_MD)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
