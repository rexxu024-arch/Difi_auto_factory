import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config

INDEX_PATH = PROJECT_ROOT / "Database" / "Digital_Printable_Pack_Index.csv"
OUTPUT_PATH = PROJECT_ROOT / "Database" / "Digital_Etsy_Metadata.csv"


def _clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _fit_title(value):
    title = _clean(re.sub(r"[^\x00-\x7F]+", " ", value))
    if len(title) <= 140:
        return title
    words = title.split()
    out = []
    for word in words:
        if len(" ".join(out + [word])) > 140:
            break
        out.append(word)
    return " ".join(out)


def _fallback(row):
    title = _fit_title(
        f"{row['Title']} Printable Wall Art, Dark Academia Decor, Digital Download, Study Room Poster"
    )
    tags = [
        "printable wall art",
        "digital download",
        "dark academia",
        "study room decor",
        "library wall art",
        "poster print",
        "gallery wall",
        "moody decor",
        "scholar decor",
        "instant download",
        "wall art print",
        "home office decor",
        "unique wall art",
    ]
    description = (
        f"Digital printable wall art pack for {row['Title']}.\n\n"
        "This is an instant digital download. No physical item will be shipped.\n\n"
        "Included files:\n"
        "- 2x3 ratio JPG\n"
        "- 3x4 ratio JPG\n"
        "- 4x5 ratio JPG\n"
        "- 5x7 ratio JPG\n"
        "- 11x14 JPG\n\n"
        "AI disclosure: this artwork is an original AI-assisted design curated, edited, and prepared for printable wall art.\n\n"
        "For personal use only. Do not resell or redistribute the files."
    )
    return {"Title": title, "Tags": tags[:13], "Description": description, "Price": "6.99"}


def _deepseek(row):
    api_key = Config.DEEPSEEK_API_KEY
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is missing")
    base_url = (Config.DEEPSEEK_BASE_URL or "https://api.deepseek.com").rstrip("/")
    payload = {
        "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        "messages": [
            {
                "role": "system",
                "content": (
                    "Output strict JSON only. Keys: Title, Tags, Description, Price. "
                    "Create Etsy SEO for a premium digital printable wall art listing. "
                    "Title max 140 chars. Tags must be exactly 13 Etsy-style tags, each <=20 chars. "
                    "Description must clearly say this is a digital download and no physical item is shipped. "
                    "Include AI-assisted artwork disclosure in a tasteful way. "
                    "Tone: premium, poetic, searchable, not spammy."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "source_title": row["Title"],
                        "zip_mb": row["Zip_MB"],
                        "file_ratios": ["2x3", "3x4", "4x5", "5x7", "11x14"],
                        "shop_positioning": "premium Zen, dark academia, jade relic, quiet study decor",
                    },
                    ensure_ascii=False,
                ),
            },
        ],
        "temperature": 0.55,
    }
    response = requests.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=90,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    data = json.loads(content)
    data["Title"] = _fit_title(data.get("Title") or row["Title"])
    tags = []
    seen = set()
    for tag in data.get("Tags") or []:
        tag = _clean(tag).lower()[:20]
        if tag and tag not in seen:
            seen.add(tag)
            tags.append(tag)
    fallback = _fallback(row)["Tags"]
    for tag in fallback:
        if len(tags) >= 13:
            break
        if tag not in seen:
            tags.append(tag)
            seen.add(tag)
    data["Tags"] = tags[:13]
    data["Description"] = _clean(data.get("Description") or _fallback(row)["Description"])
    if "digital" not in data["Description"].lower() or "no physical" not in data["Description"].lower():
        data["Description"] = _fallback(row)["Description"]
    data["Price"] = str(data.get("Price") or "6.99").replace("$", "")
    return data


def _read_index(limit=0, ids=None):
    wanted = {item.strip() for item in (ids or []) if item.strip()}
    existing = set()
    if OUTPUT_PATH.exists() and not wanted:
        with OUTPUT_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                item_id = _clean(row.get("ID"))
                if item_id:
                    existing.add(item_id)
    rows = []
    if not INDEX_PATH.exists():
        return rows
    with INDEX_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if wanted and row.get("ID") not in wanted:
                continue
            if not wanted and row.get("ID") in existing:
                continue
            if row.get("Listing_Status") != "LOCAL_READY_NOT_PUBLISHED":
                continue
            rows.append(row)
            if limit and len(rows) >= limit:
                break
    return rows


def build(limit=10, ids=None, use_api=True):
    rows = _read_index(limit=limit, ids=ids)
    exists = OUTPUT_PATH.exists()
    with OUTPUT_PATH.open("a", encoding="utf-8-sig", newline="", errors="ignore") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "Timestamp",
                "ID",
                "Title",
                "Description",
                "Tags",
                "Price",
                "Zip_Path",
                "Zip_MB",
                "Status",
            ],
        )
        if not exists:
            writer.writeheader()
        done = 0
        for row in rows:
            try:
                meta = _deepseek(row) if use_api else _fallback(row)
            except Exception as exc:
                print(f"[DIGITAL-META-WARN] {row['ID']} fallback: {exc}")
                meta = _fallback(row)
            writer.writerow(
                {
                    "Timestamp": datetime.now().isoformat(timespec="seconds"),
                    "ID": row["ID"],
                    "Title": meta["Title"],
                    "Description": meta["Description"],
                    "Tags": ", ".join(meta["Tags"]),
                    "Price": meta["Price"],
                    "Zip_Path": row["Zip_Path"],
                    "Zip_MB": row["Zip_MB"],
                    "Status": "READY_FOR_ETSY_DRAFT",
                }
            )
            handle.flush()
            done += 1
            print(f"[DIGITAL-META] {row['ID']} tags={len(meta['Tags'])} title_len={len(meta['Title'])}")
    print(f"[DONE] digital etsy metadata rows={done}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--ids", default="")
    parser.add_argument("--no-api", action="store_true")
    args = parser.parse_args()
    ids = [part.strip() for part in args.ids.split(",") if part.strip()]
    build(limit=args.limit, ids=ids, use_api=not args.no_api)


if __name__ == "__main__":
    main()
