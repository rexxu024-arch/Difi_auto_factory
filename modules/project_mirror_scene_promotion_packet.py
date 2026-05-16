"""Package promoted Project Mirror scene crops into a review folder."""

from __future__ import annotations

import csv
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB = PROJECT_ROOT / "Database" / "Project_Mirror_Identity_Locked_Scene_Preselect.csv"
OUT_DIR = PROJECT_ROOT / "Review_Packets" / "Project_Mirror" / "Scene_Promoted"
CONTACT = OUT_DIR / "PROJECT_MIRROR_SCENE_PROMOTED_CONTACT_SHEET.jpg"
REPORT = OUT_DIR / "PROJECT_MIRROR_SCENE_PROMOTED_PACKET.md"
PROGRESS = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")


def now_et() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M ET")


def read_rows() -> list[dict[str, str]]:
    if not DB.exists():
        return []
    with DB.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def font(size: int) -> ImageFont.ImageFont:
    for name in ("arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def thumb(path: Path, size: tuple[int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    out = Image.new("RGB", size, (242, 240, 234))
    out.paste(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return out


def main() -> int:
    rows = [
        row
        for row in read_rows()
        if str(row.get("Decision") or "").startswith("PROMOTE")
        and "DUPLICATE" not in str(row.get("Decision") or "")
    ]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    packaged: list[dict[str, str]] = []
    for row in rows:
        src = Path(row["Draft_File"])
        if not src.exists():
            continue
        dest = OUT_DIR / f"{row['Queue_ID']}_{row['Cell']}_{row['Decision']}.jpg"
        shutil.copy2(src, dest)
        item = dict(row)
        item["Packaged_File"] = str(dest)
        packaged.append(item)

    cell_w, cell_h = 300, 360
    header_h = 88
    cols = 3
    contact = Image.new(
        "RGB",
        (cell_w * cols, header_h + cell_h * max(1, ((len(packaged) + cols - 1) // cols))),
        (230, 228, 220),
    )
    draw = ImageDraw.Draw(contact)
    draw.rectangle((0, 0, contact.width, header_h), fill=(24, 24, 22))
    draw.text((22, 18), "Project Mirror promoted scene crops", fill=(245, 243, 236), font=font(24))
    draw.text((22, 52), "Review only. Local draft crops. No upscale / no publish / no fee.", fill=(206, 202, 190), font=font(14))
    for idx, row in enumerate(packaged):
        x = (idx % cols) * cell_w
        y = header_h + (idx // cols) * cell_h
        contact.paste(thumb(Path(row["Packaged_File"]), (260, 260)), (x + 20, y + 12))
        draw.text((x + 20, y + 284), f"{row['Queue_ID']} {row['Cell']} | {row['Score']}", fill=(20, 20, 20), font=font(14))
        draw.text((x + 20, y + 306), row["Decision"][:32], fill=(28, 105, 54), font=font(14))
        draw.text((x + 20, y + 328), row["Scene_Value"], fill=(76, 76, 72), font=font(13))
    contact.save(CONTACT, "JPEG", quality=92, optimize=True)

    lines = [
        "# Project Mirror Promoted Scene Packet",
        "",
        f"- Generated: {now_et()}",
        f"- Promoted crops: {len(packaged)}",
        f"- Folder: `{OUT_DIR}`",
        f"- Contact sheet: `{CONTACT}`",
        "- Policy: review-only scene candidates; no upscale, no public listing, no marketplace fee.",
        "",
        "| Queue | Cell | Score | Scene | File | Notes |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for row in packaged:
        lines.append(
            f"| {row['Queue_ID']} | {row['Cell']} | {row['Score']} | {row['Scene_Value']} | `{row['Packaged_File']}` | {row['Notes']} |"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {now_et()} - Project Mirror promoted scene packet\n"
            f"- Packaged {len(packaged)} promoted scene crop(s) for Rex/Grey review.\n"
            f"- Folder: `{OUT_DIR}`; contact sheet: `{CONTACT}`.\n"
            "- No upscale, publish, or fee action was taken.\n"
        )
    print(f"[PM-SCENE-PROMOTED-PACKET] packaged={len(packaged)} folder={OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
