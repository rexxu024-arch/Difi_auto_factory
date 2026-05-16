"""Build an Adobe Stock upload-ready folder from QA-passed pilot rows."""

from __future__ import annotations

import argparse
import csv
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

from adobe_stock_isolation import assert_adobe_write_paths
from adobe_stock_quality_policy import validate_adobe_production_image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
FACTORY = PROJECT_ROOT / "adobe_stock_factory"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

BATCH = DATABASE / "Adobe_Stock_Pilot_Batch.csv"
META_QA = DATABASE / "Adobe_Stock_Metadata_QA.csv"
OUT_INDEX = DATABASE / "Adobe_Stock_Upload_Ready.csv"
OUT_ADOBE_CSV = FACTORY / "upload_ready" / "RexAdobe_20260516.csv"
OUT_REPORT = REVIEW / "Adobe_Stock_Upload_Ready_latest.md"

FILENAME_FAMILY_PREFIXES = {
    "aged_bronze": "Aged Bronze Patina",
    "architectural": "Architectural Concrete",
    "archival": "Archival Vellum",
    "brushed": "Brushed Titanium",
    "carbon_fiber": "Carbon Fiber",
    "champagne": "Champagne Frosted Glass",
    "kintsugi": "Kintsugi Marble",
    "linen_canvas": "Linen Canvas",
    "manhattan": "Manhattan Order",
    "manhatta": "Manhattan Order",
    "nero_marble": "Nero Marble",
    "obsidian": "Obsidian Glass",
    "smoky_jade": "Smoky Jade",
    "travertine": "Travertine Plaster",
    "walnut_burl": "Walnut Burl",
    "aged_bro": "Aged Bronze Patina",
    "abp": "Aged Bronze Patina",
    "architec": "Architectural Concrete",
    "ac": "Architectural Concrete",
    "carbon_f": "Carbon Fiber",
    "champagn": "Champagne Frosted Glass",
    "linen_ca": "Linen Canvas",
    "nero_mar": "Nero Marble",
    "traverti": "Travertine Plaster",
    "walnut_b": "Walnut Burl",
    "av": "Archival Vellum",
    "bt": "Brushed Titanium",
    "cf": "Carbon Fiber",
    "cfg": "Champagne Frosted Glass",
    "km": "Kintsugi Marble",
    "lc": "Linen Canvas",
    "mo": "Manhattan Order",
    "nm": "Nero Marble",
    "og": "Obsidian Glass",
    "sj": "Smoky Jade",
    "tp": "Travertine Plaster",
    "wb": "Walnut Burl",
}


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def today_slug() -> str:
    return datetime.now(NY_TZ).strftime("%Y%m%d")


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_adobe_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["Filename", "Title", "Keywords", "Category", "Releases"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def write_contact_sheet(rows: list[dict[str, str]], out_dir: Path) -> Path:
    contact_path = out_dir / "ADOBE_UPLOAD_READY_CONTACT_SHEET.jpg"
    if not rows:
        return contact_path
    thumb_w, thumb_h = 190, 190
    label_h = 58
    pad = 16
    cols = min(5, len(rows))
    rows_count = (len(rows) + cols - 1) // cols
    width = cols * thumb_w + (cols + 1) * pad
    height = rows_count * (thumb_h + label_h) + (rows_count + 1) * pad
    sheet = Image.new("RGB", (width, height), (244, 242, 236))
    draw = ImageDraw.Draw(sheet)
    title_font = load_font(14, bold=True)
    small_font = load_font(11)
    for idx, row in enumerate(rows):
        x = pad + (idx % cols) * (thumb_w + pad)
        y = pad + (idx // cols) * (thumb_h + label_h + pad)
        image_path = out_dir / row["Filename"]
        try:
            with Image.open(image_path) as image:
                image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                px = x + (thumb_w - image.width) // 2
                py = y + (thumb_h - image.height) // 2
                sheet.paste(image.convert("RGB"), (px, py))
        except Exception:
            draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline=(170, 70, 70), width=2)
        draw.text((x, y + thumb_h + 7), row.get("Family", "")[:24], fill=(28, 31, 35), font=title_font)
        draw.text((x, y + thumb_h + 28), row.get("Filename", "")[:30], fill=(90, 94, 99), font=small_font)
    sheet.save(contact_path, "JPEG", quality=92, optimize=True)
    return contact_path


def resolve_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def expected_family_from_filename(filename: str) -> str:
    stem = Path(filename).stem.lower()
    if stem.startswith("ad_"):
        stem = stem[3:]
    for prefix, family in sorted(FILENAME_FAMILY_PREFIXES.items(), key=lambda item: len(item[0]), reverse=True):
        if stem.startswith(prefix):
            return family
    return ""


def family_matches_source(row: dict[str, str]) -> tuple[bool, str]:
    source = row.get("Source_Path", "")
    if not source:
        return False, "missing source path"
    expected = expected_family_from_filename(resolve_path(source).name)
    actual = row.get("Family", "").strip()
    if not expected:
        return False, "unknown source filename family"
    if actual != expected:
        return False, f"family mismatch: csv={actual!r}, file={expected!r}"
    return True, ""


def meta_pass_ids() -> set[str]:
    passed: set[str] = set()
    for row in read_rows(META_QA):
        if row.get("QA_Status") != "METADATA_QA_PASS":
            continue
        source = row.get("Source_ID", "")
        if source:
            passed.add(source)
    return passed


def batch_row_passes(row: dict[str, str], passed_meta: set[str]) -> bool:
    ids = {row.get("Batch_ID", ""), row.get("Queue_ID", "")}
    if not ids & passed_meta:
        return False
    if not row.get("QA_Status", "").startswith("QA_PASS"):
        return False
    upload_status = row.get("Upload_Status", "").strip().upper()
    if upload_status.startswith("UPLOADED") or upload_status in {"SUBMITTED", "ADOBE_SUBMITTED"}:
        return False
    source = row.get("Source_Path", "")
    return bool(source and resolve_path(source).exists())


def reset_upload_dir(out_dir: Path) -> None:
    """Keep the upload folder physically equal to the current ready index."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for path in out_dir.iterdir():
        if path.is_file():
            path.unlink()


def build(limit: int, max_per_family: int) -> tuple[list[dict[str, str]], Path, list[dict[str, str]]]:
    assert_adobe_write_paths((OUT_INDEX, OUT_ADOBE_CSV, OUT_REPORT))
    passed_meta = meta_pass_ids()
    rows = read_rows(BATCH)
    out_dir = FACTORY / "upload_ready" / f"pilot_{today_slug()}"
    if not rows:
        return [], out_dir, []
    assert_adobe_write_paths((out_dir / "placeholder.txt",))
    reset_upload_dir(out_dir)

    ready: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    family_counts: dict[str, int] = {}
    for row in rows:
        if limit and len(ready) >= limit:
            break
        if not batch_row_passes(row, passed_meta):
            continue
        family_ok, family_reason = family_matches_source(row)
        if not family_ok:
            skipped.append(
                {
                    "Batch_ID": row.get("Batch_ID", ""),
                    "Queue_ID": row.get("Queue_ID", ""),
                    "Family": row.get("Family", ""),
                    "Source_Path": row.get("Source_Path", ""),
                    "Reason": family_reason,
                }
            )
            continue
        family = row.get("Family", "unknown").strip().lower() or "unknown"
        if max_per_family and family_counts.get(family, 0) >= max_per_family:
            continue
        source = resolve_path(row["Source_Path"])
        quality_ok, quality_status, quality_info = validate_adobe_production_image(source, row)
        if not quality_ok:
            skipped.append(
                {
                    "Batch_ID": row.get("Batch_ID", ""),
                    "Queue_ID": row.get("Queue_ID", ""),
                    "Family": row.get("Family", ""),
                    "Source_Path": row.get("Source_Path", ""),
                    "Reason": f"{quality_status}: {quality_info.get('Quality_Reasons', '')}".strip(),
                }
            )
            continue
        filename = source.name
        dest = out_dir / filename
        shutil.copy2(source, dest)
        ready.append(
            {
                "Filename": filename,
                "Title": row.get("Adobe_Title", ""),
                "Keywords": row.get("Adobe_Keywords", ""),
                "Category": row.get("Adobe_Category", "8"),
                "Releases": "",
                "Created_Using_AI": "true",
                "Family": row.get("Family", ""),
                "Local_Path": str(dest.relative_to(PROJECT_ROOT)),
                "Source_Batch_ID": row.get("Batch_ID", ""),
                "Status": "READY_FOR_ADOBE_CONTRIBUTOR_SMALL_PILOT_MACRO_UPSCALE_ONLY",
            }
        )
        family_counts[family] = family_counts.get(family, 0) + 1
    return ready, out_dir, skipped


def write_report(rows: list[dict[str, str]], out_dir: Path, skipped: list[dict[str, str]], contact_sheet: Path) -> None:
    lines = [
        "# Adobe Stock Upload Ready Pack",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Ready files: {len(rows)}",
        f"- Folder: `{out_dir.relative_to(PROJECT_ROOT)}`",
        f"- Contact sheet: `{contact_sheet.relative_to(PROJECT_ROOT)}`",
        f"- Internal metadata CSV: `{OUT_INDEX.relative_to(PROJECT_ROOT)}`",
        f"- Adobe upload CSV: `{OUT_ADOBE_CSV.relative_to(PROJECT_ROOT)}`",
        f"- Family/source mismatches skipped: {len(skipped)}",
        "",
        "## Upload Discipline",
        "",
        "- Start with a tiny diversified pilot, not the full batch, to avoid similar-content rejection.",
        "- Only use real MJ U-button / 2x-upscaled macro-photography production assets.",
        "- Never submit 1024 drafts, sliced grid quarters, or procedural flat texture placeholders.",
        "- In Adobe Contributor, mark each file as created using generative AI tools.",
        "- Submit only image QA pass + metadata QA pass rows.",
        "- If Adobe returns rejection reasons, feed them back before scaling to 50/day.",
        "",
        "## Files",
        "",
    ]
    lines.extend(f"- {row['Filename']}: {row['Title']}" for row in rows)
    if skipped:
        lines.extend(["", "## Skipped Family Mismatches", ""])
        for row in skipped:
            lines.append(
                f"- {row.get('Batch_ID') or row.get('Queue_ID')}: {row.get('Reason')} | "
                f"{row.get('Family')} | {row.get('Source_Path')}"
            )
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def append_progress(rows: list[dict[str, str]], out_dir: Path, skipped: list[dict[str, str]]) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock upload-ready pack built; files={len(rows)}; "
            f"family_mismatches_skipped={len(skipped)}; folder={out_dir.relative_to(PROJECT_ROOT)}; "
            "waiting Adobe Contributor pilot upload.\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--max-per-family", type=int, default=2)
    args = parser.parse_args()
    rows, out_dir, skipped = build(args.limit, args.max_per_family)
    write_rows(OUT_INDEX, rows)
    write_adobe_csv(OUT_ADOBE_CSV, rows)
    contact_sheet = write_contact_sheet(rows, out_dir)
    write_report(rows, out_dir, skipped, contact_sheet)
    append_progress(rows, out_dir, skipped)
    print(f"[ADOBE-UPLOAD-READY] files={len(rows)} family_mismatches_skipped={len(skipped)} folder={out_dir}")


if __name__ == "__main__":
    main()
