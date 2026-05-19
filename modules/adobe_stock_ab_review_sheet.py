"""Build a Rex review sheet for Adobe Stock Codex A/B/C draft grids.

The Adobe production QA gate intentionally refuses draft grids. This script
creates a visual review artifact from harvested Midjourney grids so Rex can
choose which arms deserve U/2x upscale before any Adobe upload work begins.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
OUT_DIR = REVIEW / "Adobe_Stock_AB_Review"
ET = ZoneInfo("America/New_York")


def resolve_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def read_rows(queue: Path) -> list[dict[str, str]]:
    with queue.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_font(size: int = 18) -> ImageFont.ImageFont:
    for name in ("arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def fit_image(path: Path, box: tuple[int, int]) -> Image.Image:
    with Image.open(path) as image:
        image = image.convert("RGB")
        image.thumbnail(box, Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", box, (18, 20, 24))
        x = (box[0] - image.width) // 2
        y = (box[1] - image.height) // 2
        canvas.paste(image, (x, y))
        return canvas


def run(
    limit: int = 12,
    queue: Path | None = None,
    label: str = "ab",
    title_text: str = "Adobe Stock Codex A/B Draft Grid Review",
) -> dict[str, str | int]:
    queue = queue or (DATABASE / "Adobe_Stock_Codex_AB_MJ_Dispatch_Queue.csv")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for row in read_rows(queue):
        grid = (row.get("Grid_File") or "").strip()
        if not grid:
            continue
        path = resolve_path(grid)
        if not path.exists():
            continue
        rows.append(row)
        if limit and len(rows) >= limit:
            break

    thumb_w, thumb_h = 360, 240
    label_h = 88
    cols = 3
    rows_n = max(1, (len(rows) + cols - 1) // cols)
    margin = 24
    gap = 18
    width = margin * 2 + cols * thumb_w + (cols - 1) * gap
    height = margin * 2 + rows_n * (thumb_h + label_h) + (rows_n - 1) * gap
    sheet = Image.new("RGB", (width, height), (12, 15, 19))
    draw = ImageDraw.Draw(sheet)
    font = load_font(16)
    small = load_font(13)

    for idx, row in enumerate(rows):
        col = idx % cols
        r = idx // cols
        x = margin + col * (thumb_w + gap)
        y = margin + r * (thumb_h + label_h + gap)
        image = fit_image(resolve_path(row["Grid_File"]), (thumb_w, thumb_h))
        sheet.paste(image, (x, y))
        title = f"{row.get('Internal_SKU','')}  {row.get('Concept_Name','')}"
        note = row.get("Review_Note", "")
        draw.text((x, y + thumb_h + 8), title[:62], fill=(226, 235, 247), font=font)
        draw.text((x, y + thumb_h + 34), note[:78], fill=(158, 177, 198), font=small)
        draw.text((x, y + thumb_h + 56), "Draft grid only: choose best arm before U/2x", fill=(113, 220, 185), font=small)

    stamp = datetime.now(ET).strftime("%Y%m%d_%H%M%S")
    safe_label = "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in label).strip("_") or "ab"
    sheet_path = OUT_DIR / f"adobe_stock_{safe_label}_contact_sheet_{stamp}.jpg"
    latest_path = OUT_DIR / f"adobe_stock_{safe_label}_contact_sheet_latest.jpg"
    sheet.save(sheet_path, quality=90)
    sheet.save(latest_path, quality=90)

    md_path = REVIEW / f"Adobe_Stock_{safe_label.upper()}_Review_latest.md"
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write(f"# {title_text}\n\n")
        handle.write(f"- Generated: {datetime.now(ET).isoformat(timespec='seconds')}\n")
        handle.write(f"- Source queue: `{queue}`\n")
        handle.write(f"- Grids ready: {len(rows)}\n")
        handle.write("- Policy: no upload, no upscale until Rex approves a specific arm.\n\n")
        handle.write(f"![Adobe Stock A/B contact sheet]({latest_path.as_posix()})\n\n")
        for row in rows:
            handle.write(
                f"- **{row.get('Internal_SKU','')}** | {row.get('Concept_Name','')} | "
                f"{row.get('Review_Note','')} | `{row.get('Grid_File','')}`\n"
            )

    return {"ready_grids": len(rows), "contact_sheet": str(latest_path), "review_packet": str(md_path)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--queue", default=str(DATABASE / "Adobe_Stock_Codex_AB_MJ_Dispatch_Queue.csv"))
    parser.add_argument("--label", default="ab")
    parser.add_argument("--title", default="Adobe Stock Codex A/B Draft Grid Review")
    args = parser.parse_args()
    result = run(limit=args.limit, queue=Path(args.queue), label=args.label, title_text=args.title)
    print("[ADOBE-AB-REVIEW-SHEET]", result)


if __name__ == "__main__":
    main()
