"""Free local resolution upscale for Adobe Stock U-button candidates.

Midjourney Discord U-button files can still be below Adobe's 4MP minimum.
For stock assets we do not spend Fast/creative upscale minutes. Instead, use
the selected U-button image as provenance, resize locally to a conservative
3000x2000px target, and keep the file in a separate production folder for QA.
Grid crops are never accepted as source.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageEnhance, ImageFilter

from adobe_stock_quality_policy import (
    MIN_SHARP_TILE_COVERAGE,
    MIN_UPSCALED_EDGE_SCORE,
    SOFT_MIN_FILE_BYTES,
    edge_detail_score,
    sharp_tile_coverage,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
SOURCE = DATABASE / "Adobe_Stock_Daily_U_Candidates.csv"
OUT = DATABASE / "Adobe_Stock_Local_Upscaled_Candidates.csv"
REPORT = REVIEW / "Adobe_Stock_Local_Upscaled_Candidates_latest.md"
OUT_DIR = PROJECT_ROOT / "Output" / "Adobe_Stock" / "Daily_Production_Upscaled"
NY_TZ = ZoneInfo("America/New_York")

TARGET_WIDTH = 3000
TARGET_HEIGHT = 2000
JPEG_QUALITY = 94


FIELDS = [
    "Asset_ID",
    "Parent_Asset_ID",
    "Family",
    "Title",
    "Keywords",
    "Category",
    "Created_Using_AI",
    "Source_Path",
    "Upscaled_Path",
    "Source_Width",
    "Source_Height",
    "Width",
    "Height",
    "Pixels",
    "File_Bytes",
    "Edge_Detail_Score",
    "Sharp_Tile_Coverage",
    "QA_Status",
    "Upload_Status",
    "Issues",
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\r", " ").replace("\n", " ").split()).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
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


def safe_filename(asset_id: str) -> str:
    safe = "".join(ch.lower() if ch.isalnum() else "_" for ch in asset_id)
    while "__" in safe:
        safe = safe.replace("__", "_")
    return f"{safe.strip('_')}_3000x2000.jpg"


def upscale_one(row: dict[str, str]) -> dict[str, str]:
    source = resolve(clean(row.get("Source_Path")))
    asset_id = clean(row.get("Asset_ID"))
    out_path = OUT_DIR / safe_filename(asset_id)
    base = {
        "Asset_ID": f"{asset_id}-LOCAL3000",
        "Parent_Asset_ID": asset_id,
        "Family": clean(row.get("Family")),
        "Title": clean(row.get("Title")),
        "Keywords": clean(row.get("Keywords")),
        "Category": clean(row.get("Category")) or "8",
        "Created_Using_AI": clean(row.get("Created_Using_AI")) or "true",
        "Source_Path": str(source.relative_to(PROJECT_ROOT)) if source.exists() else clean(row.get("Source_Path")),
        "Upscaled_Path": str(out_path.relative_to(PROJECT_ROOT)),
    }
    if not source.exists():
        return {**base, "QA_Status": "HOLD_SOURCE_MISSING", "Upload_Status": "HOLD_DO_NOT_UPLOAD", "Issues": "source path missing"}

    try:
        with Image.open(source) as image:
            source_width, source_height = image.size
            image = image.convert("RGB")
            # Preserve 3:2 framing, enlarge from U-button source, then mild sharpening.
            resized = image.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
            resized = resized.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=3))
            resized = ImageEnhance.Contrast(resized).enhance(1.03)
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            resized.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    except Exception as exc:
        return {**base, "QA_Status": f"HOLD_UPSCALE_ERROR:{type(exc).__name__}", "Upload_Status": "HOLD_DO_NOT_UPLOAD", "Issues": repr(exc)[:200]}

    file_bytes = out_path.stat().st_size
    edge_score = edge_detail_score(out_path)
    sharp_coverage = sharp_tile_coverage(out_path)
    pixels = TARGET_WIDTH * TARGET_HEIGHT
    status = "QA_PASS_LOCAL_RESOLUTION_UPSCALE_PENDING_VISUAL_QA"
    issues = ""
    if file_bytes < SOFT_MIN_FILE_BYTES:
        issues = (
            f"soft file-size warning: {file_bytes} bytes after local upscale; "
            "Adobe has no 4MB file-size minimum, but visual QA must confirm detail"
        )
    if edge_score < MIN_UPSCALED_EDGE_SCORE:
        status = "HOLD_LOCAL_UPSCALE_DETAIL_TOO_LOW"
        issues = f"edge detail score {edge_score:.2f} below {MIN_UPSCALED_EDGE_SCORE:.2f}; likely too blurry for Adobe"
    elif sharp_coverage < MIN_SHARP_TILE_COVERAGE:
        status = "HOLD_SHALLOW_DOF_OR_LOW_SHARP_AREA"
        issues = (
            f"sharp tile coverage {sharp_coverage:.3f} below {MIN_SHARP_TILE_COVERAGE:.2f}; "
            "first Adobe batch requires broad clear material texture, not foreground/background blur"
        )
    return {
        **base,
        "Source_Width": str(source_width),
        "Source_Height": str(source_height),
        "Width": str(TARGET_WIDTH),
        "Height": str(TARGET_HEIGHT),
        "Pixels": str(pixels),
        "File_Bytes": str(file_bytes),
        "Edge_Detail_Score": f"{edge_score:.2f}",
        "Sharp_Tile_Coverage": f"{sharp_coverage:.3f}",
        "QA_Status": status,
        "Upload_Status": "QA_PASS_NOT_UPLOADED" if status.startswith("QA_PASS") else "HOLD_DO_NOT_UPLOAD",
        "Issues": issues,
    }


def build(limit: int = 0) -> list[dict[str, str]]:
    source_rows = read_csv(SOURCE)
    rows: list[dict[str, str]] = []
    for row in source_rows:
        if not clean(row.get("Source_Path")):
            continue
        rows.append(upscale_one(row))
        if limit and len(rows) >= limit:
            break
    return rows


def write_report(rows: list[dict[str, str]]) -> None:
    passed = sum(1 for row in rows if row.get("QA_Status", "").startswith("QA_PASS"))
    lines = [
        "# Adobe Stock Local Resolution Upscale",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Source U-button candidates: {len(rows)}",
        f"- Local 3000x2000 outputs passing mechanical QA: {passed}",
        f"- Output CSV: `{OUT.relative_to(PROJECT_ROOT)}`",
        "",
        "## Policy",
        "",
        "- This does not use Midjourney Fast or creative/subtle upscale.",
        "- Source must be an actual selected U-button/full-res file, not a grid crop.",
        "- Local upscale only solves Adobe's 4MP floor. Visual usefulness still needs QA.",
        "",
        "## First 20 Outputs",
        "",
    ]
    for row in rows[:20]:
        lines.append(f"- {row['Parent_Asset_ID']} | {row['QA_Status']} | {row['Upscaled_Path']}")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    passed = sum(1 for row in rows if row.get("QA_Status", "").startswith("QA_PASS"))
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock local U-button resolution upscale rebuilt; "
            f"outputs={len(rows)}; mechanical_pass={passed}; no upload/spend.\n"
        )


def main() -> int:
    rows = build()
    write_csv(OUT, rows)
    write_report(rows)
    append_progress(rows)
    print(f"[ADOBE-LOCAL-UPSCALE] outputs={len(rows)} pass={sum(1 for row in rows if row.get('QA_Status', '').startswith('QA_PASS'))} csv={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
