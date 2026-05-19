"""Mark an Adobe Stock upload-ready batch as uploaded after human confirmation.

This script is intentionally not called by the upload-ready builder. It should
run only after Rex/Codex confirms one or more files were actually accepted by the
Adobe Contributor upload flow. It renames confirmed staged files with an
`_uploaded` suffix and records the original filenames in the submission ledger
so future packs do not reuse them. The batch folder receives `_completed` only
after every real upload image in that folder is confirmed uploaded.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
FACTORY = PROJECT_ROOT / "adobe_stock_factory" / "upload_ready"
LEDGER = DATABASE / "Adobe_Stock_Submission_Ledger.csv"
ET = ZoneInfo("America/New_York")

IMAGE_EXTS = {".jpg", ".jpeg", ".png"}
SKIP_NAMES = {"adobe_daily_upload_ready_contact_sheet.jpg"}


def now_text() -> str:
    return datetime.now(ET).strftime("%Y-%m-%d %H:%M:%S %Z")


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\r", " ").replace("\n", " ").split()).strip()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def resolve_batch(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = FACTORY / value if not value.lower().startswith("adobe_stock_factory") else PROJECT_ROOT / value
    return path


def uploaded_name(path: Path) -> Path:
    if path.stem.lower().endswith("_uploaded"):
        return path
    return path.with_name(f"{path.stem}_uploaded{path.suffix}")


def is_upload_image(path: Path) -> bool:
    if not path.is_file() or path.suffix.lower() not in IMAGE_EXTS:
        return False
    if path.name.lower() in SKIP_NAMES or "contact_sheet" in path.name.lower():
        return False
    return True


def all_upload_images(batch_dir: Path) -> list[Path]:
    return [path for path in sorted(batch_dir.iterdir()) if is_upload_image(path)]


def is_uploaded(path: Path) -> bool:
    return path.stem.lower().endswith("_uploaded")


def folder_completed_name(batch_dir: Path) -> Path:
    if batch_dir.name.endswith("_completed"):
        return batch_dir
    return batch_dir.with_name(f"{batch_dir.name}_completed")


def complete_folder_if_ready(batch_dir: Path, dry_run: bool = False) -> tuple[bool, Path]:
    images = all_upload_images(batch_dir)
    if not images:
        return False, batch_dir
    if not all(is_uploaded(path) for path in images):
        return False, batch_dir
    completed = folder_completed_name(batch_dir)
    if completed == batch_dir:
        return True, batch_dir
    if dry_run:
        return True, completed
    if completed.exists():
        suffix = 2
        while batch_dir.with_name(f"{completed.name}_{suffix}").exists():
            suffix += 1
        completed = batch_dir.with_name(f"{completed.name}_{suffix}")
    batch_dir.rename(completed)
    return True, completed


def selected_paths(batch_dir: Path, file_names: set[str], limit: int | None) -> list[Path]:
    candidates = [path for path in all_upload_images(batch_dir) if not is_uploaded(path)]
    if file_names:
        wanted = {name.lower() for name in file_names}
        candidates = [
            path
            for path in candidates
            if path.name.lower() in wanted or uploaded_name(path).name.lower() in wanted
        ]
    if limit is not None:
        candidates = candidates[: max(0, limit)]
    return candidates


def mark(
    batch_dir: Path,
    dry_run: bool = False,
    file_names: set[str] | None = None,
    limit: int | None = None,
) -> tuple[int, list[tuple[str, str]], bool, Path]:
    if not batch_dir.exists() or not batch_dir.is_dir():
        raise FileNotFoundError(f"batch folder not found: {batch_dir}")
    manifest = batch_dir / "batch_manifest.csv"
    rows = read_rows(manifest)
    fields = list(rows[0].keys()) if rows else []
    row_by_filename = {clean(row.get("Filename")): row for row in rows if clean(row.get("Filename"))}
    renamed: list[tuple[str, str]] = []
    selected = selected_paths(batch_dir, file_names or set(), limit)
    for path in selected:
        target = uploaded_name(path)
        if target == path:
            continue
        renamed.append((path.name, target.name))
        if dry_run:
            continue
        path.rename(target)
        row = row_by_filename.get(path.name)
        if row:
            row["Filename"] = target.name
            row["Local_Path"] = str(target.relative_to(PROJECT_ROOT))
            row["Status"] = "UPLOADED_CONFIRMED_BY_REX"
    if rows and fields and not dry_run:
        write_rows(manifest, rows, fields)
    if dry_run:
        selected_names = {path.name for path in selected}
        images = all_upload_images(batch_dir)
        completed = bool(images) and all(is_uploaded(path) or path.name in selected_names for path in images)
        final_folder = folder_completed_name(batch_dir) if completed else batch_dir
    else:
        completed, final_folder = complete_folder_if_ready(batch_dir, dry_run=False)
    if rows and fields and not dry_run and final_folder != batch_dir:
        final_manifest = final_folder / "batch_manifest.csv"
        final_rows = read_rows(final_manifest)
        for row in final_rows:
            filename = clean(row.get("Filename"))
            if filename:
                row["Local_Path"] = str((final_folder / filename).relative_to(PROJECT_ROOT))
        write_rows(final_manifest, final_rows, list(final_rows[0].keys()) if final_rows else fields)
    if not dry_run:
        append_ledger(final_folder, renamed)
        append_progress(final_folder, renamed, completed)
    return len(renamed), renamed, completed, final_folder


def parse_file_args(values: list[str] | None) -> set[str]:
    names: set[str] = set()
    for value in values or []:
        for part in value.split(","):
            cleaned = clean(part)
            if cleaned:
                names.add(cleaned)
    return names


def remaining_count(folder: Path, dry_run_count: int = 0) -> int:
    images = all_upload_images(folder)
    remaining = sum(1 for path in images if not is_uploaded(path))
    return max(0, remaining - max(0, dry_run_count))


def append_ledger(batch_dir: Path, renamed: list[tuple[str, str]]) -> None:
    fields = ["Filename", "Batch", "Status", "Updated_ET", "Notes"]
    existing = read_rows(LEDGER)
    seen = {clean(row.get("Filename")).lower() for row in existing}
    rows = list(existing)
    for original, uploaded in renamed:
        if original.lower() in seen:
            continue
        rows.append(
            {
                "Filename": original,
                "Batch": batch_dir.name,
                "Status": "UPLOADED_CONFIRMED_BY_REX",
                "Updated_ET": now_text(),
                "Notes": f"local upload-ready copy renamed to {uploaded}",
            }
        )
    write_rows(LEDGER, rows, fields)


def append_progress(batch_dir: Path, renamed: list[tuple[str, str]], completed: bool) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock batch marked uploaded; "
            f"batch={batch_dir.relative_to(PROJECT_ROOT)}; files={len(renamed)}; "
            f"completed={completed}; local names suffixed `_uploaded`.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="Batch folder name or path, e.g. batch_001")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None, help="Mark only the next N unuploaded images in the batch.")
    parser.add_argument("--files", nargs="*", default=None, help="Optional exact filenames confirmed uploaded.")
    args = parser.parse_args()
    batch_dir = resolve_batch(args.folder)
    count, _renamed, completed, final_folder = mark(
        batch_dir,
        dry_run=args.dry_run,
        file_names=parse_file_args(args.files),
        limit=args.limit,
    )
    mode = "DRY_RUN" if args.dry_run else "APPLIED"
    remaining = remaining_count(batch_dir if args.dry_run else final_folder, dry_run_count=count if args.dry_run else 0)
    print(
        f"[ADOBE-MARK-UPLOADED] {mode} folder={args.folder} marked={count} "
        f"remaining={remaining} completed={completed} final_folder={final_folder}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
