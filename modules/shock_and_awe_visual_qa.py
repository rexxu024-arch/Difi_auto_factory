"""Local visual QA for Shock & Awe private-showcase MJ outputs.

This is a no-spend, local-only gate. It scores U1-U4, picks the strongest
candidate for each SKU, and builds a contact sheet before Printify private draft
creation.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont, ImageStat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATABASE = ROOT / "Database"
REVIEW = ROOT / "Review_Packets"
DEFAULT_QUEUE = DATABASE / "Shock_And_Awe_V5_Zones1_3_MJ_Dispatch_Queue.csv"
DEFAULT_QA_CSV = DATABASE / "Shock_And_Awe_V5_Zones1_3_Visual_QA.csv"
DEFAULT_QA_MD = REVIEW / "OPERATION_SHOCK_AND_AWE_V5_ZONES1_3_VISUAL_QA.md"
DEFAULT_CONTACT = REVIEW / "OPERATION_SHOCK_AND_AWE_V5_ZONES1_3_CONTACT_SHEET.jpg"
NY_TZ = ZoneInfo("America/New_York")


@dataclass
class Metrics:
    path: Path
    width: int
    height: int
    file_kb: int
    brightness: float
    contrast: float
    saturation: float
    score: float
    flags: list[str]


def clean(value: object) -> str:
    return str(value or "").strip()


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def write_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def resolve_path(value: str) -> Path | None:
    raw = clean(value)
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    return path if path.exists() else None


def product_min_dim(row: dict[str, str]) -> int:
    product = clean(row.get("Product_Type")).lower()
    prompt = clean(row.get("MJ_Master_Prompt")).lower()
    if product == "mug" or "--ar 2:1" in prompt:
        return 700
    if product in {"phone case", "notebook"}:
        return 900
    return 1000


def metrics_for(path: Path) -> Metrics:
    with Image.open(path) as img:
        width, height = img.size
        work = img.convert("RGB")
        work.thumbnail((420, 420))
        gray = work.convert("L")
        gray_stat = ImageStat.Stat(gray)
        hsv_stat = ImageStat.Stat(work.convert("HSV"))
        brightness = float(gray_stat.mean[0])
        contrast = float(gray_stat.stddev[0])
        saturation = float(hsv_stat.mean[1])
    flags: list[str] = []
    if path.stat().st_size < 450_000:
        flags.append("SMALL_FILE")
    if brightness < 24:
        flags.append("SHADOW_CLIPPING")
    if contrast < 20:
        flags.append("LOW_CONTRAST")
    score = contrast + min(saturation, 110) * 0.12 + min(brightness, 180) * 0.035
    score -= len(flags) * 18
    return Metrics(
        path=path,
        width=width,
        height=height,
        file_kb=max(1, path.stat().st_size // 1024),
        brightness=brightness,
        contrast=contrast,
        saturation=saturation,
        score=score,
        flags=flags,
    )


def gate_for(row: dict[str, str], metrics: Metrics) -> tuple[str, list[str]]:
    flags = list(metrics.flags)
    min_dim = product_min_dim(row)
    short_edge = min(metrics.width, metrics.height)
    if short_edge < 640:
        flags.append("LOW_RESOLUTION_HARD_FAIL")
    elif short_edge < min_dim:
        flags.append("UPSCALE_NEEDED")
    prompt = clean(row.get("MJ_Master_Prompt")).lower()
    if "--ar 2:1" in prompt and metrics.width <= metrics.height:
        flags.append("PANORAMIC_EXPECTED")
    if "--ar 5:7" in prompt and metrics.height <= metrics.width:
        flags.append("VERTICAL_EXPECTED")
    if "LOW_RESOLUTION_HARD_FAIL" in flags or "SHADOW_CLIPPING" in flags:
        return "HOLD", flags
    if flags:
        return "REVIEW", flags
    return "PASS", flags


def create_contact_sheet(qa_rows: list[dict[str, str]], contact_path: Path) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    cols = 4
    thumb_w, thumb_h, label_h = 250, 250, 82
    rows = max(1, math.ceil(len(qa_rows) / cols))
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 13)
        small = ImageFont.truetype("arial.ttf", 11)
    except OSError:
        font = ImageFont.load_default()
        small = ImageFont.load_default()
    colors = {"PASS": (0, 120, 60), "REVIEW": (180, 110, 0), "HOLD": (170, 0, 0)}
    for idx, row in enumerate(qa_rows):
        x = (idx % cols) * thumb_w
        y = (idx // cols) * (thumb_h + label_h)
        with Image.open(row["Image_Path"]) as img:
            thumb = img.convert("RGB")
            thumb.thumbnail((thumb_w, thumb_h))
            sheet.paste(thumb, (x + (thumb_w - thumb.width) // 2, y + (thumb_h - thumb.height) // 2))
        draw.rectangle((x, y + thumb_h, x + thumb_w, y + thumb_h + label_h), fill=(245, 245, 245))
        draw.text((x + 6, y + thumb_h + 5), f"{row['Internal_SKU']} {row['Image_Key']}", fill=(0, 0, 0), font=small)
        draw.text((x + 6, y + thumb_h + 23), f"{row['Gate_Status']} score={row['Score']}", fill=colors.get(row["Gate_Status"], (0, 0, 0)), font=font)
        draw.text((x + 6, y + thumb_h + 43), clean(row.get("Concept_Name"))[:34], fill=(55, 55, 55), font=small)
        draw.text((x + 6, y + thumb_h + 60), clean(row.get("Flags"))[:46], fill=(90, 90, 90), font=small)
    sheet.save(contact_path, quality=92)


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def run(queue: Path, limit: int, qa_csv: Path, qa_md: Path, contact: Path, force: bool = False) -> int:
    if not queue.is_absolute():
        queue = ROOT / queue
    if not qa_csv.is_absolute():
        qa_csv = ROOT / qa_csv
    if not qa_md.is_absolute():
        qa_md = ROOT / qa_md
    if not contact.is_absolute():
        contact = ROOT / contact
    rows, fields = read_rows(queue)
    for field in ["Visual_QA_Status", "Visual_QA_Best_File", "Visual_QA_Flags", "Visual_QA_At_ET"]:
        if field not in fields:
            fields.append(field)
    qa_rows: list[dict[str, str]] = []
    touched = 0
    for row in rows:
        if limit and touched >= limit:
            break
        if clean(row.get("Harvest_Status")) != "READY_FOR_VISUAL_QA":
            continue
        if not force and clean(row.get("Visual_QA_Status")) and clean(row.get("Visual_QA_Status")) != "PENDING_IMAGE_GENERATION":
            continue
        options: list[tuple[str, Metrics, str, list[str]]] = []
        for key in ["U1_File", "U2_File", "U3_File", "U4_File"]:
            path = resolve_path(row.get(key, ""))
            if not path:
                continue
            m = metrics_for(path)
            status, flags = gate_for(row, m)
            qa_rows.append(
                {
                    "Checked_At_ET": datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %z"),
                    "Internal_SKU": clean(row.get("Internal_SKU")),
                    "Concept_Name": clean(row.get("Concept_Name")),
                    "Product_Type": clean(row.get("Product_Type")),
                    "Image_Key": key.replace("_File", ""),
                    "Image_Path": str(path),
                    "Width": str(m.width),
                    "Height": str(m.height),
                    "KB": str(m.file_kb),
                    "Brightness": f"{m.brightness:.1f}",
                    "Contrast": f"{m.contrast:.1f}",
                    "Saturation": f"{m.saturation:.1f}",
                    "Score": f"{m.score:.1f}",
                    "Gate_Status": status,
                    "Flags": ";".join(flags),
                }
            )
            options.append((key, m, status, flags))
        if not options:
            row["Visual_QA_Status"] = "HOLD_NO_U_IMAGES"
            row["Visual_QA_Flags"] = "NO_U_IMAGES"
        else:
            options.sort(key=lambda item: (item[2] == "PASS", item[2] == "REVIEW", item[1].score), reverse=True)
            best_key, best_metrics, best_status, best_flags = options[0]
            row["Visual_QA_Status"] = f"{best_status}_BEST_{best_key.replace('_File', '')}"
            row["Visual_QA_Best_File"] = str(best_metrics.path.relative_to(ROOT))
            row["Visual_QA_Flags"] = ";".join(best_flags)
        row["Visual_QA_At_ET"] = datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %z")
        touched += 1
        print(f"[SHOCK-QA] {row.get('Internal_SKU')} {row['Visual_QA_Status']} {row.get('Visual_QA_Flags') or 'none'}")
        write_rows(queue, rows, fields)
    if qa_rows:
        qa_fields = list(qa_rows[0].keys())
        with qa_csv.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=qa_fields)
            writer.writeheader()
            writer.writerows(qa_rows)
        create_contact_sheet(qa_rows, contact)
    pass_count = sum(1 for row in rows if clean(row.get("Visual_QA_Status")).startswith("PASS"))
    review_count = sum(1 for row in rows if clean(row.get("Visual_QA_Status")).startswith("REVIEW"))
    hold_count = sum(1 for row in rows if clean(row.get("Visual_QA_Status")).startswith("HOLD"))
    lines = [
        "# Shock & Awe V5 Zones 1/3 Visual QA",
        "",
        f"Updated: {datetime.now(NY_TZ).strftime('%Y-%m-%d %H:%M:%S %z')}",
        f"Queue: `{rel(queue)}`",
        f"Summary: PASS={pass_count}, REVIEW={review_count}, HOLD={hold_count}",
        f"Contact sheet: `{rel(contact)}`",
        "",
    ]
    for row in rows:
        status = clean(row.get("Visual_QA_Status"))
        if status:
            lines.append(f"- {row['Internal_SKU']} / {row.get('Concept_Name')}: {status} | {row.get('Visual_QA_Flags') or 'no flags'}")
    qa_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[SHOCK-QA-DONE] touched={touched} pass={pass_count} review={review_count} hold={hold_count}")
    print(f"[SHOCK-QA-CONTACT] {contact}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Shock & Awe private-showcase visual QA")
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE))
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--qa-csv", default=str(DEFAULT_QA_CSV))
    parser.add_argument("--qa-md", default=str(DEFAULT_QA_MD))
    parser.add_argument("--contact", default=str(DEFAULT_CONTACT))
    parser.add_argument("--force", action="store_true", help="Re-run QA even when rows already have a QA decision")
    args = parser.parse_args()
    return run(
        Path(args.queue),
        max(0, args.limit),
        Path(args.qa_csv),
        Path(args.qa_md),
        Path(args.contact),
        args.force,
    )


if __name__ == "__main__":
    raise SystemExit(main())
