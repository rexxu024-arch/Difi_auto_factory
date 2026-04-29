import io
import os
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageFilter
from rembg import new_session, remove

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.spec_registry import Registry


REMBG_SESSION = new_session("u2net", providers=["CPUExecutionProvider"])


STICKER_KISS_CUT_CONFIG = {
    "production_canvas_size": 1664,
    "cover_canvas_size": 1800,
    "production_margin": 0,
    "production_center_gap": 32,
    "min_tile_area_ratio": 0.94,
    "cover_margin": 90,
    "safe_zone": 150,
    "shadow_offset": 10,
    "shadow_blur": 12,
}


def _clean_master_id(folder_path):
    return (
        os.path.basename(folder_path)
        .replace("MASTER_", "")
        .replace("_Completed", "")
        .replace("_Ready_for_Steaming", "")
    )


def _remove_background(image):
    buffer = io.BytesIO()
    image.convert("RGBA").save(buffer, format="PNG")
    cleaned = remove(buffer.getvalue(), session=REMBG_SESSION)
    return Image.open(io.BytesIO(cleaned)).convert("RGBA")


def _trim_alpha(image, padding=12):
    alpha = image.getchannel("A")
    solid_alpha = alpha.point(lambda value: 255 if value > 24 else 0)
    bbox = solid_alpha.getbbox()
    if not bbox:
        return image
    left = max(0, bbox[0] - padding)
    top = max(0, bbox[1] - padding)
    right = min(image.width, bbox[2] + padding)
    bottom = min(image.height, bbox[3] + padding)
    return image.crop((left, top, right, bottom))


def _trim_light_background(image, padding=8):
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    xs = []
    ys = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a < 16:
                continue
            # Keep pale but intentional details; discard only the near-white paper field.
            if min(r, g, b) < 238 or (max(r, g, b) - min(r, g, b)) > 18:
                xs.append(x)
                ys.append(y)
    if not xs:
        return rgba
    left = max(0, min(xs) - padding)
    top = max(0, min(ys) - padding)
    right = min(width, max(xs) + padding + 1)
    bottom = min(height, max(ys) + padding + 1)
    return rgba.crop((left, top, right, bottom))


def _white_to_alpha(image):
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            distance = ((255 - r) ** 2 + (255 - g) ** 2 + (255 - b) ** 2) ** 0.5
            if distance <= 18:
                pixels[x, y] = (r, g, b, 0)
            elif distance <= 58:
                alpha_scale = min(1.0, (distance - 18) / 40)
                pixels[x, y] = (r, g, b, round(a * alpha_scale))
    return rgba


def _preserve_quadrant(image):
    rgba = image.convert("RGBA")
    alpha = Image.new("L", rgba.size, 255)
    rgba.putalpha(alpha)
    return rgba


def _alpha_bbox(image, threshold=24):
    alpha = image.getchannel("A")
    return alpha.point(lambda value: 255 if value > threshold else 0).getbbox()


def _alpha_area_ratio(image, threshold=24):
    bbox = _alpha_bbox(image, threshold)
    if not bbox:
        return 0
    return ((bbox[2] - bbox[0]) * (bbox[3] - bbox[1])) / max(1, image.width * image.height)


def _alpha_coverage_ratio(image, threshold=16):
    alpha = image.getchannel("A")
    solid = sum(1 for value in alpha.getdata() if value > threshold)
    return solid / max(1, image.width * image.height)


def _visual_coverage_ratio(image):
    rgba = image.convert("RGBA")
    pixels = rgba.getdata()
    solid = 0
    for r, g, b, a in pixels:
        if a < 16:
            continue
        if min(r, g, b) < 245 or (max(r, g, b) - min(r, g, b)) > 12:
            solid += 1
    return solid / max(1, rgba.width * rgba.height)


def _fit_to_box(image, box_size):
    result = _trim_alpha(image)
    scale = min(box_size / result.width, box_size / result.height)
    new_size = (max(1, round(result.width * scale)), max(1, round(result.height * scale)))
    return result.resize(new_size, Image.Resampling.LANCZOS)


def _grid_quadrants(grid_image):
    w, h = grid_image.size
    mid_x, mid_y = w // 2, h // 2
    boxes = [
        (0, 0, mid_x, mid_y),
        (mid_x, 0, w, mid_y),
        (0, mid_y, mid_x, h),
        (mid_x, mid_y, w, h),
    ]
    return [grid_image.crop(box).convert("RGBA") for box in boxes]


def _slot_positions(canvas_size, thumb_size, gap):
    total = thumb_size * 2 + gap
    start = (canvas_size - total) // 2
    return [
        (start, start),
        (start + thumb_size + gap, start),
        (start, start + thumb_size + gap),
        (start + thumb_size + gap, start + thumb_size + gap),
    ]


def _paste_centered(canvas, sticker, slot_pos, slot_size, shadow=False):
    x, y = slot_pos
    px = x + (slot_size - sticker.width) // 2
    py = y + (slot_size - sticker.height) // 2
    if shadow:
        cfg = STICKER_KISS_CUT_CONFIG
        shadow_mask = sticker.getchannel("A").filter(ImageFilter.GaussianBlur(cfg["shadow_blur"]))
        shadow_layer = Image.new("RGBA", sticker.size, (0, 0, 0, 42))
        canvas.paste(
            shadow_layer,
            (px + cfg["shadow_offset"], py + cfg["shadow_offset"]),
            shadow_mask,
        )
    canvas.paste(sticker, (px, py), sticker)


def _write_png(image, path):
    image.save(path, "PNG", dpi=(300, 300))


def _normalize_cover_grid(grid_path, output_path, canvas_size, margin):
    grid = Image.open(grid_path).convert("RGBA")
    cover = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))
    max_size = max(1, canvas_size - margin * 2)
    scale = min(max_size / grid.width, max_size / grid.height)
    new_size = (max(1, round(grid.width * scale)), max(1, round(grid.height * scale)))
    grid = grid.resize(new_size, Image.Resampling.LANCZOS)
    pos = ((canvas_size - grid.width) // 2, (canvas_size - grid.height) // 2)
    cover.paste(grid, pos, grid)
    _write_png(cover, output_path)


def _main_grid_path(folder, master_id):
    direct = folder / f"{master_id}_Grid.png"
    if direct.exists():
        return direct
    candidates = sorted(
        p for p in folder.glob("*_Grid.*")
        if "_U" not in p.name and p.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )
    return candidates[0] if candidates else None


def _u_paths(folder, master_id):
    paths = []
    for index in range(1, 5):
        candidates = [
            folder / f"{master_id}_U{index}_Grid.png",
            folder / f"{master_id}_U{index}.png",
            folder / f"Grid{index}.png",
        ]
        found = next((path for path in candidates if path.exists()), None)
        if not found:
            return []
        paths.append(found)
    return paths


def process_sticker_kiss_cut(folder_path):
    """
    Sticker Kiss-Cut stage:
    - Production_Design.png starts from the original Grid, removes its background once,
      then shrinks the four quadrants just enough to create a center cross cut line.
    - Cover_Mockup.png keeps the original Grid composition with only a small safe margin.
    - Production output keeps the outer edges full and guards against excessive tile shrink.
    """
    folder = Path(folder_path)
    master_id = _clean_master_id(folder_path)
    cfg = STICKER_KISS_CUT_CONFIG

    grid_path = _main_grid_path(folder, master_id)
    if not grid_path:
        print(f"  [SKIP] Missing Grid asset: {master_id}")
        return False

    print(f"  [IRON] Processing {master_id}")

    production_size = cfg["production_canvas_size"]
    production_canvas = Image.new("RGBA", (production_size, production_size), (255, 255, 255, 0))
    source_grid = Image.open(grid_path).convert("RGBA")
    tile_size = (production_size - cfg["production_center_gap"]) // 2
    tile_area_ratio = (tile_size / (production_size / 2)) ** 2
    if tile_area_ratio < cfg["min_tile_area_ratio"]:
        print(f"  [SKIP] Center gap shrinks tile area too much: {tile_area_ratio:.2%}")
        return False
    right_x = production_size - tile_size
    bottom_y = production_size - tile_size
    positions = [
        (0, 0),
        (right_x, 0),
        (0, bottom_y),
        (right_x, bottom_y),
    ]
    grid_quadrants = _grid_quadrants(source_grid)
    for index, quadrant in enumerate(grid_quadrants, 1):
        print(f"    [CUT] Grid Q{index} independent removal...", end="\r")
        original_coverage = _visual_coverage_ratio(quadrant)
        sticker = _remove_background(quadrant)
        sticker_coverage = _alpha_coverage_ratio(sticker)
        if sticker_coverage < 0.08 or (
            original_coverage > 0.18 and sticker_coverage < original_coverage * 0.45
        ):
            print(f"    [CUT] Grid Q{index} fallback soft white removal...", end="\r")
            sticker = _white_to_alpha(quadrant)
            sticker_coverage = _alpha_coverage_ratio(sticker)
        if sticker_coverage < 0.08 or (
            original_coverage > 0.18 and sticker_coverage < original_coverage * 0.45
        ):
            print(f"    [CUT] Grid Q{index} fallback preserved quadrant...", end="\r")
            sticker = _preserve_quadrant(quadrant)
        sticker = sticker.resize((tile_size, tile_size), Image.Resampling.LANCZOS)
        pos = positions[index - 1]
        production_canvas.paste(sticker, pos, sticker)
    _write_png(production_canvas, folder / "Production_Design.png")

    _normalize_cover_grid(grid_path, folder / "Cover_Mockup.png", cfg["cover_canvas_size"], cfg["cover_margin"])

    print(f"  [OK] {master_id} -> Production_Design.png + Cover_Mockup.png")
    return True


def run_logic():
    print("\n--- INITIALIZING IRON_AUDIT ---")

    for key, value in Registry.CATALOG.items():
        print(f"[{key}] {value.name}")
    type_choice = input("Confirm audit product type (default 1): ") or "1"
    product = Registry.CATALOG.get(type_choice, Registry.STICKER)

    for index, spec_name in enumerate(product.specs, 1):
        print(f"[{index}] {spec_name}")
    spec_idx = int(input(f"Confirm {product.name} audit spec (default 1): ") or "1") - 1
    spec = product.specs[spec_idx]

    target_dir = Path("Output") / product.name / spec
    if not target_dir.exists():
        print(f"[SKIP] Missing audit path: {target_dir}")
        return

    subfolders = [path for path in target_dir.iterdir() if path.is_dir()]
    active_tasks = [
        path for path in subfolders
        if path.name.startswith("MASTER_")
        and not path.name.endswith("_Completed")
        and not path.name.endswith("_Ready_for_Steaming")
    ]
    limit = int(os.getenv("IRON_AUDIT_LIMIT", "0") or "0")
    if limit:
        active_tasks = active_tasks[:limit]

    print(f"[SCAN] Pending audit folders: {len(active_tasks)}")

    for folder in active_tasks:
        if product.name == "Sticker" and spec == "Kiss-Cut":
            if process_sticker_kiss_cut(folder):
                new_path = folder.with_name(folder.name + "_Ready_for_Steaming")
                if new_path.exists():
                    print(f"  [WARN] Target folder already exists, skip rename: {new_path}")
                    continue
                shutil.move(str(folder), str(new_path))
                print(f"[SUCCESS] {folder.name} -> _Ready_for_Steaming")
        else:
            print(f"[WARN] No audit logic for {product.name}-{spec}")


if __name__ == "__main__":
    run_logic()
