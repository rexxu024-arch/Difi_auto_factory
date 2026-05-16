"""Create V7 Etsy listing readiness packet after image QA.

No publishing and no fee spending happens here. The module separates assets into
ready candidates, upscale-review candidates, vectorization holds, and reprompt
holds so the launch runner cannot accidentally publish weak files.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATABASE = ROOT / "Database"
REVIEW = ROOT / "Review_Packets"
MJ_QUEUE = DATABASE / "Etsy_Darwinian_Lab_V7_MJ_Dispatch_Queue.csv"
PACKET_CSV = DATABASE / "Etsy_Darwinian_Lab_V7_Listing_Packet.csv"
PACKET_MD = REVIEW / "ETSY_DARWINIAN_LAB_V7_LISTING_PACKET.md"
NY_TZ = ZoneInfo("America/New_York")


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %z")


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def abs_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path


def upscale_if_needed(path: Path, sku: str, flags: str) -> tuple[str, str]:
    if "LOW_RESOLUTION" not in flags:
        return str(path), ""
    out_dir = path.parent / "production"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{sku}_printable_upscaled.png"
    with Image.open(path) as img:
        rgb = img.convert("RGB")
        w, h = rgb.size
        scale = max(2, int(3000 / max(1, max(w, h))) + 1)
        resized = rgb.resize((w * scale, h * scale), Image.Resampling.LANCZOS)
        resized.save(out)
    return str(out), f"UPSCALED_{scale}X_FROM_{path.name}"


def readiness(row: dict[str, str]) -> tuple[str, str]:
    status = clean(row.get("Visual_QA_Status"))
    flags = clean(row.get("Visual_QA_Flags"))
    pool = clean(row.get("Pool_ID"))
    if not status:
        return "WAITING_VISUAL_QA", "No visual QA best file selected."
    if pool == "POOL07":
        return "HOLD_NEEDS_VECTOR_SVG_DXF", "Laser/CNC product must be converted to closed SVG/DXF before paid Etsy launch."
    if status.startswith("PASS"):
        return "READY_FOR_METADATA_QA", "Image QA passed; prepare Etsy-native final packet."
    if set(filter(None, flags.split(";"))) == {"LOW_RESOLUTION"}:
        return "READY_AFTER_UPSCALE_REVIEW", "Only local metric issue is low resolution; upscaled production file created for review."
    if "PLANNER_CENTER_TOO_BUSY" in flags:
        return "HOLD_REPROMPT_LAYOUT", "Planner needs clear central writing space before it can be sold."
    if "STREETWEAR_THUMBNAIL_WEAK" in flags:
        return "HOLD_REPROMPT_THUMBNAIL", "Streetwear graphic lacks enough thumbnail punch."
    if "TATTOO_FLASH_NOT_BLACK_INK_ONLY" in flags:
        return "HOLD_REPROMPT_BLACK_INK", "Tattoo flash must be pure black ink / white background."
    return "HOLD_REVIEW_REQUIRED", flags or status


def build_packet(limit: int = 0) -> int:
    rows, _ = read_csv(MJ_QUEUE)
    packet: list[dict[str, str]] = []
    touched = 0
    for row in rows:
        if limit and touched >= limit:
            break
        best_file = clean(row.get("Visual_QA_Best_File"))
        if not best_file:
            continue
        sku = clean(row.get("Internal_SKU"))
        status, note = readiness(row)
        source = abs_path(best_file)
        production_file = str(source)
        production_note = ""
        if status == "READY_AFTER_UPSCALE_REVIEW":
            production_file, production_note = upscale_if_needed(source, sku, clean(row.get("Visual_QA_Flags")))
        packet.append(
            {
                "Internal_SKU": sku,
                "Pool_ID": clean(row.get("Pool_ID")),
                "Pool_Name": clean(row.get("Pool_Name")),
                "Format": clean(row.get("Format")),
                "Price_USD": clean(row.get("Price_USD")),
                "Etsy_Title": clean(row.get("Etsy_Title")),
                "Etsy_Tags": clean(row.get("Etsy_Tags")),
                "Etsy_Description": clean(row.get("Etsy_Description")),
                "Source_Image": str(source),
                "Production_File": production_file,
                "Visual_QA_Status": clean(row.get("Visual_QA_Status")),
                "Visual_QA_Flags": clean(row.get("Visual_QA_Flags")),
                "Launch_Readiness": status,
                "Readiness_Note": note,
                "Production_Note": production_note,
                "Publish_Status": "NOT_PUBLISHED_FEE_GUARD_REQUIRED",
                "Prepared_At_ET": now_text(),
            }
        )
        touched += 1
    fields = list(packet[0].keys()) if packet else [
        "Internal_SKU",
        "Pool_ID",
        "Launch_Readiness",
        "Readiness_Note",
        "Prepared_At_ET",
    ]
    write_csv(PACKET_CSV, packet, fields)
    counts: dict[str, int] = {}
    for item in packet:
        counts[item["Launch_Readiness"]] = counts.get(item["Launch_Readiness"], 0) + 1
    lines = [
        "# Etsy Darwinian Lab V7 Listing Packet",
        "",
        f"Generated: {now_text()} America/New_York",
        "",
        "No Etsy fees spent by this module.",
        "",
        "## Readiness Counts",
        "",
    ]
    for key, value in sorted(counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Items", ""])
    for item in packet:
        lines.append(f"### {item['Internal_SKU']} - {item['Pool_Name']}")
        lines.append(f"- Readiness: {item['Launch_Readiness']}")
        lines.append(f"- Note: {item['Readiness_Note']}")
        lines.append(f"- Price: ${item['Price_USD']}")
        lines.append(f"- File: `{item['Production_File']}`")
        lines.append(f"- Title: {item['Etsy_Title']}")
        lines.append("")
    PACKET_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"[ETSY-V7-PACKET] rows={len(packet)} csv={PACKET_CSV}")
    for key, value in sorted(counts.items()):
        print(f"[ETSY-V7-PACKET] {key}={value}")
    print(f"[ETSY-V7-PACKET] report={PACKET_MD}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build V7 Etsy listing readiness packet")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    return build_packet(args.limit)


if __name__ == "__main__":
    raise SystemExit(main())
