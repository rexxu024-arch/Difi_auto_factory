"""Build a final Etsy upload packet for local digital printable listings."""

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
UPLOAD_QUEUE = DATABASE_DIR / "Etsy_Digital_Upload_Queue.csv"
PREVIEW_QUEUE = DATABASE_DIR / "Etsy_Digital_Preview_Assets.csv"
EXPORT_CSV = DATABASE_DIR / "Etsy_Digital_Final_Upload_Packet.csv"
EXPORT_MD = DATABASE_DIR / "Etsy_Digital_Final_Upload_Packet.md"


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_tags(tags: str) -> str:
    values = []
    seen = set()
    for tag in (tags or "").split(","):
        clean = tag.strip().lower()
        if not clean or clean in seen:
            continue
        seen.add(clean)
        values.append(clean[:20])
    return ", ".join(values[:13])


def tidy_title(title: str) -> str:
    replacements = [
        ("Wall Art Wall Art", "Wall Art"),
        ("Decor Wall Library", "Library Decor"),
        ("Decor Wall Study", "Study Wall Decor"),
        ("Decor Wall Gift Room", "Wall Decor Gift"),
        ("Decor Wall Digital", "Wall Decor Digital"),
        ("Timeless Tomes", "Reading Nook"),
        ("Mentor Wisdom", "Scholar Decor"),
        ("Academia Mentor-Grade", "Dark Academia"),
    ]
    clean = " ".join((title or "").split())
    for old, new in replacements:
        clean = clean.replace(old, new)
    words = clean.split()
    compact = []
    for word in words:
        if compact and compact[-1].lower() == word.lower():
            continue
        compact.append(word)
    return " ".join(compact)[:140].strip()


def build() -> list[dict]:
    preview_map = {row.get("ID", ""): row for row in read_csv(PREVIEW_QUEUE)}
    rows = []
    for row in read_csv(UPLOAD_QUEUE):
        item_id = row.get("ID", "")
        previews = preview_map.get(item_id, {})
        title = tidy_title(row.get("Title", ""))
        tags = normalize_tags(row.get("Tags", ""))
        export = {
            "ID": item_id,
            "Listing_Status": "Prepared_Not_Uploaded",
            "Platform": "Etsy",
            "Shop_Positioning": "Quiet Relic Studio",
            "Type": "Digital",
            "Price_USD": row.get("Price_USD", "9.99"),
            "Quantity": "999",
            "Title": title,
            "Description": row.get("Description", "").strip(),
            "Tags": tags,
            "Materials": "digital jpg, printable wall art, instant download",
            "AI_Disclosure": row.get("AI_Disclosure", ""),
            "License": row.get("License", ""),
            "Preview_Image_1": previews.get("Preview_1", ""),
            "Preview_Image_2": previews.get("Preview_2", ""),
            "Preview_Image_3": previews.get("Preview_3", ""),
            "Digital_File_1": row.get("Digital_File_1", ""),
            "Digital_File_2": row.get("Digital_File_2", ""),
            "Digital_File_3": row.get("Digital_File_3", ""),
            "Digital_File_4": row.get("Digital_File_4", ""),
            "Digital_File_5": row.get("Digital_File_5", ""),
            "Source_Path": row.get("Source_Path", ""),
        }
        rows.append(export)
    return rows


def write_outputs(rows: list[dict]) -> None:
    headers = [
        "ID",
        "Listing_Status",
        "Platform",
        "Shop_Positioning",
        "Type",
        "Price_USD",
        "Quantity",
        "Title",
        "Description",
        "Tags",
        "Materials",
        "AI_Disclosure",
        "License",
        "Preview_Image_1",
        "Preview_Image_2",
        "Preview_Image_3",
        "Digital_File_1",
        "Digital_File_2",
        "Digital_File_3",
        "Digital_File_4",
        "Digital_File_5",
        "Source_Path",
    ]
    with EXPORT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    md = [
        "# Etsy Digital Final Upload Packet",
        "",
        f"- Listings prepared: {len(rows)}",
        "- Status: local assets and copy prepared; no Etsy listing fees triggered.",
        "- Upload mode: manual UI or Etsy API after approval/token setup.",
        "- Files per listing: 3 preview images plus 5 instant-download JPG files.",
        "- Default price: $9.99 single printable wall art set.",
        "- Bundle concepts are tracked separately in Database/Etsy_Digital_Bundle_Queue.csv.",
        "",
        "## First 20 Listings",
        "",
    ]
    for idx, row in enumerate(rows, start=1):
        md.append(f"{idx}. {row['ID']} - ${row['Price_USD']} - {row['Title']}")
    EXPORT_MD.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    rows = build()
    write_outputs(rows)
    print(f"[ETSY-DIGITAL-EXPORT] rows={len(rows)} csv={EXPORT_CSV}")
    print(f"[ETSY-DIGITAL-EXPORT] md={EXPORT_MD}")


if __name__ == "__main__":
    main()
