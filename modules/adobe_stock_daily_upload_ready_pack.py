"""Build a daily Adobe Stock upload/review pack from local 4MP candidates."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

from adobe_stock_isolation import assert_adobe_write_paths
from adobe_stock_theme_stats import candidate_has_mixup, load_theme_pressure


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
FACTORY = PROJECT_ROOT / "adobe_stock_factory"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

SOURCE = DATABASE / "Adobe_Stock_Local_Upscaled_Candidates.csv"
REX_QA = DATABASE / "Adobe_Stock_Rex_Visual_QA.csv"
OUT_INDEX = DATABASE / "Adobe_Stock_Daily_Upload_Ready.csv"
OUT_REPORT = REVIEW / "Adobe_Stock_Daily_Upload_Ready_latest.md"
SUBMISSION_LEDGER = DATABASE / "Adobe_Stock_Submission_Ledger.csv"
UPLOAD_READY_ROOT = FACTORY / "upload_ready"
BATCH_RE = re.compile(r"^batch_(?P<num>\d{3})(?:_|$)")
IMAGE_EXTS = {".jpg", ".jpeg", ".png"}
SKIP_IMAGE_NAMES = {"adobe_daily_upload_ready_contact_sheet.jpg"}


FIELDS = [
    "Filename",
    "Title",
    "Keywords",
    "Category",
    "Releases",
    "Created_Using_AI",
    "Family",
    "Parent_Asset_ID",
    "Source_Path",
    "Local_Path",
    "Status",
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def today_slug() -> str:
    return datetime.now(NY_TZ).strftime("%Y%m%d")


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\n", " ").replace("\r", " ").split()).strip()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def write_adobe_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["Filename", "Title", "Keywords", "Category", "Releases"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def resolve_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rex_decisions() -> dict[str, str]:
    return {
        clean(row.get("Parent_Asset_ID")): clean(row.get("Decision")).upper()
        for row in read_rows(REX_QA)
        if clean(row.get("Parent_Asset_ID"))
    }


def blocked_submitted_filenames() -> set[str]:
    blocked: set[str] = set()
    terminal_markers = ("ADOBE_SUBMITTED", "SUBMITTED", "UPLOADED")
    for row in read_rows(SUBMISSION_LEDGER):
        filename = clean(row.get("Filename")).lower()
        status = clean(row.get("Status")).upper()
        if filename and (status.startswith(terminal_markers) or "PENDING_HUMAN_VERIFICATION" in status):
            blocked.add(filename)
    return blocked


def load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    for path in (
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
    ):
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def reset_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for child in path.iterdir():
        if child.is_file():
            child.unlink()


def next_batch_slug() -> str:
    UPLOAD_READY_ROOT.mkdir(parents=True, exist_ok=True)
    max_seen = 0
    for folder in UPLOAD_READY_ROOT.glob("batch_*"):
        if not folder.is_dir():
            continue
        match = BATCH_RE.match(folder.name)
        if match:
            max_seen = max(max_seen, int(match.group("num")))
    return f"batch_{max_seen + 1:03d}"


def prepared_parent_ids() -> set[str]:
    """Block anything already placed into a previous 50-file batch folder."""
    blocked: set[str] = set()
    for manifest in UPLOAD_READY_ROOT.glob("batch_*/batch_manifest.csv"):
        for row in read_rows(manifest):
            parent = clean(row.get("Parent_Asset_ID"))
            if parent:
                blocked.add(parent)
    return blocked


def is_upload_image(path: Path) -> bool:
    if not path.is_file() or path.suffix.lower() not in IMAGE_EXTS:
        return False
    lower_name = path.name.lower()
    if lower_name in SKIP_IMAGE_NAMES or "contact_sheet" in lower_name:
        return False
    return True


def is_uploaded_file(path: Path) -> bool:
    return path.stem.lower().endswith("_uploaded")


def upload_images(folder: Path) -> list[Path]:
    return [path for path in sorted(folder.iterdir()) if is_upload_image(path)]


def batch_sort_key(folder: Path) -> tuple[int, str]:
    match = BATCH_RE.match(folder.name)
    return (int(match.group("num")) if match else 999999, folder.name)


def incomplete_batch_folders() -> list[Path]:
    folders: list[Path] = []
    for folder in sorted(UPLOAD_READY_ROOT.glob("batch_*"), key=batch_sort_key):
        if not folder.is_dir() or folder.name.endswith("_completed"):
            continue
        manifest = folder / "batch_manifest.csv"
        images = upload_images(folder)
        if not manifest.exists() or not images:
            continue
        if any(not is_uploaded_file(path) for path in images):
            folders.append(folder)
    return folders


def reconcile_existing_rows(folder: Path, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Keep manifest rows aligned with file-level `_uploaded` resume markers."""
    by_name = {path.name: path for path in upload_images(folder)}
    by_unuploaded_name = {
        path.name.replace("_uploaded", ""): path
        for path in upload_images(folder)
        if is_uploaded_file(path)
    }
    reconciled: list[dict[str, str]] = []
    for row in rows:
        filename = clean(row.get("Filename"))
        if not filename:
            continue
        path = by_name.get(filename) or by_unuploaded_name.get(filename)
        if path:
            row = dict(row)
            row["Filename"] = path.name
            row["Local_Path"] = str(path.relative_to(PROJECT_ROOT))
            if is_uploaded_file(path):
                row["Status"] = "UPLOADED_CONFIRMED_BY_REX"
        reconciled.append(row)
    return reconciled


def resume_existing_batch() -> tuple[list[dict[str, str]], Path, Path] | None:
    folders = incomplete_batch_folders()
    if not folders:
        return None
    folder = folders[0]
    manifest = folder / "batch_manifest.csv"
    rows = reconcile_existing_rows(folder, read_rows(manifest))
    if rows:
        write_rows(manifest, rows)
    adobe_csvs = sorted(folder.glob("RexAdobe_*.csv"))
    adobe_csv = adobe_csvs[0] if adobe_csvs else folder / f"RexAdobe_{folder.name}.csv"
    write_rows(OUT_INDEX, rows)
    write_adobe_csv(adobe_csv, rows)
    contact = folder / "ADOBE_DAILY_UPLOAD_READY_CONTACT_SHEET.jpg"
    if not contact.exists():
        contact = write_contact_sheet(rows, folder)
    write_report(rows, folder, adobe_csv, contact, manifest)
    append_progress(rows, folder)
    remaining = sum(1 for path in upload_images(folder) if not is_uploaded_file(path))
    print(f"[ADOBE-DAILY-UPLOAD-READY] resume_existing files={len(rows)} remaining={remaining} folder={folder}")
    return rows, folder, contact


def safe_filename(batch_slug: str, item_number: int, source: Path) -> str:
    """Use neutral batch-local names; source dates stay only in the manifest."""
    stem = batch_slug.replace("_", "-")
    return f"{stem}-{item_number:03d}{source.suffix.lower() or '.jpg'}"


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return cleaned[:32] or "materials"


def folder_theme(rows: list[dict[str, str]]) -> str:
    counts = Counter(clean(row.get("Family")) or "Unknown" for row in rows)
    if not counts:
        return "empty"
    top = counts.most_common(3)
    if top[0][1] >= max(12, int(len(rows) * 0.55)):
        return slugify(top[0][0])
    return slugify("_".join(family for family, _count in top[:2]) + "_mix")


def dominant_allowed_families(source_rows: list[dict[str, str]], max_families: int = 3) -> set[str]:
    """Keep each Adobe upload folder coherent instead of mixing every material."""
    counts = Counter(clean(row.get("Family")) or "Unknown" for row in source_rows)
    return {family for family, _count in counts.most_common(max(1, max_families))}


def finalize_folder(batch_slug: str, out_dir: Path, rows: list[dict[str, str]]) -> Path:
    final_dir = UPLOAD_READY_ROOT / f"{batch_slug}_{folder_theme(rows)}"
    if final_dir == out_dir:
        return out_dir
    if final_dir.exists():
        suffix = 2
        while (UPLOAD_READY_ROOT / f"{final_dir.name}_{suffix}").exists():
            suffix += 1
        final_dir = UPLOAD_READY_ROOT / f"{final_dir.name}_{suffix}"
    out_dir.rename(final_dir)
    for row in rows:
        filename = clean(row.get("Filename"))
        if filename:
            row["Local_Path"] = str((final_dir / filename).relative_to(PROJECT_ROOT))
    return final_dir


def build(limit: int, max_per_family: int) -> tuple[list[dict[str, str]], Path, Path]:
    existing = resume_existing_batch()
    if existing is not None:
        return existing

    batch_slug = next_batch_slug()
    out_dir = UPLOAD_READY_ROOT / batch_slug
    assert_adobe_write_paths((OUT_INDEX, OUT_REPORT, out_dir))
    prior_status_by_parent = {
        clean(row.get("Parent_Asset_ID")): clean(row.get("Status"))
        for row in read_rows(OUT_INDEX)
        if clean(row.get("Parent_Asset_ID"))
    }
    blocked_filenames = blocked_submitted_filenames()
    already_prepared = prepared_parent_ids()
    out_dir.mkdir(parents=True, exist_ok=False)

    rows: list[dict[str, str]] = []
    decisions = rex_decisions()
    source_rows = [
        row
        for row in read_rows(SOURCE)
        if clean(row.get("QA_Status")).startswith("QA_PASS")
        and not clean(row.get("Upload_Status")).upper().startswith(("UPLOADED", "SUBMITTED", "ADOBE_SUBMITTED"))
        and not prior_status_by_parent.get(clean(row.get("Parent_Asset_ID")), "").upper().startswith(
            ("UPLOADED", "SUBMITTED", "ADOBE_SUBMITTED")
        )
        and "PENDING_HUMAN_VERIFICATION" not in prior_status_by_parent.get(clean(row.get("Parent_Asset_ID")), "").upper()
        and clean(row.get("Parent_Asset_ID")) not in already_prepared
        # Upload-ready means Rex explicitly approved this exact generated asset
        # for submission. Training/reference/pending assets stay in QA/DNA lanes.
        and decisions.get(clean(row.get("Parent_Asset_ID")), "PENDING") == "PASS"
    ]
    allowed_families = dominant_allowed_families(source_rows, max_families=3)
    family_seen: Counter[str] = Counter()
    pressure_skipped: Counter[str] = Counter()
    cohesion_skipped: Counter[str] = Counter()
    theme_pressure = load_theme_pressure()
    seen_hashes: set[str] = set()
    for row in source_rows:
        if limit and len(rows) >= limit:
            break
        family = clean(row.get("Family")) or "Unknown"
        if allowed_families and family not in allowed_families:
            cohesion_skipped[family] += 1
            continue
        pressure = theme_pressure.get(family.lower(), {})
        mixed = candidate_has_mixup(row)
        if pressure.get("Pressure") == "CAP_REACHED_REQUIRE_MIXUP" and not mixed:
            pressure_skipped[family] += 1
            continue
        effective_max_per_family = max_per_family
        if pressure.get("Pressure") == "WARN_REDUCE_SAME_FAMILY" and not mixed:
            effective_max_per_family = min(max_per_family, 2) if max_per_family else 2
        if effective_max_per_family and family_seen[family] >= effective_max_per_family:
            continue
        source = resolve_path(clean(row.get("Upscaled_Path")))
        if not source.exists():
            continue
        source_hash = file_sha256(source)
        if source_hash in seen_hashes:
            continue
        seen_hashes.add(source_hash)
        filename = safe_filename(batch_slug, len(rows) + 1, source)
        if filename.lower() in blocked_filenames:
            continue
        dest = out_dir / filename
        shutil.copy2(source, dest)
        family_seen[family] += 1
        rows.append(
            {
                "Filename": filename,
                "Title": clean(row.get("Title"))[:70],
                "Keywords": clean(row.get("Keywords")),
                "Category": clean(row.get("Category")) or "8",
                "Releases": "",
                "Created_Using_AI": "true",
                "Family": family,
                "Parent_Asset_ID": clean(row.get("Parent_Asset_ID")),
                "Source_Path": clean(row.get("Upscaled_Path")),
                "Local_Path": str(dest.relative_to(PROJECT_ROOT)),
                "Status": "READY_FOR_ADOBE_SUBMISSION_AFTER_METADATA_CHECK",
            }
        )
    out_dir = finalize_folder(batch_slug, out_dir, rows)
    adobe_csv = out_dir / f"RexAdobe_{out_dir.name}.csv"
    batch_manifest = out_dir / "batch_manifest.csv"
    assert_adobe_write_paths((OUT_INDEX, OUT_REPORT, adobe_csv, batch_manifest))
    write_rows(OUT_INDEX, rows)
    write_rows(batch_manifest, rows)
    write_adobe_csv(adobe_csv, rows)
    contact = write_contact_sheet(rows, out_dir)
    write_report(rows, out_dir, adobe_csv, contact, batch_manifest, pressure_skipped, cohesion_skipped)
    append_progress(rows, out_dir)
    return rows, out_dir, contact


def write_contact_sheet(rows: list[dict[str, str]], out_dir: Path) -> Path:
    contact_path = out_dir / "ADOBE_DAILY_UPLOAD_READY_CONTACT_SHEET.jpg"
    if not rows:
        return contact_path
    thumb_w, thumb_h = 230, 154
    label_h = 58
    pad = 16
    cols = min(4, len(rows))
    row_count = (len(rows) + cols - 1) // cols
    width = cols * thumb_w + (cols + 1) * pad
    height = row_count * (thumb_h + label_h + pad) + pad
    sheet = Image.new("RGB", (width, height), (18, 22, 27))
    draw = ImageDraw.Draw(sheet)
    font = load_font(11)
    bold = load_font(13, bold=True)
    for idx, row in enumerate(rows):
        x = pad + (idx % cols) * (thumb_w + pad)
        y = pad + (idx // cols) * (thumb_h + label_h + pad)
        image_path = out_dir / row["Filename"]
        try:
            with Image.open(image_path) as image:
                image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                sheet.paste(image.convert("RGB"), (x + (thumb_w - image.width) // 2, y + (thumb_h - image.height) // 2))
        except Exception:
            draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline=(180, 70, 70), width=2)
        draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline=(82, 100, 118), width=1)
        draw.text((x, y + thumb_h + 7), f"{idx + 1}. {row.get('Family', '')[:24]}", fill=(235, 235, 235), font=bold)
        draw.text((x, y + thumb_h + 28), row.get("Title", "")[:34], fill=(176, 220, 208), font=font)
        draw.text((x, y + thumb_h + 45), row.get("Filename", "")[:35], fill=(160, 166, 174), font=font)
    sheet.save(contact_path, "JPEG", quality=92, optimize=True)
    return contact_path


def write_report(
    rows: list[dict[str, str]],
    out_dir: Path,
    adobe_csv: Path,
    contact: Path,
    batch_manifest: Path,
    pressure_skipped: Counter[str] | None = None,
    cohesion_skipped: Counter[str] | None = None,
) -> None:
    family_counts = Counter(row.get("Family", "") for row in rows)
    source_rows = read_rows(SOURCE)
    decisions = rex_decisions()
    decision_counts = Counter(decisions.values())
    source_status_counts = Counter(clean(row.get("QA_Status")) or "BLANK" for row in source_rows)
    blocked_filenames = blocked_submitted_filenames()
    qa_pass_source_rows = [
        row
        for row in source_rows
        if clean(row.get("QA_Status")).startswith("QA_PASS")
        and not clean(row.get("Upload_Status")).upper().startswith(("UPLOADED", "SUBMITTED", "ADOBE_SUBMITTED"))
        and decisions.get(clean(row.get("Parent_Asset_ID")), "PENDING") not in {"REJECT", "HOLD"}
    ]
    unique_hashes: set[str] = set()
    duplicate_hash_rows = 0
    for row in qa_pass_source_rows:
        path = resolve_path(clean(row.get("Upscaled_Path")))
        if not path.exists():
            continue
        try:
            source_hash = file_sha256(path)
        except OSError:
            continue
        if source_hash in unique_hashes:
            duplicate_hash_rows += 1
        else:
            unique_hashes.add(source_hash)
    missing_upscaled = sum(1 for row in qa_pass_source_rows if not resolve_path(clean(row.get("Upscaled_Path"))).exists())
    lines = [
        "# Adobe Stock Daily Upload Ready Pack",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Files staged: {len(rows)}",
        f"- Folder: `{out_dir.relative_to(PROJECT_ROOT)}`",
        f"- Adobe CSV: `{adobe_csv.relative_to(PROJECT_ROOT)}`",
        f"- Batch manifest: `{batch_manifest.relative_to(PROJECT_ROOT)}`",
        f"- Contact sheet: `{contact.relative_to(PROJECT_ROOT)}`",
        f"- Public status: not submitted; requires visual QA and Adobe AI checkbox.",
        "- Folder policy: 50 files per neutral batch folder; no date-based upload folder is used for new packs.",
        "- Cohesion policy: keep each upload folder within 1-3 related material themes; avoid chaotic all-topic folders.",
        "- After Adobe confirms upload/submission, run the uploaded marker so file names receive `_uploaded` and the ledger blocks reuse.",
        f"- Rex QA filter: rejected/held assets are excluded from this pack.",
        f"- Theme pressure guard: families near 120 are reduced; families at 150 require clear mix-up factors.",
        "",
        "## Selection Diagnostics",
        "",
        f"- Source local-upscaled candidate rows: {len(source_rows)}",
        f"- Source QA statuses: {dict(source_status_counts)}",
        f"- Rex visual QA decisions loaded: {dict(decision_counts)}",
        f"- Ledger-blocked filenames already submitted/uploaded/pending: {len(blocked_filenames)}",
        f"- QA-pass source rows missing local upscaled file: {missing_upscaled}",
        f"- Unique not-yet-uploaded QA-pass image hashes: {len(unique_hashes)}",
        f"- Exact duplicate QA-pass rows skipped by hash guard: {duplicate_hash_rows}",
        f"- Theme-pressure skipped rows: {dict(pressure_skipped or {})}",
        f"- Folder-cohesion skipped rows: {dict(cohesion_skipped or {})}",
        "",
    ]
    if not rows and not source_rows:
        lines.extend(
            [
                "No new files were staged because `Database\\Adobe_Stock_Local_Upscaled_Candidates.csv` has no candidate rows.",
                "Next safe work is to harvest selected Adobe U-button files or run the local/superres resolution lane after U files exist; do not upload more while Adobe third-submit remains captcha/pending-human blocked.",
                "",
            ]
        )
    lines.extend(
        [
        "## Family Mix",
        "",
        ]
    )
    for family, count in family_counts.most_common():
        lines.append(f"- {family or 'unknown'}: {count}")
    lines.extend(["", "## Files", ""])
    for row in rows:
        lines.append(f"- {row['Filename']} | {row['Title']} | {row['Family']}")
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]], out_dir: Path) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock daily upload-ready review pack staged; files={len(rows)}; "
            f"folder={out_dir.relative_to(PROJECT_ROOT)}; not submitted.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument(
        "--max-per-family",
        type=int,
        default=18,
        help="Cap each material family while keeping a 50-file folder coherent across 1-3 related themes.",
    )
    args = parser.parse_args()
    rows, out_dir, _contact = build(max(1, min(args.limit, 50)), max(0, args.max_per_family))
    print(f"[ADOBE-DAILY-UPLOAD-READY] files={len(rows)} folder={out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
