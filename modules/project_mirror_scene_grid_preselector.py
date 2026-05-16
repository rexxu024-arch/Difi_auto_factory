"""Split Project Mirror scene grids into local draft crops and preselect cells.

No Midjourney upscale is requested. This is a local-only QA step for
identity-locked scene experiments.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"
QUEUE = DATABASE / "Project_Mirror_Identity_Locked_Scene_Dispatch_Queue.csv"
OUT = DATABASE / "Project_Mirror_Identity_Locked_Scene_Preselect.csv"
CONTACT = REVIEW / "PROJECT_MIRROR_IDENTITY_LOCKED_SCENE_PRESELECT_CONTACT_SHEET.jpg"
REPORT = REVIEW / "PROJECT_MIRROR_IDENTITY_LOCKED_SCENE_PRESELECT.md"
PROGRESS = PROJECT_ROOT / "PROGRESS_LOG.md"


HEADERS = [
    "Queue_ID",
    "Cell",
    "Draft_File",
    "Score",
    "Decision",
    "Identity_Risk",
    "Scene_Value",
    "Notes",
]


def now_et() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M ET")


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


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


def visual_hash(path: Path, size: int = 12) -> str:
    image = Image.open(path).convert("L").resize((size, size), Image.Resampling.LANCZOS)
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    return "".join("1" if px >= avg else "0" for px in pixels)


def hamming(left: str, right: str) -> int:
    return sum(a != b for a, b in zip(left, right))


def apply_duplicate_guard(rows: list[dict[str, str]]) -> None:
    seen: list[tuple[str, str, str]] = []
    for row in rows:
        path = Path(row["Draft_File"])
        if not path.exists():
            continue
        sig = visual_hash(path)
        duplicate_of = ""
        for prior_sig, prior_queue, prior_cell in seen:
            if hamming(sig, prior_sig) <= 6:
                duplicate_of = f"{prior_queue} {prior_cell}"
                break
        if duplicate_of:
            row["Score"] = str(min(int(row["Score"]), 55))
            row["Decision"] = "HOLD_DUPLICATE_SCENE"
            row["Identity_Risk"] = "DUPLICATE"
            row["Scene_Value"] = "LOW"
            row["Notes"] = f"Near-duplicate of {duplicate_of}; hold to avoid repeated marketplace gallery assets. {row['Notes']}"
        else:
            seen.append((sig, row["Queue_ID"], row["Cell"]))


def split_grid(row: dict[str, str]) -> list[dict[str, str]]:
    queue_id = clean(row.get("Internal_SKU"))
    grid_raw = clean(row.get("Grid_File"))
    if not queue_id or not grid_raw:
        return []
    grid_path = PROJECT_ROOT / grid_raw
    if not grid_path.exists():
        return []
    image = Image.open(grid_path).convert("RGB")
    w, h = image.size
    cells = {
        "U1": (0, 0, w // 2, h // 2),
        "U2": (w // 2, 0, w, h // 2),
        "U3": (0, h // 2, w // 2, h),
        "U4": (w // 2, h // 2, w, h),
    }
    out_dir = grid_path.parent / "preselect"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    for cell, box in cells.items():
        crop = image.crop(box)
        out_file = out_dir / f"{queue_id}_{cell}_draft.jpg"
        crop.save(out_file, "JPEG", quality=95, optimize=True)
        score, decision, identity_risk, scene_value, notes = score_cell(queue_id, cell)
        rows.append(
            {
                "Queue_ID": queue_id,
                "Cell": cell,
                "Draft_File": str(out_file),
                "Score": str(score),
                "Decision": decision,
                "Identity_Risk": identity_risk,
                "Scene_Value": scene_value,
                "Notes": notes,
            }
        )
    return rows


def score_cell(queue_id: str, cell: str) -> tuple[int, str, str, str, str]:
    """Small deterministic preselection for known draft-grid layout.

    The first run is visually inspected through the contact sheet. Scores are
    conservative: they only decide which cells deserve Rex/Grey review, not
    which cells can be used commercially.
    """
    if queue_id == "PM-SCENE-001-01":
        table = {
            "U1": (86, "PROMOTE_DRAFT_REVIEW", "LOW", "HIGH", "Strong executive desk context; acrylic thickness and jade-gold face remain readable."),
            "U2": (76, "HOLD_WEAK_CONTEXT", "LOW", "LOW", "Good material preservation but too close/cropped for marketplace scene value."),
            "U3": (88, "PROMOTE_DRAFT_REVIEW", "LOW", "HIGH", "Best balance of product scale, desk realism, and preserved smoky-jade identity."),
            "U4": (82, "PROMOTE_SECONDARY_REVIEW", "LOW", "MEDIUM", "Clean product read; useful backup if U3 identity check passes."),
        }
        return table[cell]
    if queue_id == "PM-SCENE-001-02":
        table = {
            "U1": (79, "REVIEW_DRAFT", "LOW", "MEDIUM", "Readable gallery/plinth context, but product face is cropped too tight."),
            "U2": (72, "HOLD_WEAK_CONTEXT", "MEDIUM", "LOW", "Identity preserved but too macro and not enough spatial persuasion."),
            "U3": (84, "PROMOTE_DRAFT_REVIEW", "LOW", "HIGH", "Best private-gallery balance; plinth reads clearly and object remains premium."),
            "U4": (80, "PROMOTE_SECONDARY_REVIEW", "LOW", "MEDIUM", "Useful backup; product shape is attractive but composition is less calm."),
        }
        return table[cell]
    if queue_id == "PM-SCENE-003-01":
        table = {
            "U1": (75, "HOLD_WEAK_PRODUCT_READ", "MEDIUM", "LOW", "Elegant library scene, but the artwork reads as a blank red/brown placeholder."),
            "U2": (78, "REVIEW_DRAFT", "LOW", "MEDIUM", "Good architectural depth; product is too small for primary sales image."),
            "U3": (87, "PROMOTE_DRAFT_REVIEW", "LOW", "HIGH", "Best framed-poster gallery scene; centered, legible, and visually expensive."),
            "U4": (82, "PROMOTE_SECONDARY_REVIEW", "LOW", "MEDIUM", "Strong corridor mood and good frame scale, but slightly cramped."),
        }
        return table[cell]
    if queue_id == "PM-SCENE-003-02":
        table = {
            "U1": (79, "REVIEW_DRAFT", "LOW", "MEDIUM", "Strong architectural mood, but the artwork risks becoming corridor decoration."),
            "U2": (74, "HOLD_WEAK_PRODUCT_READ", "MEDIUM", "LOW", "Too much tunnel depth; product face is not persuasive enough."),
            "U3": (86, "PROMOTE_DRAFT_REVIEW", "LOW", "HIGH", "Best wall-gallery read; product is visible and scene feels like a credible private study."),
            "U4": (80, "PROMOTE_SECONDARY_REVIEW", "LOW", "MEDIUM", "Good secondary scene; slightly distant but premium enough for gallery support."),
        }
        return table[cell]
    if queue_id == "PM-SCENE-004-01":
        table = {
            "U1": (83, "PROMOTE_SECONDARY_REVIEW", "LOW", "MEDIUM", "Strong Gothic library mood and credible wall scale; product is slightly small."),
            "U2": (77, "REVIEW_DRAFT", "LOW", "MEDIUM", "Clean window-library context, but not enough visual authority for primary use."),
            "U3": (68, "HOLD_FAKE_SCREEN_RISK", "MEDIUM", "LOW", "Risks reading as a digital monitor/UI panel rather than a physical print."),
            "U4": (85, "PROMOTE_DRAFT_REVIEW", "LOW", "HIGH", "Best private-library wall scene; warm light and framed product feel plausible and premium."),
        }
        return table[cell]
    if queue_id == "PM-SCENE-004-02":
        table = {
            "U1": (84, "PROMOTE_DRAFT_REVIEW", "LOW", "HIGH", "Best side-wall gallery scene; product is plausible and the room feels quietly expensive."),
            "U2": (75, "REVIEW_DRAFT", "LOW", "MEDIUM", "Clean but too static; useful only if stronger crops fail."),
            "U3": (82, "PROMOTE_SECONDARY_REVIEW", "LOW", "MEDIUM", "Centered wall scene with clear architecture; product is slightly small but credible."),
            "U4": (76, "REVIEW_DRAFT", "LOW", "MEDIUM", "Good Gothic window mood, but framing feels less intentional."),
        }
        return table[cell]
    default = {
        "U1": (78, "REVIEW_DRAFT", "UNKNOWN", "MEDIUM", "Needs visual review."),
        "U2": (74, "REVIEW_DRAFT", "UNKNOWN", "MEDIUM", "Needs visual review."),
        "U3": (80, "REVIEW_DRAFT", "UNKNOWN", "MEDIUM", "Needs visual review."),
        "U4": (76, "REVIEW_DRAFT", "UNKNOWN", "MEDIUM", "Needs visual review."),
    }
    return default[cell]


def build_contact(rows: list[dict[str, str]]) -> None:
    if not rows:
        REPORT.write_text(f"# Project Mirror Scene Preselect\n\nGenerated: {now_et()}\n\nNo rows.\n", encoding="utf-8")
        return
    cell_w, cell_h = 260, 330
    header_h = 82
    canvas = Image.new("RGB", (cell_w * 4, header_h + cell_h * ((len(rows) + 3) // 4)), (230, 228, 220))
    draw = ImageDraw.Draw(canvas)
    title_font = font(22)
    small = font(14)
    draw.rectangle((0, 0, canvas.width, header_h), fill=(25, 25, 24))
    draw.text((20, 18), "Project Mirror Scene Preselect - draft crops only, no upscale", fill=(245, 243, 236), font=title_font)
    for idx, row in enumerate(rows):
        x = (idx % 4) * cell_w
        y = header_h + (idx // 4) * cell_h
        path = Path(row["Draft_File"])
        canvas.paste(thumb(path, (232, 232)), (x + 14, y + 10))
        color = (28, 110, 55) if row["Decision"].startswith("PROMOTE") else (130, 74, 38)
        draw.text((x + 14, y + 252), f"{row['Queue_ID']} {row['Cell']} | {row['Score']}", fill=(18, 18, 18), font=small)
        draw.text((x + 14, y + 274), row["Decision"][:30], fill=color, font=small)
        draw.text((x + 14, y + 296), row["Scene_Value"], fill=(70, 70, 70), font=small)
    CONTACT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(CONTACT, "JPEG", quality=92, optimize=True)


def write_report(rows: list[dict[str, str]]) -> None:
    lines = [
        "# Project Mirror Identity-Locked Scene Preselect",
        "",
        f"- Generated: {now_et()}",
        f"- Rows: {len(rows)}",
        f"- Contact sheet: `{CONTACT}`",
        "- Policy: local split only; no MJ upscale, no publish, no fee.",
        "",
        "| Queue | Cell | Score | Decision | Risk | Scene | Notes |",
        "| --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['Queue_ID']} | {row['Cell']} | {row['Score']} | {row['Decision']} | {row['Identity_Risk']} | {row['Scene_Value']} | {row['Notes']} |"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    promoted = sum(1 for row in rows if row["Decision"].startswith("PROMOTE"))
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {now_et()} - Project Mirror scene grid preselect\n"
            f"- Split {len(rows)} local draft scene crops; promoted/review={promoted}.\n"
            f"- Output: `{OUT}`; contact sheet: `{CONTACT}`.\n"
            "- No MJ upscale, marketplace publish, or fee action was taken.\n"
        )


def main() -> int:
    rows: list[dict[str, str]] = []
    for row in read_csv(QUEUE):
        if clean(row.get("Harvest_Status")) in {"GRID_FOUND", "READY_FOR_VISUAL_QA"}:
            rows.extend(split_grid(row))
    if not rows:
        print("[PROJECT-MIRROR-SCENE-PRESELECT] no reviewable grids")
        return 0
    apply_duplicate_guard(rows)
    write_csv(OUT, rows)
    build_contact(rows)
    write_report(rows)
    append_progress(rows)
    print(f"[PROJECT-MIRROR-SCENE-PRESELECT] rows={len(rows)} csv={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
