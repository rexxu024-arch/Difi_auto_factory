"""Build Etsy-ready digital sticker liquidation packs from local U1-U4 assets.

This is a local-only packaging tool. It does not publish, spend, or call Etsy.
It deliberately excludes Printify mockups, production sheets, and original grids;
only harvested U1-U4 PNG assets from ready sticker folders are sanitized and
packed into protected ZIP archives.
"""

from __future__ import annotations

import csv
import re
import shutil
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "Output" / "Sticker" / "Kiss-Cut"
WORK_ROOT = PROJECT_ROOT / "Database" / "Sticker_Liquidation"
ASSET_ROOT = WORK_ROOT / "assets"
RELEASE_ROOT = PROJECT_ROOT / "Release" / "Digital_Warehouse"
PREVIEW_ROOT = RELEASE_ROOT / "previews"
REPORT_ROOT = PROJECT_ROOT / "Reports"

MIN_EDGE = 900
DPI = (300, 300)
ETSY_MAX_FILE_BYTES = 19 * 1024 * 1024
ETSY_MAX_FILES = 5


@dataclass(frozen=True)
class PackSpec:
    pack_id: str
    filename: str
    price: str
    min_assets: int
    max_assets: int
    title: str
    tags: list[str]
    description: str


def digital_spec_block(asset_count: int, style_note: str) -> str:
    return (
        "[ FILE SPECS - PLEASE READ BEFORE PURCHASE ]\n"
        f"- Quantity: {asset_count}+ individual PNG sticker / clipart assets.\n"
        "- Format: PNG files packed into Etsy-safe ZIP parts.\n"
        "- Background: clean transparent backgrounds where the source artwork supports alpha transparency.\n"
        "- Resolution: most assets are approximately 1024 x 1024 px, with exact pixel sizes varying by artwork.\n"
        "- Print metadata: exported with 300 DPI metadata for sharp digital-planner and design use.\n"
        "- Delivery: instant digital download only; no physical product will be shipped.\n"
        f"- Visual style: {style_note}\n\n"
    )


PACKS: dict[str, PackSpec] = {
    "cyberpunk_acid": PackSpec(
        pack_id="cyberpunk_acid",
        filename="cyberpunk_acid_aesthetics_pack.zip",
        price="$5.99",
        min_assets=20,
        max_assets=20,
        title=(
            "20+ High Resolution Cyberpunk Digital Stickers, Acid Y2K PNG Clipart Pack, "
            "Futuristic Grunge GoodNotes Notion Graphics"
        ),
        tags=[
            "cyberpunk stickers",
            "acid graphics",
            "y2k stickers png",
            "digital clipart",
            "goodnotes stickers",
            "notion elements",
            "future punk png",
            "grunge stickers",
            "techwear art",
            "futuristic png",
            "sticker bundle",
            "designer assets",
            "digital planner",
        ],
        description=(
            "EXPLORE THE DIGITAL REVOLUTION - OPENCLAW DESIGN STUDIO EXCLUSIVE\n\n"
            "Inject raw future-punk energy into your digital layouts, planners, or design projects. "
            "This curated collection of 20+ Premium Cyberpunk & Acid Aesthetic digital stickers is "
            "engineered for high-end creators, digital journalers, and techwear culture enthusiasts.\n\n"
            + digital_spec_block(20, "cyberpunk, acid graphics, Y2K grunge, future-punk digital elements.")
            +
            "[ WHAT YOU RECEIVE ]\n"
            "- Split ZIP volumes containing the high-resolution PNG elements listed above.\n"
            "- Transparent-ready digital graphics for seamless layering on GoodNotes, Notion, iPad planners, or Photoshop canvas.\n"
            "- Professionally calibrated 300 DPI rendering ensuring zero digital distortion.\n\n"
            "[ USAGE SCENARIOS ]\n"
            "Perfect for GoodNotes digital journaling, iPad tablet customization, streetwear mockups, "
            "graphic design asset libraries, or Notion dashboard aesthetics.\n\n"
            "Note: This is an instant digital download. No physical relic will be shipped. "
            "For personal and limited commercial creation use. Reselling raw files is strictly forbidden."
        ),
    ),
    "zen_jade": PackSpec(
        pack_id="zen_jade",
        filename="zen_crystal_imperial_jade_pack.zip",
        price="$5.99",
        min_assets=20,
        max_assets=20,
        title=(
            "20+ High Resolution Zen Jade Digital Stickers, Kintsugi Crystal PNG Clipart, "
            "Luxury Gemstone GoodNotes Notion Art"
        ),
        tags=[
            "zen stickers png",
            "imperial jade",
            "kintsugi png",
            "crystal clipart",
            "oriental design",
            "luxury mineral",
            "goodnotes art",
            "notion design",
            "stone stickers",
            "gemstone elements",
            "digital assets",
            "relic clipart",
            "aesthetic planner",
        ],
        description=(
            "DISCOVER THE TRANQUILITY OF IMPERIAL MATERIALS - LUXURY DIGITAL RELICS\n\n"
            "Elevate your digital canvas with the tactile luxury of the Far East. OpenClaw Studio presents "
            "a high-density asset collection featuring 20+ Zen Crystal, Kintsugi seams, and Imperial Jade "
            "digital stickers, beautifully rendered to mimic expensive material illusions.\n\n"
            + digital_spec_block(20, "imperial jade, kintsugi seams, crystal minerals, calm Wabi Sabi planner accents.")
            +
            "[ WHAT YOU RECEIVE ]\n"
            "- Split lossless ZIP volumes enclosing the luxury mineral and gemstone PNGs listed above.\n"
            "- Delivered as Etsy-safe ZIP parts under the platform file-size limit.\n"
            "- Fully transparent backgrounds, perfectly cut for immediate overlay on dark or light themes.\n"
            "- Masterfully rendered 300 DPI textures with rich refraction metrics.\n\n"
            "[ USAGE SCENARIOS ]\n"
            "Designed for high-end digital planner layouts, calm academic Notion spaces, interior design mood boards, "
            "or bespoke branding presentations.\n\n"
            "Note: Instant digital delivery. Secure download link generated immediately post-purchase. "
            "No physical item will be dispatched."
        ),
    ),
    "dark_academia": PackSpec(
        pack_id="dark_academia",
        filename="dark_academia_alchemical_sigils_pack.zip",
        price="$5.99",
        min_assets=20,
        max_assets=20,
        title=(
            "20+ High Resolution Dark Academia Digital Stickers, Gothic Alchemy PNG Clipart, "
            "Vintage Occult GoodNotes Notion Aesthetic"
        ),
        tags=[
            "dark academia png",
            "alchemical sigils",
            "medieval clipart",
            "vintage occult",
            "gothic stickers",
            "antique design",
            "goodnotes gothic",
            "notion library",
            "alchemy symbols",
            "witchy sticker png",
            "dark academic aesthetic",
            "relic assets",
            "mystical art",
        ],
        description=(
            "RECLAIM THE LOST ARCHIVES - AN INFUSION OF INTELLECTUAL BRAGGING\n\n"
            "Step into the dark academic sanctuary. This premium pack features 20+ masterfully distilled "
            "Medieval Alchemical Sigils, Gothic architectural cues, and antique dark academia aesthetic elements, "
            "tailored for intellectual collectors and dark mode purists.\n\n"
            + digital_spec_block(20, "dark academia, gothic alchemy, occult sigils, antique library planner elements.")
            +
            "[ WHAT YOU RECEIVE ]\n"
            "- Split secure ZIP volumes with the vintage mystical and alchemical PNG graphics listed above.\n"
            "- Delivered as Etsy-safe ZIP parts under the platform file-size limit.\n"
            "- Transparent backdrops calibrated flawlessly for dark mode planners, PDF readers, and digital notebooks.\n"
            "- High-density 300 DPI outputs for premium sharp presentation.\n\n"
            "[ USAGE SCENARIOS ]\n"
            "Immersive dark mode journaling, digital book-journal decoration, tabletop RPG asset mapping, "
            "or high-concept graphic asset accumulation.\n\n"
            "Note: Digital interactive product. Available instantly. No shipping delays. No physical overhead."
        ),
    ),
    "mega_vault": PackSpec(
        pack_id="mega_vault",
        filename="ultimate_creator_vault_50_stickers.zip",
        price="$11.99",
        min_assets=50,
        max_assets=50,
        title=(
            "50+ High Resolution Digital Sticker PNG Bundle, Ultimate Creator Vault for GoodNotes, "
            "Dark Academia Zen Jade Notion Clipart"
        ),
        tags=[
            "mega sticker bundle",
            "ultimate creator vault",
            "50+ digital stickers",
            "cyberpunk png box",
            "dark academia clip",
            "zen jade assets",
            "goodnotes master",
            "notion megapack",
            "designer clipart",
            "all in one bundle",
            "graphic asset vault",
            "premium planner",
            "ipad png bundle",
        ],
        description=(
            "THE ULTIMATE VISUAL IMPERIUM - MONUMENTAL 50+ ASSET MEGAPACK\n\n"
            "Why compromise when you can dominate the entire aesthetic landscape? OpenClaw Design Studio opens "
            "the central vault, combining our signature digital kingdoms into one massive, cost-efficient master collection.\n\n"
            "OVER 50+ PREMIUM DIGITAL RELICS COVERING ZEN JADE AND DARK ACADEMIA, WITH FUTURE CYBERPUNK VOLUME SLOT RESERVED.\n\n"
            + digital_spec_block(50, "mixed dark academia, zen jade, kintsugi mineral, and premium creator-vault assets.")
            +
            "[ WHAT IS LOCKED INSIDE THE VAULT ]\n"
            "- Vol. 01: EASTERN HARMONY: Imperial Jade, Crystals & Kintsugi Minerals\n"
            "- Vol. 02: THE LOST LIBRARY: Dark Academia & Alchemical Mystical Sigils\n"
            "- Bonus: Seamless integration notes for advanced digital planner setups.\n\n"
            "[ CRITICAL VALUE ANCHOR ]\n"
            "Purchased separately, these elite volumes total over $11. By locking down the Ultimate Creator Vault today, "
            "you receive the complete 50+ premium asset bundle for a single fraction of the resource cost.\n\n"
            "[ TECHNICAL METRICS ]\n"
            "- Multi-volume compressed ZIP archives.\n"
            "- Zero background artifacts - clean PNG export optimization.\n"
            "- High-precision 300 DPI metadata.\n\n"
            "- Delivered in Etsy-safe ZIP parts below the platform file-size limit.\n\n"
            "Note: Digital asset liquidation deployment. Immediate access granted upon payment processing."
        ),
    ),
}


def slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return re.sub(r"_+", "_", text)


def folder_item_id(folder: Path) -> str:
    return folder.name.replace("MASTER_", "").replace("_Ready_for_Steaming", "")


def read_metadata(folder: Path) -> str:
    path = folder / "metadata.txt"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def classify(folder: Path) -> str:
    haystack = f"{folder.name}\n{read_metadata(folder)}".lower()
    if re.search(r"cyber|acid|y2k|grunge|punk|techwear|futuristic", haystack):
        return "cyberpunk_acid"
    if "academia" in haystack or re.search(r"alchemy|alchemical|gothic|occult|library|raven|grimoire", haystack):
        return "dark_academia"
    if re.search(r"zen|jade|crystal|kintsugi|oriental|lotus|bonsai|mineral|stone", haystack):
        return "zen_jade"
    return "zen_jade"


def candidate_folders() -> list[Path]:
    if not SOURCE_ROOT.exists():
        return []
    return sorted(
        folder
        for folder in SOURCE_ROOT.iterdir()
        if folder.is_dir()
        and folder.name.startswith("MASTER_")
        and folder.name.endswith("_Ready_for_Steaming")
        and "Not_Working" not in folder.name
        and "LowRes" not in folder.name
    )


def u_assets(folder: Path) -> list[Path]:
    # These files are the Midjourney U1-U4 outputs for sticker concepts. The
    # historical suffix says "_Grid", but they are the individual U images Rex
    # asked to count as separate digital assets.
    return sorted(folder.glob("*_U[1-4]_Grid.png"))


def image_ok(path: Path) -> tuple[bool, str, tuple[int, int]]:
    try:
        with Image.open(path) as im:
            size = im.size
            if min(size) < MIN_EDGE:
                return False, f"LOW_RES_{size[0]}x{size[1]}", size
            return True, "OK", size
    except Exception as exc:  # noqa: BLE001
        return False, f"OPEN_ERROR_{type(exc).__name__}", (0, 0)


def sanitize_png(src: Path, dest: Path) -> tuple[int, int]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        out = im.convert("RGBA")
        out.save(dest, "PNG", dpi=DPI, optimize=True)
        return out.size


def select_assets() -> tuple[dict[str, list[tuple[Path, Path]]], list[dict[str, str]]]:
    selected: dict[str, list[tuple[Path, Path]]] = {key: [] for key in PACKS if key != "mega_vault"}
    audit: list[dict[str, str]] = []

    for folder in candidate_folders():
        pack = classify(folder)
        for src in u_assets(folder):
            ok, reason, size = image_ok(src)
            audit.append(
                {
                    "item_id": folder_item_id(folder),
                    "source_folder": str(folder),
                    "source_file": str(src),
                    "assigned_pack": pack,
                    "status": reason,
                    "width": str(size[0]),
                    "height": str(size[1]),
                }
            )
            if ok and pack in selected:
                selected[pack].append((folder, src))

    for pack_id, spec in PACKS.items():
        if pack_id == "mega_vault":
            continue
        selected[pack_id] = selected[pack_id][: spec.max_assets]
    return selected, audit


def build_preview(pack_id: str, assets: list[Path], title: str) -> Path | None:
    if not assets:
        return None
    PREVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    tile = 360
    gutter = 28
    header = 110
    canvas = Image.new("RGB", (tile * 3 + gutter * 4, header + tile * 3 + gutter * 4), (235, 232, 223))
    draw = ImageDraw.Draw(canvas, "RGBA")
    font = ImageFont.load_default()
    draw.rectangle((0, 0, canvas.width, header), fill=(26, 24, 22, 255))
    draw.text((gutter, 34), title[:110], fill=(255, 255, 255, 255), font=font)

    for idx, src in enumerate(assets[:9]):
        with Image.open(src) as im:
            img = im.convert("RGBA")
            img.thumbnail((tile, tile), Image.Resampling.LANCZOS)
            x = gutter + (idx % 3) * (tile + gutter)
            y = header + gutter + (idx // 3) * (tile + gutter)
            bg = Image.new("RGB", (tile, tile), (250, 248, 242))
            px = (tile - img.width) // 2
            py = (tile - img.height) // 2
            bg.paste(img, (px, py), img)
            canvas.paste(bg, (x, y))
            draw.rectangle((x, y, x + tile, y + tile), outline=(180, 172, 150, 255), width=2)

    # Preview-only defensive watermark. Paid ZIP assets remain clean.
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay, "RGBA")
    for x in range(-canvas.width, canvas.width * 2, 260):
        odraw.text((x, canvas.height // 2), "OPENCLAW PREVIEW", fill=(0, 0, 0, 34), font=font)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    out = PREVIEW_ROOT / f"{pack_id}_preview_mockup.jpg"
    canvas.save(out, "JPEG", quality=88, optimize=True)
    return out


def write_zip(zip_path: Path, files: list[Path], root: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for file in files:
            zf.write(file, file.relative_to(root).as_posix())


def cleanup_old_pack_zips(filename: str) -> None:
    stem = Path(filename).stem
    for path in RELEASE_ROOT.glob(f"{stem}*.zip"):
        path.unlink()


def split_zip_volumes(base_filename: str, files: list[Path], root: Path) -> list[Path]:
    """Write Etsy-safe ZIP volumes under 20MB each and no more than 5 files."""
    cleanup_old_pack_zips(base_filename)
    if not files:
        return []

    volumes: list[list[Path]] = []
    current: list[Path] = []
    current_bytes = 0
    for file in files:
        size = file.stat().st_size
        if size > ETSY_MAX_FILE_BYTES:
            continue
        if current and current_bytes + size > ETSY_MAX_FILE_BYTES:
            volumes.append(current)
            current = []
            current_bytes = 0
        current.append(file)
        current_bytes += size
    if current:
        volumes.append(current)

    volumes = volumes[:ETSY_MAX_FILES]
    written: list[Path] = []
    stem = Path(base_filename).stem
    suffix = Path(base_filename).suffix
    for index, volume_files in enumerate(volumes, start=1):
        out = RELEASE_ROOT / f"{stem}_part_{index:02d}{suffix}"
        write_zip(out, volume_files, root)
        # Deflated PNGs can sometimes grow slightly because PNGs are already
        # compressed. If that happens, drop trailing files until Etsy-safe.
        while out.exists() and out.stat().st_size > ETSY_MAX_FILE_BYTES and len(volume_files) > 1:
            volume_files = volume_files[:-1]
            write_zip(out, volume_files, root)
        if out.exists() and out.stat().st_size <= ETSY_MAX_FILE_BYTES:
            written.append(out)
        elif out.exists():
            out.unlink()
    return written


def build() -> dict[str, object]:
    for path in [WORK_ROOT, ASSET_ROOT, RELEASE_ROOT, PREVIEW_ROOT, REPORT_ROOT]:
        path.mkdir(parents=True, exist_ok=True)

    selected, audit = select_assets()
    sanitized_by_pack: dict[str, list[Path]] = {key: [] for key in PACKS}
    manifest_rows: list[dict[str, str]] = []

    for pack_id, assets in selected.items():
        pack_dir = ASSET_ROOT / pack_id
        if pack_dir.exists():
            shutil.rmtree(pack_dir)
        pack_dir.mkdir(parents=True, exist_ok=True)
        for folder, src in assets:
            item_id = folder_item_id(folder)
            u_match = re.search(r"_U([1-4])_", src.name)
            u_label = f"u{u_match.group(1)}" if u_match else "u"
            dest = pack_dir / f"{slug(item_id)}_{u_label}.png"
            width, height = sanitize_png(src, dest)
            sanitized_by_pack[pack_id].append(dest)
            manifest_rows.append(
                {
                    "pack_id": pack_id,
                    "item_id": item_id,
                    "source_file": str(src),
                    "sanitized_file": str(dest),
                    "width": str(width),
                    "height": str(height),
                    "dpi": "300",
                    "status": "PACKAGED",
                }
            )

    # Mega vault uses a balanced mix from the whole sticker reference archive.
    # Fixed Rex rule: small packs target 20 assets; mega vault targets 50 assets.
    # Do not return to the old 100+ concept unless Rex explicitly reopens it.
    # Original sticker folders remain internal references; this creates only
    # sanitized digital-bundle copies for Etsy digital downloads.
    mega_dir = ASSET_ROOT / "mega_vault"
    if mega_dir.exists():
        shutil.rmtree(mega_dir)
    mega_dir.mkdir(parents=True, exist_ok=True)
    existing_sources = {str(path) for path in sanitized_by_pack["dark_academia"] + sanitized_by_pack["zen_jade"] + sanitized_by_pack["cyberpunk_acid"]}
    used_source_files = {row["source_file"] for row in manifest_rows}
    mega_sources = sanitized_by_pack["cyberpunk_acid"] + sanitized_by_pack["dark_academia"] + sanitized_by_pack["zen_jade"]

    extra_counter = 0
    for folder in candidate_folders():
        if len(mega_sources) >= PACKS["mega_vault"].max_assets:
            break
        for src in u_assets(folder):
            if len(mega_sources) >= PACKS["mega_vault"].max_assets:
                break
            if str(src) in used_source_files:
                continue
            ok, _reason, _size = image_ok(src)
            if not ok:
                continue
            item_id = folder_item_id(folder)
            u_match = re.search(r"_U([1-4])_", src.name)
            u_label = f"u{u_match.group(1)}" if u_match else "u"
            if str(src) not in existing_sources:
                mega_sources.append(src)
                existing_sources.add(str(src))
                extra_counter += 1

    for src in mega_sources[: PACKS["mega_vault"].max_assets]:
        subfolder = "dark_academia" if "dark_academia" in src.parts else "zen_jade"
        if "cyberpunk_acid" in src.parts:
            subfolder = "cyberpunk_acid"
        elif SOURCE_ROOT in src.parents:
            subfolder = "bonus_archive"
        dest = mega_dir / subfolder / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if SOURCE_ROOT in src.parents:
            sanitize_png(src, dest)
        else:
            shutil.copy2(src, dest)
        sanitized_by_pack["mega_vault"].append(dest)

    listing_rows: list[dict[str, str]] = []
    pack_summary: list[dict[str, str]] = []

    for pack_id, spec in PACKS.items():
        files = sanitized_by_pack[pack_id]
        status = "READY" if len(files) >= spec.min_assets else "SOURCE_SHORTAGE"
        preview = build_preview(pack_id, files, spec.title)
        zip_paths: list[Path] = []
        if files and status == "READY":
            root = ASSET_ROOT / pack_id
            zip_paths = split_zip_volumes(spec.filename, files, root)
            zipped_assets = count_zip_assets(zip_paths)
            if len(zip_paths) > ETSY_MAX_FILES or zipped_assets < spec.min_assets:
                status = "ETSY_FILE_LIMIT_EXCEEDED"
                cleanup_old_pack_zips(spec.filename)
                zip_paths = []
        else:
            cleanup_old_pack_zips(spec.filename)

        pack_summary.append(
            {
                "pack_id": pack_id,
                "status": status,
                "asset_count": str(len(files)),
                "zip_path": ";".join(str(path) for path in zip_paths),
                "preview_path": str(preview or ""),
                "price": spec.price,
                "etsy_file_count": str(len(zip_paths)),
                "zip_total_mb": f"{sum(path.stat().st_size for path in zip_paths) / 1024 / 1024:.2f}" if zip_paths else "0.00",
            }
        )
        publish_guard = "PASS_LOCAL_READY_NOT_PUBLISHED" if status == "READY" else "HOLD_DO_NOT_PUBLISH"
        guard_issues = (
            "Ready locally; still requires Rex/Codex visual and buyer-expectation QA before paid publish."
            if status == "READY"
            else f"{status}: pack has {len(files)} assets; public metadata must not be published until it reaches {spec.min_assets}."
        )
        listing_rows.append(
            {
                "pack_id": pack_id,
                "status": status,
                "publish_guard": publish_guard,
                "title": spec.title,
                "price": spec.price,
                "tags": ", ".join(spec.tags),
                "description": spec.description,
                "zip_path": ";".join(str(path) for path in zip_paths),
                "preview_path": str(preview or ""),
                "asset_count": str(len(files)),
                "etsy_file_count": str(len(zip_paths)),
                "zip_total_mb": f"{sum(path.stat().st_size for path in zip_paths) / 1024 / 1024:.2f}" if zip_paths else "0.00",
                "guard_issues": guard_issues,
                "notes": "Do not publish until Rex/Codex QA confirms preview and ZIP contents." if status == "READY" else "Needs source assets or smaller pack before listing.",
            }
        )

    write_csv(WORK_ROOT / "Sticker_Liquidation_Manifest.csv", manifest_rows)
    write_csv(WORK_ROOT / "Sticker_Liquidation_Source_Audit.csv", audit)
    write_csv(WORK_ROOT / "Etsy_Sticker_Liquidation_Metadata.csv", listing_rows)
    write_csv(WORK_ROOT / "Sticker_Liquidation_Pack_Summary.csv", pack_summary)

    report_path = REPORT_ROOT / f"Sticker_Liquidation_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    latest_report = REPORT_ROOT / "Sticker_Liquidation_Report_latest.md"
    report = render_report(pack_summary)
    report_path.write_text(report, encoding="utf-8")
    latest_report.write_text(report, encoding="utf-8")

    return {
        "summary": pack_summary,
        "manifest": str(WORK_ROOT / "Sticker_Liquidation_Manifest.csv"),
        "metadata": str(WORK_ROOT / "Etsy_Sticker_Liquidation_Metadata.csv"),
        "report": str(latest_report),
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def count_zip_assets(zip_paths: Iterable[Path]) -> int:
    total = 0
    for path in zip_paths:
        with zipfile.ZipFile(path) as zf:
            total += sum(1 for name in zf.namelist() if name.lower().endswith(".png"))
    return total


def render_report(summary: list[dict[str, str]]) -> str:
    lines = [
        "# Sticker Liquidation Build Report",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}",
        "",
        "Local-only build. No Etsy publishing, no marketplace spend.",
        "",
        "## Pack Summary",
        "",
        "| Pack | Status | Assets | Etsy Files | ZIP MB | ZIP | Preview | Price |",
        "|---|---:|---:|---:|---:|---|---|---:|",
    ]
    for row in summary:
        lines.append(
            f"| {row['pack_id']} | {row['status']} | {row['asset_count']} | {row.get('etsy_file_count', '')} | "
            f"{row.get('zip_total_mb', '')} | {row['zip_path']} | {row['preview_path']} | {row['price']} |"
        )
    lines += [
        "",
        "## Guard Notes",
        "",
        "- Source harvesting only accepts `*_U1_Grid.png` to `*_U4_Grid.png` from `*_Ready_for_Steaming` folders.",
        "- `Cover_Mockup.png`, `Production_Design.png`, and low-resolution/not-working folders are excluded.",
        "- Preview JPGs are watermarked. Paid ZIP assets are clean 300 DPI PNGs.",
        "- Etsy file guard: ZIP output is split into no more than 5 files, each below 20MB.",
        "- Original sticker POD folders are not deleted. Sticker assets are now treated as internal reference material and digital bundle source inventory.",
        "- Cyberpunk/Acid pack is not published if no matching source assets exist.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    result = build()
    for row in result["summary"]:  # type: ignore[index]
        print(
            f"{row['pack_id']}: {row['status']} assets={row['asset_count']} "
            f"zip={row['zip_path']} preview={row['preview_path']}"
        )
    print(f"metadata={result['metadata']}")
    print(f"report={result['report']}")


if __name__ == "__main__":
    main()
