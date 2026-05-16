from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules.resilient_http import request_with_retry

DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
RAW = DATABASE / "Printify_Catalog_Raw"
NY = ZoneInfo("America/New_York")


TRACKS = [
    {
        "track": "Tower",
        "keywords": ["acrylic", "photo block", "acrylic print", "framed", "frame", "canvas", "wall art", "metal", "wood"],
        "exclude": ["t-shirt", "tee", "hoodie", "tank", "onesie", "sock"],
        "why": "Private high-ticket visual object: depth, wall presence, museum/gift use.",
    },
    {
        "track": "Base",
        "keywords": ["phone case", "tough case", "mug", "notebook", "journal", "poster", "matte", "puzzle", "ornament", "sticker"],
        "exclude": ["t-shirt", "tee", "hoodie"],
        "why": "Lower barrier gifts and channel samples when private buyer wants volume.",
    },
    {
        "track": "Experimental",
        "keywords": ["lamp", "blanket", "throw", "tapestry", "pillow", "clock", "calendar", "card", "tray"],
        "exclude": ["shirt", "tee"],
        "why": "Possible private-client extension after visual fit and mockups are verified.",
    },
]


def headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {Config.Printify_API_KEY}"}


def get_json(path: str, cache_name: str) -> object:
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / cache_name
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    response = request_with_retry("GET", f"{Config.Printify_API_URL.rstrip()}{path}", headers=headers(), timeout=45, attempts=3)
    response.raise_for_status()
    data = response.json()
    cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def clean_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def score_blueprint(bp: dict) -> list[dict[str, object]]:
    title = str(bp.get("title") or "")
    description = clean_html(str(bp.get("description") or ""))
    hay = f"{title} {description}".lower()
    rows = []
    for track in TRACKS:
        if any(term in hay for term in track["exclude"]):
            continue
        hits = [term for term in track["keywords"] if term in hay]
        if not hits:
            continue
        score = len(hits) * 10
        if any(term in hay for term in ["premium", "fine art", "gallery", "acrylic", "framed", "canvas", "metal"]):
            score += 12
        if any(term in hay for term in ["usa", "assembled", "pinewood", "plexiglass", "satin", "matte"]):
            score += 5
        rows.append(
            {
                "Track": track["track"],
                "Blueprint_ID": bp.get("id"),
                "Blueprint_Title": title,
                "Score": score,
                "Matched_Keywords": ", ".join(hits),
                "Why": track["why"],
                "Description_Snippet": description[:260],
            }
        )
    return rows


def build(limit: int = 40) -> None:
    DATABASE.mkdir(exist_ok=True)
    REVIEW.mkdir(exist_ok=True)
    data = get_json("/catalog/blueprints.json", "all_blueprints.json")
    blueprints = data if isinstance(data, list) else data.get("data", [])
    scored = []
    for bp in blueprints:
        if isinstance(bp, dict):
            scored.extend(score_blueprint(bp))
    scored.sort(key=lambda row: (-int(row["Score"]), str(row["Track"]), str(row["Blueprint_Title"])))
    top = scored[:limit]

    csv_path = DATABASE / "Shock_And_Awe_Blueprint_RnD.csv"
    fields = ["Track", "Blueprint_ID", "Blueprint_Title", "Score", "Matched_Keywords", "Why", "Description_Snippet", "Initial_Decision"]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in top:
            decision = "PRIORITY_VERIFY_PROVIDER_VARIANTS" if row["Track"] == "Tower" else "VERIFY_AFTER_ZONE2"
            writer.writerow({**row, "Initial_Decision": decision})

    md_path = REVIEW / "OPERATION_SHOCK_AND_AWE_V5_BLUEPRINT_RND_20260509.md"
    lines = [
        "# Operation Shock and Awe V5 - Printify Blueprint R&D",
        "",
        f"Generated: {datetime.now(NY).strftime('%Y-%m-%d %H:%M:%S %z')}",
        "",
        "Purpose: expand product formats for private-client high-ticket visual assets while staying on official Printify catalog truth.",
        "",
        "## Important Correction",
        "- User/Grey target IDs 107, 118, 211, and 1 do not resolve as official Printify blueprints in the current API.",
        "- User/Grey target ID 518 resolves to Single Jersey T-shirt, and 11 resolves to Women's Jersey Short Sleeve Deep V-Neck Tee.",
        "- For production payloads, use verified official blueprint IDs only.",
        "",
        "## Top Candidates",
    ]
    for row in top[:24]:
        lines.extend(
            [
                f"### {row['Track']} - Blueprint {row['Blueprint_ID']} - {row['Blueprint_Title']}",
                f"- Score: {row['Score']} | matched: {row['Matched_Keywords']}",
                f"- Why: {row['Why']}",
                f"- Snippet: {row['Description_Snippet']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[SHOCK-RND] csv={csv_path}")
    print(f"[SHOCK-RND] report={md_path}")
    print(f"[SHOCK-RND] candidates={len(top)}")


if __name__ == "__main__":
    build()
