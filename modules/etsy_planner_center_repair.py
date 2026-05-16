"""Create local clean-center planner variants from harvested POOL09 art.

POOL09 planner products need a real writing area. Midjourney often makes the
whole page decorative, so this repair step turns promising border/atmosphere
art into a usable printable page without another paid/slow generation round.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.etsy_darwinian_lab_visual_qa import metrics_for, pool_gate


DATABASE = ROOT / "Database"
REVIEW = ROOT / "Review_Packets"
DEFAULT_QUEUE = DATABASE / "Etsy_Darwinian_Lab_V7_Planner_Reprompt_MJ_Queue.csv"
DEFAULT_QA = DATABASE / "Etsy_Darwinian_Lab_V7_Planner_Reprompt_MJ_Queue_Visual_QA.csv"
REPAIR_CSV = DATABASE / "Etsy_Darwinian_Lab_V7_Planner_Local_Repair.csv"
REPAIR_MD = REVIEW / "ETSY_V7_PLANNER_LOCAL_REPAIR.md"
NY_TZ = ZoneInfo("America/New_York")


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %z")


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def resolve_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path


def best_source_by_qa(qa_path: Path) -> dict[str, str]:
    if not qa_path.exists():
        return {}
    rows, _ = read_csv(qa_path)
    best: dict[str, tuple[float, str]] = {}
    for row in rows:
        sku = clean(row.get("Internal_SKU"))
        path = clean(row.get("Image_Path"))
        if not sku or not path:
            continue
        try:
            score = float(clean(row.get("Score")) or "0")
        except ValueError:
            score = 0.0
        if sku not in best or score > best[sku][0]:
            best[sku] = (score, path)
    return {sku: path for sku, (_, path) in best.items()}


def output_path_for(source: Path, sku: str) -> Path:
    return source.parent / f"{sku}_PLANNER_CLEAN_CENTER.png"


def repair_planner(source: Path, target: Path) -> None:
    with Image.open(source) as img:
        base = img.convert("RGB")
        if base.width < 1700 or base.height < 2200:
            scale = max(1700 / base.width, 2200 / base.height)
            new_size = (int(base.width * scale), int(base.height * scale))
            base = base.resize(new_size, Image.Resampling.LANCZOS)

        target_ratio = 2 / 3
        current_ratio = base.width / base.height
        if abs(current_ratio - target_ratio) > 0.03:
            if current_ratio > target_ratio:
                new_w = int(base.height * target_ratio)
                left = (base.width - new_w) // 2
                base = base.crop((left, 0, left + new_w, base.height))
            else:
                new_h = int(base.width / target_ratio)
                top = max(0, (base.height - new_h) // 2)
                base = base.crop((0, top, base.width, top + new_h))

        canvas = base.copy()
        w, h = canvas.size
        draw = ImageDraw.Draw(canvas, "RGBA")

        # Slightly soften the writing surface so thumbnails still show atmosphere
        # while the middle becomes genuinely usable as a planner page.
        panel = (int(w * 0.18), int(h * 0.22), int(w * 0.82), int(h * 0.78))
        shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            (panel[0] + 8, panel[1] + 10, panel[2] + 8, panel[3] + 10),
            radius=max(24, int(w * 0.025)),
            fill=(45, 33, 20, 45),
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=max(8, int(w * 0.008))))
        canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow).convert("RGB")
        draw = ImageDraw.Draw(canvas, "RGBA")

        draw.rounded_rectangle(
            panel,
            radius=max(24, int(w * 0.025)),
            fill=(244, 238, 222, 246),
            outline=(104, 78, 45, 135),
            width=max(3, int(w * 0.003)),
        )

        # Add faint guide lines that read as useful, not fake typography.
        line_color = (115, 92, 60, 70)
        x1 = int(w * 0.24)
        x2 = int(w * 0.76)
        step = max(46, int(h * 0.028))
        y = int(h * 0.31)
        while y < int(h * 0.71):
            draw.line((x1, y, x2, y), fill=line_color, width=max(1, int(w * 0.0015)))
            y += step

        target.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(target, quality=96)


def run(limit: int, queue_path: Path, qa_path: Path) -> int:
    rows, _ = read_csv(queue_path)
    best_sources = best_source_by_qa(qa_path)
    repair_rows: list[dict[str, str]] = []
    processed = 0
    for row in rows:
        if limit and processed >= limit:
            break
        sku = clean(row.get("Internal_SKU"))
        pool = clean(row.get("Pool_ID"))
        if pool != "POOL09" or not sku:
            continue
        status = clean(row.get("Visual_QA_Status"))
        if "HOLD" not in status and clean(row.get("Harvest_Status")) != "READY_FOR_VISUAL_QA":
            continue
        source_value = best_sources.get(sku) or clean(row.get("Visual_QA_Best_File"))
        if not source_value:
            for key in ("U3_File", "U4_File", "U1_File", "U2_File"):
                if clean(row.get(key)):
                    source_value = clean(row.get(key))
                    break
        if not source_value:
            continue
        source = resolve_path(source_value)
        if not source.exists():
            continue
        target = output_path_for(source, sku)
        repair_planner(source, target)
        metrics = metrics_for(target)
        gate, flags = pool_gate("POOL09", metrics)
        repair_rows.append(
            {
                "Internal_SKU": sku,
                "Source_File": str(source),
                "Repaired_File": str(target),
                "Width": str(metrics.width),
                "Height": str(metrics.height),
                "File_KB": str(metrics.file_kb),
                "Center_Whitespace": f"{metrics.center_whitespace:.3f}",
                "Contrast": f"{metrics.contrast:.2f}",
                "Gate_Status": gate,
                "Flags": ";".join(flags),
                "Checked_At_ET": now_text(),
            }
        )
        processed += 1
        print(f"[PLANNER-REPAIR] {sku} -> {gate} whitespace={metrics.center_whitespace:.3f} {target}")

    fields = [
        "Internal_SKU",
        "Source_File",
        "Repaired_File",
        "Width",
        "Height",
        "File_KB",
        "Center_Whitespace",
        "Contrast",
        "Gate_Status",
        "Flags",
        "Checked_At_ET",
    ]
    write_csv(REPAIR_CSV, repair_rows, fields)
    REVIEW.mkdir(parents=True, exist_ok=True)
    passed = sum(1 for row in repair_rows if row["Gate_Status"] == "PASS")
    held = sum(1 for row in repair_rows if row["Gate_Status"] == "HOLD")
    reviewed = sum(1 for row in repair_rows if row["Gate_Status"] == "REVIEW")
    REPAIR_MD.write_text(
        "\n".join(
            [
                "# Etsy V7 Planner Local Repair",
                "",
                f"- Generated: {now_text()}",
                f"- Repaired: {len(repair_rows)}",
                f"- PASS: {passed}",
                f"- REVIEW: {reviewed}",
                f"- HOLD: {held}",
                "",
                "Repair rule: upscale/crop to printable planner ratio, preserve border atmosphere, and inject a physical clean writing panel.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair POOL09 planner art with local clean-center layout")
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE))
    parser.add_argument("--qa", default=str(DEFAULT_QA))
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    return run(args.limit, Path(args.queue), Path(args.qa))


if __name__ == "__main__":
    raise SystemExit(main())
