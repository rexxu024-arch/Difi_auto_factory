"""Build controlled Project Mirror production-refinement prompts.

This is the no-spend bridge from Project Mirror research to future physical
products. It does not create Printify products, publish marketplace listings,
or trigger Midjourney upscale. The output is a short, curated queue that can be
reviewed or dispatched later as draft grids only.
"""

from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
REVIEW_DIR = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"

MATRIX_CSV = DATABASE_DIR / "Project_Mirror_Product_Matrix.csv"
PROMOTED_CSV = DATABASE_DIR / "Project_Mirror_Promoted_DNA.csv"
OUT_CSV = DATABASE_DIR / "Project_Mirror_Production_Refinement_Queue.csv"
OUT_MD = REVIEW_DIR / "PROJECT_MIRROR_PRODUCTION_REFINEMENT_QUEUE.md"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"

HEADERS = [
    "Refinement_ID",
    "Rank",
    "Promoted_ID",
    "Pair_ID",
    "Title",
    "Carrier",
    "Blueprint_ID",
    "Target_Retail",
    "Production_Intent",
    "MJ_Refinement_Prompt",
    "Mockup_Need",
    "QA_Gates",
    "Status",
    "Next_Action",
]


def now_et() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def strip_mj_suffix(prompt: str) -> str:
    prompt = clean(prompt)
    prompt = re.sub(r"\s+--v\s+\S+.*$", "", prompt).strip()
    prompt = re.sub(r"\s+", " ", prompt)
    return prompt.rstrip(" ,")


def carrier_suffix(carrier: str, target_retail: str) -> tuple[str, str, str]:
    carrier_l = carrier.lower()
    if "acrylic" in carrier_l:
        return (
            "as a premium optical acrylic block artwork, deep internal refraction, heavy glass edge depth, "
            "executive desk object, quiet luxury gift, centered but full-frame object hierarchy, no cheap souvenir look",
            "one official product mockup plus one luxury walnut executive desk scene and one gallery shelf scene",
            "Acrylic: design must read clearly at 5x7, no tiny text, no low contrast, no duplicated mockups, target " + target_retail,
        )
    if "framed" in carrier_l:
        return (
            "as a framed archival wall art composition, gallery-grade paper texture, matte black or walnut frame logic, "
            "quiet luxury apartment decor, executive office wall focal point, edge-to-edge composition",
            "one clean wall mockup, one close crop, one executive-office wall scene, one gallery hallway scene",
            "Framed poster: verify final blueprint/variant before publish, no frame mismatch, target " + target_retail,
        )
    return (
        "as a premium matte 12x18 studio print, crisp paper texture, vertical composition, room-friendly negative space, "
        "giftable business decor, clean gallery print finish",
        "Printify official mockups plus one interior wall scene and one detail crop",
        "Poster: 12x18 safe crop, no text artifacts, no repeated gallery images, target " + target_retail,
    )


def build_prompt(base_prompt: str, carrier: str, target_retail: str) -> tuple[str, str, str]:
    base = strip_mj_suffix(base_prompt)
    suffix, mockup, qa = carrier_suffix(carrier, target_retail)
    prompt = (
        f"{base}, refined for physical product production, {suffix}, shot on 85mm lens, f/8, "
        "ultra-sharp focus, controlled chiaroscuro, realistic material response, no AI smear, no muddy shadows, "
        "no text, no watermark --v 6.1 --ar 2:3 --style raw --stylize 250 --chaos 18"
    )
    return re.sub(r"\s+", " ", prompt).strip(), mockup, qa


def build_rows(limit: int | None = None) -> list[dict[str, str]]:
    matrix_rows = read_csv(MATRIX_CSV)
    promoted = {clean(row.get("Promoted_ID")): row for row in read_csv(PROMOTED_CSV)}
    rows: list[dict[str, str]] = []
    for idx, matrix in enumerate(matrix_rows, start=1):
        if limit is not None and len(rows) >= limit:
            break
        promoted_id = clean(matrix.get("Promoted_ID"))
        dna = promoted.get(promoted_id, {})
        carrier = clean(matrix.get("Carrier"))
        target = clean(matrix.get("Target_Retail"))
        prompt, mockup, qa = build_prompt(clean(dna.get("Gold_Prompt_DNA")), carrier, target)
        title = clean(matrix.get("Title")) or clean(dna.get("Title"))
        rows.append(
            {
                "Refinement_ID": f"PM-REFINE-{idx:03d}",
                "Rank": clean(matrix.get("Rank")),
                "Promoted_ID": promoted_id,
                "Pair_ID": clean(matrix.get("Pair_ID")) or clean(dna.get("Pair_ID")),
                "Title": title,
                "Carrier": carrier,
                "Blueprint_ID": clean(matrix.get("Blueprint_ID")),
                "Target_Retail": target,
                "Production_Intent": "Controlled draft-grid refinement for premium POD candidate; no publish until gallery and product-fit QA pass.",
                "MJ_Refinement_Prompt": prompt,
                "Mockup_Need": mockup,
                "QA_Gates": qa,
                "Status": "READY_FOR_CONTROLLED_DRAFT_GRID_NO_UPSCALE",
                "Next_Action": "Dispatch only as draft grid, then score for product fit before any Printify creation.",
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Project Mirror Production Refinement Queue",
        "",
        f"Generated: {now_et().strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        "- No Printify product was created.",
        "- No Etsy/eBay listing was created.",
        "- No Midjourney upscale was triggered.",
        "",
        "| ID | Carrier | Target | Status |",
        "| --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['Refinement_ID']} | {row['Carrier']} | {row['Target_Retail']} | {row['Status']} |")
    lines.append("")
    for row in rows[:5]:
        lines.extend(
            [
                f"## {row['Refinement_ID']} - {row['Title']}",
                f"- Carrier: {row['Carrier']} / Blueprint {row['Blueprint_ID']} / Target {row['Target_Retail']}",
                f"- Mockup need: {row['Mockup_Need']}",
                f"- QA gates: {row['QA_Gates']}",
                "",
                "```text",
                row["MJ_Refinement_Prompt"],
                "```",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    msg = (
        f"\n## {now_et().strftime('%Y-%m-%d %H:%M ET')} - Project Mirror production refinement queue\n"
        f"- Built {len(rows)} product-specific Project Mirror refinement prompts in `Database\\Project_Mirror_Production_Refinement_Queue.csv`.\n"
        f"- Review packet: `Review_Packets\\Project_Mirror\\PROJECT_MIRROR_PRODUCTION_REFINEMENT_QUEUE.md`.\n"
        "- No publish, fee, or upscale action was taken.\n"
    )
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(msg)


def main() -> int:
    rows = build_rows()
    write_csv(rows)
    write_md(rows)
    append_progress(rows)
    print(f"[PROJECT-MIRROR-REFINE] rows={len(rows)} csv={OUT_CSV}")
    if rows:
        print(f"[PROJECT-MIRROR-REFINE] top={rows[0]['Refinement_ID']} {rows[0]['Carrier']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
