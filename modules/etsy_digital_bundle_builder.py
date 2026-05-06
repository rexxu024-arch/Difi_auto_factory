"""Build low-bandwidth Etsy digital bundle concepts from prepared printable packs."""

from __future__ import annotations

import csv
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
UPLOAD_QUEUE = DATABASE_DIR / "Etsy_Digital_Upload_Queue.csv"
BUNDLE_CSV = DATABASE_DIR / "Etsy_Digital_Bundle_Queue.csv"
BUNDLE_MD = DATABASE_DIR / "Etsy_Digital_Bundle_Strategy.md"


def load_rows() -> list[dict]:
    with UPLOAD_QUEUE.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def bundle_title(theme: str, count: int) -> str:
    if theme == "Academia":
        return f"Dark Academia Printable Wall Art Bundle {count} Piece Digital Gallery Set"
    if theme == "Zen":
        return f"Zen Printable Wall Art Bundle {count} Piece Meditation Room Digital Set"
    return f"Quiet Relic Printable Wall Art Bundle {count} Piece Digital Download Set"


def bundle_tags(theme: str) -> list[str]:
    base = [
        "digital download",
        "printable art",
        "gallery wall",
        "wall art bundle",
        "instant download",
        "study room decor",
        "quiet relic",
    ]
    if theme == "Academia":
        base += ["dark academia", "library decor", "vintage study", "scholar decor", "book lover gift"]
    elif theme == "Zen":
        base += ["zen decor", "meditation room", "wabi sabi decor", "japanese decor", "calm wall art"]
    else:
        base += ["eclectic decor", "mystic art", "home office art", "printable poster", "art collection"]
    return base[:13]


def build_description(theme: str, rows: list[dict]) -> str:
    titles = "\n".join(f"- {row['ID']}: {row['Title']}" for row in rows)
    return (
        f"{bundle_title(theme, len(rows))}\n\n"
        "Instant digital download bundle. No physical product will be shipped.\n\n"
        "This bundle contains multiple printable wall art designs prepared for home, office, "
        "study room, meditation room, or gallery-wall styling. Each artwork includes five "
        "common JPG print ratios in its own prepared pack: 2:3, 3:4, 4:5, 11x14, and ISO A-series.\n\n"
        "Included source designs:\n"
        f"{titles}\n\n"
        "AI-assisted disclosure: these artworks were created with AI-assisted tools and then curated, "
        "cropped, formatted, and prepared by Quiet Relic Studio.\n\n"
        "Personal use only. Commercial resale, redistribution, and file sharing are not included."
    )


def build() -> list[dict]:
    rows = load_rows()
    academia = [row for row in rows if "Academia" in row["ID"]][:12]
    zen = [row for row in rows if "Zen" in row["ID"]][:4]
    mixed = rows[:8]
    bundles = [
        ("Academia", academia, "19.99"),
        ("Zen", zen, "12.99"),
        ("Mixed", mixed, "17.99"),
    ]
    out = []
    for theme, members, price in bundles:
        if not members:
            continue
        pack_dirs = [row["Pack_Dir"] for row in members]
        out.append(
            {
                "Bundle_ID": f"Digital-Bundle-{theme}",
                "Theme": theme,
                "Member_Count": len(members),
                "Price_USD": price,
                "Title": bundle_title(theme, len(members)),
                "Description": build_description(theme, members),
                "Tags": ", ".join(bundle_tags(theme)),
                "Pack_Dirs_JSON": json.dumps(pack_dirs, ensure_ascii=False),
                "Delivery_Note": "Bundle may need ZIP packaging or PDF link sheet because Etsy allows limited direct files per listing.",
            }
        )
    return out


def write(rows: list[dict]) -> None:
    headers = [
        "Bundle_ID",
        "Theme",
        "Member_Count",
        "Price_USD",
        "Title",
        "Description",
        "Tags",
        "Pack_Dirs_JSON",
        "Delivery_Note",
    ]
    with BUNDLE_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    md = ["# Etsy Digital Bundle Strategy", ""]
    for row in rows:
        md.extend(
            [
                f"## {row['Bundle_ID']}",
                f"- Theme: {row['Theme']}",
                f"- Member count: {row['Member_Count']}",
                f"- Price: ${row['Price_USD']}",
                f"- Title: {row['Title']}",
                f"- Tags: {row['Tags']}",
                f"- Note: {row['Delivery_Note']}",
                "",
            ]
        )
    BUNDLE_MD.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    rows = build()
    write(rows)
    print(f"[DIGITAL-BUNDLE] bundles={len(rows)} csv={BUNDLE_CSV}")
    for row in rows:
        print(f"[DIGITAL-BUNDLE] {row['Bundle_ID']} count={row['Member_Count']} price={row['Price_USD']}")


if __name__ == "__main__":
    main()
