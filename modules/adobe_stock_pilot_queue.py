"""Build a guarded Adobe Stock pilot queue.

This module does not upload files. It prepares low-risk background/texture
prompt rows and Adobe CSV metadata shells, with an explicit ban list for any
internal OpenClaw language that must never leak to public stock metadata.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from adobe_stock_isolation import assert_adobe_write_paths
from adobe_stock_two_layer_schema import reconcile_two_layer_tables


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

SOURCE_KEYWORDS = DATABASE / "Adobe_Stock_Keyword_Pack.csv"
OUT_QUEUE = DATABASE / "Adobe_Stock_Pilot_Queue.csv"
OUT_ADOBE_CSV = DATABASE / "Adobe_Stock_Upload_Metadata_DRAFT.csv"
OUT_PACKET = REVIEW / "Adobe_Stock_Pilot_Execution_Packet.md"

ADOBE_CATEGORY_GRAPHIC_RESOURCES = "8"
DEFAULT_LIMIT = 25

PUBLIC_BAN_TERMS = {
    "sweatshop",
    "openclaw",
    "first audit",
    "rex",
    "grey",
    "gemini",
    "codex",
    "midjourney",
    "claude",
    "deepseek",
    "dify",
    "adobe stock passive fortress",
}

IP_RISK_TERMS = {
    "disney",
    "marvel",
    "dc comics",
    "star wars",
    "pokemon",
    "warhammer",
    "lego",
    "pixar",
    "studio ghibli",
    "banksy",
    "basquiat",
    "warhol",
    "haring",
    "yayoikusama",
    "kusama",
    "giger",
}


@dataclass(frozen=True)
class Family:
    name: str
    asset_type: str
    prompt_stem: str
    title_template: str
    keyword_seed: str
    risk_guard: str
    production_spec: str


VARIANTS = [
    ("matte negative space", "matte, subtle, minimal, copy space"),
    ("fine surface grain", "fine grain, tactile, detailed, premium"),
    ("soft gallery light", "gallery light, soft shadow, refined, elegant"),
    ("edge-to-edge seamless field", "seamless, edge to edge, pattern, repeat"),
    ("high contrast studio surface", "contrast, studio, dramatic, crisp"),
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def ascii_slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return re.sub(r"_+", "_", text)


def compact_filename(family: str, index: int) -> str:
    # Adobe CSV filenames must be 30 chars or fewer including the extension.
    base = ascii_slug(family)
    initials = "".join(part[:1] for part in base.split("_") if part)[:4] or "adbe"
    return f"ad_{initials}_{index:04d}.png"


def clean_public_text(text: str, *, max_len: int | None = None) -> str:
    text = re.sub(r"\s+", " ", text.replace(",", " ")).strip()
    lowered = text.lower()
    blocked = PUBLIC_BAN_TERMS | IP_RISK_TERMS
    for term in blocked:
        if term in lowered:
            raise ValueError(f"blocked public term found: {term}")
    if max_len and len(text) > max_len:
        text = text[:max_len].rsplit(" ", 1)[0].strip()
    return text


def split_keywords(seed: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for piece in re.split(r"[;,]", seed):
        kw = clean_public_text(piece.strip().lower())
        if not kw or kw in seen:
            continue
        seen.add(kw)
        out.append(kw)
    return out


def keywords_for(family: Family, variant_keywords: str) -> str:
    base = split_keywords(family.keyword_seed)
    extra = split_keywords(variant_keywords)
    tail = [
        "commercial use",
        "design resource",
        "digital background",
        "decorative surface",
        "high resolution",
        "stock image",
        "graphic resource",
        "material study",
        "surface design",
        "abstract art",
        "visual texture",
        "printable background",
        "modern decor",
        "creative asset",
        "tactile design",
        "sensory texture",
        "interior backdrop",
        "branding background",
        "editorial layout",
        "presentation background",
        "web banner",
        "social media design",
        "packaging design",
        "premium material",
        "copy space",
        "design template",
        "neutral backdrop",
        "decorative pattern",
        "creative workspace",
    ]
    ordered: list[str] = []
    for kw in [*base, *extra, *tail]:
        if kw not in ordered:
            ordered.append(kw)
    return ",".join(ordered[:49])


def load_families(path: Path = SOURCE_KEYWORDS) -> list[Family]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    families: list[Family] = []
    for row in rows:
        families.append(
            Family(
                name=row["Family"],
                asset_type=row["Asset_Type"],
                prompt_stem=row["Prompt_Stem"],
                title_template=row["Title_Template"],
                keyword_seed=row["Keyword_Seed"],
                risk_guard=row["Risk_Guard"],
                production_spec=row["Production_Spec"],
            )
        )
    return families


def build_rows(limit: int) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    families = load_families()
    if not families:
        raise RuntimeError("Adobe keyword family pack is empty. Run adobe_stock_scaffold.py first.")

    queue_rows: list[dict[str, str]] = []
    adobe_rows: list[dict[str, str]] = []
    index = 1
    while len(queue_rows) < limit:
        family = families[(index - 1) % len(families)]
        variant, variant_keywords = VARIANTS[(index - 1) % len(VARIANTS)]
        filename = compact_filename(family.name, index)
        title = clean_public_text(f"{family.title_template} {variant.title()}", max_len=70)
        keywords = keywords_for(family, variant_keywords)
        prompt = clean_public_text(
            f"{family.prompt_stem}, {variant}, no people, no faces, no brand, no logo, no text, no watermark, stock-ready 4K background, clean edges, sRGB --v 6.1 --ar 1:1 --style raw",
            max_len=None,
        )

        row = {
            "ID": f"ADOBE-PILOT-{index:04d}",
            "Status": "READY_FOR_MJ_DRAFT_NO_UPLOAD",
            "Family": family.name,
            "Asset_Type": family.asset_type,
            "Prompt": prompt,
            "Target_Filename": filename,
            "Adobe_Title": title,
            "Adobe_Keywords": keywords,
            "Adobe_Category": ADOBE_CATEGORY_GRAPHIC_RESOURCES,
            "Created_Using_AI": "true",
            "Release_Required": "false",
            "Source_Path": "",
            "QA_Status": "PENDING_IMAGE",
            "Upload_Status": "BLOCKED_UNTIL_IMAGE_QA_AND_REX_OR_GUARD_APPROVAL",
            "Risk_Guard": family.risk_guard,
        }
        queue_rows.append(row)
        adobe_rows.append(
            {
                "Filename": filename,
                "Title": title,
                "Keywords": keywords,
                "Category": ADOBE_CATEGORY_GRAPHIC_RESOURCES,
                "Releases": "",
            }
        )
        index += 1
    return queue_rows, adobe_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_packet(queue_rows: list[dict[str, str]]) -> None:
    families = sorted({row["Family"] for row in queue_rows})
    lines = [
        "# Adobe Stock Pilot Execution Packet",
        "",
        f"Generated: {now_text()}",
        "",
        "Scope: local-only Adobe Stock pilot queue for background, texture, and material assets.",
        "",
        "## Hard Guards",
        "",
        "- The internal codename is forbidden in public filenames, titles, keywords, CSV rows, and uploads.",
        "- Do not submit First Audit, Etsy, eBay, or private-client hero artwork to Adobe Stock.",
        "- Every asset is AI-generated and must be marked as Created using generative AI tools in Adobe Contributor.",
        "- Do not upload until image QA passes: 4K/sRGB, no text, no watermark, no faces, no brand, no IP reference, no near-duplicate spam.",
        "- Use category 8, Graphic Resources, for this pilot queue unless Adobe Contributor UI requires a different category at review time.",
        "",
        "## Pilot Queue",
        "",
        f"- Rows prepared: {len(queue_rows)}",
        f"- Families: {', '.join(families)}",
        f"- Queue CSV: `{OUT_QUEUE.relative_to(PROJECT_ROOT)}`",
        f"- Draft Adobe metadata CSV: `{OUT_ADOBE_CSV.relative_to(PROJECT_ROOT)}`",
        "",
        "## Next Execution",
        "",
        "1. Dispatch a small batch of 5-10 prompt rows in Relaxed mode.",
        "2. Run image QA and duplicate QA locally.",
        "3. Only after QA, create the real Adobe CSV using actual filenames and submit a tiny pilot batch.",
    ]
    OUT_PACKET.parent.mkdir(parents=True, exist_ok=True)
    OUT_PACKET.write_text("\n".join(lines), encoding="utf-8")


def append_progress(count: int) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock pilot queue prepared; rows={count}; "
            f"no upload, no public metadata leak, no platform spend.\n"
        )


def main() -> None:
    raise SystemExit(
        "DEPRECATED_ADOBE_FLAT_QUEUE_DISABLED: Rex rejected the old flat/--ar 1:1 "
        "Adobe Stock queue on 2026-05-16. Use modules/adobe_stock_mentor_expander.py "
        "and strict macro/upscale QA only."
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    assert_adobe_write_paths((OUT_QUEUE, OUT_ADOBE_CSV, OUT_PACKET))
    queue_rows, adobe_rows = build_rows(args.limit)
    if not args.dry_run:
        write_csv(OUT_QUEUE, queue_rows)
        write_csv(OUT_ADOBE_CSV, adobe_rows)
        write_packet(queue_rows)
        mentor_count, production_count = reconcile_two_layer_tables(write_progress=False)
        append_progress(len(queue_rows))
    else:
        mentor_count, production_count = (0, 0)
    print(
        f"[ADOBE-PILOT] rows={len(queue_rows)} dry_run={args.dry_run} "
        f"queue={OUT_QUEUE} two_layer={mentor_count}/{production_count}"
    )


if __name__ == "__main__":
    main()
