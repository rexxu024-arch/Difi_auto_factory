"""Build the smallest Adobe Stock first-submit pack from upload-ready assets.

This is intentionally conservative: one strong image per material family, with
the most visually competitive families first. It creates a folder and Adobe CSV
for the first real Contributor test after Rex logs in.
"""

from __future__ import annotations

import csv
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

from adobe_stock_isolation import assert_adobe_write_paths


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
FACTORY = PROJECT_ROOT / "adobe_stock_factory"
REVIEW = PROJECT_ROOT / "Review_Packets"
NY_TZ = ZoneInfo("America/New_York")

SOURCE_INDEX = DATABASE / "Adobe_Stock_Upload_Ready.csv"

PREFERRED_FAMILIES = [
    "Carbon Fiber",
    "Aged Bronze Patina",
    "Architectural Concrete",
    "Champagne Frosted Glass",
    "Smoky Jade",
    "Travertine Plaster",
    "Walnut Burl",
]

ADOBE_FIELDS = ["Filename", "Title", "Keywords", "Category", "Releases"]

TITLE_OVERRIDES = {
    "Carbon Fiber": "Carbon Fiber Texture Background for Branding and Product Design",
    "Aged Bronze Patina": "Aged Bronze Patina Texture Background for Luxury Design",
    "Architectural Concrete": "Architectural Concrete Texture Background for Modern Branding",
    "Champagne Frosted Glass": "Champagne Frosted Glass Texture Background for Luxury Design",
    "Smoky Jade": "Smoky Jade Stone Texture Background for Interior Design",
    "Travertine Plaster": "Travertine Plaster Texture Background for Interior Design",
    "Walnut Burl": "Walnut Burl Wood Texture Background for Premium Branding",
}


def now_slug() -> str:
    return datetime.now(NY_TZ).strftime("%Y%m%d")


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]], fields: list[str] | None = None) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = fields or list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def reset_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for child in path.iterdir():
        if child.is_file():
            child.unlink()


def load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def select_first_submit(rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    by_family: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        family = row.get("Family", "").strip()
        if family:
            by_family.setdefault(family, []).append(row)
    for family in PREFERRED_FAMILIES:
        bucket = by_family.get(family, [])
        if bucket:
            selected.append({**bucket[0], "First_Submit_Rank": str(len(selected) + 1)})
        if len(selected) >= limit:
            break
    if len(selected) < limit:
        used = {row.get("Filename", "") for row in selected}
        for row in rows:
            if row.get("Filename", "") in used:
                continue
            selected.append({**row, "First_Submit_Rank": str(len(selected) + 1)})
            if len(selected) >= limit:
                break
    return selected


def write_contact_sheet(rows: list[dict[str, str]], folder: Path, output: Path) -> None:
    if not rows:
        return
    thumb_w, thumb_h = 240, 240
    label_h = 66
    pad = 22
    cols = min(4, len(rows))
    rows_count = (len(rows) + cols - 1) // cols
    width = cols * thumb_w + (cols + 1) * pad
    height = rows_count * (thumb_h + label_h) + (rows_count + 1) * pad
    sheet = Image.new("RGB", (width, height), (246, 244, 238))
    draw = ImageDraw.Draw(sheet)
    title_font = load_font(18, bold=True)
    small_font = load_font(13)
    for idx, row in enumerate(rows):
        x = pad + (idx % cols) * (thumb_w + pad)
        y = pad + (idx // cols) * (thumb_h + label_h + pad)
        image_path = folder / row["Filename"]
        try:
            with Image.open(image_path) as image:
                image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                px = x + (thumb_w - image.width) // 2
                py = y + (thumb_h - image.height) // 2
                sheet.paste(image.convert("RGB"), (px, py))
        except Exception:
            draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline=(180, 80, 80), width=2)
        draw.text((x, y + thumb_h + 8), f"{row.get('First_Submit_Rank')}. {row.get('Family')}", fill=(28, 31, 35), font=title_font)
        draw.text((x, y + thumb_h + 32), row.get("Filename", ""), fill=(90, 94, 99), font=small_font)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def main() -> None:
    source_rows = read_rows(SOURCE_INDEX)
    selected = select_first_submit(source_rows, 7)
    slug = now_slug()
    folder = FACTORY / "upload_ready" / f"first_submit_{slug}"
    report = REVIEW / "Adobe_Stock_First_Submit_7_latest.md"
    index = DATABASE / "Adobe_Stock_First_Submit_7.csv"
    adobe_csv = folder / f"RexAdobe_FirstSubmit7_{slug}.csv"
    contact_sheet = folder / "ADOBE_FIRST_SUBMIT_7_CONTACT_SHEET.jpg"
    assert_adobe_write_paths((folder / "placeholder.txt", report, index, adobe_csv))
    reset_dir(folder)
    copied: list[dict[str, str]] = []
    for row in selected:
        src = PROJECT_ROOT / row.get("Local_Path", "")
        if not src.exists():
            continue
        dest = folder / row["Filename"]
        shutil.copy2(src, dest)
        family = row.get("Family", "")
        copied.append(
            {
                **row,
                "Title": TITLE_OVERRIDES.get(family, row.get("Title", "")),
                "Local_Path": str(dest.relative_to(PROJECT_ROOT)),
                "First_Submit_Status": "READY_LOGIN_REQUIRED",
            }
        )
    write_rows(index, copied)
    write_rows(adobe_csv, copied, ADOBE_FIELDS)
    write_contact_sheet(copied, folder, contact_sheet)
    lines = [
        "# Adobe Stock First Submit 7",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Files: {len(copied)}",
        f"- Folder: `{folder.relative_to(PROJECT_ROOT)}`",
        f"- Adobe CSV: `{adobe_csv.relative_to(PROJECT_ROOT)}`",
        f"- Contact sheet: `{contact_sheet.relative_to(PROJECT_ROOT)}`",
        "- Status: ready after Adobe Contributor login in dedicated Edge profile.",
        "",
        "## Selection Logic",
        "",
        "One strong image per premium material family, prioritized for visual competitiveness and low similar-content risk.",
        "",
        "## Submit Order",
        "",
    ]
    for row in copied:
        lines.append(f"{row.get('First_Submit_Rank')}. `{row['Filename']}` - {row.get('Family')} - {row.get('Title')}")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"[ADOBE-FIRST-SUBMIT-7] files={len(copied)} folder={folder.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
