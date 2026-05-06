"""QA Etsy digital upload queue files before Etsy API/UI upload."""

from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
QUEUE = DATABASE_DIR / "Etsy_Digital_Upload_Queue.csv"
PREVIEW_QUEUE = DATABASE_DIR / "Etsy_Digital_Preview_Assets.csv"
QA_CSV = DATABASE_DIR / "Etsy_Digital_QA.csv"
QA_MD = DATABASE_DIR / "Etsy_Digital_QA_Report.md"


EXPECTED_FILE_COLUMNS = [f"Digital_File_{i}" for i in range(1, 6)]
EXPECTED_PREVIEW_COLUMNS = [f"Preview_{i}" for i in range(1, 4)]


def check_file(path: str, *, min_width: int, min_height: int, max_mb: int = 20, suffixes: set[str] | None = None) -> dict:
    p = Path(path)
    if not path or not p.exists():
        return {"exists": False, "width": "", "height": "", "mb": "", "mode": "", "ok": False, "issue": "missing"}
    try:
        with Image.open(p) as im:
            width, height, mode = im.width, im.height, im.mode
        mb = round(p.stat().st_size / (1024 * 1024), 2)
        issues = []
        if mb > max_mb:
            issues.append(f"over_{max_mb}mb")
        if width < min_width or height < min_height:
            issues.append("low_pixel_size")
        allowed = suffixes or {".jpg", ".jpeg"}
        if p.suffix.lower() not in allowed:
            issues.append("bad_suffix")
        return {
            "exists": True,
            "width": width,
            "height": height,
            "mb": mb,
            "mode": mode,
            "ok": not issues,
            "issue": ";".join(issues),
        }
    except Exception as exc:  # noqa: BLE001
        return {"exists": False, "width": "", "height": "", "mb": "", "mode": "", "ok": False, "issue": str(exc)}


def load_queue() -> list[dict]:
    with QUEUE.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_preview_map() -> dict[str, dict]:
    if not PREVIEW_QUEUE.exists():
        return {}
    with PREVIEW_QUEUE.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row.get("ID", ""): row for row in csv.DictReader(handle)}


def run() -> None:
    rows = []
    summary = {"listings": 0, "files": 0, "previews": 0, "bad_files": 0, "missing_files": 0}
    preview_map = load_preview_map()
    for listing in load_queue():
        summary["listings"] += 1
        listing_bad = False
        for col in EXPECTED_FILE_COLUMNS:
            info = check_file(listing.get(col, ""), min_width=3000, min_height=4000)
            summary["files"] += 1
            if not info["ok"]:
                summary["bad_files"] += 1
                listing_bad = True
            if not info["exists"]:
                summary["missing_files"] += 1
            rows.append(
                {
                    "ID": listing.get("ID"),
                    "Title": listing.get("Title"),
                    "File_Column": col,
                    "Path": listing.get(col, ""),
                    "Exists": info["exists"],
                    "Width": info["width"],
                    "Height": info["height"],
                    "MB": info["mb"],
                    "Mode": info["mode"],
                    "OK": info["ok"],
                    "Issue": info["issue"],
                    "Listing_OK": not listing_bad,
                }
            )
        preview_row = preview_map.get(listing.get("ID", ""), {})
        for col in EXPECTED_PREVIEW_COLUMNS:
            info = check_file(preview_row.get(col, ""), min_width=1800, min_height=1800)
            summary["previews"] += 1
            if not info["ok"]:
                summary["bad_files"] += 1
                listing_bad = True
            if not info["exists"]:
                summary["missing_files"] += 1
            rows.append(
                {
                    "ID": listing.get("ID"),
                    "Title": listing.get("Title"),
                    "File_Column": col,
                    "Path": preview_row.get(col, ""),
                    "Exists": info["exists"],
                    "Width": info["width"],
                    "Height": info["height"],
                    "MB": info["mb"],
                    "Mode": info["mode"],
                    "OK": info["ok"],
                    "Issue": info["issue"],
                    "Listing_OK": not listing_bad,
                }
            )
    headers = ["ID", "Title", "File_Column", "Path", "Exists", "Width", "Height", "MB", "Mode", "OK", "Issue", "Listing_OK"]
    with QA_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    md = [
        "# Etsy Digital QA Report",
        "",
        f"- Listings checked: {summary['listings']}",
        f"- Digital files checked: {summary['files']}",
        f"- Preview images checked: {summary['previews']}",
        f"- Bad files: {summary['bad_files']}",
        f"- Missing files: {summary['missing_files']}",
        "",
    ]
    bad = [row for row in rows if str(row["OK"]) != "True" and row["OK"] is not True]
    if bad:
        md.append("## Issues")
        for row in bad[:50]:
            md.append(f"- {row['ID']} {row['File_Column']}: {row['Issue']} ({row['Path']})")
    else:
        md.append("All digital files pass local pre-upload QA.")
    QA_MD.write_text("\n".join(md), encoding="utf-8")
    print(
        f"[ETSY-DIGITAL-QA] listings={summary['listings']} "
        f"files={summary['files']} previews={summary['previews']} "
        f"bad={summary['bad_files']} missing={summary['missing_files']}"
    )
    print(f"[ETSY-DIGITAL-QA] csv={QA_CSV}")


if __name__ == "__main__":
    run()
