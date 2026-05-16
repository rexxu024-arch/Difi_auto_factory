"""Create a small human-curated Adobe Stock first-submit pack.

The broader upload-ready pack proves throughput. This curated pack is for the
first real Contributor test: fewer files, more visual diversity, less similar
content risk.
"""

from __future__ import annotations

import argparse
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
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

SOURCE_INDEX = DATABASE / "Adobe_Stock_Upload_Ready.csv"
CURATED_INDEX = DATABASE / "Adobe_Stock_Curated_Pilot.csv"
CURATED_CSV = FACTORY / "upload_ready" / "RexAdobe_CuratedPilot_20260516.csv"
CURATED_REPORT = REVIEW / "Adobe_Stock_Curated_Pilot_latest.md"

ADOBE_FIELDS = ["Filename", "Title", "Keywords", "Category", "Releases"]

FAMILY_LABELS = [
    "aged bronze patina",
    "architectural concrete",
    "archival vellum",
    "brushed titanium",
    "carbon fiber",
    "champagne frosted glass",
    "kintsugi marble",
    "linen canvas",
    "manhattan order",
    "nero marble",
    "obsidian glass",
    "smoky jade",
    "travertine plaster",
    "walnut burl",
]

PREFERRED_FILES = {
    "aged bronze patina": ["ad_abp_0038.jpg", "ad_abp_0010.jpg"],
    "architectural concrete": ["ad_ac_0026.jpg", "ad_ac_0040.jpg"],
    "archival vellum": ["ad_av_0033.jpg", "ad_av_0005.jpg"],
    "brushed titanium": ["ad_bt_0004.jpg", "ad_bt_0032.jpg"],
    "carbon fiber": ["ad_cf_0027.jpg", "ad_cf_0041.jpg"],
    "champagne frosted glass": ["ad_cfg_0014.jpg", "ad_cfg_0028.jpg"],
    "kintsugi marble": ["ad_km_0017.jpg", "ad_km_0031.jpg"],
    "linen canvas": ["ad_lc_0011.jpg", "ad_lc_0025.jpg"],
    "manhattan order": ["ad_mo_0015.jpg", "ad_mo_0001.jpg"],
    "nero marble": ["ad_nm_0021.jpg", "ad_nm_0035.jpg"],
    "obsidian glass": ["ad_og_0006.jpg", "ad_og_0024.jpg"],
    "smoky jade": ["ad_sj_0016.jpg", "ad_sj_0030.jpg"],
    "travertine plaster": ["ad_tp_0008.jpg", "ad_tp_0036.jpg"],
    "walnut burl": ["ad_wb_0037.jpg", "ad_wb_0009.jpg"],
}

STRICT_PREMIUM_FILES = [
    "ad_cf_0027.jpg",
    "ad_cfg_0014.jpg",
    "ad_km_0017.jpg",
    "ad_mo_0015.jpg",
    "ad_nm_0021.jpg",
    "ad_og_0006.jpg",
    "ad_sj_0016.jpg",
    "ad_tp_0008.jpg",
    "ad_wb_0037.jpg",
    "ad_abp_0038.jpg",
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def today_slug() -> str:
    return datetime.now(NY_TZ).strftime("%Y%m%d")


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


def row_family(row: dict[str, str]) -> str:
    text = f"{row.get('Title', '')} {row.get('Keywords', '')}".lower()
    for family in FAMILY_LABELS:
        if all(piece in text for piece in family.split()[:2]):
            return family
    return ""


def select_rows(rows: list[dict[str, str]], limit: int, profile: str) -> list[dict[str, str]]:
    by_file = {row.get("Filename", ""): row for row in rows}
    selected: list[dict[str, str]] = []
    used: set[str] = set()
    if profile == "strict-premium":
        for filename in STRICT_PREMIUM_FILES:
            row = by_file.get(filename)
            if not row or filename in used:
                continue
            selected.append(
                {
                    **row,
                    "Curated_Family": row_family(row),
                    "Curated_Reason": "strict_premium_first_submit",
                }
            )
            used.add(filename)
            if limit and len(selected) >= limit:
                return selected[:limit]
        # Current upload-ready packs may contain only a few families (for example
        # kintsugi / Manhattan order / smoky jade). Fall back with a round-robin
        # family fill so the strict pack still reaches the requested count
        # without submitting ten near-identical images from one family.
        groups: dict[str, list[dict[str, str]]] = {}
        for row in rows:
            filename = row.get("Filename", "")
            family = row_family(row)
            if filename in used or not family:
                continue
            groups.setdefault(family, []).append(row)
        while groups and (not limit or len(selected) < limit):
            progressed = False
            for family in sorted(groups):
                if limit and len(selected) >= limit:
                    break
                bucket = groups[family]
                while bucket and bucket[0].get("Filename", "") in used:
                    bucket.pop(0)
                if not bucket:
                    continue
                row = bucket.pop(0)
                filename = row.get("Filename", "")
                selected.append(
                    {
                        **row,
                        "Curated_Family": family,
                        "Curated_Reason": "strict_premium_round_robin_fill",
                    }
                )
                used.add(filename)
                progressed = True
            if not progressed:
                break
        return selected[:limit] if limit else selected
    for family in FAMILY_LABELS:
        for filename in PREFERRED_FILES.get(family, []):
            row = by_file.get(filename)
            if row and filename not in used:
                selected.append({**row, "Curated_Family": family, "Curated_Reason": "manual_family_best_of_batch"})
                used.add(filename)
                break
        if limit and len(selected) >= limit:
            return selected[:limit]
    for row in rows:
        filename = row.get("Filename", "")
        if filename in used:
            continue
        family = row_family(row)
        if family and family not in {item.get("Curated_Family") for item in selected}:
            selected.append({**row, "Curated_Family": family, "Curated_Reason": "auto_diversity_fill"})
            used.add(filename)
        if limit and len(selected) >= limit:
            break
    return selected[:limit] if limit else selected


def build(limit: int, profile: str) -> tuple[list[dict[str, str]], Path, Path, Path, Path]:
    suffix = "" if profile == "broad" else f"_{profile.replace('-', '_')}"
    curated_index = DATABASE / f"Adobe_Stock_Curated_Pilot{suffix}.csv"
    curated_csv = FACTORY / "upload_ready" / f"RexAdobe_CuratedPilot_{today_slug()}{suffix}.csv"
    curated_report = REVIEW / f"Adobe_Stock_Curated_Pilot{suffix}_latest.md"
    assert_adobe_write_paths((curated_index, curated_csv, curated_report))
    source_rows = read_rows(SOURCE_INDEX)
    out_dir = FACTORY / "upload_ready" / f"curated_pilot_{today_slug()}{suffix}"
    assert_adobe_write_paths((out_dir / "placeholder.txt",))
    reset_dir(out_dir)
    selected = select_rows(source_rows, limit, profile)
    curated: list[dict[str, str]] = []
    for row in selected:
        src = PROJECT_ROOT / row.get("Local_Path", "")
        if not src.exists():
            continue
        dest = out_dir / row["Filename"]
        shutil.copy2(src, dest)
        curated.append({**row, "Local_Path": str(dest.relative_to(PROJECT_ROOT))})
    return curated, out_dir, curated_index, curated_csv, curated_report


def write_report(rows: list[dict[str, str]], out_dir: Path, curated_csv: Path, curated_report: Path) -> None:
    contact_sheet = out_dir / "ADOBE_CURATED_PILOT_CONTACT_SHEET.jpg"
    lines = [
        "# Adobe Stock Curated Pilot",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Curated files: {len(rows)}",
        f"- Folder: `{out_dir.relative_to(PROJECT_ROOT)}`",
        f"- Adobe CSV: `{curated_csv.relative_to(PROJECT_ROOT)}`",
        f"- Contact sheet: `{contact_sheet.relative_to(PROJECT_ROOT)}`",
        "",
        "## Reason",
        "",
        "This is the first-submit candidate pack. It is intentionally smaller than the throughput pack to reduce similar-content rejection risk.",
        "",
        "## Files",
        "",
    ]
    for row in rows:
        lines.append(f"- {row['Filename']} | {row.get('Curated_Family', '')} | {row['Title']}")
    curated_report.parent.mkdir(parents=True, exist_ok=True)
    curated_report.write_text("\n".join(lines), encoding="utf-8")


def load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def wrap_text(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        probe = " ".join(current + [word])
        if len(probe) > width and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines[:3]


def write_contact_sheet(rows: list[dict[str, str]], out_dir: Path) -> Path:
    """Build a compact human QA sheet for the exact files copied to the pack."""
    contact_path = out_dir / "ADOBE_CURATED_PILOT_CONTACT_SHEET.jpg"
    assert_adobe_write_paths((contact_path,))
    if not rows:
        return contact_path

    cols = 5 if len(rows) > 6 else 3
    thumb_w, thumb_h = 300, 220
    label_h = 104
    pad = 16
    header_h = 74
    sheet_rows = (len(rows) + cols - 1) // cols
    width = pad + cols * (thumb_w + pad)
    height = header_h + pad + sheet_rows * (thumb_h + label_h + pad)
    canvas = Image.new("RGB", (width, height), (245, 243, 237))
    draw = ImageDraw.Draw(canvas)
    title_font = load_font(24, bold=True)
    label_font = load_font(13)
    small_font = load_font(11)

    draw.rectangle((0, 0, width, header_h), fill=(28, 29, 31))
    draw.text((pad, 18), "Adobe Stock First Submit - Curated Pilot QA", fill=(242, 238, 226), font=title_font)
    draw.text((pad, 46), f"{len(rows)} files | no upload/spend | AI disclosure required in Adobe portal", fill=(184, 204, 214), font=small_font)

    for index, row in enumerate(rows):
        col = index % cols
        row_index = index // cols
        x = pad + col * (thumb_w + pad)
        y = header_h + pad + row_index * (thumb_h + label_h + pad)
        image_path = PROJECT_ROOT / row.get("Local_Path", "")
        draw.rounded_rectangle((x, y, x + thumb_w, y + thumb_h + label_h), radius=10, fill=(255, 255, 255), outline=(204, 198, 184), width=1)
        try:
            with Image.open(image_path) as image:
                work = image.convert("RGB")
                work.thumbnail((thumb_w - 18, thumb_h - 18), Image.Resampling.LANCZOS)
                ix = x + (thumb_w - work.width) // 2
                iy = y + 9 + (thumb_h - 18 - work.height) // 2
                canvas.paste(work, (ix, iy))
        except Exception as exc:
            draw.text((x + 14, y + 24), f"IMAGE ERROR: {exc}", fill=(146, 38, 38), font=label_font)

        label_y = y + thumb_h + 8
        draw.text((x + 10, label_y), f"{index + 1:02d} {row.get('Filename', '')}", fill=(20, 24, 28), font=label_font)
        for line_no, line in enumerate(wrap_text(row.get("Title", ""), 38)):
            draw.text((x + 10, label_y + 22 + line_no * 17), line, fill=(54, 56, 58), font=small_font)
        family = row.get("Curated_Family", "")
        if family:
            draw.text((x + 10, label_y + 76), family, fill=(94, 98, 103), font=small_font)

    canvas.save(contact_path, quality=88, optimize=True)
    return contact_path


def append_progress(rows: list[dict[str, str]], out_dir: Path) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock curated first-submit pack built; files={len(rows)}; "
            f"folder={out_dir.relative_to(PROJECT_ROOT)}; no upload/spend.\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=14)
    parser.add_argument("--profile", choices=["broad", "strict-premium"], default="broad")
    args = parser.parse_args()
    rows, out_dir, curated_index, curated_csv, curated_report = build(args.limit, args.profile)
    write_rows(curated_index, rows)
    write_rows(curated_csv, rows, ADOBE_FIELDS)
    write_contact_sheet(rows, out_dir)
    write_report(rows, out_dir, curated_csv, curated_report)
    append_progress(rows, out_dir)
    print(f"[ADOBE-CURATED-PILOT] files={len(rows)} folder={out_dir}")


if __name__ == "__main__":
    main()
