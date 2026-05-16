"""Generate Etsy listing preview images for prepared digital printable packs."""

from __future__ import annotations

import csv
import json
import re
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
QUEUE = DATABASE_DIR / "Etsy_Digital_Upload_Queue.csv"
GRAY_QUEUE = DATABASE_DIR / "Etsy_Digital_Gray_Launch_Queue.csv"
PREVIEW_CSV = DATABASE_DIR / "Etsy_Digital_Preview_Assets.csv"
EXTRACT_ROOT = PROJECT_ROOT / "Output" / "Digital" / "_PreviewExtracts"


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


def preview_detail_zoom(pack_dir: Path, manifest: dict) -> Path:
    source = Path(manifest["files"][0]["path"])
    out = pack_dir / "Preview_04_Detail_Zoom.jpg"
    canvas = Image.new("RGB", (2000, 2000), (244, 241, 235))
    draw = ImageDraw.Draw(canvas)
    art = open_fit(source, (1350, 1700), fill=(238, 236, 230))
    canvas.paste(art, (90, 150))
    draw.rectangle([90, 150, 1440, 1850], outline=(48, 43, 38), width=8)
    draw.rounded_rectangle([1270, 230, 1880, 760], radius=26, fill=(255, 254, 250), outline=(180, 172, 160), width=3)
    draw.text((1325, 290), "Detail Preview", fill=(32, 30, 28), font=FONT_CARD_TITLE)
    draw_wrapped(
        draw,
        (1328, 370),
        "High-resolution printable file prepared for crisp linework, subtle texture, and gallery-style wall decor.",
        31,
        fill=(78, 72, 65),
        text_font=FONT_BODY,
    )
    draw.rounded_rectangle([1270, 980, 1880, 1510], radius=26, fill=(235, 231, 222), outline=(180, 172, 160), width=3)
    draw.text((1325, 1040), "What you receive", fill=(32, 30, 28), font=FONT_CARD_TITLE)
    draw_wrapped(
        draw,
        (1328, 1120),
        "A digital download pack. Frames, props, and printed samples shown in previews are not included.",
        31,
        fill=(78, 72, 65),
        text_font=FONT_BODY,
    )
    canvas.save(out, "JPEG", quality=92, optimize=True)
    return out


def preview_download_info(pack_dir: Path, manifest: dict) -> Path:
    out = pack_dir / "Preview_05_Download_Info.jpg"
    canvas = Image.new("RGB", (2000, 2000), (250, 248, 244))
    draw = ImageDraw.Draw(canvas)
    draw.text((145, 140), "Digital Download Guide", fill=(34, 32, 30), font=FONT_TITLE)
    draw.text((150, 245), "No physical item ships", fill=(120, 74, 52), font=FONT_SUBTITLE)
    cards = [
        ("1", "Purchase", "After checkout, Etsy makes the files available from your account downloads."),
        ("2", "Print", "Use the ratio that matches your frame and print at home, locally, or online."),
        ("3", "Frame", "Choose matte paper for a quiet gallery look, or textured paper for a vintage archive feel."),
        ("4", "Note", "Preview scenes show styling ideas only. Your download includes the printable artwork files."),
    ]
    y = 420
    for number, title, body in cards:
        draw.rounded_rectangle([145, y, 1855, y + 260], radius=28, fill=(255, 254, 250), outline=(190, 182, 170), width=3)
        draw.ellipse([205, y + 70, 325, y + 190], fill=(41, 37, 33))
        centered_text(draw, (205, y + 70, 325, y + 190), number, fill=(255, 254, 250), text_font=FONT_CARD_TITLE)
        draw.text((380, y + 58), title, fill=(35, 33, 30), font=FONT_CARD_TITLE)
        draw_wrapped(draw, (382, y + 126), body, 78, fill=(78, 72, 65), text_font=FONT_BODY)
        y += 315
    draw.text((145, 1780), "Quiet Relic Studio", fill=(82, 75, 68), font=FONT_BODY)
    canvas.save(out, "JPEG", quality=92, optimize=True)
    return out


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pack_dir_for(row: dict) -> Path | None:
    if clean(row.get("Pack_Dir")):
        pack_dir = Path(clean(row.get("Pack_Dir")))
        if pack_dir.exists():
            return pack_dir
    if clean(row.get("Zip_Path")):
        zip_path = Path(clean(row.get("Zip_Path")))
        unpacked = zip_path.with_suffix("")
        if unpacked.exists():
            return unpacked
        if zip_path.exists() and zip_path.suffix.lower() == ".zip":
            return extract_zip_pack(zip_path, clean(row.get("ID")) or zip_path.stem)
    return None


def safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())
    return value.strip("-._") or "preview-pack"


def extract_zip_pack(zip_path: Path, item_id: str) -> Path | None:
    """Extract image payloads from legacy zip-only digital packs for previews."""
    dest = EXTRACT_ROOT / safe_name(item_id)
    existing = list(dest.glob("*.jpg")) + list(dest.glob("*.jpeg")) + list(dest.glob("*.png"))
    if existing:
        return dest

    dest.mkdir(parents=True, exist_ok=True)
    extracted = 0
    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            source_name = Path(info.filename).name
            if source_name.lower().startswith("preview_"):
                continue
            if Path(source_name).suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue
            target = dest / f"{extracted + 1:02d}_{safe_name(source_name)}"
            with archive.open(info) as source, target.open("wb") as handle:
                handle.write(source.read())
            extracted += 1
            if extracted >= 8:
                break
    return dest if extracted else None


def infer_ratio(path: Path) -> str:
    name = path.name.lower()
    for ratio in ("2x3", "3x4", "4x5", "5x7", "11x14"):
        if ratio in name:
            return ratio
    return "printable"


def manifest_from_pack(pack_dir: Path) -> dict | None:
    manifest_path = pack_dir / "manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    image_files = [
        path
        for path in sorted(pack_dir.iterdir())
        if path.is_file()
        and path.suffix.lower() in {".jpg", ".jpeg", ".png"}
        and not path.name.lower().startswith("preview_")
    ]
    if not image_files:
        return None
    order = {"2x3": 0, "3x4": 1, "4x5": 2, "5x7": 3, "11x14": 4}
    image_files.sort(key=lambda path: (order.get(infer_ratio(path), 99), path.name))
    files = []
    for path in image_files[:5]:
        try:
            with Image.open(path) as im:
                size_px = f"{im.width}x{im.height}"
        except Exception:
            size_px = "high resolution"
        ratio = infer_ratio(path)
        files.append(
            {
                "path": str(path),
                "label": f"{ratio} printable JPG",
                "ratio": ratio,
                "size_px": size_px,
            }
        )
    return {"files": files}


def load_queue() -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    for row in read_csv(QUEUE) + read_csv(GRAY_QUEUE):
        item_id = clean(row.get("ID"))
        if not item_id or item_id in seen:
            continue
        pack_dir = pack_dir_for(row)
        if not pack_dir or not pack_dir.exists():
            continue
        row = dict(row)
        row["Pack_Dir"] = str(pack_dir)
        rows.append(row)
        seen.add(item_id)
    return rows


def run(limit: int = 0) -> None:
    rows = []
    for row in load_queue():
        pack_dir = Path(row["Pack_Dir"])
        manifest = manifest_from_pack(pack_dir)
        if not manifest:
            continue
        p1 = preview_main(pack_dir, manifest)
        p2 = preview_sizes(pack_dir, manifest)
        p3 = preview_ratio_gallery(pack_dir, manifest)
        p4 = preview_detail_zoom(pack_dir, manifest)
        p5 = preview_download_info(pack_dir, manifest)
        rows.append(
            {
                "ID": row["ID"],
                "Title": row["Title"],
                "Preview_1": str(p1),
                "Preview_2": str(p2),
                "Preview_3": str(p3),
                "Preview_4": str(p4),
                "Preview_5": str(p5),
                "Pack_Dir": row["Pack_Dir"],
            }
        )
        if limit and len(rows) >= limit:
            break
    with PREVIEW_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["ID", "Title", "Preview_1", "Preview_2", "Preview_3", "Preview_4", "Preview_5", "Pack_Dir"],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"[DIGITAL-PREVIEW] rows={len(rows)} csv={PREVIEW_CSV}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    run(limit=args.limit)
