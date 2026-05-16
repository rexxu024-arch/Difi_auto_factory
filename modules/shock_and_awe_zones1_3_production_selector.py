"""Select Shock & Awe Zones 1/3 visual winners and build production files.

This is local-only. It does not publish or create Printify products. The goal is
to turn harvested U-images into a vetted production CSV that can later feed the
private draft creator.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATABASE = ROOT / "Database"
REPORTS = ROOT / "Review_Packets"
QUEUE = DATABASE / "Shock_And_Awe_V5_Zones1_3_MJ_Dispatch_Queue.csv"
PRIVATE_QUEUE = DATABASE / "Shock_And_Awe_V5_Zones1_3_Printify_Private_Queue.csv"
SELECTION = DATABASE / "Shock_And_Awe_V5_Zones1_3_Final_Selection.csv"
PRODUCTION = DATABASE / "Shock_And_Awe_V5_Zones1_3_Printify_Production_Files.csv"
REPORT = REPORTS / "OPERATION_SHOCK_AND_AWE_V5_ZONES1_3_PRODUCTION_SELECTION.md"
NY_TZ = ZoneInfo("America/New_York")


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
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def resolve(value: str) -> Path:
    path = Path(clean(value))
    return path if path.is_absolute() else ROOT / path


def center_crop_resize(src: Path, dst: Path, width: int, height: int) -> tuple[int, int]:
    with Image.open(src) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        original = image.size
        target_ratio = width / height
        current_ratio = image.width / image.height
        if current_ratio > target_ratio:
            new_width = int(image.height * target_ratio)
            left = (image.width - new_width) // 2
            image = image.crop((left, 0, left + new_width, image.height))
        elif current_ratio < target_ratio:
            new_height = int(image.width / target_ratio)
            top = (image.height - new_height) // 2
            image = image.crop((0, top, image.width, top + new_height))
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        image.save(dst, "PNG")
        return original


def target_size(private: dict[str, str]) -> tuple[int, int]:
    print_area = clean(private.get("Print_Area")).lower()
    if "2475x1155" in print_area:
        return 2475, 1155
    if "1725x2625" in print_area:
        return 1725, 2625
    if "1538x2138" in print_area:
        return 1538, 2138
    if "3592x5387" in print_area:
        return 3592, 5387
    return 3600, 5400


def select_status(row: dict[str, str]) -> tuple[str, str]:
    qa = clean(row.get("Visual_QA_Status"))
    flags = clean(row.get("Visual_QA_Flags"))
    harvest = clean(row.get("Harvest_Status"))
    if harvest == "HARVEST_HOLD":
        return "HOLD_MJ_UI_RESUBMIT_REQUIRED", clean(row.get("Harvest_Error"))
    if qa.startswith("HOLD"):
        return "HOLD_REPROMPT_REQUIRED", flags or qa
    if not clean(row.get("Visual_QA_Best_File")):
        return "HOLD_NO_BEST_IMAGE", "Missing Visual_QA_Best_File."
    if qa.startswith("PASS"):
        return "SELECTED_PASS", "Visual QA pass."
    if qa.startswith("REVIEW") and set(filter(None, flags.split(";"))) <= {"UPSCALE_NEEDED"}:
        return "SELECTED_REVIEW_UPSCALE", "Only upscale/reformat required; acceptable for production-file build."
    if qa.startswith("REVIEW"):
        return "HOLD_REVIEW_MANUAL", flags or qa
    return "HOLD_UNKNOWN_QA", qa or harvest


def run(limit: int = 0) -> int:
    queue_rows = read_csv(QUEUE)
    private_by_sku = {clean(row.get("Internal_SKU")): row for row in read_csv(PRIVATE_QUEUE)}
    selected: list[dict[str, str]] = []
    production: list[dict[str, str]] = []
    touched = 0
    for row in queue_rows:
        if limit and touched >= limit:
            break
        sku = clean(row.get("Internal_SKU"))
        private = private_by_sku.get(sku, {})
        status, note = select_status(row)
        best_file = clean(row.get("Visual_QA_Best_File"))
        selected_u = ""
        if "_BEST_U" in clean(row.get("Visual_QA_Status")):
            selected_u = "U" + clean(row.get("Visual_QA_Status")).split("_BEST_U")[-1][:1]
        selection_row = {
            "Final_SKU": sku,
            "Source_SKU": sku,
            "Selected_U": selected_u,
            "Selected_File": best_file,
            "Product_Vector": clean(private.get("Product_Type")) or clean(row.get("Product_Type")),
            "Blueprint_ID": clean(private.get("Blueprint_ID")),
            "Provider_ID": clean(private.get("Provider_ID")),
            "Variant_ID": clean(private.get("Variant_ID")),
            "Base_Cost_USD": clean(private.get("Estimated_Cost_USD")).replace("$", ""),
            "Shipping_USD": clean(private.get("Estimated_Shipping_USD")).replace("$", ""),
            "RRP_USD": clean(private.get("Recommended_Retail_USD")).replace("$", ""),
            "Final_Status": status,
            "QA_Note": note,
            "Concept_Name": clean(row.get("Concept_Name")),
        }
        selected.append(selection_row)
        if status.startswith("SELECTED"):
            source = resolve(best_file)
            width, height = target_size(private)
            dst = ROOT / "Output" / "Shock_And_Awe" / "V5" / "Zones1_3_Final" / sku / "Production_Design.png"
            if source.exists():
                original = center_crop_resize(source, dst, width, height)
                prod_row = dict(selection_row)
                prod_row.update(
                    {
                        "Target_Width": str(width),
                        "Target_Height": str(height),
                        "Production_Design_File": rel(dst),
                        "Production_Status": "PRODUCTION_READY",
                        "Source_Original_Size": f"{original[0]}x{original[1]}",
                        "Built_At_ET": now_text(),
                    }
                )
                production.append(prod_row)
                print(f"[ZONES1-3-PRODUCTION] {sku} {status} {rel(dst)}")
            else:
                selection_row["Final_Status"] = "HOLD_SOURCE_MISSING"
                selection_row["QA_Note"] = str(source)
        touched += 1
    write_csv(SELECTION, selected)
    write_csv(PRODUCTION, production)
    counts: dict[str, int] = {}
    for row in selected:
        counts[row["Final_Status"]] = counts.get(row["Final_Status"], 0) + 1
    lines = [
        "# Shock & Awe V5 Zones 1/3 Production Selection",
        "",
        f"Generated: {now_text()} America/New_York",
        "",
        f"- Selection rows: {len(selected)}",
        f"- Production-ready files: {len(production)}",
        "",
        "## Counts",
        "",
    ]
    for key, value in sorted(counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Holds", ""])
    for row in selected:
        if row["Final_Status"].startswith("HOLD"):
            lines.append(f"- {row['Final_SKU']} / {row['Concept_Name']}: {row['Final_Status']} - {row['QA_Note']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[ZONES1-3-PRODUCTION-DONE] selected={len(selected)} production={len(production)} csv={PRODUCTION}")
    print(f"[ZONES1-3-PRODUCTION-REPORT] {REPORT}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Shock & Awe Zones 1/3 production selections")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    return run(args.limit)


if __name__ == "__main__":
    raise SystemExit(main())
