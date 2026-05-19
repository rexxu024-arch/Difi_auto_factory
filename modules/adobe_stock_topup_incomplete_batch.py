"""Top up the oldest incomplete Adobe upload-ready batch to 50 files.

The normal pack builder resumes incomplete folders but does not add more files
to them. Rex's current rule is simpler: keep filling the same not-completed
folder before creating a new one, up to the daily target.
"""

from __future__ import annotations

import argparse
import csv
import shutil
from collections import Counter
from pathlib import Path

from adobe_stock_daily_upload_ready_pack import (
    FIELDS,
    OUT_INDEX,
    OUT_REPORT,
    PROJECT_ROOT,
    SOURCE,
    UPLOAD_READY_ROOT,
    batch_sort_key,
    blocked_submitted_filenames,
    clean,
    file_sha256,
    incomplete_batch_folders,
    is_uploaded_file,
    load_theme_pressure,
    read_rows,
    resolve_path,
    rex_decisions,
    safe_filename,
    upload_images,
    write_adobe_csv,
    write_contact_sheet,
    write_report,
    write_rows,
)
from adobe_stock_theme_stats import candidate_has_mixup


def manifest_parent_ids() -> set[str]:
    ids: set[str] = set()
    for manifest in UPLOAD_READY_ROOT.glob("batch_*/batch_manifest.csv"):
        for row in read_rows(manifest):
            parent = clean(row.get("Parent_Asset_ID"))
            if parent:
                ids.add(parent)
    return ids


def topup(target: int, max_per_family: int) -> dict:
    folders = sorted(incomplete_batch_folders(), key=batch_sort_key)
    if not folders:
        return {"status": "NO_INCOMPLETE_BATCH", "added": 0}
    folder = folders[0]
    manifest = folder / "batch_manifest.csv"
    rows = read_rows(manifest)
    real_images = [path for path in upload_images(folder) if not is_uploaded_file(path)]
    slots = max(0, target - len(real_images))
    if slots <= 0:
        return {"status": "ALREADY_AT_TARGET", "folder": str(folder), "files": len(real_images), "added": 0}

    decisions = rex_decisions()
    blocked_names = blocked_submitted_filenames()
    prepared = manifest_parent_ids()
    seen_hashes = {file_sha256(path) for path in real_images if path.exists()}
    family_seen = Counter(clean(row.get("Family")) or "Unknown" for row in rows)
    theme_pressure = load_theme_pressure()
    allowed_families = {family for family, _count in family_seen.most_common(3)} or None
    added = 0

    # First preserve folder cohesion. If the remaining strict-family images are
    # exact duplicates, widen to other approved families rather than leaving the
    # upload batch artificially tiny.
    for active_allowed in (allowed_families, None):
      for source_row in read_rows(SOURCE):
        if added >= slots:
            break
        parent = clean(source_row.get("Parent_Asset_ID"))
        if not clean(source_row.get("QA_Status")).startswith("QA_PASS"):
            continue
        if clean(source_row.get("Upload_Status")).upper().startswith(("UPLOADED", "SUBMITTED", "ADOBE_SUBMITTED")):
            continue
        if parent in prepared:
            continue
        if decisions.get(parent, "PENDING") in {"REJECT", "HOLD"}:
            continue
        family = clean(source_row.get("Family")) or "Unknown"
        if active_allowed and family not in active_allowed and len(active_allowed) >= 3:
            continue
        pressure = theme_pressure.get(family.lower(), {})
        if pressure.get("Pressure") == "CAP_REACHED_REQUIRE_MIXUP" and not candidate_has_mixup(source_row):
            continue
        if max_per_family and family_seen[family] >= max_per_family:
            continue
        source = resolve_path(clean(source_row.get("Upscaled_Path")))
        if not source.exists():
            continue
        source_hash = file_sha256(source)
        if source_hash in seen_hashes:
            continue
        filename = safe_filename(folder.name.split("_", 2)[0] + "_" + folder.name.split("_", 2)[1], len(real_images) + added + 1, source)
        if filename.lower() in blocked_names:
            continue
        dest = folder / filename
        shutil.copy2(source, dest)
        row = {
            "Filename": filename,
            "Title": clean(source_row.get("Title"))[:70],
            "Keywords": clean(source_row.get("Keywords")),
            "Category": clean(source_row.get("Category")) or "8",
            "Releases": "",
            "Created_Using_AI": "true",
            "Family": family,
            "Parent_Asset_ID": parent,
            "Source_Path": clean(source_row.get("Upscaled_Path")),
            "Local_Path": str(dest.relative_to(PROJECT_ROOT)),
            "Status": "READY_FOR_ADOBE_SUBMISSION_AFTER_METADATA_CHECK"
            if decisions.get(parent) == "PASS"
            else "READY_FOR_REX_VISUAL_QA_NOT_SUBMITTED",
        }
        rows.append(row)
        prepared.add(parent)
        seen_hashes.add(source_hash)
        family_seen[family] += 1
        added += 1
      if added >= slots:
          break

    write_rows(manifest, rows)
    adobe_csvs = sorted(folder.glob("RexAdobe_*.csv"))
    adobe_csv = adobe_csvs[0] if adobe_csvs else folder / f"RexAdobe_{folder.name}.csv"
    write_adobe_csv(adobe_csv, rows)
    write_rows(OUT_INDEX, rows)
    contact = write_contact_sheet(rows, folder)
    write_report(rows, folder, adobe_csv, contact, manifest)
    return {"status": "TOPPED_UP", "folder": str(folder), "files": len(rows), "added": added, "contact": str(contact)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=50)
    parser.add_argument("--max-per-family", type=int, default=18)
    args = parser.parse_args()
    print(topup(args.target, args.max_per_family))


if __name__ == "__main__":
    main()
