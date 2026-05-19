"""Local Etsy digital-file guard for sticker liquidation packs."""

from __future__ import annotations

import csv
import re
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database" / "Sticker_Liquidation"
REPORTS = PROJECT_ROOT / "Reports"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
SUMMARY = DATABASE / "Sticker_Liquidation_Pack_Summary.csv"
METADATA = DATABASE / "Etsy_Sticker_Liquidation_Metadata.csv"
OUT = DATABASE / "Sticker_Liquidation_File_Guard.csv"
REPORT = REPORTS / "Sticker_Liquidation_File_Guard_latest.md"

ETSY_MAX_FILE_BYTES = 20 * 1024 * 1024
ETSY_MAX_FILES = 5

FIELDS = [
    "pack_id",
    "status",
    "asset_count",
    "etsy_file_count",
    "zip_total_mb",
    "largest_zip_mb",
    "zipped_png_count",
    "preview_exists",
    "metadata_quantity_status",
    "file_limit_status",
    "publish_guard",
    "issues",
]


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\r", " ").replace("\n", " ").split()).strip()


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


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def zip_paths(row: dict[str, str]) -> list[Path]:
    return [resolve(part) for part in clean(row.get("zip_path")).split(";") if clean(part)]


def metadata_by_pack() -> dict[str, dict[str, str]]:
    return {clean(row.get("pack_id")): row for row in read_rows(METADATA) if clean(row.get("pack_id"))}


def claimed_quantities(text: str) -> list[int]:
    return [int(match.group(1)) for match in re.finditer(r"(\d+)\s*\+", text)]


def check_quantity(pack: dict[str, str], metadata: dict[str, str]) -> tuple[str, str]:
    asset_count = int(clean(pack.get("asset_count")) or "0")
    text = f"{metadata.get('title', '')} {metadata.get('description', '')}"
    claims = claimed_quantities(text)
    if not claims:
        return "HOLD_NO_QUANTITY_CLAIM", "metadata lacks buyer-visible quantity claim"
    max_claim = max(claims)
    if asset_count < max_claim:
        return "HOLD_METADATA_OVERCLAIMS_QUANTITY", f"claims {max_claim}+ but pack has {asset_count}"
    return "PASS_QUANTITY_CLAIM", ""


def check_zip_contents(paths: list[Path]) -> tuple[str, int, float, list[str]]:
    issues: list[str] = []
    png_count = 0
    largest = 0.0
    if len(paths) > ETSY_MAX_FILES:
        issues.append(f"{len(paths)} zip files exceeds Etsy max {ETSY_MAX_FILES}")
    for path in paths:
        if not path.exists():
            issues.append(f"zip missing: {path}")
            continue
        size = path.stat().st_size
        largest = max(largest, size / 1024 / 1024)
        if size > ETSY_MAX_FILE_BYTES:
            issues.append(f"{path.name} is {size / 1024 / 1024:.2f}MB over 20MB")
        try:
            with zipfile.ZipFile(path) as zf:
                names = zf.namelist()
                png_count += sum(1 for name in names if name.lower().endswith(".png"))
                bad_names = [name for name in names if name.startswith("/") or ".." in Path(name).parts]
                if bad_names:
                    issues.append(f"unsafe zip paths in {path.name}: {bad_names[:3]}")
        except zipfile.BadZipFile:
            issues.append(f"bad zip: {path.name}")
    return ("PASS_FILE_LIMITS" if not issues else "HOLD_FILE_LIMIT_REVIEW"), png_count, largest, issues


def build() -> list[dict[str, str]]:
    meta = metadata_by_pack()
    rows: list[dict[str, str]] = []
    for pack in read_rows(SUMMARY):
        pack_id = clean(pack.get("pack_id"))
        status = clean(pack.get("status"))
        asset_count = int(clean(pack.get("asset_count")) or "0")
        paths = zip_paths(pack)
        metadata = meta.get(pack_id, {})
        quantity_status, quantity_issue = check_quantity(pack, metadata)
        file_status, zipped_png_count, largest_mb, file_issues = check_zip_contents(paths)
        preview_path = resolve(clean(pack.get("preview_path"))) if clean(pack.get("preview_path")) else Path()
        issues = []
        if quantity_issue:
            issues.append(quantity_issue)
        issues.extend(file_issues)
        if status == "READY" and not preview_path.exists():
            issues.append("preview missing")
        if status == "READY" and zipped_png_count < asset_count:
            issues.append(f"zip contains {zipped_png_count} PNGs but summary says {asset_count}")
        if status != "READY":
            issues.append(f"pack status is {status}; do not publish")
        publish_guard = "PASS_LOCAL_READY_NOT_PUBLISHED"
        if issues or status != "READY" or not file_status.startswith("PASS") or not quantity_status.startswith("PASS"):
            publish_guard = "HOLD_DO_NOT_PUBLISH"
        rows.append(
            {
                "pack_id": pack_id,
                "status": status,
                "asset_count": str(asset_count),
                "etsy_file_count": clean(pack.get("etsy_file_count")),
                "zip_total_mb": clean(pack.get("zip_total_mb")),
                "largest_zip_mb": f"{largest_mb:.2f}",
                "zipped_png_count": str(zipped_png_count),
                "preview_exists": "yes" if preview_path.exists() else "no",
                "metadata_quantity_status": quantity_status,
                "file_limit_status": file_status,
                "publish_guard": publish_guard,
                "issues": " | ".join(issues),
            }
        )
    return rows


def write_report(rows: list[dict[str, str]]) -> None:
    guard_counts = Counter(row.get("publish_guard", "") for row in rows)
    lines = [
        "# Sticker Liquidation File Guard",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Packs checked: {len(rows)}",
        f"- Publish guard: {dict(guard_counts)}",
        "",
        "## Results",
        "",
    ]
    for row in rows:
        lines.append(
            f"- {row['pack_id']}: {row['publish_guard']} | files={row['etsy_file_count']} | "
            f"largest={row['largest_zip_mb']}MB | pngs={row['zipped_png_count']} | {row['issues']}"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    guard_counts = Counter(row.get("publish_guard", "") for row in rows)
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Sticker liquidation file guard checked; packs={len(rows)}; "
            f"publish_guard={dict(guard_counts)}; no Etsy publish/spend.\n"
        )


def main() -> int:
    rows = build()
    write_rows(OUT, rows)
    write_report(rows)
    append_progress(rows)
    print(f"[STICKER-FILE-GUARD] packs={len(rows)} csv={OUT} report={REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
