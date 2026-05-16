from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "Database" / "First_Audit_V5_Top4_Refinement_MJ_Dispatch_Queue.csv"
OUT_DIR = ROOT / "Review_Packets"
SHEET = OUT_DIR / "First_Audit_V5_Top4_Refinement_GRID_CONTACT_SHEET.jpg"
REVIEW = OUT_DIR / "First_Audit_V5_Top4_Refinement_GRID_REVIEW.md"


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def load_rows() -> list[dict[str, str]]:
    with QUEUE.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def fit_image(path: Path, size: tuple[int, int]) -> Image.Image:
    canvas = Image.new("RGB", size, (245, 243, 237))
    im = Image.open(path).convert("RGB")
    im.thumbnail(size, Image.LANCZOS)
    canvas.paste(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2))
    return canvas


def build_sheet(rows: list[dict[str, str]]) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    title_font = font(26)
    body_font = font(17)
    small_font = font(15)
    grid_w, grid_h = 360, 420
    info_w = 720
    margin = 34
    row_h = grid_h + 44
    width = margin * 2 + grid_w + info_w + 22
    height = margin * 2 + 72 + row_h * len(rows)
    sheet = Image.new("RGB", (width, height), (237, 234, 226))
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 18), "FIRST AUDIT TOP 4 REFINEMENT GRIDS", font=title_font, fill=(24, 22, 20))
    draw.text(
        (margin, 50),
        "Relaxed draft grids only. No U1-U4, no Fast/Upscale until Rex selects a final.",
        font=body_font,
        fill=(72, 68, 62),
    )
    y = margin + 70
    for row in rows:
        grid_file = row.get("Grid_File") or ""
        grid_path = ROOT / grid_file
        draw.rounded_rectangle(
            (margin - 10, y - 12, width - margin + 10, y + row_h - 12),
            radius=12,
            fill=(250, 249, 246),
            outline=(205, 200, 190),
            width=1,
        )
        if grid_path.exists():
            sheet.paste(fit_image(grid_path, (grid_w, grid_h)), (margin, y))
        info_x = margin + grid_w + 22
        lines = [
            row.get("Internal_SKU", ""),
            row.get("Concept_Name", ""),
            f"Carrier: {row.get('Product_Type', '')}",
            f"Status: {row.get('Harvest_Status', '')}",
            f"Lock: {row.get('Fast_Upscale_Lock', '')}",
            "Next: Rex/Gemini select grid quadrant before any upscale.",
        ]
        ty = y + 12
        for index, line in enumerate(lines):
            draw.text((info_x, ty), line, font=body_font if index < 2 else small_font, fill=(31, 30, 27))
            ty += 30 if index < 2 else 24
        prompt = " ".join((row.get("MJ_Master_Prompt") or "").split())
        draw.multiline_text(
            (info_x, ty + 8),
            prompt[:480] + ("..." if len(prompt) > 480 else ""),
            font=small_font,
            fill=(70, 67, 61),
            spacing=5,
        )
        y += row_h
    sheet.save(SHEET, quality=92)
    return SHEET


def build_review(rows: list[dict[str, str]]) -> Path:
    lines = [
        "# First Audit Top 4 Refinement Grid Review",
        "",
        f"Contact sheet: `{SHEET}`",
        "",
        "Rule: these are Relaxed draft grids. Do not request U1-U4 or Fast/Upscale until Rex selects a Top 1% final.",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row.get('Internal_SKU', '')}",
                "",
                f"- Concept: {row.get('Concept_Name', '')}",
                f"- Carrier: {row.get('Product_Type', '')}",
                f"- Grid: `{ROOT / (row.get('Grid_File') or '')}`",
                f"- Status: {row.get('Harvest_Status', '')}",
                "- Decision needed later: reject / refine once more / select quadrant for upscale.",
                "",
            ]
        )
    REVIEW.write_text("\n".join(lines), encoding="utf-8")
    return REVIEW


def main() -> int:
    rows = [row for row in load_rows() if row.get("Grid_File")]
    if not rows:
        raise SystemExit("No grid files found in queue.")
    sheet = build_sheet(rows)
    review = build_review(rows)
    print(f"[FIRST-AUDIT-TOP4-GRIDS] sheet={sheet}")
    print(f"[FIRST-AUDIT-TOP4-GRIDS] review={review}")
    print(f"[FIRST-AUDIT-TOP4-GRIDS] grids={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
