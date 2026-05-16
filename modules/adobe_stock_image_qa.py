"""Local QA gate for Adobe Stock pilot assets.

The script reads Database/Adobe_Stock_Pilot_Queue.csv, validates rows that have
Source_Path populated, and updates QA_Status without uploading anything.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image

from adobe_stock_isolation import assert_adobe_write_path
from adobe_stock_quality_policy import validate_adobe_production_image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
QUEUE = DATABASE / "Adobe_Stock_Pilot_Queue.csv"
BATCH = DATABASE / "Adobe_Stock_Pilot_Batch.csv"
NY_TZ = ZoneInfo("America/New_York")

HAMMING_DUPLICATE_THRESHOLD = 4


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def resolve_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def average_hash(path: Path) -> str:
    with Image.open(path) as image:
        gray = image.convert("L").resize((8, 8))
        pixels = list(gray.getdata())
    avg = sum(pixels) / len(pixels)
    bits = "".join("1" if pixel >= avg else "0" for pixel in pixels)
    return f"{int(bits, 2):016x}"


def hamming_hex(left: str, right: str) -> int:
    return bin(int(left, 16) ^ int(right, 16)).count("1")


def validate_image(path: Path, row: dict[str, str] | None = None) -> tuple[bool, str, dict[str, str]]:
    return validate_adobe_production_image(path, row)


def choose_source(source: str) -> Path:
    if source == "batch":
        return BATCH
    if source == "queue":
        return QUEUE
    return BATCH if BATCH.exists() else QUEUE


def run(limit: int = 0, source: str = "auto") -> dict[str, int]:
    source_csv = choose_source(source)
    assert_adobe_write_path(source_csv)
    rows = read_rows(source_csv)
    checked = passed = held = skipped = duplicate_hold = 0
    seen_hashes: list[tuple[str, str]] = []

    for row in rows:
        if limit and checked >= limit:
            break
        source = (row.get("Source_Path") or "").strip()
        if not source:
            skipped += 1
            continue
        checked += 1
        image_path = resolve_path(source)
        ok, status, info = validate_image(image_path, row)
        row.update(info)
        if ok:
            current_hash = average_hash(image_path)
            row["Perceptual_Hash"] = current_hash
            for prior_id, prior_hash in seen_hashes:
                if hamming_hex(current_hash, prior_hash) <= HAMMING_DUPLICATE_THRESHOLD:
                    ok = False
                    status = f"HOLD_NEAR_DUPLICATE_OF:{prior_id}"
                    duplicate_hold += 1
                    break
            seen_hashes.append((row.get("ID", ""), current_hash))

        row["QA_Status"] = status
        if ok:
            passed += 1
            row["Upload_Status"] = "QA_PASS_NOT_UPLOADED"
        else:
            held += 1
            row["Upload_Status"] = "HOLD_DO_NOT_UPLOAD"

    write_rows(source_csv, rows)
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock image QA source={source_csv.name}; checked={checked}; "
            f"passed={passed}; held={held}; skipped_no_source={skipped}; near_duplicates={duplicate_hold}.\n"
        )
    return {
        "checked": checked,
        "passed": passed,
        "held": held,
        "skipped": skipped,
        "near_duplicates": duplicate_hold,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--source", choices=["auto", "batch", "queue"], default="auto")
    args = parser.parse_args()
    result = run(limit=args.limit, source=args.source)
    print("[ADOBE-QA]", result)


if __name__ == "__main__":
    main()
