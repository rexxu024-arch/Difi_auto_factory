"""Generate Etsy listing preview images for prepared digital printable packs."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
QUEUE = DATABASE_DIR / "Etsy_Digital_Upload_Queue.csv"
PREVIEW_CSV = DATABASE_DIR / "Etsy_Digital_Preview_Assets.csv"


def clean(value) -> str:
    return str(value or "").strip()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


FONT_TITLE = font(82, bold=True)
FONT_SUBTITLE = font(48, bold=False)
FONT_CARD_TITLE = font(44, bold=True)
FONT_BODY = font(34, bold=False)
FONT_SMALL = font(28, bold=False)


def open_fit(path: Path, size: tuple[int, int], fill=(245, 245, 242)) -> Image.Image:
    canvas = Image.new("RGB", size, fill)
    with Image.open(path) as im:
        im = im.convert("RGB")
        im.thumbnail(size, Image.Resampling.LANCZOS)
        x = (size[0] - im.width) // 2
        y = (size[1] - im.height) // 2
        canvas.paste(im, (x, y))
    return canvas


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    width_chars: int,
    fill=(35, 35, 35),
    line_gap=10,
    text_font: ImageFont.ImageFont = FONT_BODY,
) -> None:
    words = text.split()
    lines = []
    current = []
    for word in words:
        probe = " ".join(current + [word])
        if len(probe) > width_chars and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    x, y = xy
    for line in lines:
        draw.text((x, y), line, fill=fill, font=text_font)
        box = draw.textbbox((x, y), line, font=text_font)
        y += (box[3] - box[1]) + line_gap


def centered_text(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, fill, text_font) -> None:
    text_box = draw.textbbox((0, 0), text, font=text_font)
    x = box[0] + (box[2] - box[0] - (text_box[2] - text_box[0])) // 2
    y = box[1] + (box[3] - box[1] - (text_box[3] - text_box[1])) // 2
    draw.text((x, y), text, fill=fill, font=text_font)


def preview_main(pack_dir: Path, manifest: dict) -> Path:
    source = Path(manifest["files"][0]["path"])
    out = pack_dir / "Preview_01_Framed_Wall_Art.jpg"
    canvas = Image.new("RGB", (2000, 2000), (239, 236, 229))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, 2000, 1480], fill=(242, 240, 234))
    draw.rectangle([0, 1480, 2000, 2000], fill=(224, 218, 206))

    frame = (610, 170, 1510, 1520)
    draw.rounded_rectangle([frame[0] - 52, frame[1] - 38, frame[2] + 70, frame[3] + 70], radius=18, fill=(197, 190, 179))
    draw.rectangle([frame[0] - 34, frame[1] - 34, frame[2] + 34, frame[3] + 34], fill=(52, 45, 38))
    draw.rectangle([frame[0] - 18, frame[1] - 18, frame[2] + 18, frame[3] + 18], fill=(236, 232, 224))
    art = open_fit(source, (frame[2] - frame[0], frame[3] - frame[1]), fill=(236, 232, 224))
    canvas.paste(art, (frame[0], frame[1]))

    draw.rounded_rectangle([105, 1610, 915, 1888], radius=30, fill=(255, 254, 250), outline=(190, 183, 172), width=3)
    draw.text((160, 1665), "Digital Download", fill=(36, 32, 28), font=FONT_TITLE)
    draw.text((164, 1768), "5 printable JPG ratios included", fill=(72, 66, 58), font=FONT_SUBTITLE)
    draw.text((164, 1830), "No physical item is shipped", fill=(108, 72, 52), font=FONT_BODY)
    draw.text((1260, 1762), "Quiet Relic Studio", fill=(68, 60, 53), font=FONT_BODY)
    draw.text((1260, 1810), "Printable wall art", fill=(96, 88, 78), font=FONT_SMALL)
    canvas.save(out, "JPEG", quality=92, optimize=True)
    return out


def preview_sizes(pack_dir: Path, manifest: dict) -> Path:
    out = pack_dir / "Preview_02_Included_Sizes.jpg"
    canvas = Image.new("RGB", (2000, 2000), (250, 249, 246))
    draw = ImageDraw.Draw(canvas)
    draw.text((130, 105), "Included Files", fill=(30, 30, 30), font=FONT_TITLE)
    draw.text((132, 205), "5 high-resolution JPG ratios for common frames", fill=(70, 70, 70), font=FONT_SUBTITLE)
    y = 330
    for file_info in manifest["files"]:
        label = file_info["label"]
        size_px = file_info["size_px"]
        draw.rounded_rectangle([130, y, 1870, y + 205], radius=22, fill=(255, 254, 250), outline=(190, 185, 176), width=3)
        draw.text((190, y + 40), label, fill=(35, 35, 35), font=FONT_CARD_TITLE)
        draw.text((190, y + 108), f"{size_px} pixels at 300 DPI", fill=(80, 80, 80), font=FONT_BODY)
        y += 240
    draw.rounded_rectangle([130, 1600, 1870, 1875], radius=26, fill=(242, 237, 229), outline=(190, 185, 176), width=2)
    draw.text((185, 1644), "Instant download only", fill=(35, 35, 35), font=FONT_CARD_TITLE)
    draw_wrapped(
        draw,
        (185, 1714),
        "Print at home, at a local print shop, or through an online photo lab. Colors may vary slightly by monitor and printer.",
        72,
        fill=(80, 80, 80),
        text_font=FONT_BODY,
    )
    canvas.save(out, "JPEG", quality=92, optimize=True)
    return out


def preview_ratio_gallery(pack_dir: Path, manifest: dict) -> Path:
    out = pack_dir / "Preview_03_Ratio_Gallery.jpg"
    canvas = Image.new("RGB", (2000, 2000), (248, 247, 244))
    draw = ImageDraw.Draw(canvas)
    draw.text((100, 80), "Printable Ratios", fill=(35, 35, 35), font=FONT_TITLE)
    draw.text((104, 180), "Use the best file for your frame size", fill=(75, 75, 75), font=FONT_SUBTITLE)
    boxes = [
        (120, 330, 610, 1065),
        (755, 330, 1245, 985),
        (1400, 330, 1840, 880),
        (360, 1190, 800, 1750),
        (1180, 1190, 1620, 1810),
    ]
    for box, file_info in zip(boxes, manifest["files"]):
        path = Path(file_info["path"])
        w, h = box[2] - box[0], box[3] - box[1]
        art = open_fit(path, (w, h), fill=(238, 236, 231))
        draw.rounded_rectangle([box[0] - 18, box[1] - 18, box[2] + 18, box[3] + 78], radius=18, fill=(255, 254, 250), outline=(188, 181, 171), width=2)
        canvas.paste(art, (box[0], box[1]))
        draw.rectangle(box, outline=(170, 165, 156), width=2)
        centered_text(draw, (box[0] - 5, box[3] + 18, box[2] + 5, box[3] + 72), file_info["ratio"], fill=(40, 40, 40), text_font=FONT_BODY)
    canvas.save(out, "JPEG", quality=92, optimize=True)
    return out


def load_queue() -> list[dict]:
    with QUEUE.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def run() -> None:
    rows = []
    for row in load_queue():
        pack_dir = Path(row["Pack_Dir"])
        manifest_path = pack_dir / "manifest.json"
        if not manifest_path.exists():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        p1 = preview_main(pack_dir, manifest)
        p2 = preview_sizes(pack_dir, manifest)
        p3 = preview_ratio_gallery(pack_dir, manifest)
        rows.append(
            {
                "ID": row["ID"],
                "Title": row["Title"],
                "Preview_1": str(p1),
                "Preview_2": str(p2),
                "Preview_3": str(p3),
                "Pack_Dir": row["Pack_Dir"],
            }
        )
    with PREVIEW_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ID", "Title", "Preview_1", "Preview_2", "Preview_3", "Pack_Dir"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"[DIGITAL-PREVIEW] rows={len(rows)} csv={PREVIEW_CSV}")


if __name__ == "__main__":
    run()
