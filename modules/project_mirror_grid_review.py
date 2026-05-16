"""Build Rex-facing contact sheets for Project Mirror A/B draft grids."""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"
QUEUE = DATABASE / "Project_Mirror_MJ_Dispatch_Queue.csv"
CONTACT = REVIEW / "PROJECT_MIRROR_AB_GRID_CONTACT_SHEET.jpg"
REPORT = REVIEW / "PROJECT_MIRROR_AB_GRID_REVIEW.md"
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
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def fit(path: Path, size: tuple[int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image.thumbnail(size, Image.LANCZOS)
    canvas = Image.new("RGB", size, (238, 235, 228))
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
    cols = 2
    tile_w, tile_h = 720, 650
    image_box = (680, 510)
    sheet = Image.new("RGB", (cols * tile_w, ((len(rows) + 1) // 2) * tile_h + 95), (246, 244, 239))
    draw = ImageDraw.Draw(sheet)
    title_font = font(30, bold=True)
    label_font = font(17, bold=True)
    small_font = font(14)
    draw.text((28, 22), "Project Mirror / A-B Draft Grid Review", fill=(28, 26, 22), font=title_font)
    draw.text((28, 58), "Compare old prompt logic against reference-derived premium DNA. Draft grids only; no upscale.", fill=(96, 85, 70), font=small_font)

    for idx, row in enumerate(rows):
        x = (idx % cols) * tile_w
        y = 95 + (idx // cols) * tile_h
        draw.rounded_rectangle((x + 16, y + 12, x + tile_w - 16, y + tile_h - 18), radius=14, fill=(255, 255, 252), outline=(204, 196, 181))
        grid = PROJECT_ROOT / clean(row.get("Grid_File"))
        try:
            sheet.paste(fit(grid, image_box), (x + 20, y + 22))
        except Exception:
            draw.rectangle((x + 20, y + 22, x + 700, y + 532), fill=(226, 222, 214))
            draw.text((x + 36, y + 255), "GRID MISSING", fill=(130, 38, 32), font=label_font)
        draw.text((x + 26, y + 548), clean(row.get("Internal_SKU"))[:62], fill=(22, 20, 18), font=label_font)
        draw.text((x + 26, y + 575), clean(row.get("Concept_Name"))[:70], fill=(56, 51, 44), font=small_font)
        draw.text((x + 26, y + 598), clean(row.get("Review_Note"))[:76], fill=(96, 85, 70), font=small_font)
    sheet.save(CONTACT, quality=92)


def write_report(rows: list[dict[str, str]]) -> None:
    by_dna: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        sku = clean(row.get("Internal_SKU"))
        dna = sku.rsplit("-", 1)[0]
        by_dna[dna].append(sku)
    complete_pairs = sum(1 for values in by_dna.values() if len(values) >= 2)
    hold = [row for row in read_csv(QUEUE) if clean(row.get("Harvest_Status")) != "GRID_FOUND"]
    lines = [
        "# Project Mirror A/B Grid Review",
        "",
        f"- Contact sheet: `{CONTACT}`",
        f"- Ready grids: {len(rows)}",
        f"- Complete A/B pairs: {complete_pairs}",
        f"- Hold / not harvested: {len(hold)}",
        "- Decision rule: promote Project Mirror DNA only if it beats old logic on material depth, executive-gift fit, non-generic luxury signal, and thumbnail clarity.",
        "",
        "## Ready Rows",
        "",
    ]
    for row in rows:
        lines.append(f"- {clean(row.get('Internal_SKU'))}: {clean(row.get('Review_Note'))}; grid=`{PROJECT_ROOT / clean(row.get('Grid_File'))}`")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    by_dna: dict[str, int] = defaultdict(int)
    for row in rows:
        by_dna[clean(row.get("Internal_SKU")).rsplit("-", 1)[0]] += 1
    complete_pairs = sum(1 for count in by_dna.values() if count >= 2)
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {now_et()} - Project Mirror A/B Contact Sheet\n"
            f"- Built Project Mirror review contact sheet with {len(rows)} grid(s) and {complete_pairs} complete A/B pair(s).\n"
            f"- Contact sheet: `{CONTACT}`; report: `{REPORT}`.\n"
        )


def main() -> int:
    rows = ready_rows()
    if not rows:
        print("[PROJECT-MIRROR-REVIEW] no ready grid rows")
        return 1
    build_contact(rows)
    write_report(rows)
    append_progress(rows)
    print(f"[PROJECT-MIRROR-REVIEW] grids={len(rows)} contact={CONTACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
