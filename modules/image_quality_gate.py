import argparse
import csv
import sys
from pathlib import Path

from PIL import Image, ImageFilter, ImageStat

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = PROJECT_ROOT / "Database" / "Image_Quality_Gate.csv"


def _metrics(path):
    with Image.open(path) as image:
        image = image.convert("RGB")
        gray = image.convert("L")
        small = gray.resize((512, 512), Image.Resampling.LANCZOS)
        stat = ImageStat.Stat(small)
        pixels = list(small.getdata())
        total = len(pixels)
        black_clip = sum(1 for pixel in pixels if pixel <= 3) / total
        white_clip = sum(1 for pixel in pixels if pixel >= 252) / total
        edges = small.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        return {
            "width": image.width,
            "height": image.height,
            "mean_luma": stat.mean[0],
            "stddev_luma": stat.stddev[0],
            "black_clip_pct": black_clip * 100,
            "white_clip_pct": white_clip * 100,
            "edge_energy": edge_stat.mean[0],
        }


def _verdict(m):
    reasons = []
    if min(m["width"], m["height"]) < 1200:
        reasons.append("LOW_RESOLUTION")
    if m["black_clip_pct"] > 18:
        reasons.append("SHADOW_CLIPPING")
    if m["white_clip_pct"] > 18:
        reasons.append("HIGHLIGHT_CLIPPING")
    if m["stddev_luma"] < 24:
        reasons.append("LOW_CONTRAST_MUDDY")
    if m["stddev_luma"] > 95 and (m["black_clip_pct"] + m["white_clip_pct"]) > 12:
        reasons.append("OVERDRAMATIC_FAKE_CONTRAST")
    if m["edge_energy"] < 7:
        reasons.append("LOW_SHARPNESS_OR_SOFT_DETAIL")
    hard = {"LOW_RESOLUTION", "SHADOW_CLIPPING", "HIGHLIGHT_CLIPPING"}
    if any(reason in hard for reason in reasons):
        return "HOLD", ";".join(reasons)
    if reasons:
        return "REVIEW_RECOMMENDED", ";".join(reasons)
    return "PASS", ""


def audit_paths(paths, append=True):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    exists = REPORT_PATH.exists() and append
    mode = "a" if append else "w"
    rows = []
    with REPORT_PATH.open(mode, encoding="utf-8-sig", newline="") as handle:
        fieldnames = [
            "Path",
            "Verdict",
            "Reason",
            "Width",
            "Height",
            "Mean_Luma",
            "Stddev_Luma",
            "Black_Clip_Pct",
            "White_Clip_Pct",
            "Edge_Energy",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        for raw in paths:
            path = Path(raw)
            try:
                m = _metrics(path)
                verdict, reason = _verdict(m)
                row = {
                    "Path": str(path),
                    "Verdict": verdict,
                    "Reason": reason,
                    "Width": m["width"],
                    "Height": m["height"],
                    "Mean_Luma": f"{m['mean_luma']:.2f}",
                    "Stddev_Luma": f"{m['stddev_luma']:.2f}",
                    "Black_Clip_Pct": f"{m['black_clip_pct']:.2f}",
                    "White_Clip_Pct": f"{m['white_clip_pct']:.2f}",
                    "Edge_Energy": f"{m['edge_energy']:.2f}",
                }
            except Exception as exc:
                row = {
                    "Path": str(path),
                    "Verdict": "HOLD",
                    "Reason": f"ERROR:{exc}",
                    "Width": "",
                    "Height": "",
                    "Mean_Luma": "",
                    "Stddev_Luma": "",
                    "Black_Clip_Pct": "",
                    "White_Clip_Pct": "",
                    "Edge_Energy": "",
                }
            writer.writerow(row)
            rows.append(row)
            print(f"[IMAGE-QA] {Path(row['Path']).name} {row['Verdict']} {row['Reason']}")
    return rows


def _discover(root, limit=0):
    root = Path(root)
    if root.is_file():
        return [root]
    paths = []
    for pattern in ("Production_Design.png", "Cover_Mockup.png", "*.jpg", "*.jpeg", "*.png"):
        for path in root.rglob(pattern):
            if path not in paths:
                paths.append(path)
            if limit and len(paths) >= limit:
                return paths
    return paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args()
    paths = []
    for raw in args.paths:
        paths.extend(_discover(raw, limit=args.limit))
    if args.limit:
        paths = paths[: args.limit]
    audit_paths(paths, append=not args.fresh)


if __name__ == "__main__":
    main()
