"""Build Printify-ready production design files for Shock & Awe V5 finalists."""

from __future__ import annotations

import csv
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageOps


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SELECTION = PROJECT_ROOT / "Database" / "Shock_And_Awe_V5_Final_Selection.csv"
OUTPUT_CSV = PROJECT_ROOT / "Database" / "Shock_And_Awe_V5_Printify_Production_Files.csv"
NY_TZ = ZoneInfo("America/New_York")


def clean(value: object) -> str:
    return str(value or "").strip()


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


def build() -> int:
    if not SELECTION.exists():
        raise FileNotFoundError(f"Missing selection file: {SELECTION}")
    with SELECTION.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    out_rows: list[dict[str, str]] = []
    for row in rows:
        final_sku = clean(row.get("Final_SKU"))
        src = PROJECT_ROOT / clean(row.get("Selected_File"))
        width = int(float(clean(row.get("Target_Width"))))
        height = int(float(clean(row.get("Target_Height"))))
        if not src.exists():
            status = "SOURCE_MISSING"
            original = ""
            dst = ""
        else:
            dst_path = PROJECT_ROOT / "Output" / "Shock_And_Awe" / "V5" / "Final" / final_sku / "Production_Design.png"
            original_size = center_crop_resize(src, dst_path, width, height)
            status = "PRODUCTION_READY"
            original = f"{original_size[0]}x{original_size[1]}"
            dst = str(dst_path.relative_to(PROJECT_ROOT))
        out = dict(row)
        out.update(
            {
                "Production_Design_File": dst,
                "Production_Status": status,
                "Source_Original_Size": original,
                "Built_At_ET": datetime.now(NY_TZ).strftime("%Y-%m-%d %I:%M:%S %p %Z"),
            }
        )
        out_rows.append(out)
        print(f"[SHOCK-PRODUCTION] {final_sku} {status} {dst}")
    fields = list(out_rows[0].keys()) if out_rows else []
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)
    print(f"[SHOCK-PRODUCTION-DONE] rows={len(out_rows)} csv={OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
