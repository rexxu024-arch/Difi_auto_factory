from __future__ import annotations

import csv
import os
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
REVIEW_DIR = PROJECT_ROOT / "Review_Packets"
INVENTORY_CSV = DATABASE_DIR / "SSD_Migration_Inventory.csv"
PLAN_MD = REVIEW_DIR / "SSD_1TB_ASSET_MIGRATION_PLAN.md"

ASSET_DIRS = [
    ("Output", "hot_assets", "Generated source images and production folders."),
    ("Release", "studio_release", "Public/controlled release packets and high-value assets."),
    ("First_Audit_Release", "private_studio", "Private First Audit release folders. Do not upload to git."),
    ("Review_Packets", "review_packets", "Contact sheets, reports, and Gemini/Rex review material."),
    ("harvest_results", "mj_harvest", "Midjourney harvest artifacts."),
    ("audit_harvest", "audit_harvest", "Audit/harvest scratch outputs."),
]

KEEP_INTERNAL = [
    ".venv",
    ".git",
    "Database",
    "modules",
    "scripts",
]


def bytes_for(path: Path) -> int:
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    total = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in {".git", ".venv", "__pycache__"}]
        for name in files:
            fp = Path(root) / name
            try:
                total += fp.stat().st_size
            except OSError:
                continue
    return total


def human_size(value: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{value} B"


def drive_candidates() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for letter in "DEFGHIJKLMNOPQRSTUVWXYZ":
        root = Path(f"{letter}:\\")
        if not root.exists():
            continue
        try:
            total, used, free = os.statvfs(root)  # type: ignore[attr-defined]
        except Exception:
            try:
                import shutil

                total, used, free = shutil.disk_usage(root)
            except Exception:
                total = used = free = 0
        rows.append(
            {
                "drive": str(root),
                "total": human_size(total),
                "free": human_size(free),
            }
        )
    return rows


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    DATABASE_DIR.mkdir(exist_ok=True)
    REVIEW_DIR.mkdir(exist_ok=True)

    rows = []
    total_movable = 0
    for rel, class_name, note in ASSET_DIRS:
        path = PROJECT_ROOT / rel
        size = bytes_for(path)
        total_movable += size
        rows.append(
            {
                "path": rel,
                "exists": str(path.exists()),
                "asset_class": class_name,
                "size_bytes": str(size),
                "size_human": human_size(size),
                "migration_action": "move_to_ssd_then_junction" if path.exists() else "create_on_ssd_when_needed",
                "note": note,
            }
        )

    with INVENTORY_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "path",
                "exists",
                "asset_class",
                "size_bytes",
                "size_human",
                "migration_action",
                "note",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    drive_rows = drive_candidates()
    drive_lines = (
        "\n".join(f"- {row['drive']}: total {row['total']}, free {row['free']}" for row in drive_rows)
        if drive_rows
        else "- No non-C: drive detected yet. Re-run after the PNY 1TB SSD is plugged in."
    )
    asset_lines = "\n".join(
        f"- `{row['path']}`: {row['size_human']} -> {row['migration_action']} ({row['asset_class']})"
        for row in rows
    )
    keep_lines = "\n".join(f"- `{item}`" for item in KEEP_INTERNAL)
    PLAN_MD.write_text(
        "\n".join(
            [
                "# PNY 1TB SSD Migration Plan",
                "",
                f"Generated: {now} ET",
                "",
                "Purpose: make OpenClaw portable and keep C: from filling while preserving fast local execution.",
                "",
                "## Current Drive Candidates",
                "",
                drive_lines,
                "",
                "## Move To SSD",
                "",
                asset_lines,
                "",
                f"Estimated currently movable asset footprint: {human_size(total_movable)}.",
                "",
                "## Keep On Internal Disk",
                "",
                keep_lines,
                "",
                "Reason: code, virtualenv, git metadata, and active databases should stay on the fastest/stablest internal disk unless benchmarking proves otherwise.",
                "",
                "## Arrival Procedure",
                "",
                "1. Plug in the PNY 1TB SSD and format it as NTFS if Windows asks.",
                "2. Create `OpenClaw_Assets`, `OpenClaw_Backups`, and `OpenClaw_AdobeStock` folders on the SSD.",
                "3. Re-run `py modules\\ssd_migration_plan.py` to refresh the drive candidate list.",
                "4. Move only asset directories first, then create NTFS junctions back to the original paths.",
                "5. Verify with checksums and a small Printify/Etsy/Adobe dry run before deleting any duplicate local copy.",
                "",
                "## Policy",
                "",
                "- Never put `.env`, OAuth tokens, browser profiles, or payment/account material on the external drive.",
                "- Do not git-track raw assets, release images, private showcase art, or marketplace image packs.",
                "- Treat the SSD as an asset warehouse and cold/warm production buffer, not as the primary code runtime until tested.",
            ]
        ),
        encoding="utf-8",
    )
    print(f"[SSD-MIGRATION] rows={len(rows)} total={human_size(total_movable)}")
    print(f"[SSD-MIGRATION] inventory={INVENTORY_CSV}")
    print(f"[SSD-MIGRATION] plan={PLAN_MD}")


if __name__ == "__main__":
    main()
