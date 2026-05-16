"""Local visual QA for V7 Etsy Darwinian Lab samples.

This is a no-spend gate. It checks harvested U1-U4 images, produces a contact
sheet for Rex/Gemini review, and writes machine-readable QA decisions before
anything can become a paid Etsy listing.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont, ImageStat


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATABASE = ROOT / "Database"
REVIEW = ROOT / "Review_Packets"
MJ_QUEUE = DATABASE / "Etsy_Darwinian_Lab_V7_MJ_Dispatch_Queue.csv"
QA_CSV = DATABASE / "Etsy_Darwinian_Lab_V7_Visual_QA.csv"
QA_MD = REVIEW / "ETSY_DARWINIAN_LAB_V7_VISUAL_QA.md"
CONTACT_SHEET = REVIEW / "ETSY_DARWINIAN_LAB_V7_CONTACT_SHEET.jpg"
NY_TZ = ZoneInfo("America/New_York")


@dataclass
class ImageMetrics:
    path: Path
    width: int
    height: int
    file_kb: int
    brightness: float
    contrast: float
    saturation: float
    center_whitespace: float
    edge_repeat_delta: float
    score: float
    flags: list[str]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %z")


def clean(value: object) -> str:
    return str(value or "").strip()


def needs_visual_qa(row: dict[str, str]) -> bool:
    """Return true only for harvested rows that have not received a final QA gate."""
    if clean(row.get("Harvest_Status")) != "READY_FOR_VISUAL_QA":
        return False
    status = clean(row.get("Visual_QA_Status"))
    return status in {"", "PENDING_IMAGE_GENERATION"}


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing queue: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def write_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def image_path(row: dict[str, str], key: str) -> Path | None:
    value = clean(row.get(key))
    if not value:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path if path.exists() else None


def resize_for_metric(img: Image.Image, size: int = 384) -> Image.Image:
    work = img.convert("RGB")
    work.thumbnail((size, size))
    return work


def saturation_mean(img: Image.Image) -> float:
    hsv = img.convert("HSV")
    stat = ImageStat.Stat(hsv)
    return float(stat.mean[1])


def center_whitespace_ratio(img: Image.Image) -> float:
    gray = img.convert("L")
    w, h = gray.size
    crop = gray.crop((int(w * 0.3), int(h * 0.3), int(w * 0.7), int(h * 0.7)))
    data = list(crop.getdata())
    return sum(1 for px in data if px > 210) / max(1, len(data))


def edge_repeat_delta(img: Image.Image) -> float:
    """Small value roughly means opposite edges resemble each other for tile art."""
    work = resize_for_metric(img, 256).convert("RGB")
    w, h = work.size
    left = work.crop((0, 0, 8, h))
    right = work.crop((w - 8, 0, w, h))
    top = work.crop((0, 0, w, 8))
    bottom = work.crop((0, h - 8, w, h))

    def rms(a: Image.Image, b: Image.Image) -> float:
        pairs = zip(a.getdata(), b.getdata())
        total = 0.0
        count = 0
        for p, q in pairs:
            total += sum((p[i] - q[i]) ** 2 for i in range(3))
            count += 3
        return math.sqrt(total / max(1, count))

    return (rms(left, right) + rms(top, bottom)) / 2


def metrics_for(path: Path) -> ImageMetrics:
    with Image.open(path) as img:
        work = resize_for_metric(img)
        gray = work.convert("L")
        stat = ImageStat.Stat(gray)
        contrast = float(stat.stddev[0])
        brightness = float(stat.mean[0])
        saturation = saturation_mean(work)
        whitespace = center_whitespace_ratio(work)
        seam = edge_repeat_delta(work)
        width, height = img.size
    flags: list[str] = []
    if width < 1000 or height < 1000:
        flags.append("LOW_RESOLUTION")
    if contrast < 22:
        flags.append("LOW_CONTRAST")
    if brightness < 28:
        flags.append("SHADOW_CLIPPING")
    if path.stat().st_size < 500_000:
        flags.append("SMALL_FILE")
    score = contrast + min(saturation, 90) * 0.15 + (1 if not flags else -18 * len(flags))
    return ImageMetrics(
        path=path,
        width=width,
        height=height,
        file_kb=int(path.stat().st_size / 1024),
        brightness=brightness,
        contrast=contrast,
        saturation=saturation,
        center_whitespace=whitespace,
        edge_repeat_delta=seam,
        score=score,
        flags=flags,
    )


def pool_gate(pool_id: str, metrics: ImageMetrics) -> tuple[str, list[str]]:
    flags = list(metrics.flags)
    if pool_id == "POOL10" and metrics.saturation > 45:
        flags.append("TATTOO_FLASH_NOT_BLACK_INK_ONLY")
    if pool_id == "POOL09" and metrics.center_whitespace < 0.35:
        flags.append("PLANNER_CENTER_TOO_BUSY")
    if pool_id == "POOL08" and metrics.edge_repeat_delta > 52:
        flags.append("SEAMLESS_REPEAT_RISK")
    if pool_id == "POOL07" and metrics.saturation > 55:
        flags.append("VECTOR_CUT_FILE_TOO_PHOTOGRAPHIC")
    if pool_id == "POOL04" and metrics.contrast < 35:
        flags.append("STREETWEAR_THUMBNAIL_WEAK")
    if "LOW_RESOLUTION" in flags or "SHADOW_CLIPPING" in flags:
        return "HOLD", flags
    if flags:
        return "REVIEW", flags
    return "PASS", flags


def output_paths(queue_path: Path) -> tuple[Path, Path, Path]:
    if queue_path.resolve() == MJ_QUEUE.resolve():
        return QA_CSV, QA_MD, CONTACT_SHEET
    suffix = queue_path.stem.replace("Etsy_Darwinian_Lab_V7_", "")
    return (
        DATABASE / f"Etsy_Darwinian_Lab_V7_{suffix}_Visual_QA.csv",
        REVIEW / f"ETSY_DARWINIAN_LAB_V7_{suffix.upper()}_VISUAL_QA.md",
        REVIEW / f"ETSY_DARWINIAN_LAB_V7_{suffix.upper()}_CONTACT_SHEET.jpg",
    )


def create_contact_sheet(qa_rows: list[dict[str, str]], contact_sheet: Path) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    thumb_w, thumb_h = 220, 220
    label_h = 70
    cols = 4
    rows = max(1, math.ceil(len(qa_rows) / cols))
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
        small = ImageFont.truetype("arial.ttf", 12)
    except OSError:
        font = ImageFont.load_default()
        small = ImageFont.load_default()
    for idx, row in enumerate(qa_rows):
        path = Path(row["Image_Path"])
        x = (idx % cols) * thumb_w
        y = (idx // cols) * (thumb_h + label_h)
        with Image.open(path) as img:
            thumb = img.convert("RGB")
            thumb.thumbnail((thumb_w, thumb_h))
            px = x + (thumb_w - thumb.width) // 2
            py = y + (thumb_h - thumb.height) // 2
            sheet.paste(thumb, (px, py))
        status = row["Gate_Status"]
        color = {"PASS": (0, 120, 60), "REVIEW": (180, 110, 0), "HOLD": (170, 0, 0)}.get(status, (0, 0, 0))
        draw.rectangle((x, y + thumb_h, x + thumb_w, y + thumb_h + label_h), fill=(245, 245, 245))
        draw.text((x + 6, y + thumb_h + 6), f"{row['Internal_SKU']} {row['Image_Key']}", fill=(0, 0, 0), font=small)
        draw.text((x + 6, y + thumb_h + 24), f"{status} score={row['Score']}", fill=color, font=font)
        draw.text((x + 6, y + thumb_h + 44), row["Flags"][:42], fill=(80, 80, 80), font=small)
    sheet.save(contact_sheet, quality=92)


def run_qa(limit: int = 0, queue_path: Path = MJ_QUEUE) -> int:
    qa_csv, qa_md, contact_sheet = output_paths(queue_path)
    rows, fields = read_rows(queue_path)
    qa_rows: list[dict[str, str]] = []
    touched = 0
    for row in rows:
        if limit and touched >= limit:
            break
        if not needs_visual_qa(row):
            continue
        sku = clean(row.get("Internal_SKU"))
        pool_id = clean(row.get("Pool_ID"))
        candidates: list[tuple[str, ImageMetrics, str, list[str]]] = []
        for key in ["U1_File", "U2_File", "U3_File", "U4_File"]:
            path = image_path(row, key)
            if not path:
                continue
            metrics = metrics_for(path)
            status, flags = pool_gate(pool_id, metrics)
            candidates.append((key, metrics, status, flags))
            qa_rows.append(
                {
                    "Internal_SKU": sku,
                    "Pool_ID": pool_id,
                    "Image_Key": key,
                    "Image_Path": str(path),
                    "Width": str(metrics.width),
                    "Height": str(metrics.height),
                    "File_KB": str(metrics.file_kb),
                    "Brightness": f"{metrics.brightness:.2f}",
                    "Contrast": f"{metrics.contrast:.2f}",
                    "Saturation": f"{metrics.saturation:.2f}",
                    "Center_Whitespace": f"{metrics.center_whitespace:.3f}",
                    "Edge_Repeat_Delta": f"{metrics.edge_repeat_delta:.2f}",
                    "Score": f"{metrics.score:.2f}",
                    "Gate_Status": status,
                    "Flags": ";".join(flags),
                    "Checked_At_ET": now_text(),
                }
            )
        if candidates:
            candidates.sort(key=lambda item: (item[2] == "PASS", item[1].score), reverse=True)
            best_key, best_metrics, best_status, best_flags = candidates[0]
            row["Visual_QA_Status"] = f"{best_status}_BEST_{best_key}"
            row["Visual_QA_Best_File"] = str(best_metrics.path)
            row["Visual_QA_Flags"] = ";".join(best_flags)
            touched += 1
            print(f"[ETSY-V7-QA] {sku} best={best_key} status={best_status} flags={row['Visual_QA_Flags'] or 'none'}")
    for field in ["Visual_QA_Status", "Visual_QA_Best_File", "Visual_QA_Flags"]:
        if field not in fields:
            fields.append(field)
    write_rows(queue_path, rows, fields)

    if qa_rows:
        with qa_csv.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(qa_rows[0].keys()))
            writer.writeheader()
            writer.writerows(qa_rows)
        create_contact_sheet(qa_rows, contact_sheet)
    pass_count = sum(1 for row in rows if clean(row.get("Visual_QA_Status")).startswith("PASS"))
    review_count = sum(1 for row in rows if clean(row.get("Visual_QA_Status")).startswith("REVIEW"))
    hold_count = sum(1 for row in rows if clean(row.get("Visual_QA_Status")).startswith("HOLD"))
    lines = [
        "# Etsy Darwinian Lab V7 Visual QA",
        "",
        f"Generated: {now_text()} America/New_York",
        "",
        f"- SKUs checked: {touched}",
        f"- PASS best candidates: {pass_count}",
        f"- REVIEW best candidates: {review_count}",
        f"- HOLD best candidates: {hold_count}",
        f"- Queue: `{queue_path}`",
        f"- Contact sheet: `{contact_sheet}`",
        f"- QA CSV: `{qa_csv}`",
        "",
        "Policy: no Etsy listing fee is spent from this queue until image QA, metadata QA, fee guard, and duplicate checks pass.",
        "",
        "## Best Candidate Summary",
        "",
    ]
    for row in rows:
        if clean(row.get("Visual_QA_Status")):
            lines.append(f"- {row['Internal_SKU']} / {row['Pool_ID']}: {row.get('Visual_QA_Status')} | {row.get('Visual_QA_Flags') or 'no local metric flags'}")
    qa_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"[ETSY-V7-QA-DONE] checked={touched} pass={pass_count} review={review_count} hold={hold_count}")
    print(f"[ETSY-V7-QA] report={qa_md}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local visual QA for V7 Etsy samples")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--queue", default=str(MJ_QUEUE))
    args = parser.parse_args()
    return run_qa(limit=args.limit, queue_path=Path(args.queue))


if __name__ == "__main__":
    raise SystemExit(main())
