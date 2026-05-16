"""Audit local Printify production design files for print-resolution risk."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REPORTS = PROJECT_ROOT / "Reports"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
REGISTRY = DATABASE / "Unified_Listing_Registry.csv"
OUT_CSV = DATABASE / "Printify_Design_Resolution_Audit.csv"
OUT_REPORT = REPORTS / "Printify_Design_Resolution_Audit_latest.md"
NY_TZ = ZoneInfo("America/New_York")


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], headers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalize_path(value: str) -> Path:
    path = Path(value.strip())
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def infer_product_type(identifier: str, path: Path) -> str:
    text = f"{identifier} {path}".lower()
    if "sticker" in text:
        return "Sticker"
    if "acrylic" in text:
        return "Acrylic"
    if "poster" in text:
        return "Poster"
    if "canvas" in text:
        return "Canvas"
    if "digital" in text:
        return "Digital"
    return "Unknown"


def registry_candidates() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(REGISTRY):
        path_value = (row.get("Production_Path") or "").strip()
        if not path_value:
            continue
        path = normalize_path(path_value)
        rows.append(
            {
                "ID": row.get("ID", ""),
                "Source": "Unified_Listing_Registry",
                "Product_Type": row.get("Product_Type") or infer_product_type(row.get("ID", ""), path),
                "Local_Status": row.get("Local_Status", ""),
                "Printify_Product_ID": row.get("Printify_Product_ID", ""),
                "Etsy_Launch_Status": row.get("Etsy_Launch_Status", ""),
                "Production_Path": str(path),
            }
        )
    return rows


def output_candidates(existing: set[str]) -> list[dict[str, str]]:
    rows = []
    for path in (PROJECT_ROOT / "Output").glob("**/Production_Design.*"):
        key = str(path.resolve()).lower()
        if key in existing:
            continue
        identifier = path.parent.name
        rows.append(
            {
                "ID": identifier,
                "Source": "Output_Glob",
                "Product_Type": infer_product_type(identifier, path),
                "Local_Status": "",
                "Printify_Product_ID": "",
                "Etsy_Launch_Status": "",
                "Production_Path": str(path),
            }
        )
    return rows


def risk_for(product_type: str, width: int, height: int, path: Path, local_status: str) -> tuple[str, str]:
    pixels = width * height
    short_edge = min(width, height)
    long_edge = max(width, height)
    text = f"{path} {local_status}".lower()
    if "not_working_lowres" in text or "lowres" in text:
        return "HOLD_LOWRES_SOURCE_PATH", "Path/status already marks this production source as low-res."
    if "grid" in text or "_u1" in text or "_u2" in text or "_u3" in text or "_u4" in text:
        return "HOLD_GRID_OR_U_SOURCE_RISK", "Production path looks like a grid/U crop source; verify it is not a draft."
    if product_type == "Sticker":
        if short_edge < 1500:
            return "HOLD_STICKER_BELOW_250DPI_6IN", "Sticker source is below 1500px short edge."
        if short_edge < 1800:
            return "WARN_STICKER_BORDERLINE", "Sticker source is printable for 6in, but below preferred 300DPI."
        return "OK_STICKER_PRINT_SOURCE", "Sticker source meets preferred small-format threshold."
    if product_type == "Acrylic":
        # Current Printify photo block SKU is 5x7-class; 1500x2100 is roughly
        # 300DPI and should not be treated like a large wall-art poster.
        if short_edge < 1500 or long_edge < 2100 or pixels < 3_000_000:
            return "HOLD_ACRYLIC_5X7_BELOW_PRINT_REDLINE", "Acrylic source is below the 5x7 300DPI-class threshold."
        if short_edge < 1800 or long_edge < 2400:
            return "OK_ACRYLIC_5X7_PRINT_SOURCE", "Acrylic 5x7 source is printable; upscale only for future premium/larger variants."
        return "OK_PREMIUM_ACRYLIC_PRINT_SOURCE", "Acrylic source meets premium threshold."
    if product_type in {"Poster", "Canvas"}:
        if pixels < 8_000_000 or short_edge < 2200 or long_edge < 3300:
            return "HOLD_WALL_ART_BELOW_PREMIUM_PRINT_REDLINE", "Poster/canvas source is below OpenClaw premium print threshold."
        if pixels < 12_000_000 or short_edge < 2600:
            return "WARN_WALL_ART_ACCEPTABLE_NOT_HERO", "Usable for small wall art, but not ideal for premium/hero SKU."
        return "OK_PREMIUM_POD_PRINT_SOURCE", "Source meets premium POD threshold."
    if pixels < 4_000_000:
        return "WARN_UNKNOWN_BELOW_4MP", "Unknown product source below 4MP."
    return "OK_UNKNOWN_SOURCE_SIZE", "Unknown product type but source is above 4MP."


def inspect(row: dict[str, str]) -> dict[str, str]:
    path = normalize_path(row["Production_Path"])
    out = dict(row)
    out["Exists"] = str(path.exists())
    if not path.exists():
        out.update(
            {
                "Width": "",
                "Height": "",
                "Pixels": "",
                "Short_Edge": "",
                "File_Bytes": "",
                "Resolution_Status": "HOLD_MISSING_FILE",
                "Resolution_Note": "Production source path does not exist locally.",
            }
        )
        return out
    try:
        with Image.open(path) as image:
            width, height = image.size
            fmt = image.format or ""
            mode = image.mode
    except Exception as exc:
        out.update(
            {
                "Width": "",
                "Height": "",
                "Pixels": "",
                "Short_Edge": "",
                "File_Bytes": str(path.stat().st_size),
                "Resolution_Status": f"HOLD_IMAGE_READ_ERROR:{type(exc).__name__}",
                "Resolution_Note": "Image could not be opened by Pillow.",
            }
        )
        return out
    status, note = risk_for(row.get("Product_Type", "Unknown"), width, height, path, row.get("Local_Status", ""))
    out.update(
        {
            "Width": str(width),
            "Height": str(height),
            "Pixels": str(width * height),
            "Short_Edge": str(min(width, height)),
            "Long_Edge": str(max(width, height)),
            "Format": fmt,
            "Mode": mode,
            "File_Bytes": str(path.stat().st_size),
            "Resolution_Status": status,
            "Resolution_Note": note,
        }
    )
    return out


def write_report(rows: list[dict[str, str]]) -> None:
    counts: dict[str, int] = {}
    product_counts: dict[str, int] = {}
    for row in rows:
        counts[row["Resolution_Status"]] = counts.get(row["Resolution_Status"], 0) + 1
        product = row.get("Product_Type", "Unknown")
        product_counts[product] = product_counts.get(product, 0) + 1
    hold_rows = [row for row in rows if row["Resolution_Status"].startswith("HOLD")]
    warn_rows = [row for row in rows if row["Resolution_Status"].startswith("WARN")]
    lines = [
        "# Printify Production Design Resolution Audit",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Checked production design files: {len(rows)}",
        f"- HOLD rows: {len(hold_rows)}",
        f"- WARN rows: {len(warn_rows)}",
        f"- CSV: `{OUT_CSV.relative_to(PROJECT_ROOT)}`",
        "",
        "## Product Mix",
        "",
    ]
    for key, value in sorted(product_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Resolution Status", ""])
    for key, value in sorted(counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Highest-Risk Samples", ""])
    for row in (hold_rows + warn_rows)[:30]:
        lines.append(
            f"- {row.get('ID')} | {row.get('Product_Type')} | {row.get('Resolution_Status')} | "
            f"{row.get('Width')}x{row.get('Height')} | {row.get('Production_Path')}"
        )
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    registry = registry_candidates()
    existing = {str(normalize_path(row["Production_Path"]).resolve()).lower() for row in registry if row.get("Production_Path")}
    candidates = registry + output_candidates(existing)
    audited = [inspect(row) for row in candidates]
    headers = [
        "ID",
        "Source",
        "Product_Type",
        "Local_Status",
        "Printify_Product_ID",
        "Etsy_Launch_Status",
        "Production_Path",
        "Exists",
        "Width",
        "Height",
        "Pixels",
        "Short_Edge",
        "Long_Edge",
        "Format",
        "Mode",
        "File_Bytes",
        "Resolution_Status",
        "Resolution_Note",
    ]
    write_csv(OUT_CSV, audited, headers)
    write_report(audited)
    hold = sum(1 for row in audited if row["Resolution_Status"].startswith("HOLD"))
    warn = sum(1 for row in audited if row["Resolution_Status"].startswith("WARN"))
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Printify production design resolution audit refreshed; "
            f"checked={len(audited)}; hold={hold}; warn={warn}; report={OUT_REPORT.relative_to(PROJECT_ROOT)}.\n"
        )
    print(f"[PRINTIFY-RESOLUTION-AUDIT] checked={len(audited)} hold={hold} warn={warn} report={OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
