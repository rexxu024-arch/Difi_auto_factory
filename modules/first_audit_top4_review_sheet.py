from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "Database" / "First_Audit_V5_Zones1_3_Release_Manifest.csv"
OUT_DIR = ROOT / "Review_Packets"
TOP_IDS = ["V5-02", "V5-08", "V5-10", "V5-19"]


def load_manifest() -> list[dict[str, str]]:
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def safe_open(path_text: str) -> Image.Image:
    path = ROOT / path_text
    im = Image.open(path).convert("RGB")
    return im


def fit_image(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    canvas = Image.new("RGB", size, (246, 244, 239))
    copy = im.copy()
    copy.thumbnail(size, Image.LANCZOS)
    x = (size[0] - copy.width) // 2
    y = (size[1] - copy.height) // 2
    canvas.paste(copy, (x, y))
    return canvas


def build_sheet(rows: list[dict[str, str]]) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    font_path = next(
        (
            p
            for p in [
                Path("C:/Windows/Fonts/msyh.ttc"),
                Path("C:/Windows/Fonts/simhei.ttf"),
                Path("C:/Windows/Fonts/arial.ttf"),
            ]
            if p.exists()
        ),
        None,
    )
    font = ImageFont.truetype(str(font_path), 17) if font_path else ImageFont.load_default()
    title_font = ImageFont.truetype(str(font_path), 24) if font_path else ImageFont.load_default()

    cell_w, cell_h = 330, 430
    info_w = 460
    margin = 36
    gap = 18
    row_h = cell_h + 64
    width = margin * 2 + cell_w * 3 + info_w + gap * 3
    height = margin * 2 + row_h * len(rows) + 70
    sheet = Image.new("RGB", (width, height), (238, 235, 228))
    draw = ImageDraw.Draw(sheet)

    draw.text(
        (margin, 18),
        "FIRST AUDIT V5 TOP 4 REVIEW - DRAFT ONLY / NO FAST UPSCALE",
        fill=(22, 22, 20),
        font=title_font,
    )
    draw.text(
        (margin, 42),
        "Review these before spending MJ Fast/Upscale minutes.",
        fill=(70, 70, 64),
        font=font,
    )

    y = margin + 54
    labels = ["Hero", "Desk Mockup", "Gallery Mockup"]
    for row in rows:
        draw.rounded_rectangle(
            (margin - 10, y - 12, width - margin + 10, y + row_h - 20),
            radius=14,
            fill=(250, 249, 246),
            outline=(205, 201, 193),
            width=1,
        )
        x = margin
        for label, key in [
            ("Hero", "Hero_File"),
            ("Desk", "Desk_Mockup"),
            ("Gallery", "Gallery_Mockup"),
        ]:
            im = fit_image(safe_open(row[key]), (cell_w, cell_h))
            sheet.paste(im, (x, y))
            draw.text((x + 8, y + cell_h + 8), label, fill=(40, 40, 36), font=font)
            x += cell_w + gap

        info_x = x
        info_lines = [
            f"{row['Release_ID']} | {row['SKU']}",
            row["Chinese_Name"],
            row["Concept_Name"],
            f"Carrier: {row['Source_Product_Vector']}",
            f"Tier: {row['Tier']}",
            "Action: Rex selects / rejects before Fast Upscale.",
        ]
        text_y = y + 12
        for line in info_lines:
            draw.text((info_x, text_y), line, fill=(32, 32, 28), font=font)
            text_y += 28
        y += row_h

    out = OUT_DIR / "First_Audit_V5_Zones1_3_TOP4_CONTACT_SHEET.jpg"
    sheet.save(out, quality=92)
    return out


def build_markdown(rows: list[dict[str, str]], sheet_path: Path) -> Path:
    lines = [
        "# First Audit V5 Top 4 Review",
        "",
        "Purpose: give Rex a fast, visual Top 1% selection packet before any MJ Fast/Upscale spend.",
        "",
        f"Contact sheet: `{sheet_path}`",
        "",
        "## Candidates",
        "",
    ]
    for row in rows:
        folder = ROOT / Path(row["Hero_File"]).parent
        lines.extend(
            [
                f"### {row['Release_ID']} - {row['Chinese_Name']}",
                "",
                f"- SKU: `{row['SKU']}`",
                f"- Concept: {row['Concept_Name']}",
                f"- Carrier: {row['Source_Product_Vector']}",
                f"- Tier: {row['Tier']}",
                f"- Folder: `{folder}`",
                f"- Narrative: `{ROOT / row['Narrative_File']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Resource Rule",
            "",
            "- Relaxed Mode can continue draft exploration for high-value concepts.",
            "- Fast/Upscale is locked until Rex selects a Top 1% candidate.",
            "- No marketplace publishing from this packet.",
            "",
        ]
    )
    out = OUT_DIR / "First_Audit_V5_Zones1_3_TOP4_REVIEW.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> int:
    manifest = load_manifest()
    by_id = {row["Release_ID"]: row for row in manifest}
    rows = [by_id[rid] for rid in TOP_IDS if rid in by_id]
    if len(rows) != len(TOP_IDS):
        missing = sorted(set(TOP_IDS) - {row["Release_ID"] for row in rows})
        raise SystemExit(f"missing release ids: {missing}")
    sheet = build_sheet(rows)
    md = build_markdown(rows, sheet)
    print(f"[TOP4] sheet={sheet}")
    print(f"[TOP4] review={md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
