"""Build a local A/B scorecard for Project Mirror draft grids.

The goal is not to replace Rex/Gemini visual taste.  It gives us a cheap,
repeatable first-pass signal so reference-derived DNA can be compared against
the old prompt style before spending upscale or marketplace attention.
"""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageFilter, ImageStat


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "Database"
REVIEW = ROOT / "Review_Packets" / "Project_Mirror"
QUEUE = DB / "Project_Mirror_MJ_Dispatch_Queue.csv"
OUT_CSV = DB / "Project_Mirror_AB_Scorecard.csv"
OUT_MD = REVIEW / "PROJECT_MIRROR_AB_SCORECARD.md"


def clean(value: object) -> str:
    return str(value or "").strip()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else [
        "Pair_ID",
        "Variant",
        "Internal_SKU",
        "Grid_File",
        "Sharpness",
        "Contrast",
        "Color_Depth",
        "Composition_Balance",
        "Premium_Signal",
        "Score",
        "Winner",
        "Notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def norm(value: float, low: float, high: float) -> float:
    if high <= low:
        return 0.0
    return max(0.0, min(100.0, (value - low) / (high - low) * 100.0))


def entropy(gray: Image.Image) -> float:
    hist = gray.histogram()
    total = sum(hist) or 1
    ent = 0.0
    for count in hist:
        if count:
            p = count / total
            ent -= p * math.log2(p)
    return ent


def image_metrics(path: Path) -> dict[str, float]:
    img = Image.open(path).convert("RGB")
    # Downsample for stable and fast metrics; grids only need coarse scoring.
    img.thumbnail((768, 768))
    gray = img.convert("L")
    stat = ImageStat.Stat(img)
    gray_stat = ImageStat.Stat(gray)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_stat = ImageStat.Stat(edges)

    sharpness_raw = edge_stat.var[0] if edge_stat.var else 0.0
    contrast_raw = gray_stat.stddev[0] if gray_stat.stddev else 0.0
    color_raw = sum(stat.stddev[:3]) / 3.0 if stat.stddev else 0.0
    ent_raw = entropy(gray)

    # Penalize extremely lopsided brightness; premium product art usually has
    # hierarchy, but the draft should not collapse into pure black or blown white.
    mean_luma = gray_stat.mean[0] if gray_stat.mean else 127.0
    balance = 100.0 - min(100.0, abs(mean_luma - 128.0) / 1.28)

    sharpness = norm(sharpness_raw, 50.0, 1800.0)
    contrast = norm(contrast_raw, 18.0, 78.0)
    color_depth = (norm(color_raw, 12.0, 68.0) * 0.55) + (norm(ent_raw, 4.0, 7.8) * 0.45)
    composition_balance = max(0.0, balance)

    premium_signal = (
        sharpness * 0.30
        + contrast * 0.25
        + color_depth * 0.25
        + composition_balance * 0.20
    )
    return {
        "Sharpness": round(sharpness, 2),
        "Contrast": round(contrast, 2),
        "Color_Depth": round(color_depth, 2),
        "Composition_Balance": round(composition_balance, 2),
        "Premium_Signal": round(premium_signal, 2),
        "Score": round(premium_signal, 2),
    }


def pair_id(internal_sku: str) -> str:
    sku = internal_sku
    for suffix in ("-A_OLD_LOGIC", "-B_PROJECT_MIRROR"):
        if sku.endswith(suffix):
            return sku[: -len(suffix)]
    return sku


def variant(internal_sku: str) -> str:
    if internal_sku.endswith("-B_PROJECT_MIRROR"):
        return "B_PROJECT_MIRROR"
    if internal_sku.endswith("-A_OLD_LOGIC"):
        return "A_OLD_LOGIC"
    return "UNKNOWN"


def build_scorecard() -> tuple[list[dict[str, object]], list[str]]:
    rows = []
    skipped = []
    for row in read_rows(QUEUE):
        if clean(row.get("Harvest_Status")) != "GRID_FOUND":
            continue
        grid = ROOT / clean(row.get("Grid_File"))
        if not grid.exists():
            skipped.append(clean(row.get("Internal_SKU")))
            continue
        metrics = image_metrics(grid)
        item: dict[str, object] = {
            "Pair_ID": pair_id(clean(row.get("Internal_SKU"))),
            "Variant": variant(clean(row.get("Internal_SKU"))),
            "Internal_SKU": clean(row.get("Internal_SKU")),
            "Grid_File": str(grid),
            **metrics,
            "Winner": "",
            "Notes": clean(row.get("Review_Note")),
        }
        rows.append(item)

    by_pair: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_pair[str(row["Pair_ID"])].append(row)

    for pair_rows in by_pair.values():
        if len(pair_rows) < 2:
            continue
        best = max(pair_rows, key=lambda r: float(r["Score"]))
        for row in pair_rows:
            row["Winner"] = "YES" if row is best else "NO"
    return rows, skipped


def write_report(rows: list[dict[str, object]], skipped: list[str]) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    pairs = sorted({str(row["Pair_ID"]) for row in rows})
    b_wins = sum(1 for row in rows if row["Variant"] == "B_PROJECT_MIRROR" and row["Winner"] == "YES")
    a_wins = sum(1 for row in rows if row["Variant"] == "A_OLD_LOGIC" and row["Winner"] == "YES")
    avg_a = [
        float(row["Score"]) for row in rows if row["Variant"] == "A_OLD_LOGIC"
    ]
    avg_b = [
        float(row["Score"]) for row in rows if row["Variant"] == "B_PROJECT_MIRROR"
    ]
    lines = [
        "# Project Mirror A/B Scorecard",
        "",
        f"Generated: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}",
        "",
        "This is a cheap local image-metric scorecard for draft grids only. It does not replace Rex/Gemini taste review.",
        "",
        "## Summary",
        f"- Complete evaluated pairs: {len(pairs)}",
        f"- Old-logic metric wins: {a_wins}",
        f"- Project-Mirror metric wins: {b_wins}",
        f"- Old-logic average score: {round(sum(avg_a) / len(avg_a), 2) if avg_a else 'n/a'}",
        f"- Project-Mirror average score: {round(sum(avg_b) / len(avg_b), 2) if avg_b else 'n/a'}",
        f"- Skipped missing grids: {len(skipped)}",
        "",
        "## Pair Winners",
        "| Pair | Winner | A Score | B Score |",
        "|---|---:|---:|---:|",
    ]
    by_pair: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_pair[str(row["Pair_ID"])].append(row)
    for pair in sorted(by_pair):
        a = next((r for r in by_pair[pair] if r["Variant"] == "A_OLD_LOGIC"), None)
        b = next((r for r in by_pair[pair] if r["Variant"] == "B_PROJECT_MIRROR"), None)
        winner = next((r["Variant"] for r in by_pair[pair] if r["Winner"] == "YES"), "INCOMPLETE")
        lines.append(
            f"| {pair} | {winner} | {a['Score'] if a else 'n/a'} | {b['Score'] if b else 'n/a'} |"
        )
    if skipped:
        lines += ["", "## Skipped", *[f"- {sku}" for sku in skipped]]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rows, skipped = build_scorecard()
    write_rows(OUT_CSV, rows)
    write_report(rows, skipped)
    b_wins = sum(1 for row in rows if row["Variant"] == "B_PROJECT_MIRROR" and row["Winner"] == "YES")
    a_wins = sum(1 for row in rows if row["Variant"] == "A_OLD_LOGIC" and row["Winner"] == "YES")
    print(f"[PROJECT-MIRROR-SCORECARD] rows={len(rows)} pairs={len({r['Pair_ID'] for r in rows})} old_wins={a_wins} mirror_wins={b_wins} csv={OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
