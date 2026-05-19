"""Track Adobe Stock material-family volume and repetition pressure.

This is a small guardrail, not a strategy engine. It counts the images already
staged or confirmed uploaded in Adobe upload-ready batch folders, then marks
families that should be reduced before they become low-quality repetition.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REPORTS = PROJECT_ROOT / "Reports"
UPLOAD_READY_ROOT = PROJECT_ROOT / "adobe_stock_factory" / "upload_ready"
OUT_CSV = DATABASE / "Adobe_Stock_Theme_Stats.csv"
OUT_REPORT = REPORTS / "Adobe_Stock_Theme_Stats_latest.md"
ET = ZoneInfo("America/New_York")

IMAGE_EXTS = {".jpg", ".jpeg", ".png"}
SKIP_IMAGE_NAMES = {"adobe_daily_upload_ready_contact_sheet.jpg"}
MIXUP_TERMS = {
    "and",
    "with",
    "hybrid",
    "fusion",
    "mixed",
    "layered",
    "composite",
    "iridescent",
    "inlay",
    "overlay",
    "strata",
    "vein",
    "gold",
    "jade",
    "marble",
    "wood",
    "metal",
    "bronze",
    "paper",
    "fiber",
    "titanium",
}


def now_text() -> str:
    return datetime.now(ET).strftime("%Y-%m-%d %H:%M:%S %Z")


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\n", " ").replace("\r", " ").split()).strip()


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


def is_upload_image(path: Path) -> bool:
    if not path.is_file() or path.suffix.lower() not in IMAGE_EXTS:
        return False
    lower_name = path.name.lower()
    return lower_name not in SKIP_IMAGE_NAMES and "contact_sheet" not in lower_name


def is_uploaded_name(filename: str) -> bool:
    return Path(filename).stem.lower().endswith("_uploaded")


def infer_family(row: dict[str, str]) -> str:
    family = clean(row.get("Family"))
    if family:
        return family
    title = clean(row.get("Title")).lower()
    keywords = clean(row.get("Keywords")).lower()
    text = f"{title} {keywords}"
    for label, needles in {
        "Nero Marble": ("nero marble", "black marble"),
        "Kintsugi Marble": ("kintsugi", "gold vein marble"),
        "Smoky Jade": ("smoky jade", "jade"),
        "Walnut Burl": ("walnut burl", "wood burl"),
        "Aged Bronze Patina": ("aged bronze", "bronze patina", "oxidized metal"),
        "Brushed Titanium": ("brushed titanium", "brushed metal"),
        "Archival Vellum": ("vellum", "vintage paper", "paper texture"),
        "Carbon Fiber": ("carbon fiber",),
    }.items():
        if any(needle in text for needle in needles):
            return label
    return "Unknown"


def batch_folders() -> list[Path]:
    if not UPLOAD_READY_ROOT.exists():
        return []
    return [
        folder
        for folder in sorted(UPLOAD_READY_ROOT.glob("batch_*"))
        if folder.is_dir() and not folder.name.startswith("_superseded")
    ]


def collect_stats(warn_at: int = 120, cap_at: int = 150) -> list[dict[str, str]]:
    family_rows: dict[str, dict[str, object]] = {}
    examples: dict[str, list[str]] = defaultdict(list)
    batch_count_by_family: dict[str, Counter[str]] = defaultdict(Counter)
    for folder in batch_folders():
        manifest = folder / "batch_manifest.csv"
        if not manifest.exists():
            continue
        rows = read_rows(manifest)
        existing_names = {path.name for path in folder.iterdir() if is_upload_image(path)}
        for row in rows:
            filename = clean(row.get("Filename"))
            if filename and existing_names and filename not in existing_names:
                # The manifest may be stale after partial upload renames. Keep
                # the family count but do not claim file-level uploaded state.
                pass
            family = infer_family(row)
            key = family.lower()
            record = family_rows.setdefault(
                key,
                {
                    "Family": family,
                    "Staged_Total": 0,
                    "Uploaded_Confirmed": 0,
                    "Open_Unuploaded": 0,
                    "Completed_Batches": 0,
                    "Active_Batches": 0,
                },
            )
            record["Staged_Total"] = int(record["Staged_Total"]) + 1
            uploaded = is_uploaded_name(filename) or "UPLOADED" in clean(row.get("Status")).upper()
            if uploaded:
                record["Uploaded_Confirmed"] = int(record["Uploaded_Confirmed"]) + 1
            else:
                record["Open_Unuploaded"] = int(record["Open_Unuploaded"]) + 1
            batch_count_by_family[key][folder.name] += 1
            if len(examples[key]) < 5:
                examples[key].append(filename or clean(row.get("Parent_Asset_ID")))

    output: list[dict[str, str]] = []
    for key, record in family_rows.items():
        batches = batch_count_by_family[key]
        completed_batches = sum(1 for name in batches if name.endswith("_completed"))
        active_batches = len(batches) - completed_batches
        staged = int(record["Staged_Total"])
        if staged >= cap_at:
            pressure = "CAP_REACHED_REQUIRE_MIXUP"
            recommendation = "Stop plain same-family uploads; only allow clear hybrid/new-use-case variants."
        elif staged >= warn_at:
            pressure = "WARN_REDUCE_SAME_FAMILY"
            recommendation = "Reduce same-family slots to 1-2 per batch unless mixed with new factors."
        else:
            pressure = "OK"
            recommendation = "Normal sampling allowed."
        output.append(
            {
                "Family": str(record["Family"]),
                "Staged_Total": str(staged),
                "Uploaded_Confirmed": str(record["Uploaded_Confirmed"]),
                "Open_Unuploaded": str(record["Open_Unuploaded"]),
                "Completed_Batches": str(completed_batches),
                "Active_Batches": str(active_batches),
                "Pressure": pressure,
                "Recommendation": recommendation,
                "Example_Filenames": "; ".join(name for name in examples[key] if name),
            }
        )
    output.sort(key=lambda row: (-int(row["Staged_Total"]), row["Family"]))
    return output


def load_theme_pressure(warn_at: int = 120, cap_at: int = 150) -> dict[str, dict[str, str]]:
    return {row["Family"].lower(): row for row in collect_stats(warn_at=warn_at, cap_at=cap_at)}


def candidate_has_mixup(row: dict[str, str]) -> bool:
    text = f"{clean(row.get('Title'))} {clean(row.get('Keywords'))} {clean(row.get('Family'))}".lower()
    tokens = set(re.findall(r"[a-z]+", text))
    material_hits = tokens & MIXUP_TERMS
    connector_hit = any(term in text for term in (" hybrid ", " fusion ", " with ", " and ", "&", " layered "))
    return connector_hit or len(material_hits) >= 3


def write_report(rows: list[dict[str, str]], warn_at: int, cap_at: int) -> None:
    lines = [
        "# Adobe Stock Theme Stats",
        "",
        f"Generated: {now_text()}",
        f"Warn threshold: {warn_at} staged/upload-ready images per family",
        f"Cap threshold: {cap_at} staged/upload-ready images per family",
        "",
        "## Pressure Table",
        "",
        "| Family | Staged | Uploaded | Open | Pressure | Recommendation |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['Family']} | {row['Staged_Total']} | {row['Uploaded_Confirmed']} | "
            f"{row['Open_Unuploaded']} | {row['Pressure']} | {row['Recommendation']} |"
        )
    lines.extend(["", "## Notes", "", "- Counts are based on Adobe upload-ready `batch_*` manifests only."])
    lines.append("- `_superseded*` folders and contact sheets are ignored.")
    lines.append("- Families at cap require obvious new mix-up factors before more same-family uploads.")
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warn-at", type=int, default=120)
    parser.add_argument("--cap-at", type=int, default=150)
    args = parser.parse_args()
    rows = collect_stats(warn_at=args.warn_at, cap_at=args.cap_at)
    fields = [
        "Family",
        "Staged_Total",
        "Uploaded_Confirmed",
        "Open_Unuploaded",
        "Completed_Batches",
        "Active_Batches",
        "Pressure",
        "Recommendation",
        "Example_Filenames",
    ]
    write_rows(OUT_CSV, rows, fields)
    write_report(rows, args.warn_at, args.cap_at)
    pressure = Counter(row["Pressure"] for row in rows)
    print(f"[ADOBE-THEME-STATS] families={len(rows)} pressure={dict(pressure)} report={OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
