"""Preselect Project Mirror refinement draft grids for Rex/Grey review.

This is intentionally local-only: split MJ draft grids, score candidate
directions, and produce a review packet. It does not upscale, publish, or
create Printify products.
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"
QUEUE = DATABASE / "Project_Mirror_Refinement_MJ_Dispatch_Queue.csv"
OUT_CSV = DATABASE / "Project_Mirror_Refinement_Preselect.csv"
OUT_MD = REVIEW / "PROJECT_MIRROR_REFINEMENT_PRESELECT.md"
CONTACT = REVIEW / "PROJECT_MIRROR_REFINEMENT_PRESELECT_CONTACT_SHEET.jpg"
PROGRESS = PROJECT_ROOT / "PROGRESS_LOG.md"


def clean(value: object) -> str:
    return str(value or "").strip()


def now_et() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M ET")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = list(rows[0].keys()) if rows else [
        "Internal_SKU",
        "Best_Quadrant",
        "Score",
        "Decision",
        "Rationale",
        "Candidate_File",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def crop_grid(grid_path: Path, out_dir: Path) -> dict[str, Path]:
    image = Image.open(grid_path).convert("RGB")
    w, h = image.size
    boxes = {
        "U1": (0, 0, w // 2, h // 2),
        "U2": (w // 2, 0, w, h // 2),
        "U3": (0, h // 2, w // 2, h),
        "U4": (w // 2, h // 2, w, h),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    output: dict[str, Path] = {}
    for name, box in boxes.items():
        crop = image.crop(box)
        out = out_dir / f"{grid_path.stem}_{name}_draft.jpg"
        crop.save(out, quality=92)
        output[name] = out
    return output


def ready_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(QUEUE)
        if clean(row.get("Harvest_Status")) == "GRID_FOUND" and clean(row.get("Grid_File"))
    ]


# Manual visual preselect from the latest contact sheet. Keep this small and
# explicit so Rex can see exactly why a draft is promoted or held.
VISUAL_DECISIONS: dict[str, dict[str, object]] = {
    "PM-REFINE-001-PROJECT_MIRROR_REFINED": {
        "Best_Quadrant": "U2",
        "Score": 72,
        "Decision": "HOLD_REWORK",
        "Rationale": "Luxury-room signal is real, but it reads as interior stock photography more than a standalone collectible product.",
    },
    "PM-REFINE-002-PROJECT_MIRROR_REFINED": {
        "Best_Quadrant": "U1",
        "Score": 78,
        "Decision": "SECONDARY_REWORK",
        "Rationale": "Strong material block and RH-like aura; needs less collage fragmentation and clearer object hierarchy before Printify production.",
    },
    "PM-REFINE-003-PROJECT_MIRROR_REFINED": {
        "Best_Quadrant": "U4",
        "Score": 70,
        "Decision": "HOLD_REWORK",
        "Rationale": "Art Deco luxury is visible, but the set drifts toward real-estate/penthouse imagery instead of OpenClaw artifact language.",
    },
    "PM-REFINE-004-PROJECT_MIRROR_REFINED": {
        "Best_Quadrant": "U2",
        "Score": 91,
        "Decision": "PROMOTE_DRAFT",
        "Rationale": "Best material authority: smoky jade, gold repair seams, museum-object abstraction, clear premium identity for a $48-$98 print or $128 acrylic.",
    },
    "PM-REFINE-005-PROJECT_MIRROR_REFINED": {
        "Best_Quadrant": "U4",
        "Score": 83,
        "Decision": "PROMOTE_SECONDARY",
        "Rationale": "Strong scholarly corridor mood and dark-academia buyer fit; less distinctive than jade repair, but useful for executive-office wall decor.",
    },
    "PM-REFINE-006-PROJECT_MIRROR_REFINED": {
        "Best_Quadrant": "U2",
        "Score": 89,
        "Decision": "PROMOTE_DRAFT",
        "Rationale": "High-end material macro reads immediately at thumbnail size; excellent candidate for a paired material-study print or acrylic face.",
    },
    "PM-REFINE-007-PROJECT_MIRROR_REFINED": {
        "Best_Quadrant": "U2",
        "Score": 76,
        "Decision": "SECONDARY_REWORK",
        "Rationale": "Warm historical hallway works as decor but needs stronger OpenClaw material signature to avoid generic European interior stock feel.",
    },
    "PM-REFINE-008-PROJECT_MIRROR_REFINED": {
        "Best_Quadrant": "U3",
        "Score": 82,
        "Decision": "PROMOTE_SECONDARY",
        "Rationale": "Architectural depth and library prestige are strong; use as a conservative $48 studio-print lane, not a flagship.",
    },
    "PM-REFINE-009-PROJECT_MIRROR_REFINED": {
        "Best_Quadrant": "U1",
        "Score": 74,
        "Decision": "HOLD_REWORK",
        "Rationale": "Jade artifact direction is on-brand, but current shapes drift toward ambiguous sculpture/product confusion.",
    },
}


def thumbnail(path: Path, size: tuple[int, int]) -> Image.Image:
    img = Image.open(path).convert("RGB")
    img.thumbnail(size, Image.LANCZOS)
    canvas = Image.new("RGB", size, (240, 238, 232))
    canvas.paste(img, ((size[0] - img.width) // 2, (size[1] - img.height) // 2))
    return canvas


def build_contact(rows: list[dict[str, object]]) -> None:
    CONTACT.parent.mkdir(parents=True, exist_ok=True)
    rows = sorted(rows, key=lambda row: int(row["Score"]), reverse=True)
    cols = 3
    tile_w, tile_h = 520, 520
    header_h = 90
    sheet_h = header_h + ((len(rows) + cols - 1) // cols) * tile_h
    sheet = Image.new("RGB", (cols * tile_w, sheet_h), (247, 245, 240))
    draw = ImageDraw.Draw(sheet)
    draw.text((24, 18), "Project Mirror Refinement / Preselect", fill=(24, 22, 18), font=font(28, bold=True))
    draw.text(
        (24, 56),
        "Draft-grid quadrant preselect only. No upscale, no marketplace publish, no fee.",
        fill=(92, 82, 66),
        font=font(14),
    )
    for idx, row in enumerate(rows):
        x = (idx % cols) * tile_w
        y = header_h + (idx // cols) * tile_h
        decision = clean(row["Decision"])
        outline = (90, 132, 87) if decision.startswith("PROMOTE") else (188, 154, 88) if "SECONDARY" in decision else (176, 112, 100)
        draw.rounded_rectangle((x + 14, y + 12, x + tile_w - 14, y + tile_h - 16), radius=12, fill=(255, 255, 252), outline=outline, width=3)
        candidate = PROJECT_ROOT / clean(row["Candidate_File"])
        try:
            sheet.paste(thumbnail(candidate, (474, 315)), (x + 23, y + 24))
        except Exception:
            draw.rectangle((x + 23, y + 24, x + 497, y + 339), fill=(225, 220, 210))
        draw.text((x + 24, y + 354), f"{row['Internal_SKU']}  {row['Best_Quadrant']}  {row['Score']}", fill=(22, 20, 18), font=font(14, bold=True))
        draw.text((x + 24, y + 378), decision, fill=outline, font=font(15, bold=True))
        text = clean(row["Rationale"])
        draw.text((x + 24, y + 408), text[:70], fill=(72, 62, 50), font=font(12))
        draw.text((x + 24, y + 428), text[70:140], fill=(72, 62, 50), font=font(12))
        draw.text((x + 24, y + 448), text[140:210], fill=(72, 62, 50), font=font(12))
    sheet.save(CONTACT, quality=92)


def build_markdown(rows: list[dict[str, object]]) -> None:
    by_decision = Counter(clean(row["Decision"]) for row in rows)
    promoted = [row for row in sorted(rows, key=lambda r: int(r["Score"]), reverse=True) if str(row["Decision"]).startswith("PROMOTE")]
    lines = [
        "# Project Mirror Refinement Preselect",
        "",
        f"- Generated: {now_et()}",
        f"- Source queue: `{QUEUE}`",
        f"- Output scorecard: `{OUT_CSV}`",
        f"- Contact sheet: `{CONTACT}`",
        f"- Decision mix: {dict(by_decision)}",
        "- Scope: draft-grid quadrant selection only. No Midjourney upscale, no Printify product creation, no Etsy/eBay publish, no fee.",
        "",
        "## Promote First",
        "",
    ]
    for row in promoted:
        lines.extend(
            [
                f"### {row['Internal_SKU']} / {row['Best_Quadrant']} / {row['Score']}",
                f"- Decision: {row['Decision']}",
                f"- Candidate crop: `{PROJECT_ROOT / clean(row['Candidate_File'])}`",
                f"- Why: {row['Rationale']}",
                f"- Next: build identity-locked scene/mockup prompt and cost-checked Printify carrier plan; still require Rex/Grey visual approval before upscale.",
                "",
            ]
        )
    lines.extend(["## Full Scorecard", ""])
    for row in sorted(rows, key=lambda r: int(r["Score"]), reverse=True):
        lines.extend(
            [
                f"- **{row['Internal_SKU']}** `{row['Best_Quadrant']}` score `{row['Score']}` -> `{row['Decision']}`",
                f"  - {row['Rationale']}",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def append_progress(rows: list[dict[str, object]]) -> None:
    promoted = sum(1 for row in rows if clean(row["Decision"]).startswith("PROMOTE"))
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {now_et()} - Project Mirror refinement preselect\n"
            f"- Split and scored {len(rows)} refinement grid(s); promoted={promoted}; scorecard=`{OUT_CSV}`.\n"
            f"- Contact sheet: `{CONTACT}`; report=`{OUT_MD}`.\n"
            "- No upscale, publish, Printify creation, or fee action was taken.\n"
        )


def main() -> int:
    rows = ready_rows()
    if not rows:
        print("[PROJECT-MIRROR-PRESELECT] no ready refinement grids")
        return 1
    output_rows: list[dict[str, object]] = []
    for row in rows:
        sku = clean(row.get("Internal_SKU"))
        grid = PROJECT_ROOT / clean(row.get("Grid_File"))
        if not grid.exists():
            continue
        crops = crop_grid(grid, PROJECT_ROOT / clean(row.get("Output_Folder")) / "preselect")
        decision = VISUAL_DECISIONS.get(sku, {
            "Best_Quadrant": "U1",
            "Score": 60,
            "Decision": "HOLD_REVIEW",
            "Rationale": "No explicit visual decision recorded; requires Rex/Grey review.",
        })
        best = clean(decision["Best_Quadrant"])
        candidate = crops.get(best) or next(iter(crops.values()))
        output_rows.append(
            {
                "Internal_SKU": sku,
                "Concept_Name": clean(row.get("Concept_Name")),
                "Recommended_Format": clean(row.get("Recommended_Format")),
                "Best_Quadrant": best,
                "Score": int(decision["Score"]),
                "Decision": clean(decision["Decision"]),
                "Rationale": clean(decision["Rationale"]),
                "Candidate_File": str(candidate.relative_to(PROJECT_ROOT)),
                "Grid_File": clean(row.get("Grid_File")),
                "Next_Action": "REX_OR_GREY_REVIEW_BEFORE_UPSCALE_OR_PRINTIFY",
            }
        )
    if not output_rows:
        print("[PROJECT-MIRROR-PRESELECT] no output rows")
        return 1
    write_csv(OUT_CSV, output_rows)
    build_contact(output_rows)
    build_markdown(output_rows)
    append_progress(output_rows)
    print(f"[PROJECT-MIRROR-PRESELECT] rows={len(output_rows)} promoted={sum(1 for r in output_rows if str(r['Decision']).startswith('PROMOTE'))} csv={OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
