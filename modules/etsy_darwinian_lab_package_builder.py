"""Build no-fee Etsy digital packages for V7 Darwinian Lab candidates."""

from __future__ import annotations

import argparse
import csv
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATABASE = ROOT / "Database"
REVIEW = ROOT / "Review_Packets"
PACKET_CSV = DATABASE / "Etsy_Darwinian_Lab_V7_Listing_Packet.csv"
UPLOAD_QUEUE = DATABASE / "Etsy_Darwinian_Lab_V7_Upload_Queue.csv"
GRAY_QUEUE = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
PACKAGE_HOLDS = DATABASE / "Etsy_Darwinian_Lab_V7_Package_Holds.csv"
REPORT = REVIEW / "ETSY_DARWINIAN_LAB_V7_UPLOAD_PACKET.md"
PACKAGE_ROOT = ROOT / "Output" / "Etsy" / "Darwinian_Lab" / "V7" / "_packages"
NY_TZ = ZoneInfo("America/New_York")

ALLOWED_READINESS = {"READY_FOR_METADATA_QA", "READY_AFTER_UPSCALE_REVIEW"}


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %z")


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def abs_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path


def font(size: int):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def wrapped(draw: ImageDraw.ImageDraw, text: str, width: int, font_obj) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if draw.textbbox((0, 0), test, font=font_obj)[2] <= width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:4]


def build_preview(row: dict[str, str], source: Path, out_dir: Path) -> Path:
    preview = out_dir / f"{row['Internal_SKU']}_etsy_preview.jpg"
    canvas = Image.new("RGB", (2000, 2000), (245, 242, 235))
    with Image.open(source) as img:
        art = img.convert("RGB")
        art.thumbnail((1580, 1360))
        x = (2000 - art.width) // 2
        y = 160
        canvas.paste(art, (x, y))
    draw = ImageDraw.Draw(canvas)
    title_font = font(58)
    small_font = font(34)
    title = clean(row.get("Etsy_Title"))
    for i, line in enumerate(wrapped(draw, title, 1720, title_font)):
        draw.text((140, 1580 + i * 68), line, fill=(30, 30, 30), font=title_font)
    draw.text((140, 1880), "Digital download preview - files included after purchase", fill=(90, 85, 75), font=small_font)
    canvas.save(preview, quality=92)
    return preview


def build_readme(row: dict[str, str], out_dir: Path) -> Path:
    readme = out_dir / "README_OpenClaw.txt"
    content = dedent(
        f"""
        OpenClaw Digital Download
        SKU: {row['Internal_SKU']}
        Pool: {row['Pool_ID']} / {row['Pool_Name']}
        Format: {row['Format']}

        Usage:
        - Personal use and small handmade/craft use are allowed.
        - Do not resell, redistribute, or upload the raw file as a competing digital product.
        - Colors may vary by monitor, printer, paper, and production workflow.

        AI disclosure:
        This asset may use AI-assisted artwork, then human/API curation, formatting, and quality checks.

        Prepared: {now_text()} America/New_York
        """
    ).strip()
    readme.write_text(content + "\n", encoding="utf-8")
    return readme


def build_zip(row: dict[str, str], source: Path, readme: Path, out_dir: Path) -> Path:
    zip_path = out_dir / f"{row['Internal_SKU']}_digital_download.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(source, arcname=f"{row['Internal_SKU']}_artwork{source.suffix.lower()}")
        archive.write(readme, arcname=readme.name)
    return zip_path


def build(limit: int = 0) -> int:
    rows, _ = read_csv(PACKET_CSV)
    gray_rows, _ = read_csv(GRAY_QUEUE)
    already_queued = {
        clean(row.get("ID"))
        for row in gray_rows
        if clean(row.get("ID")).startswith("OC-ETSY-")
    }
    upload_rows: list[dict[str, str]] = []
    hold_rows: list[dict[str, str]] = []
    eligible_count = 0
    already_queued_count = 0
    missing_source_count = 0
    for row in rows:
        if limit and len(upload_rows) >= limit:
            break
        if clean(row.get("Launch_Readiness")) not in ALLOWED_READINESS:
            continue
        eligible_count += 1
        sku = clean(row.get("Internal_SKU"))
        if sku in already_queued:
            already_queued_count += 1
            continue
        source = abs_path(clean(row.get("Production_File")))
        if not source.exists():
            missing_source_count += 1
            continue
        out_dir = PACKAGE_ROOT / sku
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            preview = build_preview(row, source, out_dir)
            readme = build_readme(row, out_dir)
            zip_path = build_zip(row, source, readme, out_dir)
        except (OSError, ValueError) as exc:
            hold_rows.append(
                {
                    "Timestamp": now_text(),
                    "Internal_SKU": sku,
                    "Package_Status": "HOLD_PACKAGE_IMAGE_ERROR",
                    "Production_File": str(source),
                    "Error": f"{type(exc).__name__}: {clean(exc)[:300]}",
                    "Next_Action": "Regenerate or reharvest source image before Etsy packaging; do not publish this row.",
                }
            )
            continue
        upload_rows.append(
            {
                **row,
                "Preview_Image": str(preview),
                "Digital_Zip": str(zip_path),
                "Package_Status": "READY_FOR_SPOTCHECK_NO_FEE_SPENT",
                "Fee_Risk_Status": "NOT_PUBLISHED_FEE_GUARD_REQUIRED",
                "Packaged_At_ET": now_text(),
            }
        )
    fields = list(upload_rows[0].keys()) if upload_rows else ["Internal_SKU", "Package_Status"]
    write_csv(UPLOAD_QUEUE, upload_rows, fields)
    if hold_rows:
        write_csv(PACKAGE_HOLDS, hold_rows, list(hold_rows[0].keys()))
    lines = [
        "# Etsy Darwinian Lab V7 Upload Packet",
        "",
        f"Generated: {now_text()} America/New_York",
        "",
        "No Etsy fees spent. These are package-ready candidates only.",
        "",
        f"- Eligible ready candidates found: {eligible_count}",
        f"- Already in gray launch queue: {already_queued_count}",
        f"- Missing source files: {missing_source_count}",
        f"- Package-ready candidates: {len(upload_rows)}",
        f"- Package holds: {len(hold_rows)}",
        "",
    ]
    for row in upload_rows:
        lines.append(f"## {row['Internal_SKU']} - {row['Pool_Name']}")
        lines.append(f"- Readiness: {row['Launch_Readiness']}")
        lines.append(f"- Price: ${row['Price_USD']}")
        lines.append(f"- Preview: `{row['Preview_Image']}`")
        lines.append(f"- Download ZIP: `{row['Digital_Zip']}`")
        lines.append(f"- Title: {row['Etsy_Title']}")
        lines.append("")
    if hold_rows:
        lines.append("## Package Holds")
        for row in hold_rows:
            lines.append(f"- {row['Internal_SKU']}: {row['Error']}")
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[ETSY-V7-PACKAGE] eligible={eligible_count} already_queued={already_queued_count} missing_source={missing_source_count}")
    print(f"[ETSY-V7-PACKAGE] ready={len(upload_rows)} csv={UPLOAD_QUEUE}")
    print(f"[ETSY-V7-PACKAGE] holds={len(hold_rows)} csv={PACKAGE_HOLDS if hold_rows else ''}")
    print(f"[ETSY-V7-PACKAGE] report={REPORT}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build V7 Etsy upload package candidates")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    return build(args.limit)


if __name__ == "__main__":
    raise SystemExit(main())
