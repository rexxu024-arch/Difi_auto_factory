"""Build identity-locked scene mockup prompts for Project Mirror winners.

This creates a safe MJ queue only. It does not submit, upscale, publish, or
spend. The queue is designed to preserve the selected artwork exactly while
testing premium desk/gallery context images.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"
SOURCE = DATABASE / "Project_Mirror_Premium_Mentor_DNA.csv"
OUT_CSV = DATABASE / "Project_Mirror_Identity_Locked_Mockup_Queue.csv"
OUT_MD = REVIEW / "PROJECT_MIRROR_IDENTITY_LOCKED_MOCKUP_QUEUE.md"
PROGRESS = PROJECT_ROOT / "PROGRESS_LOG.md"


HEADERS = [
    "Queue_ID",
    "DNA_ID",
    "Source_SKU",
    "Scene_Type",
    "Candidate_File",
    "Source_Reference_Policy",
    "Prompt",
    "Target_AR",
    "Image_Weight",
    "Stylize",
    "Chaos",
    "Negative_Prompt",
    "QA_Gate",
    "Status",
]


def now_et() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M ET")


def clean(value: object) -> str:
    return str(value or "").strip()


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


def scene_specs(row: dict[str, str]) -> list[dict[str, str]]:
    category = clean(row.get("Category"))
    product_fit = clean(row.get("Product_Fit"))
    if "Acrylic" in product_fit or "Kintsugi" in category:
        desk = (
            "the exact same artwork printed inside a thick optical acrylic block, placed on a dark walnut executive desk beside a matte black notebook "
            "and a brushed brass pen tray, realistic refraction through the clear acrylic edges, soft window reflection, premium product photography"
        )
        gallery = (
            "the exact same artwork presented as a thick optical acrylic object on a narrow black stone plinth in a private minimalist gallery foyer, "
            "subtle reflected light on glass edges, quiet museum air, realistic shadows, no extra objects touching the art"
        )
        ar = "4:5"
    else:
        desk = (
            "the exact same artwork as a framed archival studio print leaning above a walnut executive console, warm limestone wall, soft late-afternoon "
            "window light, realistic paper texture and frame shadow, premium interior product photography"
        )
        gallery = (
            "the exact same artwork hung as a framed archival print in a restrained private gallery hallway, off-white wall, black thin frame, neutral matting, "
            "distant architectural depth, realistic scale and shadows"
        )
        ar = "4:5"
    return [
        {"Scene_Type": "Luxury_Desk", "Scene": desk, "Target_AR": ar},
        {"Scene_Type": "Private_Gallery", "Scene": gallery, "Target_AR": ar},
    ]


def prompt_for(row: dict[str, str], spec: dict[str, str]) -> str:
    title = clean(row.get("Title"))
    materials = clean(row.get("Material_Keywords"))
    lighting = clean(row.get("Lighting_Composition"))
    scene = spec["Scene"]
    return (
        "[UPLOAD_SOURCE_IMAGE_TO_DISCORD_AND_PLACE_CDN_URL_FIRST] exact same artwork, preserve the exact product design, "
        "no redesign, no pattern changes, no symbol changes, no color changes, no altered composition, "
        f"{scene}, product identity anchored to {title}, visible material cues: {materials}, lighting reference: {lighting}, "
        "natural lens compression, real catalog shadows, believable room scale, premium quiet luxury presentation "
        f"--v 6.1 --style raw --ar {spec['Target_AR']} --iw 2 --stylize 80 --chaos 4 "
        "--no text, watermark, logo, extra designs, altered artwork, distorted print, duplicate product, fake reflections, impossible geometry"
    )


def build_rows() -> list[dict[str, str]]:
    source_rows = read_csv(SOURCE)
    rows: list[dict[str, str]] = []
    for idx, row in enumerate(source_rows, start=1):
        candidate = clean(row.get("Candidate_File"))
        source_path = PROJECT_ROOT / candidate
        source_policy = (
            "Do not paste a local file path into Midjourney. Upload this source image to Discord first, "
            "then place the resulting CDN URL at the start of the prompt."
        )
        for scene_index, spec in enumerate(scene_specs(row), start=1):
            rows.append(
                {
                    "Queue_ID": f"PM-SCENE-{idx:03d}-{scene_index:02d}",
                    "DNA_ID": clean(row.get("DNA_ID")),
                    "Source_SKU": clean(row.get("Source_SKU")),
                    "Scene_Type": spec["Scene_Type"],
                    "Candidate_File": str(source_path),
                    "Source_Reference_Policy": source_policy,
                    "Prompt": prompt_for(row, spec),
                    "Target_AR": spec["Target_AR"],
                    "Image_Weight": "2",
                    "Stylize": "80",
                    "Chaos": "4",
                    "Negative_Prompt": (
                        "hold if artwork changes, material color drifts, print is distorted, product shape becomes impossible, "
                        "scene shadows look fake, or repeated gallery duplicates appear"
                    ),
                    "QA_Gate": "IDENTITY_LOCK_REQUIRED_BEFORE_UPSCALE_OR_PUBLISH",
                    "Status": "READY_FOR_MJ_DRAFT_ONLY_NO_UPSCALE",
                }
            )
    return rows


def write_md(rows: list[dict[str, str]]) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Project Mirror Identity-Locked Mockup Queue",
        "",
        f"- Generated: {now_et()}",
        f"- Source DNA: `{SOURCE}`",
        f"- Output CSV: `{OUT_CSV}`",
        "- Scope: draft-only scene prompts for Project Mirror premium winners.",
        "- Prohibition: no upscale, no marketplace publish, no fee action.",
        "- Critical rule: upload the candidate image to Discord first and use the CDN URL as the leading image reference.",
        "",
    ]
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["DNA_ID"], []).append(row)
    for dna_id, group in grouped.items():
        lines.extend([f"## {dna_id}", ""])
        for row in group:
            lines.extend(
                [
                    f"### {row['Queue_ID']} - {row['Scene_Type']}",
                    f"- Source: `{row['Candidate_File']}`",
                    f"- Status: {row['Status']}",
                    f"- QA: {row['QA_Gate']}",
                    "",
                    "```text",
                    row["Prompt"],
                    "```",
                    "",
                ]
            )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {now_et()} - Project Mirror identity-locked mockup queue\n"
            f"- Built {len(rows)} draft-only scene mockup prompts from `{SOURCE}`.\n"
            f"- Output: `{OUT_CSV}`; review packet: `{OUT_MD}`.\n"
            "- All rows are marked draft-only/no-upscale; original artwork must be uploaded to Discord and used as the first image reference.\n"
        )


def main() -> int:
    rows = build_rows()
    if not rows:
        print("[PROJECT-MIRROR-SCENE-QUEUE] no premium DNA rows")
        return 1
    write_csv(OUT_CSV, rows)
    write_md(rows)
    append_progress(rows)
    print(f"[PROJECT-MIRROR-SCENE-QUEUE] rows={len(rows)} csv={OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
