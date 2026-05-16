"""Build a QA packet for Midjourney identity-locked scene experiments.

The goal is not to auto-approve marketplace use. These scene images must prove
that the product identity stayed intact before they can become listing gallery
assets. This script creates a compact contact sheet and report for Rex/Grey.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

QUEUE = PROJECT_ROOT / "Database" / "MJ_Identity_Locked_Scene_Dispatch_Queue.csv"
REVIEW = PROJECT_ROOT / "Review_Packets"
CONTACT = REVIEW / "MJ_IDENTITY_LOCKED_SCENE_QA_CONTACT_SHEET.jpg"
REPORT = REVIEW / "MJ_IDENTITY_LOCKED_SCENE_QA_REPORT.md"
NY_TZ = ZoneInfo("America/New_York")


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def now_et() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_rows(queue: Path) -> list[dict[str, str]]:
    if not queue.exists():
        return []
    with queue.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def image_path(row: dict[str, str], field: str) -> Path | None:
    raw = clean(row.get(field))
    if not raw:
        return None
    path = PROJECT_ROOT / raw
    return path if path.exists() else None


def thumb(path: Path, size: tuple[int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    out = Image.new("RGB", size, (242, 240, 234))
    x = (size[0] - image.width) // 2
    y = (size[1] - image.height) // 2
    out.paste(image, (x, y))
    return out


def font(size: int) -> ImageFont.ImageFont:
    for name in ("arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def build_packet(
    limit: int = 12,
    queue: Path = QUEUE,
    contact: Path = CONTACT,
    report_path: Path = REPORT,
) -> int:
    reviewable_statuses = {"GRID_FOUND", "READY_FOR_VISUAL_QA", "VISUAL_QA_HOLD_IDENTITY_DRIFT"}
    rows = [
        row for row in read_rows(queue)
        if clean(row.get("Harvest_Status")) in reviewable_statuses
        and image_path(row, "Grid_File")
    ][:limit]
    contact.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        report_path.write_text(
            f"# MJ Identity-Locked Scene QA\n\nGenerated: {now_et()}\n\nNo reviewable grid rows.\n",
            encoding="utf-8-sig",
        )
        print("[IDENTITY-SCENE-QA] no rows")
        return 0

    cell_w, cell_h = 260, 310
    header_h = 78
    cols = 5
    rows_h = len(rows) * cell_h + header_h
    canvas = Image.new("RGB", (cols * cell_w, rows_h), (230, 228, 220))
    draw = ImageDraw.Draw(canvas)
    title_font = font(22)
    small_font = font(14)
    draw.rectangle((0, 0, canvas.width, header_h), fill=(28, 28, 27))
    draw.text((22, 18), "MJ Identity-Locked Scene QA - product identity must not drift", fill=(245, 243, 236), font=title_font)

    report = [
        "# MJ Identity-Locked Scene QA",
        "",
        f"Generated: {now_et()}",
        "",
        "Purpose: evaluate whether Midjourney scene mockups preserved the exact product/artwork identity.",
        "Rule: no image from this packet may enter Etsy/Printify galleries until Rex/Grey approves identity stability.",
        "Draft rule: GRID_FOUND rows are grid-only concept checks; no MJ upscale is requested during this phase.",
        "",
        "| SKU | Status | Grid | U files | Next action |",
        "| --- | --- | --- | --- | --- |",
    ]

    for r, row in enumerate(rows):
        y = header_h + r * cell_h
        sku = clean(row.get("Internal_SKU"))
        draw.rectangle((0, y, canvas.width, y + cell_h), fill=(238, 236, 229) if r % 2 == 0 else (226, 224, 218))
        draw.text((14, y + 12), sku[:34], fill=(18, 18, 18), font=small_font)
        fields = ["Grid_File", "U1_File", "U2_File", "U3_File", "U4_File"]
        labels = ["GRID", "U1", "U2", "U3", "U4"]
        for c, (field, label) in enumerate(zip(fields, labels)):
            x = c * cell_w
            draw.text((x + 14, y + 40), label, fill=(80, 76, 68), font=small_font)
            path = image_path(row, field)
            if path:
                canvas.paste(thumb(path, (232, 232)), (x + 14, y + 64))
            else:
                draw.rectangle((x + 14, y + 64, x + 246, y + 296), outline=(160, 150, 138), width=2)
                draw.text((x + 72, y + 160), "MISSING", fill=(120, 45, 40), font=small_font)
        u_count = sum(1 for field in ["U1_File", "U2_File", "U3_File", "U4_File"] if image_path(row, field))
        report.append(
            f"| {sku} | {clean(row.get('Harvest_Status'))} | {clean(row.get('Grid_Message_ID'))} | {u_count}/4 | REX_VISUAL_IDENTITY_REVIEW |"
        )

    canvas.save(contact, "JPEG", quality=92, optimize=True)
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8-sig")
    print(f"[IDENTITY-SCENE-QA] rows={len(rows)} contact={contact}")
    print(f"[IDENTITY-SCENE-QA] report={report_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build identity-locked MJ scene QA packet")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--queue", default=str(QUEUE))
    parser.add_argument("--contact", default=str(CONTACT))
    parser.add_argument("--report", default=str(REPORT))
    args = parser.parse_args()
    return build_packet(
        limit=max(1, args.limit),
        queue=Path(args.queue),
        contact=Path(args.contact),
        report_path=Path(args.report),
    )


if __name__ == "__main__":
    raise SystemExit(main())
