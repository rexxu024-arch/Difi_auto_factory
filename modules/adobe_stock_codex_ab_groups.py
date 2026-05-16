"""Build Codex-led Adobe Stock A/B/C review groups.

This is a no-spend preparation step. It does not upload to Adobe, does not call
Vision/Claude, and does not generate images. The output is a compact comparison
queue Rex can review before we spend Midjourney time:

    A - Safe commercial macro background
    B - Premium tactile macro material
    C - Designer-use contextual backdrop

The goal is to test whether Codex-authored stock DNA is good enough before
routing only the best prompts to MJ relaxed drafts and later U-button/2x upscale.
"""

from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

SOURCE_QUEUE = DATABASE / "Adobe_Stock_Daily_Production_Queue.csv"
OUT_CSV = DATABASE / "Adobe_Stock_Codex_AB_Review_Queue.csv"
OUT_MD = REVIEW / "Adobe_Stock_Codex_AB_Review_Queue_latest.md"

FAMILY_PRIORITY = [
    "Kintsugi Marble",
    "Smoky Jade",
    "Walnut Burl",
    "Aged Bronze Patina",
    "Nero Marble",
    "Brushed Titanium",
    "Architectural Concrete",
    "Champagne Frosted Glass",
]

PUBLIC_BAN = {
    "openclaw",
    "first audit",
    "rex",
    "grey",
    "codex",
    "gemini",
    "claude",
    "deepseek",
    "dify",
    "midjourney",
    "sweatshop",
}


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    lowered = text.lower()
    for term in PUBLIC_BAN:
        if term in lowered:
            raise ValueError(f"public ban term leaked into Adobe text: {term}")
    return text


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def family_rank(row: dict[str, str]) -> tuple[int, str]:
    family = row.get("Family", "")
    try:
        rank = FAMILY_PRIORITY.index(family)
    except ValueError:
        rank = len(FAMILY_PRIORITY)
    return rank, family


def unique_families(rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in sorted(rows, key=family_rank):
        family = row.get("Family", "")
        if not family or family in seen:
            continue
        selected.append(row)
        seen.add(family)
        if len(selected) >= limit:
            break
    return selected


def keywords(base: str, extras: list[str]) -> str:
    ordered: list[str] = []
    for item in [*(base or "").split(","), *extras]:
        token = clean(item).lower().strip()
        if not token or token in ordered:
            continue
        ordered.append(token)
    return ",".join(ordered[:35])


def filename(queue_id: str, arm: str, family: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", family.lower()).strip("_")[:18]
    return f"ad_{queue_id[-3:].lower()}_{arm.lower()}_{slug}.jpg"


def build_prompt(row: dict[str, str], arm: str) -> tuple[str, str, str, str]:
    family = clean(row.get("Family", "Premium Material"))
    base_keywords = row.get("Adobe_Keywords", "")
    if arm == "A":
        strategy = "safe commercial stock background"
        title = f"{family} High Resolution Macro Background With Copy Space"
        prompt = (
            f"extreme macro photography of {family.lower()} material background, "
            "clean commercial stock image, realistic surface depth, usable copy space, "
            "balanced studio side lighting, crisp micro texture, natural imperfections, "
            "not flat, not procedural, no object silhouette, no logo, no text, no people, "
            "shot on 100mm macro lens, f/8, ultra sharp focus, 8k detail "
            "--ar 3:2 --style raw --v 6.1 --no letters, watermark, brand, person"
        )
        kws = keywords(base_keywords, ["copy space", "macro background", "commercial texture", "high resolution"])
    elif arm == "B":
        strategy = "premium tactile material close-up"
        title = f"{family} Premium Tactile Material Texture Close Up"
        prompt = (
            f"luxury extreme macro photograph of {family.lower()}, rich tactile relief, "
            "dramatic grazing side light revealing micro ridges, layered physical depth, "
            "subtle color variation, premium interior design material sample, "
            "photorealistic surface, high local contrast without clipping, "
            "shot on 100mm macro lens, controlled studio lighting, 8k detail "
            "--ar 3:2 --style raw --v 6.1 --no text, logo, people, watermark, product label"
        )
        kws = keywords(base_keywords, ["luxury texture", "tactile surface", "material sample", "premium background"])
    else:
        strategy = "designer-use editorial backdrop"
        title = f"{family} Designer Backdrop For Branding And Editorial Layout"
        prompt = (
            f"photorealistic {family.lower()} designer backdrop, macro material plane with "
            "one clean negative-space zone for layout, quiet luxury editorial mood, "
            "premium packaging background, subtle depth and shadow falloff, "
            "commercially useful composition, no centered object, no text, no logo, "
            "shot on 100mm macro lens, f/8, ultra sharp material detail, 8k resolution "
            "--ar 3:2 --style raw --v 6.1 --no letters, watermark, brand, person"
        )
        kws = keywords(base_keywords, ["branding background", "editorial backdrop", "layout background", "negative space"])
    return clean(prompt), clean(title), kws, strategy


def run(family_limit: int = 6) -> dict[str, int]:
    source_rows = [row for row in read_csv(SOURCE_QUEUE) if row.get("Status", "").startswith("READY")]
    if not source_rows:
        raise RuntimeError("No Adobe Stock daily queue rows found. Run adobe_stock_mentor_expander.py first.")

    selected = unique_families(source_rows, family_limit)
    rows: list[dict[str, str]] = []
    generated_at = now_text()
    for idx, src in enumerate(selected, start=1):
        for arm in ("A", "B", "C"):
            prompt, title, kws, strategy = build_prompt(src, arm)
            rows.append(
                {
                    "Review_ID": f"ADOBE-AB-{idx:02d}-{arm}",
                    "Timestamp_ET": generated_at,
                    "Source_Queue_ID": src.get("Queue_ID", ""),
                    "Family": src.get("Family", ""),
                    "Arm": arm,
                    "Strategy": strategy,
                    "MJ_Prompt": prompt,
                    "Target_Filename": filename(src.get("Queue_ID", f"{idx:03d}"), arm, src.get("Family", "")),
                    "Adobe_Title": title[:95],
                    "Adobe_Keywords": kws,
                    "Required_Output": "MJ relaxed draft grid first; selected U image only; final file must be 4MP+ and ideally 2x/upscaled before Adobe upload.",
                    "Rex_Review_Status": "PENDING_REX_VISUAL_REVIEW_AFTER_MJ",
                    "Dispatch_Status": "READY_FOR_MJ_RELAXED_DRAFT_NO_UPLOAD",
                    "Upload_Status": "NO_UPLOAD_UNTIL_IMAGE_QA_PASS",
                }
            )

    write_csv(OUT_CSV, rows)
    REVIEW.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Adobe Stock Codex A/B/C Review Queue",
        "",
        f"Generated: {generated_at}",
        "",
        "Purpose: compare Codex-led, low-cost Adobe Stock prompt strategies before spending visual API budget.",
        "",
        "- A = safe commercial macro background",
        "- B = premium tactile material close-up",
        "- C = designer-use editorial backdrop",
        "",
        "Hard guard: no upload, no Adobe spend, no marketplace write. MJ relaxed draft only until Rex approves an arm.",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['Review_ID']} - {row['Family']} - Arm {row['Arm']}",
                f"- Strategy: {row['Strategy']}",
                f"- Title: {row['Adobe_Title']}",
                f"- Target: `{row['Target_Filename']}`",
                f"- Prompt: `{row['MJ_Prompt']}`",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {generated_at}: Adobe Stock Codex-led A/B/C review queue built; "
            f"families={len(selected)}; prompts={len(rows)}; no upload/spend; "
            f"csv={OUT_CSV.relative_to(PROJECT_ROOT)}.\n"
        )
    return {"families": len(selected), "prompts": len(rows)}


def main() -> None:
    result = run()
    print(f"[ADOBE-CODEX-AB] families={result['families']} prompts={result['prompts']} csv={OUT_CSV}")


if __name__ == "__main__":
    main()
