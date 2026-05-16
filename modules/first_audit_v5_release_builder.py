"""Build the V5 private-review release pack for First Audit.

This script is local-only. It does not call marketplaces, spend MJ Fast time,
or publish products. It turns the completed Shock & Awe V5 production files
into one-folder-per-work review packets for Rex/Grey/private-sales review.
"""

from __future__ import annotations

import csv
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.first_audit_release_builder import make_desk_mockup, make_gallery_mockup

SOURCE_CSV = PROJECT_ROOT / "Database" / "Shock_And_Awe_V5_Zones1_3_Printify_Production_Files.csv"
QUEUE_CSV = PROJECT_ROOT / "Database" / "Shock_And_Awe_V5_Zones1_3_MJ_Dispatch_Queue.csv"
RELEASE_ROOT = PROJECT_ROOT / "First_Audit_Release" / "V5_Zones1_3"
MANIFEST_OUT = PROJECT_ROOT / "Database" / "First_Audit_V5_Zones1_3_Release_Manifest.csv"
INDEX_OUT = RELEASE_ROOT / "FIRST_AUDIT_V5_ZONES1_3_INDEX.md"
CONTACT_SHEET = RELEASE_ROOT / "FIRST_AUDIT_V5_ZONES1_3_CONTACT_SHEET.jpg"
NY_TZ = ZoneInfo("America/New_York")

CN_NAMES = {
    "OC-NYC-ARCHIVE-011": "巴别塔冠冕蓝图",
    "OC-NYC-ARCHIVE-012": "布鲁克林缆索夜祷",
    "OC-NYC-ARCHIVE-013": "爵士地窖琥珀",
    "OC-NYC-ARCHIVE-014": "地铁瓷砖神谕",
    "OC-NYC-AMERICANA-015": "66号公路霓虹圣匣",
    "OC-NYC-AMERICANA-016": "好莱坞幽光",
    "OC-NYC-AMERICANA-017": "雨后加油站圣龛",
    "OC-NYC-MUSEUM-018": "星体解剖手稿",
    "OC-NYC-MUSEUM-019": "无面伦勃朗学者",
    "OC-NYC-MUSEUM-020": "静默星仪",
    "OC-NYC-CYBERPOP-021": "酸铬玩具黑豹",
    "OC-NYC-CYBERPOP-022": "热粉信号兔",
    "OC-NYC-CYBERPOP-023": "霓虹贩卖机神龛",
    "OC-NYC-CYBERPOP-024": "铬滑板遗物",
    "OC-NYC-CYBERPOP-025": "故障吉祥物图腾",
    "OC-NYC-AUSPICIOUS-026": "铬金招财猫引擎",
    "OC-NYC-AUSPICIOUS-027": "财富硬币电路",
    "OC-NYC-AUSPICIOUS-028": "红包数据金库",
    "OC-NYC-AUSPICIOUS-029": "玉石繁荣胶囊",
    "OC-NYC-AUSPICIOUS-030": "霓虹店铺守卫",
}

ANCHORS = {
    "ARCHIVE": "纽约装饰艺术、桥梁工程和地下交通纹理被重新整理成私人工业遗物",
    "AMERICANA": "美国公路、旧好莱坞与霓虹残景被压缩成可收藏的怀旧权力符号",
    "MUSEUM": "十九世纪博物学、天文仪器和明暗法肖像被转换成冷峻的书房图腾",
    "CYBERPOP": "年轻潮牌的酸性视觉被降噪后，转化成可进入高端空间的赛博玩物",
    "AUSPICIOUS": "低门槛的发财与幸运意象被黑铬、冷玉和霓虹算法重新包裹",
}

STUDIO_CARRIER = {
    "Framed Poster": "典藏级无框/黑框版画",
    "Canvas": "典藏级画布或实木框画",
    "Acrylic Block": "加厚光学亚克力装置",
    "Notebook": "概念来源，不作为私域载体；建议转为版画或亚克力",
    "Mug": "概念来源，不作为私域载体；建议转为亚克力或版画",
}


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def now_et() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %z")


def safe_slug(text: str) -> str:
    text = re.sub(r"[\\/:*?\"<>|]+", "-", clean(text))
    text = re.sub(r"\s+", "_", text)
    return text[:110].strip("._-") or "untitled"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def family(sku: str) -> str:
    for key in ANCHORS:
        if key in sku:
            return key
    return "ARCHIVE"


def tier_for(row: dict[str, str]) -> str:
    vector = clean(row.get("Product_Vector"))
    rrp = float(clean(row.get("RRP_USD")) or 0)
    if vector == "Acrylic Block" or rrp >= 250:
        return "Anchor / Core"
    if vector in {"Framed Poster", "Canvas"}:
        return "Entrance / Gallery"
    return "Concept / Convert"


def studio_recommendation(row: dict[str, str]) -> str:
    vector = clean(row.get("Product_Vector"))
    if vector in {"Notebook", "Mug"}:
        fam = family(clean(row.get("Final_SKU")))
        if fam in {"CYBERPOP", "AUSPICIOUS"}:
            return "建议转换为 5x7 光学亚克力块；保留潮玩/祥瑞的物理体积感。"
        return "建议转换为典藏版画；保留纹理和叙事，不采用低端周边载体。"
    return f"保留为 {STUDIO_CARRIER.get(vector, vector)}。"


def folder_name(row: dict[str, str], idx: int) -> str:
    sku = clean(row.get("Final_SKU"))
    cn = CN_NAMES.get(sku, clean(row.get("Concept_Name")) or sku)
    return safe_slug(f"V5-{idx:02d}_{cn}")


def write_narrative(row: dict[str, str], folder: Path, idx: int) -> None:
    sku = clean(row.get("Final_SKU"))
    concept = clean(row.get("Concept_Name"))
    cn = CN_NAMES.get(sku, concept or sku)
    vector = clean(row.get("Product_Vector"))
    tier = tier_for(row)
    anchor = ANCHORS[family(sku)]
    recommendation = studio_recommendation(row)
    rrp = clean(row.get("RRP_USD"))
    base = clean(row.get("Base_Cost_USD"))
    shipping = clean(row.get("Shipping_USD"))
    blueprint = clean(row.get("Blueprint_ID"))
    provider = clean(row.get("Provider_ID"))
    variant = clean(row.get("Variant_ID"))
    selected = clean(row.get("Selected_U"))
    qa = clean(row.get("QA_Note"))
    upscale_note = "当前为草图级生产文件；仅当 Rex 标记为 Top 1% 时，才允许消耗 MJ Fast/Upscale。"

    text = f"""# {cn}

## 官方概念设定

《{cn}》属于 OpenClaw Design Studio 的 The First Audit 试验序列。它的底层不是普通装饰图，而是把「{anchor}」压缩成可被摆放、转赠、讨论的实物资产。视觉语言强调冷玉、黑钛金、玻璃折射、旧纽约或赛博霓虹的材质错觉，目标是让作品看起来像一件被数字算力重新铸造过的古典碎片。

## 公域/朋友圈诱饵

纽约工作室这批内部测试件里，{concept} 这一张有很强的空间压迫感。它不适合走廉价平台公卖，更像是先给懂空间、懂桌面气场的人看的小批量样品。能接住它的人，家里或办公室通常已经有胡桃木、石材、金属和落地窗。

## 1v1 核心节点私信

这件我会建议你先看 02 和 03 两张场景图。它不是靠 logo 和大众奢侈品符号撑场面，而是靠典故、材质和体积感让人停一下。如果你的空间需要一个“不是烂大街、但能显出审美权限”的对象，这类东西比普通装饰画更适合做话题入口。

## Studio 判断

- Release 序号: V5-{idx:02d}
- Studio SKU: {sku}
- 英文概念名: {concept}
- 私域中文名: {cn}
- 当前载体来源: {vector}
- Studio 层级: {tier}
- Studio 载体建议: {recommendation}
- 建议零售价参考: ${rrp}
- 生产底价参考: ${base}
- 运费参考: ${shipping}
- Printify 蓝图: {blueprint} / Provider {provider} / Variant {variant}
- 选中格位: {selected}
- QA 备注: {qa}
- 算力备注: {upscale_note}

## 禁止事项

- 不进入低价 Etsy Archive。
- 不作为 Sticker/Mug/Notebook 廉价周边主推。
- 不自动 upscale；只在 Rex 人工确认入围后升级为极清生产图。
"""
    (folder / "04_Narrative_Matrix_CN.md").write_text(text, encoding="utf-8")


def build_manifest(rows: list[dict[str, str]], out_rows: list[dict[str, str]]) -> None:
    MANIFEST_OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "Release_ID",
        "SKU",
        "Chinese_Name",
        "Concept_Name",
        "Source_Product_Vector",
        "Studio_Recommendation",
        "Tier",
        "Production_Design_File",
        "Hero_File",
        "Desk_Mockup",
        "Gallery_Mockup",
        "Narrative_File",
        "MJ_Upscale_Status",
        "Built_At_ET",
    ]
    with MANIFEST_OUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def fit_image(path: Path, size: tuple[int, int]) -> Image.Image:
    canvas = Image.new("RGB", size, (242, 239, 232))
    with Image.open(path) as image:
        image = image.convert("RGB")
        image.thumbnail(size, Image.Resampling.LANCZOS)
        canvas.paste(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return canvas


def build_contact_sheet(folders: list[Path]) -> None:
    cols = 4
    card_w = 520
    card_h = 690
    margin = 34
    rows = max(1, (len(folders) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * card_w + margin * 2, rows * card_h + margin * 2), (226, 222, 213))
    draw = ImageDraw.Draw(sheet)
    title_font = font(23, True)
    small_font = font(17)

    for i, folder in enumerate(folders):
        x = margin + (i % cols) * card_w
        y = margin + (i // cols) * card_h
        draw.rounded_rectangle([x + 8, y + 8, x + card_w - 16, y + card_h - 16], radius=16, fill=(247, 245, 239), outline=(170, 160, 148), width=2)
        draw.text((x + 28, y + 28), folder.name.replace("_", " ")[:33], fill=(28, 25, 22), font=title_font)
        hero = fit_image(folder / "01_Hero_Production.png", (205, 315))
        desk = fit_image(folder / "02_Mockup_Luxury_Desk.jpg", (220, 150))
        gallery = fit_image(folder / "03_Mockup_Art_Gallery.jpg", (220, 150))
        sheet.paste(hero, (x + 28, y + 84))
        sheet.paste(desk, (x + 260, y + 88))
        sheet.paste(gallery, (x + 260, y + 260))
        status = "Narrative OK" if (folder / "04_Narrative_Matrix_CN.md").exists() else "Narrative missing"
        draw.text((x + 28, y + 430), status, fill=(45, 80, 56), font=small_font)
        draw.text((x + 28, y + 462), str(folder.relative_to(PROJECT_ROOT))[:50], fill=(72, 65, 58), font=small_font)

    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(CONTACT_SHEET, "JPEG", quality=92, optimize=True)


def build_release() -> int:
    rows = read_csv(SOURCE_CSV)
    RELEASE_ROOT.mkdir(parents=True, exist_ok=True)
    out_rows: list[dict[str, str]] = []
    folders: list[Path] = []
    missing: list[str] = []

    for idx, row in enumerate(rows, start=1):
        sku = clean(row.get("Final_SKU"))
        production = PROJECT_ROOT / clean(row.get("Production_Design_File"))
        cn = CN_NAMES.get(sku, clean(row.get("Concept_Name")) or sku)
        folder = RELEASE_ROOT / folder_name(row, idx)
        if not production.exists():
            missing.append(f"{sku}: {production}")
            continue

        folder.mkdir(parents=True, exist_ok=True)
        hero = folder / "01_Hero_Production.png"
        desk = folder / "02_Mockup_Luxury_Desk.jpg"
        gallery = folder / "03_Mockup_Art_Gallery.jpg"
        narrative = folder / "04_Narrative_Matrix_CN.md"

        shutil.copy2(production, hero)
        with Image.open(hero) as image:
            image = image.convert("RGBA")
            make_desk_mockup(image, desk)
            make_gallery_mockup(image, gallery)
        write_narrative(row, folder, idx)
        folders.append(folder)
        out_rows.append(
            {
                "Release_ID": f"V5-{idx:02d}",
                "SKU": sku,
                "Chinese_Name": cn,
                "Concept_Name": clean(row.get("Concept_Name")),
                "Source_Product_Vector": clean(row.get("Product_Vector")),
                "Studio_Recommendation": studio_recommendation(row),
                "Tier": tier_for(row),
                "Production_Design_File": str(production.relative_to(PROJECT_ROOT)),
                "Hero_File": str(hero.relative_to(PROJECT_ROOT)),
                "Desk_Mockup": str(desk.relative_to(PROJECT_ROOT)),
                "Gallery_Mockup": str(gallery.relative_to(PROJECT_ROOT)),
                "Narrative_File": str(narrative.relative_to(PROJECT_ROOT)),
                "MJ_Upscale_Status": "DRAFT_ONLY_NO_FAST_UPSCALE",
                "Built_At_ET": now_et(),
            }
        )

    build_manifest(rows, out_rows)
    build_contact_sheet(folders)
    index_lines = [
        "# First Audit V5 Zones 1/3 Release Pack",
        "",
        f"Generated: {now_et()}",
        f"Folders: {len(folders)}",
        f"Manifest: `{MANIFEST_OUT.relative_to(PROJECT_ROOT)}`",
        f"Contact sheet: `{CONTACT_SHEET.relative_to(PROJECT_ROOT)}`",
        "",
        "MJ resource rule: this pack uses draft production crops only. Fast/Upscale is not consumed until Rex selects Top 1% assets.",
        "",
        "## Folders",
        "",
    ]
    for folder in folders:
        index_lines.append(f"- `{folder.relative_to(PROJECT_ROOT)}`")
    if missing:
        index_lines.extend(["", "## Missing Production Files", ""])
        index_lines.extend(f"- {item}" for item in missing)
    INDEX_OUT.write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print(f"[FIRST-AUDIT-V5-RELEASE] built={len(folders)} missing={len(missing)} root={RELEASE_ROOT}")
    print(f"[FIRST-AUDIT-V5-RELEASE] manifest={MANIFEST_OUT}")
    print(f"[FIRST-AUDIT-V5-RELEASE] contact_sheet={CONTACT_SHEET}")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(build_release())
