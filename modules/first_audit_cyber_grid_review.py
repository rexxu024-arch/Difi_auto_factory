"""Build a Rex-facing review packet for First Audit Cyber-Renaissance grids.

This is intentionally grid-only. It does not trigger or require Midjourney
upscales. Rex can select Top 1% candidates from the contact sheet before the
factory spends premium upscale minutes or builds final release folders.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW_DIR = PROJECT_ROOT / "Review_Packets" / "First_Audit_001"
DRAFT_QUEUE = DATABASE / "First_Audit_Cyber_Renaissance_Draft_Queue.csv"
MJ_QUEUE = DATABASE / "First_Audit_Cyber_Renaissance_MJ_Dispatch_Queue.csv"
CONTACT_SHEET = REVIEW_DIR / "FIRST_AUDIT_CYBER_RENAISSANCE_GRID_CONTACT_SHEET.jpg"
REPORT = REVIEW_DIR / "FIRST_AUDIT_CYBER_RENAISSANCE_GRID_REVIEW.md"


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def fit_image(path: Path, size: tuple[int, int]) -> Image.Image:
    img = Image.open(path).convert("RGB")
    img.thumbnail(size, Image.LANCZOS)
    canvas = Image.new("RGB", size, (238, 235, 228))
    x = (size[0] - img.width) // 2
    y = (size[1] - img.height) // 2
    canvas.paste(img, (x, y))
    return canvas


def wrapped(draw: ImageDraw.ImageDraw, text: str, max_width: int, fnt: ImageFont.ImageFont) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=fnt)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:3]


def build_contact_sheet(rows: list[dict[str, str]], draft_by_id: dict[str, dict[str, str]]) -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    cols = 3
    tile_w, tile_h = 620, 700
    image_box = (580, 500)
    rows_count = max(1, (len(rows) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * tile_w, rows_count * tile_h + 90), (246, 244, 239))
    draw = ImageDraw.Draw(sheet)
    title_font = font(30, bold=True)
    label_font = font(18, bold=True)
    small_font = font(15)
    draw.text((28, 24), "THE FIRST AUDIT: 001 / Cyber-Renaissance Draft Grids", fill=(28, 26, 22), font=title_font)
    draw.text((28, 60), "Grid-only review sheet. No upscale has been triggered.", fill=(102, 91, 75), font=small_font)

    for idx, row in enumerate(rows):
        sku = clean(row.get("Internal_SKU"))
        draft = draft_by_id.get(sku, {})
        grid_file = PROJECT_ROOT / clean(row.get("Grid_File"))
        x = (idx % cols) * tile_w
        y = 90 + (idx // cols) * tile_h
        draw.rounded_rectangle((x + 16, y + 14, x + tile_w - 16, y + tile_h - 18), radius=16, fill=(255, 255, 252), outline=(206, 198, 184))
        try:
            image = fit_image(grid_file, image_box)
            sheet.paste(image, (x + 20, y + 24))
        except Exception:
            draw.rectangle((x + 20, y + 24, x + 600, y + 524), fill=(228, 225, 218))
            draw.text((x + 40, y + 240), "GRID MISSING", fill=(126, 35, 31), font=label_font)
        code_name = clean(draft.get("code_name_cn")) or clean(row.get("Concept_Name"))
        battlefield = clean(draft.get("battlefield")) or clean(row.get("Batch"))
        vector = clean(draft.get("product_vector")) or clean(row.get("Recommended_Format"))
        draw.text((x + 28, y + 540), sku, fill=(22, 20, 18), font=label_font)
        draw.text((x + 28, y + 568), code_name[:34], fill=(44, 41, 36), font=label_font)
        for line_i, line in enumerate(wrapped(draw, f"{battlefield} / {vector}", 560, small_font)):
            draw.text((x + 28, y + 602 + line_i * 22), line, fill=(86, 78, 66), font=small_font)
    sheet.save(CONTACT_SHEET, quality=92)


def write_report(rows: list[dict[str, str]], draft_by_id: dict[str, dict[str, str]], unconfirmed: list[dict[str, str]]) -> None:
    lines = [
        "# First Audit Cyber-Renaissance Grid Review",
        "",
        f"- Contact sheet: `{CONTACT_SHEET}`",
        f"- Draft grids ready: {len(rows)}",
        f"- Unconfirmed / not harvested: {len(unconfirmed)}",
        "- Policy: grid-only concept review; no MJ upscale until Rex approves Top 1% candidates.",
        "- Review instruction: choose only images with historical composition, believable material physics, and private-studio aura. Reject cheap fantasy, static object boredom, or muddy background fog.",
        "",
        "## Ready Grids",
        "",
    ]
    for row in rows:
        sku = clean(row.get("Internal_SKU"))
        draft = draft_by_id.get(sku, {})
        lines.extend(
            [
                f"### {sku} / {clean(draft.get('code_name_cn'))}",
                f"- Battlefield: {clean(draft.get('battlefield'))}",
                f"- Product vector: {clean(draft.get('product_vector'))}",
                f"- Grid file: `{PROJECT_ROOT / clean(row.get('Grid_File'))}`",
                f"- Broker hook: {clean(draft.get('broker_hook_cn'))}",
                "",
            ]
        )
    if unconfirmed:
        lines.extend(["## Hold / Retry", ""])
        for row in unconfirmed:
            lines.append(f"- {clean(row.get('Internal_SKU'))}: dispatch={clean(row.get('Dispatch_Status'))}; harvest={clean(row.get('Harvest_Status')) or 'not harvested'}")
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    draft_rows = read_csv(DRAFT_QUEUE)
    mj_rows = read_csv(MJ_QUEUE)
    draft_by_id = {clean(row.get("id")): row for row in draft_rows}
    ready = [
        row
        for row in mj_rows
        if clean(row.get("Harvest_Status")) in {"GRID_FOUND", "READY_FOR_VISUAL_QA", "VISUAL_QA_PASSED"}
        and clean(row.get("Grid_File"))
    ]
    unconfirmed = [
        row
        for row in mj_rows
        if clean(row.get("Dispatch_Status")) != "MJ_SUBMITTED"
        or clean(row.get("Harvest_Status")) not in {"GRID_FOUND", "READY_FOR_VISUAL_QA", "VISUAL_QA_PASSED"}
    ]
    if not ready:
        print("[FIRST-AUDIT-CYBER-REVIEW] no grid files ready")
        return 1
    build_contact_sheet(ready, draft_by_id)
    write_report(ready, draft_by_id, unconfirmed)
    print(f"[FIRST-AUDIT-CYBER-REVIEW] ready={len(ready)} hold={len(unconfirmed)} contact={CONTACT_SHEET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
