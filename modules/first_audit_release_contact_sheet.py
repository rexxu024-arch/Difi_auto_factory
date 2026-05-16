"""Build a compact review sheet for First Audit release folders.

This is local-only. It helps Rex/Grey review private showcase assets without
opening each one-work folder by hand.
"""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = PROJECT_ROOT / "First_Audit_Release"
OUTPUT = RELEASE_ROOT / "FIRST_AUDIT_RELEASE_CONTACT_SHEET.jpg"
REPORT = RELEASE_ROOT / "FIRST_AUDIT_RELEASE_REVIEW_GUIDE.md"


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


TITLE_FONT = font(34, True)
SMALL_FONT = font(22)
NOTE_FONT = font(18)


def clean_name(path: Path) -> str:
    name = path.name.replace("_", " ")
    return re.sub(r"\s+", " ", name).strip()


def fit(path: Path, size: tuple[int, int]) -> Image.Image:
    canvas = Image.new("RGB", size, (242, 239, 232))
    with Image.open(path) as image:
        image = image.convert("RGB")
        image.thumbnail(size, Image.Resampling.LANCZOS)
        x = (size[0] - image.width) // 2
        y = (size[1] - image.height) // 2
        canvas.paste(image, (x, y))
    return canvas


def release_folders() -> list[Path]:
    if not RELEASE_ROOT.exists():
        return []
    return sorted(
        path
        for path in RELEASE_ROOT.iterdir()
        if path.is_dir() and (path / "01_Hero_Production.png").exists()
    )


def build() -> None:
    folders = release_folders()
    cols = 3
    card_w = 740
    card_h = 880
    margin = 42
    rows = max(1, (len(folders) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * card_w + margin * 2, rows * card_h + margin * 2), (226, 222, 213))
    draw = ImageDraw.Draw(sheet)

    lines = [
        "# THE FIRST AUDIT: 001 Review Guide",
        "",
        f"Release root: `{RELEASE_ROOT}`",
        f"Contact sheet: `{OUTPUT}`",
        "",
        "Review order: first judge the hero image, then check desk and gallery mockups for premium physical presence.",
        "",
    ]

    for index, folder in enumerate(folders):
        col = index % cols
        row = index // cols
        x = margin + col * card_w
        y = margin + row * card_h
        draw.rounded_rectangle([x + 10, y + 10, x + card_w - 20, y + card_h - 20], radius=18, fill=(247, 245, 239), outline=(170, 160, 148), width=2)
        name = clean_name(folder)
        draw.text((x + 36, y + 34), name[:38], fill=(30, 27, 24), font=TITLE_FONT)

        hero = fit(folder / "01_Hero_Production.png", (300, 420))
        desk = fit(folder / "02_Mockup_Luxury_Desk.jpg", (300, 190))
        gallery = fit(folder / "03_Mockup_Art_Gallery.jpg", (300, 190))
        sheet.paste(hero, (x + 52, y + 106))
        sheet.paste(desk, (x + 390, y + 108))
        sheet.paste(gallery, (x + 390, y + 330))

        draw.text((x + 54, y + 548), "Hero production", fill=(72, 65, 58), font=SMALL_FONT)
        draw.text((x + 392, y + 548), "Desk / gallery mockups", fill=(72, 65, 58), font=SMALL_FONT)
        draw.text((x + 54, y + 610), "Folder:", fill=(40, 36, 32), font=SMALL_FONT)
        draw.text((x + 54, y + 646), str(folder.relative_to(PROJECT_ROOT))[:55], fill=(72, 65, 58), font=NOTE_FONT)

        narrative = folder / "04_Narrative_Matrix_CN.md"
        status = "OK" if narrative.exists() else "MISSING COPY"
        draw.text((x + 54, y + 720), f"Narrative: {status}", fill=(45, 80, 56) if status == "OK" else (150, 40, 40), font=SMALL_FONT)
        lines.append(f"- `{folder.name}`: hero + two mockups + narrative = {status}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUTPUT, "JPEG", quality=92, optimize=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[FIRST-AUDIT-RELEASE-SHEET] folders={len(folders)} sheet={OUTPUT}")
    print(f"[FIRST-AUDIT-RELEASE-SHEET] report={REPORT}")


if __name__ == "__main__":
    build()
