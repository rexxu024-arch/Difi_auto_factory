import argparse
import math
import os
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageStat

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


PRODUCT_SPECS = {
    "Poster": {
        "spec": "Premium-Matte-Vertical",
        "production_size": (3600, 5400),
        "cover_size": (1800, 2700),
        "min_source_dim": 1024,
    },
    "Acrylic": {
        "spec": "Photo-Block",
        "production_size": (1538, 2138),
        "cover_size": (1500, 2100),
        "min_source_dim": 1024,
    },
}


def _folder_id(folder):
    return folder.name.replace("MASTER_", "").replace("_Ready_for_Steaming", "").replace("-Review", "")


def _u_paths(folder, item_id):
    paths = []
    for index in range(1, 5):
        candidates = [
            folder / f"{item_id}_U{index}.png",
            folder / f"{item_id}_U{index}_Grid.png",
            folder / f"Grid{index}.png",
        ]
        found = next((path for path in candidates if path.exists()), None)
        if not found:
            return []
        paths.append(found)
    return paths


def _sharpness_score(path):
    with Image.open(path) as image:
        gray = image.convert("L").resize((512, 512), Image.Resampling.LANCZOS)
        edges = gray.filter(ImageFilter.FIND_EDGES)
        stat = ImageStat.Stat(edges)
        contrast = ImageStat.Stat(gray).stddev[0]
        return stat.mean[0] + contrast * 0.35


def _fit_cover(image, target_size):
    src_w, src_h = image.size
    dst_w, dst_h = target_size
    scale = max(dst_w / src_w, dst_h / src_h)
    resized = image.resize((math.ceil(src_w * scale), math.ceil(src_h * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - dst_w) // 2)
    top = max(0, (resized.height - dst_h) // 2)
    return resized.crop((left, top, left + dst_w, top + dst_h))


def _polish_preview(image):
    image = ImageEnhance.Sharpness(image).enhance(1.08)
    image = ImageEnhance.Contrast(image).enhance(1.04)
    return image


def _write_png(image, path):
    image.save(path, "PNG", dpi=(300, 300), optimize=True)


def _ensure_metadata(folder, item_id):
    meta = folder / "metadata.txt"
    if not meta.exists():
        meta.write_text(f"ID: {item_id}\n", encoding="utf-8")


def process_folder(folder, product_type, force=False):
    spec = PRODUCT_SPECS[product_type]
    item_id = _folder_id(folder)
    u_paths = _u_paths(folder, item_id)
    if len(u_paths) != 4:
        return False, f"{item_id}: missing U1-U4"
    sizes = []
    for path in u_paths:
        with Image.open(path) as image:
            sizes.append(image.size)
    low = [f"{path.name}={size[0]}x{size[1]}" for path, size in zip(u_paths, sizes) if min(size) < spec["min_source_dim"]]
    if low:
        return False, f"{item_id}: low source resolution {'; '.join(low)}"

    scores = [(path, _sharpness_score(path)) for path in u_paths]
    best_path = max(scores, key=lambda item: item[1])[0]
    with Image.open(best_path) as source:
        source = source.convert("RGB")
        production = _fit_cover(source, spec["production_size"])
        cover = _polish_preview(_fit_cover(source, spec["cover_size"]))

    production_path = folder / "Production_Design.png"
    cover_path = folder / "Cover_Mockup.png"
    if force or not production_path.exists():
        _write_png(production, production_path)
    if force or not cover_path.exists():
        _write_png(cover, cover_path)
    _ensure_metadata(folder, item_id)
    return True, f"{item_id}: best={best_path.name} score={max(score for _, score in scores):.2f}"


def build_assets(product_type, limit=0, force=False):
    product_type = "Acrylic" if product_type.lower().startswith("acry") else "Poster"
    spec = PRODUCT_SPECS[product_type]
    root = PROJECT_ROOT / "Output" / product_type / spec["spec"]
    log_path = PROJECT_ROOT / "Database" / f"{product_type.lower()}_asset_audit.log"
    root.mkdir(parents=True, exist_ok=True)
    candidates = sorted(
        folder for folder in root.iterdir()
        if folder.is_dir() and folder.name.startswith("MASTER_") and folder.name.endswith("_Ready_for_Steaming")
    )
    if limit:
        candidates = candidates[:limit]
    ok = 0
    notes = []
    for folder in candidates:
        success, note = process_folder(folder, product_type, force=force)
        notes.append(("OK" if success else "HOLD") + " | " + note)
        if success:
            ok += 1
        else:
            hold = folder.with_name(folder.name.replace("_Ready_for_Steaming", "_Not_Working_Asset"))
            if not hold.exists():
                folder.rename(hold)
    log_path.write_text("\n".join(notes) + ("\n" if notes else ""), encoding="utf-8")
    print(f"[ART-ASSET] {product_type}: {ok}/{len(candidates)} ready")
    return ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("product_type", choices=["Poster", "Acrylic"])
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    build_assets(args.product_type, limit=args.limit, force=args.force)
