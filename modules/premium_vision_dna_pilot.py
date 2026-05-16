from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.grey_api_client import GreyApiError, extract_text, generate_with_images


PROJECT_MIRROR = ROOT / "Review_Packets" / "Project_Mirror"
SCENE_DIR = PROJECT_MIRROR / "Scene_Promoted"
DB = ROOT / "Database"
OUT_CSV = DB / "Premium_Vision_DNA_Pilot.csv"
OUT_JSON = DB / "Premium_Vision_DNA_Pilot.json"
OUT_MD = PROJECT_MIRROR / "PREMIUM_VISION_DNA_PILOT_REPORT.md"
PROGRESS_LOG = ROOT / "PROGRESS_LOG.md"


PROMPT = """You are Grey, a cold visual-audit engine for Rex's OpenClaw studio.

Analyze the attached images as internal reference material only. Do not copy any source image, do not describe an exact product for resale, and strip all direct IP/source specificity.

For each image in order, return one JSON array item with:
- image_order
- visual_quality_score_0_100
- likely_commercial_role: one of ["routine_pod", "mid_tier_premium", "first_audit_candidate", "reject"]
- material_dna: concise material/texture parameters only
- lighting_dna: light direction, color temperature, shadow behavior
- composition_dna: framing, negative space, object scale, camera logic
- buyer_intent_words: 8-12 Etsy/eBay/private-sale intent words, not generic
- negative_guards: what to avoid in Midjourney so it does not become cheap or AI-looking
- prompt_upgrade: one Midjourney-ready prompt stem that abstracts the DNA without copying the image
- codex_learning_note: what a production engine should learn from this image

Return strict JSON only. No markdown."""


def selected_images(limit: int = 4) -> list[Path]:
    images = sorted(SCENE_DIR.glob("*_REVIEW.jpg"))
    preferred = [p for p in images if "PROMOTE_DRAFT" in p.name]
    selected = preferred[:limit]
    if len(selected) < limit:
        selected += [p for p in images if p not in selected][: limit - len(selected)]
    return selected


def parse_json(text: str) -> Any:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"(\[[\s\S]*\]|\{[\s\S]*\})", text)
        if not match:
            raise
        return json.loads(match.group(1))


def run_vision(images: list[Path]) -> tuple[str, str, Any]:
    errors: list[str] = []
    for tier in ("free", "paid"):
        try:
            payload = generate_with_images(PROMPT, images, tier=tier, timeout=240)
            text = extract_text(payload)
            return tier, text, parse_json(text)
        except (GreyApiError, json.JSONDecodeError) as exc:
            errors.append(f"{tier}: {exc}")
    raise RuntimeError("VISION_DNA_FAILED: " + " | ".join(errors))


def flatten_rows(images: list[Path], data: Any, tier: str) -> list[dict[str, str]]:
    if isinstance(data, dict):
        records = data.get("items") or data.get("results") or [data]
    else:
        records = data
    rows: list[dict[str, str]] = []
    for idx, record in enumerate(records or [], start=1):
        if not isinstance(record, dict):
            continue
        image = images[idx - 1] if idx - 1 < len(images) else Path("")
        rows.append(
            {
                "Image_Order": str(record.get("image_order") or idx),
                "Source_File": str(image.relative_to(ROOT)) if image else "",
                "Vision_Tier_Used": tier,
                "Visual_Quality_Score": str(record.get("visual_quality_score_0_100") or ""),
                "Commercial_Role": str(record.get("likely_commercial_role") or ""),
                "Material_DNA": str(record.get("material_dna") or ""),
                "Lighting_DNA": str(record.get("lighting_dna") or ""),
                "Composition_DNA": str(record.get("composition_dna") or ""),
                "Buyer_Intent_Words": str(record.get("buyer_intent_words") or ""),
                "Negative_Guards": str(record.get("negative_guards") or ""),
                "Prompt_Upgrade": str(record.get("prompt_upgrade") or ""),
                "Codex_Learning_Note": str(record.get("codex_learning_note") or ""),
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build_report(images: list[Path], rows: list[dict[str, str]], raw_text: str, tier: str) -> str:
    avg = 0.0
    scores = []
    for row in rows:
        try:
            scores.append(float(row["Visual_Quality_Score"]))
        except Exception:
            pass
    if scores:
        avg = sum(scores) / len(scores)

    winners = [r for r in rows if r["Commercial_Role"] in {"mid_tier_premium", "first_audit_candidate"}]
    lines: list[str] = [
        "# Premium Vision DNA Pilot",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Vision tier used: {tier}",
        f"Images analyzed: {len(images)}",
        f"Average visual score: {avg:.1f}",
        f"Premium usable rows: {len(winners)}/{len(rows)}",
        "",
        "## Verdict",
        "",
        "Vision parsing is useful for premium/First Audit work when it extracts concrete material, lighting, and composition rules. "
        "It should not replace Rex/Codex taste judgment, and it is overkill for routine low-price POD. Use it selectively for $128+ acrylic, $149 bundle, $295 anchor, and cousin-demo assets.",
        "",
        "## Analyzed Files",
        "",
    ]
    for path in images:
        lines.append(f"- `{path.relative_to(ROOT)}`")
    lines.extend(["", "## Extracted DNA", ""])
    for row in rows:
        lines.extend(
            [
                f"### Image {row['Image_Order']} - {row['Commercial_Role']} / {row['Visual_Quality_Score']}",
                "",
                f"- Source: `{row['Source_File']}`",
                f"- Material DNA: {row['Material_DNA']}",
                f"- Lighting DNA: {row['Lighting_DNA']}",
                f"- Composition DNA: {row['Composition_DNA']}",
                f"- Buyer intent words: {row['Buyer_Intent_Words']}",
                f"- Negative guards: {row['Negative_Guards']}",
                f"- Prompt upgrade: `{row['Prompt_Upgrade']}`",
                f"- Learning note: {row['Codex_Learning_Note']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Raw Model Text",
            "",
            "```json",
            raw_text.strip(),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def append_progress(rows: list[dict[str, str]], tier: str) -> None:
    premium = sum(1 for row in rows if row["Commercial_Role"] in {"mid_tier_premium", "first_audit_candidate"})
    line = (
        f"\n- {datetime.now().strftime('%Y-%m-%d %H:%M')} Premium Vision DNA pilot ran on "
        f"{len(rows)} Project Mirror images via Gemini {tier}; premium usable {premium}/{len(rows)}. "
        f"Outputs: {OUT_CSV.relative_to(ROOT)}, {OUT_MD.relative_to(ROOT)}.\n"
    )
    with PROGRESS_LOG.open("a", encoding="utf-8") as f:
        f.write(line)


def main() -> None:
    images = selected_images()
    if not images:
        raise SystemExit("NO_SCENE_PROMOTED_IMAGES_FOUND")
    tier, raw_text, data = run_vision(images)
    rows = flatten_rows(images, data, tier)
    if not rows:
        raise SystemExit("VISION_RETURNED_NO_ROWS")
    write_csv(rows)
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_MD.write_text(build_report(images, rows, raw_text, tier), encoding="utf-8")
    append_progress(rows, tier)
    print(json.dumps({"images": len(images), "rows": len(rows), "tier": tier, "report": str(OUT_MD)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
