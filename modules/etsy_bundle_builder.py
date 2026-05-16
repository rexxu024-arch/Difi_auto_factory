"""Build no-fee Etsy digital bundle candidates from V7 package-ready items."""

from __future__ import annotations

import argparse
import csv
import sys
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATABASE = ROOT / "Database"
REPORTS = ROOT / "Reports"
PACKAGE_QUEUE = DATABASE / "Etsy_Darwinian_Lab_V7_Upload_Queue.csv"
BUNDLE_QUEUE = DATABASE / "Etsy_Darwinian_Lab_V7_Bundle_Queue.csv"
BUNDLE_ROOT = ROOT / "Output" / "Etsy" / "Darwinian_Lab" / "V7" / "_bundles"
REPORT = REPORTS / "ETSY_DARWINIAN_LAB_V7_BUNDLE_PLAN.md"
NY_TZ = ZoneInfo("America/New_York")
MAX_ETSY_FILE_MB = 20.0

POOL_TAGS = {
    "POOL05": [
        "dark academia", "junk journal", "ephemera kit", "vintage collage",
        "printable paper", "gothic paper", "digital journal", "craft supplies",
        "collage sheet", "download kit", "reading nook", "grimoire pages",
        "journal pages",
    ],
    "POOL04": [
        "streetwear png", "shirt design", "y2k graphic", "cyberpunk art",
        "digital png", "apparel graphic", "print on demand", "gothic graphic",
        "streetwear art", "hoodie design", "png download", "edgy design",
        "cyber relic",
    ],
    "POOL08": [
        "digital paper", "seamless pattern", "maximalist art", "scrapbook paper",
        "wallpaper texture", "craft paper", "pattern bundle", "gothic pattern",
        "printable paper", "baroque decor", "digital download", "journal paper",
        "damask pattern",
    ],
    "POOL09": [
        "printable planner", "reading journal", "habit tracker", "grimoire pages",
        "study planner", "planner inserts", "journal pages", "book tracker",
        "dark academia", "printable pdf", "cozy planner", "reading nook",
        "magic planner",
    ],
    "POOL10": [
        "tattoo flash", "occult tattoo", "black ink art", "line art tattoo",
        "esoteric art", "flash sheet", "printable tattoo", "mystic symbol",
        "tattoo stencil", "dark tattoo", "ink drawing", "spiritual tattoo",
        "digital tattoo",
    ],
}


def clean(value: object) -> str:
    return str(value or "").strip()


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else ["Generated_At", "Bundle_ID", "Status"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def abs_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def bundle_title(pool_name: str, items: list[dict[str, str]]) -> str:
    pool = clean(pool_name)
    if "Pattern" in pool or "Seamless" in pool:
        return "Maximalist Seamless Pattern Bundle, Gothic Digital Paper Pack, Printable Craft Set"
    if "Journal" in pool or "Ephemera" in pool:
        return "Dark Academia Junk Journal Bundle, Printable Ephemera Kit, Vintage Collage"
    if "Tattoo" in pool:
        return "Esoteric Tattoo Flash Bundle, Black Ink Printable Line Art Set"
    if "Planner" in pool:
        return "Mystic Printable Planner Bundle, Reading Nook Pages, Journal Inserts"
    if "Streetwear" in pool:
        return "Cyber Streetwear PNG Bundle, Y2K Shirt Graphics, Digital Apparel Design Pack"
    first = clean(items[0].get("Etsy_Title")) if items else "OpenClaw Digital Bundle"
    return f"{pool} Digital Download Bundle, {first}"[:135].rstrip(" -|,")


def bundle_description(pool_name: str, items: list[dict[str, str]]) -> str:
    use_cases = sorted({clean(item.get("Buyer_Use_Case")) for item in items if clean(item.get("Buyer_Use_Case"))})
    formats = sorted({clean(item.get("Format")) for item in items if clean(item.get("Format"))})
    return (
        f"A curated OpenClaw digital bundle built around {clean(pool_name)}. "
        "This bundle is designed to feel more complete than a single printable: multiple coordinated files, "
        "one visual mood, and a clear craft/decor use case. "
        f"Best for: {', '.join(use_cases[:3]) or 'journaling, decor, and craft projects'}. "
        f"Formats included: {', '.join(formats[:3]) or 'digital download files'}. "
        "No physical item is shipped. Files should be downloaded after purchase and used for personal projects or small handmade workflows. "
        "AI-assisted artwork is curated, formatted, and quality-checked before packaging."
    )


def tags(items: list[dict[str, str]], pool_id: str = "") -> str:
    tokens: list[str] = []
    for token in POOL_TAGS.get(pool_id, []):
        if len(token) <= 20 and token not in tokens:
            tokens.append(token)
    for item in items:
        for source in [item.get("Tags"), item.get("Etsy_Tags")]:
            for token in clean(source).split(","):
                token = token.strip().lower()
                if token and len(token) <= 20 and token not in tokens:
                    tokens.append(token)
        for token in clean(item.get("Etsy_Title")).replace(",", " ").split():
            token = token.strip().lower()
            if 4 <= len(token) <= 20 and token not in tokens:
                tokens.append(token)
    fallback = ["digital download", "printable bundle", "craft supply", "journal kit", "wall art"]
    for token in fallback:
        if len(token) <= 20 and token not in tokens:
            tokens.append(token)
    return ", ".join(tokens[:13])


def build_bundle(bundle_id: str, rows: list[dict[str, str]]) -> tuple[list[Path], float, bool]:
    out_dir = BUNDLE_ROOT / bundle_id
    out_dir.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    current_rows: list[dict[str, str]] = []
    current_bytes = 0

    def estimated_bytes(row: dict[str, str]) -> int:
        total = 0
        for field in ["Digital_Zip", "Preview_Image"]:
            path = abs_path(clean(row.get(field)))
            if path.exists():
                total += path.stat().st_size
        return total

    def write_part(part_rows: list[dict[str, str]], part_no: int) -> Path:
        zip_path = out_dir / f"{bundle_id}_etsy_bundle_part{part_no:02d}.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            readme = (
                f"OpenClaw Digital Bundle\nBundle: {bundle_id}\nPart: {part_no}\nPrepared: {now_text()} America/New_York\n\n"
                "This is a curated bundle package. If a nested ZIP is included, unzip it first to access the artwork files.\n"
            )
            archive.writestr("README_OpenClaw_Bundle.txt", readme)
            for row in part_rows:
                sku = clean(row.get("Internal_SKU"))
                zip_file = abs_path(clean(row.get("Digital_Zip")))
                preview = abs_path(clean(row.get("Preview_Image")))
                if zip_file.exists():
                    archive.write(zip_file, arcname=f"{sku}/{zip_file.name}")
                if preview.exists():
                    archive.write(preview, arcname=f"{sku}/{preview.name}")
        return zip_path

    # Etsy digital listings commonly accept multiple files with a per-file size
    # limit. Keep each generated part under 20 MB where possible instead of
    # holding the entire bundle just because one mega ZIP is too large.
    max_bytes = int(MAX_ETSY_FILE_MB * 1024 * 1024 * 0.92)
    for row in rows:
        row_bytes = estimated_bytes(row)
        if current_rows and current_bytes + row_bytes > max_bytes and len(files) < 4:
            files.append(write_part(current_rows, len(files) + 1))
            current_rows = []
            current_bytes = 0
        current_rows.append(row)
        current_bytes += row_bytes
    if current_rows:
        files.append(write_part(current_rows, len(files) + 1))

    total_mb = sum(path.stat().st_size for path in files) / (1024 * 1024)
    all_parts_ok = all(path.stat().st_size / (1024 * 1024) <= MAX_ETSY_FILE_MB for path in files)
    return files, total_mb, all_parts_ok


def build(limit: int = 3, per_bundle: int = 5) -> int:
    rows = [
        row for row in read_csv(PACKAGE_QUEUE)
        if clean(row.get("Package_Status")) == "READY_FOR_SPOTCHECK_NO_FEE_SPENT"
        and abs_path(clean(row.get("Digital_Zip"))).exists()
    ]
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[clean(row.get("Pool_ID")) or clean(row.get("Pool_Name")) or "MIXED"].append(row)
    bundle_rows: list[dict[str, str]] = []
    for pool_id, items in grouped.items():
        if limit and len(bundle_rows) >= limit:
            break
        items = items[: max(2, per_bundle)]
        if len(items) < 2:
            continue
        bundle_id = f"OC-ETSY-BUNDLE-{pool_id.replace(' ', '_').replace('/', '_')}-{len(bundle_rows)+1:02d}"
        zip_paths, size_mb, parts_ok = build_bundle(bundle_id, items)
        pool_name = clean(items[0].get("Pool_Name")) or pool_id
        status = "READY_FOR_ETSY_SPOTCHECK_NO_FEE_SPENT" if parts_ok and len(zip_paths) <= 5 else "REVIEW_OVER_20MB_SPLIT_REQUIRED"
        price = 14.99 if len(items) >= 5 else 11.99
        bundle_rows.append(
            {
                "Generated_At": now_text(),
                "Bundle_ID": bundle_id,
                "Pool_ID": pool_id,
                "Pool_Name": pool_name,
                "Item_Count": str(len(items)),
                "Included_SKUs": ";".join(clean(item.get("Internal_SKU")) for item in items),
                "Etsy_Title": bundle_title(pool_name, items),
                "Etsy_Description": bundle_description(pool_name, items),
                "Tags": tags(items, pool_id),
                "Price_USD": f"{price:.2f}",
                "Bundle_Zip": ";".join(str(path) for path in zip_paths),
                "Bundle_File_Count": str(len(zip_paths)),
                "Bundle_MB": f"{size_mb:.2f}",
                "Status": status,
                "Fee_Risk_Status": "NO_FEE_SPENT_LOCAL_ONLY",
            }
        )
    write_csv(BUNDLE_QUEUE, bundle_rows)
    lines = [
        "# Etsy Darwinian Lab V7 Bundle Plan",
        "",
        f"Generated: {now_text()} America/New_York",
        "",
        "No Etsy fees spent. These bundle candidates increase perceived value while Etsy UI/API writes remain risk-gated.",
        "",
        f"- Bundles created: {len(bundle_rows)}",
        "",
    ]
    for row in bundle_rows:
        lines.append(f"## {row['Bundle_ID']} - {row['Pool_Name']}")
        lines.append(f"- Status: {row['Status']}")
        lines.append(f"- Items: {row['Item_Count']}")
        lines.append(f"- Files: {row['Bundle_File_Count']}")
        lines.append(f"- Total size: {row['Bundle_MB']} MB")
        lines.append(f"- Price: ${row['Price_USD']}")
        lines.append(f"- ZIP parts: `{row['Bundle_Zip']}`")
        lines.append(f"- Title: {row['Etsy_Title']}")
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[ETSY-BUNDLE] rows={len(bundle_rows)} csv={BUNDLE_QUEUE} report={REPORT}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build V7 Etsy digital bundle candidates")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--per-bundle", type=int, default=5)
    args = parser.parse_args()
    return build(args.limit, args.per_bundle)


if __name__ == "__main__":
    raise SystemExit(main())
