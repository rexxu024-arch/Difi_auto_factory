"""Build one-folder-per-work release packets for THE FIRST AUDIT.

This is a local packaging step. It does not publish, call marketplaces, or
request new Midjourney upscales. It turns the current protected Studio manifest
into reviewable release folders with a production image, two conservative
local mockups, and Chinese private-sales narrative copy.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFilter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

MANIFEST = PROJECT_ROOT / "Database" / "First_Audit_001_Asset_Manifest.csv"
RELEASE_ROOT = PROJECT_ROOT / "First_Audit_Release"
INDEX_FILE = RELEASE_ROOT / "FIRST_AUDIT_RELEASE_INDEX.md"
NY_TZ = ZoneInfo("America/New_York")


CN_NAMES = {
    "OC-NYC-ARCHIVE-011": "巴别塔冠冕",
    "OC-NYC-ARCHIVE-012": "布鲁克林缆索夜祷",
    "OC-NYC-EPIC-001": "冰霜符文圣杯",
    "OC-NYC-EPIC-004": "灰烬女武神头盔",
    "OC-NYC-CYBER-005": "机械佛手光龛",
    "OC-NYC-ASSASSIN-008": "烟玉斯巴达",
    "OC-NYC-ASSASSIN-010": "黑曜桂冠",
    "OC-NYC-MUSEUM-020": "静默星仪",
    "OC-NYC-AMERICANA-016": "好莱坞幽光",
}

ANCHORS = {
    "ARCHIVE": "巴别塔与纽约装饰艺术的垂直权力语言",
    "EPIC": "北欧遗物、战后圣器与暗室明暗法",
    "CYBER": "包豪斯机器美学与后人类宗教手势",
    "ASSASSIN": "古典胜利符号被黑钛金与烟熏玉重新铸造",
    "MUSEUM": "十九世纪星象仪、私人图书馆和静默宇宙论",
    "AMERICANA": "旧好莱坞摄影棚、爵士夜场和美国怀旧神话",
}


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def now_et() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def safe_slug(text: str) -> str:
    text = clean(text)
    text = re.sub(r"[\\/:*?\"<>|]+", "-", text)
    text = re.sub(r"\s+", "_", text)
    return text[:90].strip("._-") or "untitled"


def read_manifest() -> list[dict[str, str]]:
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_rgba(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    return image


def fit_image(image: Image.Image, max_w: int, max_h: int) -> Image.Image:
    copy = image.copy()
    copy.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    return copy


def paste_with_shadow(canvas: Image.Image, item: Image.Image, xy: tuple[int, int], shadow_offset=(26, 32), shadow_blur=32) -> None:
    x, y = xy
    shadow = Image.new("RGBA", item.size, (0, 0, 0, 120))
    alpha = item.getchannel("A")
    shadow.putalpha(alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))
    canvas.alpha_composite(shadow, (x + shadow_offset[0], y + shadow_offset[1]))
    canvas.alpha_composite(item, (x, y))


def make_desk_mockup(hero: Image.Image, target: Path) -> None:
    canvas = Image.new("RGBA", (1800, 1200), (32, 26, 22, 255))
    draw = ImageDraw.Draw(canvas)

    # Walnut desk plane.
    for y in range(0, 1200, 18):
        tone = 42 + (y % 72) // 6
        draw.line((0, y, 1800, y + 90), fill=(tone, 31, 23, 255), width=7)
    draw.rectangle((0, 0, 1800, 1200), outline=(62, 49, 38, 255), width=18)

    # Soft lamp glow and editorial vignette.
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse((1040, -220, 2050, 760), fill=(199, 151, 86, 72))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    canvas.alpha_composite(glow)

    item = fit_image(hero, 620, 820)
    block = Image.new("RGBA", (item.width + 64, item.height + 64), (255, 255, 255, 0))
    bdraw = ImageDraw.Draw(block)
    bdraw.rounded_rectangle((18, 18, block.width - 18, block.height - 18), radius=22, fill=(20, 28, 30, 238), outline=(184, 221, 224, 130), width=5)
    bdraw.line((block.width - 36, 28, block.width - 36, block.height - 28), fill=(220, 255, 255, 80), width=6)
    block.alpha_composite(item, (32, 32))
    paste_with_shadow(canvas, block, (600, 170), shadow_offset=(34, 42), shadow_blur=38)

    # Minimal desk props, no text.
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((180, 780, 520, 910), radius=18, fill=(18, 18, 18, 230), outline=(96, 77, 58, 255), width=3)
    draw.ellipse((1280, 790, 1510, 1020), fill=(17, 15, 14, 235), outline=(93, 77, 61, 255), width=4)
    draw.arc((1304, 817, 1484, 997), 220, 40, fill=(179, 142, 89, 255), width=10)

    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(target, "JPEG", quality=93, optimize=True)


def make_gallery_mockup(hero: Image.Image, target: Path) -> None:
    canvas = Image.new("RGBA", (1800, 1200), (232, 228, 219, 255))
    draw = ImageDraw.Draw(canvas)
    # Wall/floor split with subtle gallery light.
    draw.rectangle((0, 0, 1800, 810), fill=(236, 234, 228, 255))
    draw.rectangle((0, 810, 1800, 1200), fill=(187, 181, 169, 255))
    for x in (320, 1260):
        draw.polygon([(x, 0), (x + 250, 0), (x + 80, 810), (x - 120, 810)], fill=(255, 252, 240, 52))

    item = fit_image(hero, 540, 760)
    frame = Image.new("RGBA", (item.width + 96, item.height + 96), (255, 255, 255, 0))
    fdraw = ImageDraw.Draw(frame)
    fdraw.rectangle((10, 10, frame.width - 10, frame.height - 10), fill=(18, 18, 17, 255))
    fdraw.rectangle((30, 30, frame.width - 30, frame.height - 30), fill=(246, 244, 238, 255))
    frame.alpha_composite(item, (48, 48))
    paste_with_shadow(canvas, frame, (600, 90), shadow_offset=(22, 30), shadow_blur=24)

    # Pedestal / space cue.
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((690, 900, 1110, 1090), radius=12, fill=(213, 207, 196, 255), outline=(160, 153, 142, 255), width=3)
    draw.ellipse((600, 1070, 1200, 1160), fill=(84, 78, 69, 45))

    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(target, "JPEG", quality=93, optimize=True)


def family_anchor(sku: str) -> str:
    for key, value in ANCHORS.items():
        if key in sku:
            return value
    return "古典文明碎片被数字算力重新组织后的私人收藏语言"


def write_narrative(row: dict[str, str], folder: Path, cn_name: str) -> None:
    sku = clean(row.get("SKU"))
    concept = clean(row.get("Concept"))
    medium = clean(row.get("Studio_Medium"))
    price = clean(row.get("Price_USD"))
    anchor = family_anchor(sku)
    text = f"""# {cn_name}

## 官方概念设定

《{cn_name}》是 OpenClaw Design Studio 对「{anchor}」的一次物理重构。它不是普通装饰画，而是把古典权力构图、赛博材料错觉和纽约独立工作室的冷峻审美压进一件可摆放、可转赠、可谈论的实物资产里。推荐载体为 {medium}，定价层级 ${price}，仅作为 THE FIRST AUDIT: 001 内部审计序列候选。

## 公域/朋友圈诱饵

纽约这边工作室刚落地的一批内部测试件，{concept} 这张气质很压阵。不是走公域平台的普通货，先做极少量实物样品，看谁的空间和气场接得住。

## 1v1 核心节点私信

这件我不建议按「装饰品」看。它更像一个放在桌面、玄关或书房里的审美身份牌：不靠 logo，不靠烂大街奢侈品，而是靠材质、典故和压迫感让人停一下。你先看 02/03 两张场景图，如果你的办公室或家里有胡桃木、黑金属、石材、落地窗这类环境，它会非常稳。

## 生产与交付备注

- Studio SKU: {sku}
- 审计编号: {clean(row.get("Audit_ID"))}
- 推荐载体: {medium}
- Printify Blueprint: {clean(row.get("Blueprint_ID"))} / Provider {clean(row.get("Provider_ID"))} / Variant {clean(row.get("Variant_ID"))}
- 建议零售价: ${price}
- 当前状态: 私域审核候选，禁止进入 Etsy/eBay 公域仓库。
"""
    (folder / "04_Narrative_Matrix_CN.md").write_text(text, encoding="utf-8-sig")


def build_release(limit: int | None = None) -> int:
    rows = read_manifest()
    selected = rows[:limit] if limit else rows
    RELEASE_ROOT.mkdir(parents=True, exist_ok=True)
    held_lines: list[str] = []
    built = 0
    held = 0
    for row in selected:
        sku = clean(row.get("SKU"))
        audit = clean(row.get("Audit_ID")).split(":")[-1].strip().replace(" ", "-")
        cn_name = CN_NAMES.get(sku, clean(row.get("Concept")) or sku)
        folder = RELEASE_ROOT / safe_slug(f"{audit}_{cn_name}")
        production = Path(clean(row.get("Production_File")))
        if not production.exists():
            held += 1
            held_lines.append(f"- HOLD {sku}: missing production file `{production}`")
            continue
        folder.mkdir(parents=True, exist_ok=True)
        hero_target = folder / "01_Hero_Production.png"
        shutil.copy2(production, hero_target)
        hero = load_rgba(hero_target)
        make_desk_mockup(hero, folder / "02_Mockup_Luxury_Desk.jpg")
        make_gallery_mockup(hero, folder / "03_Mockup_Art_Gallery.jpg")
        write_narrative(row, folder, cn_name)
        built += 1
    all_folders = sorted(
        path
        for path in RELEASE_ROOT.iterdir()
        if path.is_dir() and (path / "01_Hero_Production.png").exists()
    )
    index_lines = [
        "# THE FIRST AUDIT: 001 Release Index",
        "",
        f"Generated: {now_et()}",
        "",
        "This folder is private Studio material. Do not upload to Etsy/eBay public archive.",
        "",
        "## Review Folders",
        "",
    ]
    for folder in all_folders:
        index_lines.append(f"- `{folder.relative_to(PROJECT_ROOT)}`")
    if held_lines:
        index_lines.extend(["", "## Holds", "", *held_lines])
    index_lines.extend(["", f"Built this run: {built}", f"Held this run: {held}", f"Total release folders: {len(all_folders)}", ""])
    INDEX_FILE.write_text("\n".join(index_lines), encoding="utf-8-sig")
    print(f"[FIRST-AUDIT-RELEASE] built={built} held={held} root={RELEASE_ROOT}")
    print(f"[FIRST-AUDIT-RELEASE] index={INDEX_FILE}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build First Audit one-folder-per-work release folders")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    return build_release(limit=args.limit or None)


if __name__ == "__main__":
    raise SystemExit(main())
