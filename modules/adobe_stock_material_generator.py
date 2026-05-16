"""Generate Adobe-safe procedural material/background pilot assets.

These are stock "bricks", not OpenClaw finished product artwork. The generator
creates local 4K JPEG files, attaches Source_Path to the Adobe pilot batch, and
leaves upload blocked until image and metadata QA pass.
"""

from __future__ import annotations

import argparse
import csv
import math
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from adobe_stock_isolation import assert_adobe_write_paths


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
FACTORY = PROJECT_ROOT / "adobe_stock_factory"
ASSETS = FACTORY / "assets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

BATCH = DATABASE / "Adobe_Stock_Pilot_Batch.csv"
QUEUE = DATABASE / "Adobe_Stock_Pilot_Queue.csv"

DEFAULT_SIZE = 4096
DEFAULT_COUNT = 12


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def today_slug() -> str:
    return datetime.now(NY_TZ).strftime("%Y%m%d")


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def noise(size: int, seed: int, octaves: int = 5) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out = np.zeros((size, size), dtype=np.float32)
    weight_sum = 0.0
    for octave in range(octaves):
        low = max(8, size // (2 ** (octave + 5)))
        base = rng.random((low, low), dtype=np.float32)
        img = Image.fromarray((base * 255).astype(np.uint8), "L").resize((size, size), Image.Resampling.BICUBIC)
        weight = 1.0 / (2 ** octave)
        out += np.asarray(img, dtype=np.float32) / 255.0 * weight
        weight_sum += weight
    out /= weight_sum
    return out


def to_image(arr: np.ndarray) -> Image.Image:
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def smoky_jade(size: int, seed: int) -> Image.Image:
    n1 = noise(size, seed, 6)
    n2 = noise(size, seed + 11, 4)
    y, x = np.mgrid[0:size, 0:size] / size
    veins = 0.5 + 0.5 * np.sin((x * 8 + y * 4 + n2 * 3.2) * math.pi)
    highlight = np.exp(-((x - 0.32) ** 2 + (y - 0.22) ** 2) / 0.025)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 30 + n1 * 28 + veins * 10
    arr[..., 1] = 70 + n1 * 80 + veins * 42 + highlight * 25
    arr[..., 2] = 63 + n2 * 70 + veins * 32 + highlight * 35
    return to_image(arr).filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=3))


def kintsugi_marble(size: int, seed: int) -> Image.Image:
    n = noise(size, seed, 6)
    y, x = np.mgrid[0:size, 0:size] / size
    marble = 0.5 + 0.5 * np.sin((x * 10 + y * 5 + n * 4.5) * math.pi)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 182 + marble * 45 + n * 20
    arr[..., 1] = 174 + marble * 39 + n * 16
    arr[..., 2] = 158 + marble * 32 + n * 12
    img = to_image(arr).filter(ImageFilter.GaussianBlur(0.35))
    draw = ImageDraw.Draw(img, "RGBA")
    rng = np.random.default_rng(seed)
    for _ in range(9):
        x0 = int(rng.integers(0, size))
        y0 = int(rng.integers(0, size))
        points = [(x0, y0)]
        for _ in range(7):
            x0 += int(rng.integers(-420, 421))
            y0 += int(rng.integers(260, 620))
            points.append((max(0, min(size, x0)), max(0, min(size, y0))))
        draw.line(points, fill=(176, 130, 56, 150), width=max(4, size // 360), joint="curve")
        draw.line(points, fill=(255, 214, 128, 120), width=max(1, size // 900), joint="curve")
    return img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=90, threshold=4))


def brushed_titanium(size: int, seed: int) -> Image.Image:
    rng = np.random.default_rng(seed)
    base = noise(size, seed, 4)
    horizontal = rng.normal(0, 1, (size, 1)).astype(np.float32)
    horizontal = np.repeat(horizontal, size, axis=1)
    horizontal = (horizontal - horizontal.min()) / (horizontal.max() - horizontal.min())
    y, x = np.mgrid[0:size, 0:size] / size
    sheen = 0.5 + 0.5 * np.sin((y * 35 + base * 0.8) * math.pi)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 104 + base * 34 + horizontal * 18 + sheen * 20
    arr[..., 1] = 110 + base * 36 + horizontal * 20 + sheen * 20
    arr[..., 2] = 116 + base * 42 + horizontal * 22 + sheen * 26
    img = to_image(arr)
    draw = ImageDraw.Draw(img, "RGBA")
    for _ in range(220):
        y0 = int(rng.integers(0, size))
        x0 = int(rng.integers(0, size // 3))
        length = int(rng.integers(size // 10, size // 2))
        draw.line((x0, y0, min(size, x0 + length), y0 + int(rng.integers(-2, 3))), fill=(230, 235, 238, 25), width=1)
    return img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=130, threshold=5))


def archival_vellum(size: int, seed: int) -> Image.Image:
    n = noise(size, seed, 7)
    fine = noise(size, seed + 15, 3)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 214 + n * 25 + fine * 10
    arr[..., 1] = 202 + n * 21 + fine * 8
    arr[..., 2] = 174 + n * 16 + fine * 6
    img = to_image(arr)
    draw = ImageDraw.Draw(img, "RGBA")
    rng = np.random.default_rng(seed)
    for _ in range(500):
        x0 = int(rng.integers(0, size))
        y0 = int(rng.integers(0, size))
        length = int(rng.integers(size // 80, size // 15))
        color = (92, 79, 55, int(rng.integers(10, 28)))
        draw.line((x0, y0, min(size, x0 + length), y0 + int(rng.integers(-8, 9))), fill=color, width=1)
    return img.filter(ImageFilter.GaussianBlur(0.25))


def obsidian_glass(size: int, seed: int) -> Image.Image:
    n = noise(size, seed, 5)
    y, x = np.mgrid[0:size, 0:size] / size
    vignette = np.sqrt((x - 0.5) ** 2 + (y - 0.5) ** 2)
    reflection = np.exp(-((x - 0.28) ** 2 + (y - 0.18) ** 2) / 0.014)
    smoke = 0.5 + 0.5 * np.sin((x * 5 - y * 7 + n * 5) * math.pi)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 12 + n * 30 + smoke * 18 + reflection * 70 - vignette * 14
    arr[..., 1] = 16 + n * 32 + smoke * 22 + reflection * 78 - vignette * 15
    arr[..., 2] = 20 + n * 43 + smoke * 35 + reflection * 95 - vignette * 16
    return to_image(arr).filter(ImageFilter.UnsharpMask(radius=1.2, percent=100, threshold=3))


def manhattan_order(size: int, seed: int) -> Image.Image:
    base = noise(size, seed, 6)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 85 + base * 42
    arr[..., 1] = 82 + base * 38
    arr[..., 2] = 74 + base * 32
    img = to_image(arr)
    draw = ImageDraw.Draw(img, "RGBA")
    rng = np.random.default_rng(seed)
    step = size // 8
    brass = (176, 134, 74, 120)
    for offset in range(-size, size * 2, step):
        draw.line((offset, 0, offset - size, size), fill=brass, width=max(3, size // 450))
        draw.line((offset, 0, offset + size, size), fill=(230, 188, 110, 70), width=max(1, size // 900))
    for _ in range(24):
        x0 = int(rng.integers(0, size))
        y0 = int(rng.integers(0, size))
        r = int(rng.integers(size // 22, size // 9))
        draw.rectangle((x0 - r, y0 - r, x0 + r, y0 + r), outline=(220, 180, 102, 65), width=max(2, size // 700))
    return img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=80, threshold=4))


def nero_marble(size: int, seed: int) -> Image.Image:
    n1 = noise(size, seed, 6)
    n2 = noise(size, seed + 31, 5)
    y, x = np.mgrid[0:size, 0:size] / size
    flow = x * 9.0 + y * 3.4 + n1 * 4.8
    veins = np.abs(np.sin(flow * math.pi))
    sharp_veins = np.clip((veins - 0.92) * 12, 0, 1)
    soft_veins = np.clip((veins - 0.78) * 4, 0, 1)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 16 + n1 * 28 + n2 * 12 + soft_veins * 62 + sharp_veins * 160
    arr[..., 1] = 15 + n1 * 26 + n2 * 10 + soft_veins * 58 + sharp_veins * 154
    arr[..., 2] = 14 + n1 * 24 + n2 * 9 + soft_veins * 52 + sharp_veins * 146
    img = to_image(arr).filter(ImageFilter.GaussianBlur(0.25))
    return img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=120, threshold=3))


def travertine_plaster(size: int, seed: int) -> Image.Image:
    n = noise(size, seed, 7)
    pores = noise(size, seed + 7, 3)
    y, x = np.mgrid[0:size, 0:size] / size
    strata = 0.5 + 0.5 * np.sin((y * 26 + n * 1.6) * math.pi)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 158 + n * 36 + strata * 18 - pores * 8
    arr[..., 1] = 143 + n * 32 + strata * 15 - pores * 8
    arr[..., 2] = 119 + n * 26 + strata * 11 - pores * 7
    img = to_image(arr).filter(ImageFilter.GaussianBlur(0.35))
    draw = ImageDraw.Draw(img, "RGBA")
    rng = np.random.default_rng(seed)
    for _ in range(1400):
        px = int(rng.integers(0, size))
        py = int(rng.integers(0, size))
        r = int(rng.integers(1, max(2, size // 900)))
        shade = int(rng.integers(32, 74))
        draw.ellipse((px - r, py - r, px + r, py + r), fill=(shade, shade, shade, int(rng.integers(15, 36))))
    return img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=5))


def walnut_burl(size: int, seed: int) -> Image.Image:
    n = noise(size, seed, 6)
    y, x = np.mgrid[0:size, 0:size] / size
    rng = np.random.default_rng(seed)
    rings = np.zeros((size, size), dtype=np.float32)
    for _ in range(14):
        cx = float(rng.random())
        cy = float(rng.random())
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        rings += 0.5 + 0.5 * np.sin((dist * rng.uniform(28, 52) + n * 2.0) * math.pi)
    rings /= max(rings.max(), 1)
    grain = 0.5 + 0.5 * np.sin((x * 28 + n * 7) * math.pi)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 72 + rings * 92 + grain * 28 + n * 18
    arr[..., 1] = 42 + rings * 48 + grain * 14 + n * 11
    arr[..., 2] = 20 + rings * 24 + grain * 8 + n * 7
    return to_image(arr).filter(ImageFilter.UnsharpMask(radius=1.1, percent=120, threshold=4))


def aged_bronze_patina(size: int, seed: int) -> Image.Image:
    n1 = noise(size, seed, 6)
    n2 = noise(size, seed + 21, 5)
    y, x = np.mgrid[0:size, 0:size] / size
    oxidation = np.clip((n2 + 0.2 * np.sin((x * 5 + y * 8) * math.pi) - 0.52) * 2.4, 0, 1)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 92 + n1 * 68 - oxidation * 34
    arr[..., 1] = 57 + n1 * 42 + oxidation * 92
    arr[..., 2] = 31 + n1 * 24 + oxidation * 86
    img = to_image(arr)
    draw = ImageDraw.Draw(img, "RGBA")
    rng = np.random.default_rng(seed)
    for _ in range(260):
        x0 = int(rng.integers(0, size))
        y0 = int(rng.integers(0, size))
        r = int(rng.integers(size // 120, size // 30))
        draw.ellipse((x0 - r, y0 - r, x0 + r, y0 + r), outline=(42, 166, 142, 35), width=max(1, size // 900))
    return img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=100, threshold=4))


def linen_canvas(size: int, seed: int) -> Image.Image:
    n = noise(size, seed, 5)
    y, x = np.mgrid[0:size, 0:size] / size
    warp = 0.5 + 0.5 * np.sin((x * size / 9 + n * 1.4) * math.pi)
    weft = 0.5 + 0.5 * np.sin((y * size / 8 + n * 1.2) * math.pi)
    weave = (warp * 0.55 + weft * 0.45)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 185 + weave * 38 + n * 14
    arr[..., 1] = 174 + weave * 32 + n * 12
    arr[..., 2] = 151 + weave * 24 + n * 10
    return to_image(arr).filter(ImageFilter.UnsharpMask(radius=1.0, percent=100, threshold=4))


def architectural_concrete(size: int, seed: int) -> Image.Image:
    n1 = noise(size, seed, 7)
    n2 = noise(size, seed + 17, 4)
    y, x = np.mgrid[0:size, 0:size] / size
    trowel = 0.5 + 0.5 * np.sin((x * 3.0 + y * 9.0 + n2 * 2.5) * math.pi)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 101 + n1 * 48 + trowel * 12
    arr[..., 1] = 104 + n1 * 46 + trowel * 12
    arr[..., 2] = 103 + n1 * 42 + trowel * 10
    img = to_image(arr).filter(ImageFilter.GaussianBlur(0.25))
    draw = ImageDraw.Draw(img, "RGBA")
    rng = np.random.default_rng(seed)
    for _ in range(900):
        px = int(rng.integers(0, size))
        py = int(rng.integers(0, size))
        draw.point((px, py), fill=(35, 38, 39, int(rng.integers(35, 95))))
    return img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=90, threshold=4))


def carbon_fiber(size: int, seed: int) -> Image.Image:
    n = noise(size, seed, 3)
    y, x = np.mgrid[0:size, 0:size] / size
    diag1 = 0.5 + 0.5 * np.sin(((x + y) * size / 24 + n * 0.8) * math.pi)
    diag2 = 0.5 + 0.5 * np.sin(((x - y) * size / 24 + n * 0.8) * math.pi)
    weave = np.where(((x + y) * size // 64) % 2 == 0, diag1, diag2)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 15 + weave * 42 + n * 15
    arr[..., 1] = 17 + weave * 43 + n * 15
    arr[..., 2] = 19 + weave * 48 + n * 17
    return to_image(arr).filter(ImageFilter.UnsharpMask(radius=1.0, percent=150, threshold=3))


def champagne_frosted_glass(size: int, seed: int) -> Image.Image:
    n = noise(size, seed, 6)
    y, x = np.mgrid[0:size, 0:size] / size
    gradient = (1 - y) * 0.55 + x * 0.25
    caustic = np.exp(-((x - 0.72) ** 2 + (y - 0.28) ** 2) / 0.035)
    arr = np.zeros((size, size, 3), dtype=np.float32)
    arr[..., 0] = 186 + gradient * 52 + n * 16 + caustic * 24
    arr[..., 1] = 166 + gradient * 42 + n * 12 + caustic * 18
    arr[..., 2] = 127 + gradient * 28 + n * 9 + caustic * 12
    img = to_image(arr).filter(ImageFilter.GaussianBlur(0.45))
    draw = ImageDraw.Draw(img, "RGBA")
    rng = np.random.default_rng(seed)
    for _ in range(18):
        x0 = int(rng.integers(-size // 4, size))
        y0 = int(rng.integers(0, size))
        draw.line((x0, y0, x0 + size // 2, y0 - size // 4), fill=(255, 248, 221, 28), width=max(5, size // 220))
    return img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=60, threshold=5))


GENERATORS = {
    "smoky jade": smoky_jade,
    "kintsugi marble": kintsugi_marble,
    "brushed titanium": brushed_titanium,
    "archival vellum": archival_vellum,
    "obsidian glass": obsidian_glass,
    "manhattan order": manhattan_order,
    "nero marble": nero_marble,
    "travertine plaster": travertine_plaster,
    "walnut burl": walnut_burl,
    "aged bronze patina": aged_bronze_patina,
    "linen canvas": linen_canvas,
    "architectural concrete": architectural_concrete,
    "carbon fiber": carbon_fiber,
    "champagne frosted glass": champagne_frosted_glass,
}


def pick_generator(family: str):
    return GENERATORS.get(family.strip().lower(), smoky_jade)


def target_name(row: dict[str, str]) -> str:
    value = row.get("Target_Filename", "")
    stem = Path(value).stem or row.get("Batch_ID", "adobe_asset").lower()
    return f"{stem}.jpg"


def generate_asset(row: dict[str, str], index: int, out_dir: Path, size: int) -> Path:
    generator = pick_generator(row.get("Family", ""))
    seed = 81000 + index * 97 + sum(ord(ch) for ch in row.get("Family", ""))
    image = generator(size, seed)
    out_path = out_dir / target_name(row)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path, "JPEG", quality=95, subsampling=0, optimize=True)
    return out_path


def source_is_usable(row: dict[str, str]) -> bool:
    source = row.get("Source_Path", "")
    if not source:
        return False
    path = PROJECT_ROOT / source if not Path(source).is_absolute() else Path(source)
    if path.name != target_name(row):
        return False
    return path.exists() and path.stat().st_size >= 750_000


def update_queue(batch_rows: list[dict[str, str]]) -> None:
    queue_rows = read_rows(QUEUE)
    if not queue_rows:
        return
    by_id = {row.get("Queue_ID", ""): row for row in batch_rows}
    changed = False
    for row in queue_rows:
        match = by_id.get(row.get("ID", ""))
        if not match:
            continue
        row["Target_Filename"] = match["Target_Filename"]
        row["Source_Path"] = match["Source_Path"]
        row["QA_Status"] = match["QA_Status"]
        row["Upload_Status"] = match["Upload_Status"]
        changed = True
    if changed:
        write_rows(QUEUE, queue_rows)


def run(count: int, size: int) -> dict[str, int]:
    assert_adobe_write_paths((BATCH, QUEUE))
    rows = read_rows(BATCH)
    if not rows:
        raise RuntimeError("No Adobe batch rows found. Run adobe_stock_pilot_batch.py first.")
    out_dir = ASSETS / f"pilot_{today_slug()}"
    assert_adobe_write_paths((out_dir / "placeholder.txt",))

    generated = 0
    for index, row in enumerate(rows, start=1):
        if generated >= count:
            break
        if source_is_usable(row):
            continue
        out_path = generate_asset(row, index, out_dir, size)
        row["Target_Filename"] = out_path.name
        row["Source_Path"] = str(out_path.relative_to(PROJECT_ROOT))
        row["Status"] = "LOCAL_IMAGE_GENERATED_NEEDS_QA"
        row["QA_Status"] = "PENDING_IMAGE_QA"
        row["Upload_Status"] = "BLOCKED_UNTIL_IMAGE_QA"
        row["Next_Action"] = "Run image QA, then metadata QA, then submit only if both pass."
        generated += 1

    write_rows(BATCH, rows)
    update_queue(rows)
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock procedural pilot assets generated={generated}; "
            f"size={size}; output={out_dir.relative_to(PROJECT_ROOT)}; no upload/spend.\n"
        )
    return {"generated": generated, "size": size, "batch_rows": len(rows)}


def main() -> None:
    raise SystemExit(
        "DEPRECATED_ADOBE_FLAT_GENERATOR_DISABLED: Rex rejected the old flat/procedural "
        "Adobe pilot on 2026-05-16. Do not generate or submit these assets. Use the "
        "macro-photography MJ U-button/2x-upscale pipeline instead."
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT)
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
    args = parser.parse_args()
    result = run(args.count, args.size)
    print(f"[ADOBE-MATERIAL-GENERATOR] {result}")


if __name__ == "__main__":
    main()
