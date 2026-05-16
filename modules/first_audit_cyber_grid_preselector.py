"""Create a technical preselection worksheet from Cyber-Renaissance draft grids.

This is not a final aesthetic decision. It slices each Midjourney 2x2 grid into
four candidates, scores basic technical fitness, and gives Rex a shorter review
surface before spending any upscale minutes.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW_DIR = PROJECT_ROOT / "Review_Packets" / "First_Audit_001"
MJ_QUEUE = DATABASE / "First_Audit_Cyber_Renaissance_MJ_Dispatch_Queue.csv"
OUTPUT_CSV = REVIEW_DIR / "FIRST_AUDIT_CYBER_RENAISSANCE_TECHNICAL_PRESELECT.csv"
OUTPUT_MD = REVIEW_DIR / "FIRST_AUDIT_CYBER_RENAISSANCE_TECHNICAL_PRESELECT.md"
CONTACT_SHEET = REVIEW_DIR / "FIRST_AUDIT_CYBER_RENAISSANCE_PRESELECT_CONTACT_SHEET.jpg"


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


def crop_quadrants(grid: Image.Image) -> list[Image.Image]:
    width, height = grid.size
    mid_x, mid_y = width // 2, height // 2
    boxes = [
        (0, 0, mid_x, mid_y),
        (mid_x, 0, width, mid_y),
        (0, mid_y, mid_x, height),
        (mid_x, mid_y, width, height),
    ]
    return [grid.crop(box).convert("RGB") for box in boxes]


def image_score(img: Image.Image) -> dict[str, float]:
    gray = img.convert("L")
    edge = gray.filter(ImageFilter.FIND_EDGES)
    edge_stat = ImageStat.Stat(edge)
    gray_stat = ImageStat.Stat(gray)
    rgb_stat = ImageStat.Stat(img)
    edge_score = edge_stat.mean[0]
    contrast = gray_stat.stddev[0]
    channel_spread = sum(rgb_stat.stddev) / 3.0
    # Penalize very low contrast, overly blank, or muddy crops. These are
    # technical filters only; Rex still judges story/composition.
    score = edge_score * 0.45 + contrast * 0.35 + channel_spread * 0.20
    if contrast < 28:
        score -= 15
    if edge_score < 14:
        score -= 10
    return {
        "edge_score": round(edge_score, 2),
        "contrast": round(contrast, 2),
        "channel_spread": round(channel_spread, 2),
        "technical_score": round(score, 2),
    }


def save_contact_sheet(candidates: list[dict[str, object]]) -> None:
    top = candidates[:24]
    cols = 4
    tile_w, tile_h = 430, 500
    sheet = Image.new("RGB", (cols * tile_w, math.ceil(len(top) / cols) * tile_h + 90), (246, 244, 239))
    draw = ImageDraw.Draw(sheet)
    title_font = font(28, bold=True)
    label_font = font(17, bold=True)
    small_font = font(14)
    draw.text((24, 22), "First Audit Cyber-Renaissance / Technical Preselect", fill=(28, 26, 22), font=title_font)
    draw.text((24, 58), "Top crops by sharpness, contrast, and material readability. No upscale triggered.", fill=(92, 82, 70), font=small_font)
    for idx, candidate in enumerate(top):
        img = candidate["image"].copy()  # type: ignore[index, union-attr]
        img.thumbnail((390, 360), Image.LANCZOS)
        x = (idx % cols) * tile_w
        y = 90 + (idx // cols) * tile_h
        draw.rounded_rectangle((x + 14, y + 12, x + tile_w - 14, y + tile_h - 16), radius=14, fill=(255, 255, 252), outline=(207, 198, 184))
        sheet.paste(img, (x + (tile_w - img.width) // 2, y + 24))
        draw.text((x + 26, y + 395), str(candidate["candidate_id"]), fill=(23, 21, 18), font=label_font)
        draw.text((x + 26, y + 423), f"score {candidate['technical_score']} | edge {candidate['edge_score']} | contrast {candidate['contrast']}", fill=(74, 67, 58), font=small_font)
        draw.text((x + 26, y + 446), "Rex must still approve story/composition.", fill=(124, 70, 42), font=small_font)
    sheet.save(CONTACT_SHEET, quality=92)


def main() -> int:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_csv(MJ_QUEUE)
    candidates: list[dict[str, object]] = []
    for row in rows:
        if clean(row.get("Harvest_Status")) != "GRID_FOUND":
            continue
        sku = clean(row.get("Internal_SKU"))
        grid_value = clean(row.get("Grid_File"))
        if not sku or not grid_value:
            continue
        grid_path = PROJECT_ROOT / grid_value
        if not grid_path.exists():
            continue
        try:
            grid = Image.open(grid_path).convert("RGB")
        except Exception:
            continue
        for idx, crop in enumerate(crop_quadrants(grid), start=1):
            metrics = image_score(crop)
            candidates.append(
                {
                    "candidate_id": f"{sku}-Q{idx}",
                    "sku": sku,
                    "quadrant": f"Q{idx}",
                    "grid_file": str(grid_path),
                    "image": crop,
                    **metrics,
                }
            )
    candidates.sort(key=lambda item: float(item["technical_score"]), reverse=True)
    if not candidates:
        print("[FIRST-AUDIT-CYBER-PRESELECT] no candidates")
        return 1
    save_contact_sheet(candidates)
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["Rank", "Candidate_ID", "Internal_SKU", "Quadrant", "Technical_Score", "Edge_Score", "Contrast", "Channel_Spread", "Grid_File"],
        )
        writer.writeheader()
        for rank, item in enumerate(candidates, start=1):
            writer.writerow(
                {
                    "Rank": rank,
                    "Candidate_ID": item["candidate_id"],
                    "Internal_SKU": item["sku"],
                    "Quadrant": item["quadrant"],
                    "Technical_Score": item["technical_score"],
                    "Edge_Score": item["edge_score"],
                    "Contrast": item["contrast"],
                    "Channel_Spread": item["channel_spread"],
                    "Grid_File": item["grid_file"],
                }
            )
    md_lines = [
        "# First Audit Cyber-Renaissance Technical Preselect",
        "",
        f"- Contact sheet: `{CONTACT_SHEET}`",
        f"- Candidates scored: {len(candidates)}",
        "- This is a technical shortlist only. It does not approve upscale or final release.",
        "",
        "## Top 24",
        "",
    ]
    for rank, item in enumerate(candidates[:24], start=1):
        md_lines.append(
            f"{rank}. `{item['candidate_id']}` score={item['technical_score']} edge={item['edge_score']} contrast={item['contrast']} source=`{item['grid_file']}`"
        )
    OUTPUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"[FIRST-AUDIT-CYBER-PRESELECT] candidates={len(candidates)} contact={CONTACT_SHEET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
