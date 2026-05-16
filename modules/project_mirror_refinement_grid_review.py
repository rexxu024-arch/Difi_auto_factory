"""Build Rex/Gemini review artifacts for Project Mirror refinement grids."""

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
CONTACT = REVIEW / "PROJECT_MIRROR_REFINEMENT_GRID_CONTACT_SHEET.jpg"
REPORT = REVIEW / "PROJECT_MIRROR_REFINEMENT_GRID_REVIEW.md"
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


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def fit(path: Path, size: tuple[int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image.thumbnail(size, Image.LANCZOS)
    canvas = Image.new("RGB", size, (239, 237, 232))
    canvas.paste(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return canvas


def ready_rows() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(QUEUE):
        if clean(row.get("Harvest_Status")) == "GRID_FOUND" and clean(row.get("Grid_File")):
            rows.append(row)
    return rows


def build_contact(rows: list[dict[str, str]]) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    cols = 3
    tile_w, tile_h = 560, 595
    image_box = (520, 390)
    header_h = 98
    sheet = Image.new("RGB", (cols * tile_w, ((len(rows) + cols - 1) // cols) * tile_h + header_h), (246, 244, 239))
    draw = ImageDraw.Draw(sheet)
    draw.text((28, 22), "Project Mirror / Production Refinement Grid Review", fill=(28, 26, 22), font=font(30, bold=True))
    draw.text(
        (28, 60),
        "Reference-derived premium DNA, already product-carrier constrained. Draft grids only; no upscale/publish/fee.",
        fill=(96, 85, 70),
        font=font(14),
    )

    for idx, row in enumerate(rows):
        x = (idx % cols) * tile_w
        y = header_h + (idx // cols) * tile_h
        draw.rounded_rectangle((x + 14, y + 12, x + tile_w - 14, y + tile_h - 18), radius=12, fill=(255, 255, 252), outline=(204, 196, 181))
        grid = PROJECT_ROOT / clean(row.get("Grid_File"))
        try:
            sheet.paste(fit(grid, image_box), (x + 20, y + 22))
        except Exception:
            draw.rectangle((x + 20, y + 22, x + 540, y + 412), fill=(226, 222, 214))
            draw.text((x + 36, y + 198), "GRID MISSING", fill=(130, 38, 32), font=font(18, bold=True))
        draw.text((x + 24, y + 428), clean(row.get("Internal_SKU"))[:58], fill=(22, 20, 18), font=font(16, bold=True))
        draw.text((x + 24, y + 454), clean(row.get("Concept_Name"))[:62], fill=(56, 51, 44), font=font(13))
        draw.text((x + 24, y + 477), clean(row.get("Recommended_Format"))[:62], fill=(85, 72, 58), font=font(13, bold=True))
        note = clean(row.get("Review_Note")).replace("mockup need:", "mockup:")
        draw.text((x + 24, y + 500), note[:74], fill=(96, 85, 70), font=font(12))
        draw.text((x + 24, y + 520), note[74:148], fill=(96, 85, 70), font=font(12))
    sheet.save(CONTACT, quality=92)


def write_report(rows: list[dict[str, str]]) -> None:
    by_product = Counter(clean(row.get("Recommended_Format")) or "Unknown" for row in rows)
    lines = [
        "# Project Mirror Production Refinement Grid Review",
        "",
        f"- Generated: {now_et()}",
        f"- Contact sheet: `{CONTACT}`",
        f"- Ready draft grids: {len(rows)}",
        f"- Product lanes: {dict(by_product)}",
        "- Policy: draft-grid review only. No upscale, no Printify creation, no marketplace publishing, no fee.",
        "- Selection rule: pick only rows with clear thumbnail value, credible premium material depth, and product-carrier fit at 5x7 or 12x18.",
        "",
        "## Recommended Review Order",
        "",
        "1. Reject any grid with muddy shadow, obvious AI smear, tiny pseudo-text, or cheap souvenir feel.",
        "2. Shortlist one Acrylic Block, one $48 Studio Print, and one framed-poster candidate.",
        "3. Only shortlisted rows should move into official mockup/source rebuild work.",
        "",
        "## Grid Rows",
        "",
    ]
    for row in rows:
        grid = PROJECT_ROOT / clean(row.get("Grid_File"))
        lines.extend(
            [
                f"### {clean(row.get('Internal_SKU'))}",
                f"- Concept: {clean(row.get('Concept_Name'))}",
                f"- Format: {clean(row.get('Recommended_Format'))}",
                f"- QA gate: {clean(row.get('QA_Gate'))}",
                f"- Review note: {clean(row.get('Review_Note'))}",
                f"- Grid: `{grid}`",
                "",
            ]
        )
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    by_product = Counter(clean(row.get("Recommended_Format")) or "Unknown" for row in rows)
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {now_et()} - Project Mirror refinement contact sheet\n"
            f"- Built refinement review contact sheet with {len(rows)} draft grid(s); lanes={dict(by_product)}.\n"
            f"- Contact sheet: `{CONTACT}`; report: `{REPORT}`.\n"
            "- No upscale, publish, or fee action was taken.\n"
        )


def main() -> int:
    rows = ready_rows()
    if not rows:
        print("[PROJECT-MIRROR-REFINEMENT-REVIEW] no ready grid rows")
        return 1
    build_contact(rows)
    write_report(rows)
    append_progress(rows)
    print(f"[PROJECT-MIRROR-REFINEMENT-REVIEW] grids={len(rows)} contact={CONTACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
