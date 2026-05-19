"""Build a durable daily work-block queue for Rex's monthly shift.

This is deliberately plain. The queue is not a daemon and not a second brain;
it is a written contract for what the chat model should do next when awakened.
The heartbeat/steer layer can read this file and execute one multi-hour block
instead of shrinking into a 20-second watchdog check.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = ROOT / "Database"
REVIEW_DIR = ROOT / "Review_Packets"
ET = ZoneInfo("America/New_York")

CURRENT_PATH = DATABASE_DIR / "Daily_Work_Blocks_Current.json"


@dataclass
class WorkBlock:
    id: str
    title: str
    project: str
    priority: int
    target_hours: float
    task_class: str
    objective: str
    allowed_actions: list[str]
    forbidden_actions: list[str]
    done_criteria: list[str]
    artifacts: list[str]
    rex_needed_policy: str
    status: str = "PENDING"
    notes: list[str] = field(default_factory=list)


def now_et() -> datetime:
    return datetime.now(ET)


def today_slug(value: date | None = None) -> str:
    return (value or now_et().date()).strftime("%Y%m%d")


def queue_path(day: str) -> Path:
    return DATABASE_DIR / f"Daily_Work_Blocks_{day}.json"


def review_path(day: str) -> Path:
    return REVIEW_DIR / f"Daily_Work_Blocks_{day}.md"


def build_default_blocks() -> list[WorkBlock]:
    """Create today's simple, long-running work blocks.

    Priority reflects Rex's current 3-day ordering:
    1. Adobe Stock quality/product production
    2. Etsy sticker digital bundles
    3. Daily Etsy/eBay quality listing and performance work
    4. Reporting/Gemini/Git/system hygiene
    5. First Audit, now less urgent until early June
    """
    return [
        WorkBlock(
            id="adobe_stock_quality_batch",
            title="Adobe Stock quality batch and Rex-trained DNA",
            project="Adobe Stock",
            priority=100,
            target_hours=4.0,
            task_class="S-Class",
            objective=(
                "Produce and QA a batch of stock-safe high-quality material/background assets "
                "using Rex-approved visual DNA, market evidence, and local resolution guards."
            ),
            allowed_actions=[
                "Generate or extend mentor/product-line queues from approved DNA",
                "Prepare MJ relaxed prompts and harvest U/source images when thermal guard allows",
                "Run local resolution/sharpness/metadata QA and build Adobe upload-ready packs",
                "Move uncertain images to /adobe-qa for Rex review without blocking the rest",
            ],
            forbidden_actions=[
                "Do not use Midjourney Fast/upscale for Adobe Stock unless Rex explicitly changes this",
                "Do not upload flat, blurry, dirty, repetitive, or 4MP-failing assets",
                "Do not submit marketplace uploads during heartbeat/watchdog-only turns",
            ],
            done_criteria=[
                "At least one batch of approved or review-ready assets is created",
                "Metadata QA passes for title/keywords/category/AI disclosure",
                "Rejected/old flat assets are isolated from production paths",
            ],
            artifacts=[
                "Database/Adobe_Stock_Daily_Production_Queue.csv",
                "Database/Adobe_Stock_Daily_Upload_Ready.csv",
                "Review_Packets/Adobe_Stock_*",
            ],
            rex_needed_policy=(
                "If visual taste is uncertain, park it in the Adobe QA UI and continue with "
                "research, metadata, or safer families."
            ),
        ),
        WorkBlock(
            id="etsy_sticker_bundle_liquidation",
            title="Etsy digital sticker bundle packaging",
            project="Etsy Digital Warehouse",
            priority=90,
            target_hours=2.0,
            task_class="C-Class",
            objective=(
                "Convert existing sticker/POD remnants into Etsy-style digital asset packs "
                "without treating them as primary POD products."
            ),
            allowed_actions=[
                "Use U/high-resolution sticker assets, not raw grid drafts",
                "Build 20/20/50-count split ZIP packs with each ZIP <= Etsy file limit",
                "Generate Etsy-style titles and descriptions with specs mostly in description",
            ],
            forbidden_actions=[
                "Do not delete original internal source folders",
                "Do not publish blindly if ZIP size/spec/preview guard fails",
                "Do not use eBay-style cold utility titles on Etsy",
            ],
            done_criteria=[
                "Ready ZIP packs and metadata CSV exist",
                "Buyer expectations list PNG, transparent background, DPI, pixel range, ZIP volumes",
                "Preview mockups contain watermarked samples only",
            ],
            artifacts=[
                "Database/Sticker_Liquidation/",
                "Release/Digital_Warehouse/",
                "Reports/Sticker_Liquidation_Report_latest.md",
            ],
            rex_needed_policy="No Rex pause unless package size or account safety blocks publish.",
        ),
        WorkBlock(
            id="marketplace_daily_drip_and_performance",
            title="Etsy/eBay daily quality listing and performance cycle",
            project="Printify / Etsy / eBay",
            priority=82,
            target_hours=3.0,
            task_class="S/C hybrid",
            objective=(
                "Keep daily high-quality listing flow alive and inspect performance data without "
                "blind mass publishing or unsafe UI retries."
            ),
            allowed_actions=[
                "Publish within Rex budget only when account/fee/QA guards allow",
                "Prefer POD poster/acrylic over low-value digital or sticker listings",
                "Read Etsy/eBay traffic and prepare candidate fixes or new high-intent listings",
            ],
            forbidden_actions=[
                "Do not force Etsy UI login/publish if login anomaly or red banner appears",
                "Do not mass-end listings without a safe dry-run queue and clear criteria",
                "Do not keep pushing sticker POD as a primary eBay strategy",
            ],
            done_criteria=[
                "Daily publish/readback target attempted or explicitly parked with reason",
                "Traffic/performance artifacts refreshed",
                "Next listing candidates prioritized from observed evidence",
            ],
            artifacts=[
                "Database/Etsy_*",
                "Database/eBay_*",
                "Database/Printify_*",
            ],
            rex_needed_policy=(
                "If eBay policy/API eligibility or Etsy login needs owner action, mark Rex-needed "
                "and continue non-blocked marketplace work."
            ),
        ),
        WorkBlock(
            id="system_report_gemini_git",
            title="Daily report, Gemini bridge, Git hygiene, and loop selftest",
            project="System / Gemini / Git",
            priority=60,
            target_hours=1.0,
            task_class="C-Class",
            objective=(
                "At low-priority windows, compress real progress into reports, verify continuity, "
                "and keep the repository clean without staging private output assets."
            ),
            allowed_actions=[
                "Run continuity selftest and work-proof report",
                "Build Gemini Chat payload for the exact Codex automation thread",
                "Stage/push code only, excluding output/design/private asset folders",
            ],
            forbidden_actions=[
                "Do not let reporting replace production work outside the reporting window",
                "Do not stage output folders, private design assets, screenshots, or bulky caches",
            ],
            done_criteria=[
                "Daily SitRep includes progress, decisions, rejected advice, blockers",
                "Continuity selftest passes or lists exact failures",
                "Git ignore/checkpoint status is clean enough to recover on a new computer",
            ],
            artifacts=[
                "Reports/",
                "Review_Packets/Gemini_Bridge/",
                "Database/Monthly_Shift_Continuity_Selftest.json",
            ],
            rex_needed_policy="Only ask Rex for credentials, payments, private login, or destructive cleanup.",
        ),
        WorkBlock(
            id="first_audit_private_studio",
            title="First Audit private studio assets",
            project="First Audit",
            priority=55,
            target_hours=2.0,
            task_class="S-Class",
            objective=(
                "Maintain and improve private high-end release folders, but keep this behind "
                "Adobe Stock and daily marketplace production until cousin deadline approaches."
            ),
            allowed_actions=[
                "Improve release folders, contact sheets, and narrative matrices",
                "Use premium DNA learnings when relevant",
                "Keep one-design-one-folder structure",
            ],
            forbidden_actions=[
                "Do not spend high-cost upscale resources without Rex top-1% selection",
                "Do not leak First Audit assets into Etsy warehouse or Adobe Stock",
            ],
            done_criteria=[
                "Review folder/contact sheet shows only meaningful candidates",
                "Rex QA items are clearly separated from completed assets",
            ],
            artifacts=[
                "First_Audit_Release/",
                "Review_Packets/First_Audit*",
            ],
            rex_needed_policy="Park visual final selection for Rex and continue other safe work.",
        ),
    ]


def load_queue(day: str) -> dict | None:
    path = queue_path(day)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return None


def current_block(payload: dict) -> dict | None:
    for block in payload.get("blocks", []):
        if block.get("status") in {"PENDING", "IN_PROGRESS"}:
            return block
    return None


def write_queue(payload: dict, day: str) -> None:
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    path = queue_path(day)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    CURRENT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(payload, day)


def write_markdown(payload: dict, day: str) -> None:
    current = current_block(payload)
    lines = [
        f"# Daily Work Blocks {day}",
        "",
        f"- generated_at_et: `{payload.get('generated_at_et')}`",
        f"- policy: `{payload.get('policy')}`",
        f"- current_block: `{current.get('id') if current else 'none'}`",
        "",
    ]
    for block in payload.get("blocks", []):
        lines.extend(
            [
                f"## {block['priority']} - {block['title']}",
                "",
                f"- id: `{block['id']}`",
                f"- project: `{block['project']}`",
                f"- class: `{block['task_class']}`",
                f"- target_hours: `{block['target_hours']}`",
                f"- status: `{block['status']}`",
                f"- objective: {block['objective']}",
                f"- Rex-needed policy: {block['rex_needed_policy']}",
                "",
                "Allowed:",
            ]
        )
        lines.extend(f"- {item}" for item in block["allowed_actions"])
        lines.append("")
        lines.append("Forbidden:")
        lines.extend(f"- {item}" for item in block["forbidden_actions"])
        lines.append("")
        lines.append("Done criteria:")
        lines.extend(f"- {item}" for item in block["done_criteria"])
        lines.append("")
    review_path(day).write_text("\n".join(lines), encoding="utf-8")


def init_queue(force: bool = False) -> dict:
    day = today_slug()
    existing = load_queue(day)
    if existing and not force:
        CURRENT_PATH.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(existing, day)
        return existing
    blocks = [asdict(block) for block in build_default_blocks()]
    if blocks:
        blocks[0]["status"] = "IN_PROGRESS"
    payload = {
        "date": day,
        "generated_at_et": now_et().isoformat(timespec="seconds"),
        "policy": (
            "This queue is the durable steer replacement. The active main project should run as "
            "a long single-thread work block for hours; git checkpoints and current-thread "
            "visibility are sidecars only, not replacements for real project work."
        ),
        "blocks": blocks,
    }
    write_queue(payload, day)
    return payload


def advance(block_id: str, status: str, note: str = "") -> dict:
    day = today_slug()
    payload = load_queue(day) or init_queue(force=True)
    status = status.upper()
    for block in payload["blocks"]:
        if block["id"] == block_id:
            block["status"] = status
            block.setdefault("notes", []).append(f"{now_et().isoformat(timespec='seconds')} {note}".strip())
            break
    if status in {"DONE", "PARKED", "SKIPPED"}:
        for block in payload["blocks"]:
            if block["status"] == "PENDING":
                block["status"] = "IN_PROGRESS"
                break
    payload["updated_at_et"] = now_et().isoformat(timespec="seconds")
    write_queue(payload, day)
    return payload


def print_status(payload: dict) -> None:
    current = current_block(payload)
    done = sum(1 for block in payload.get("blocks", []) if block.get("status") == "DONE")
    total = len(payload.get("blocks", []))
    print(
        json.dumps(
            {
                "date": payload.get("date"),
                "done": done,
                "total": total,
                "current": current,
                "path": str(queue_path(payload.get("date") or today_slug())),
                "review_path": str(review_path(payload.get("date") or today_slug())),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create/read the daily chat-model work-block queue.")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--advance")
    parser.add_argument("--to", choices=["DONE", "PARKED", "SKIPPED", "IN_PROGRESS", "PENDING"])
    parser.add_argument("--note", default="")
    args = parser.parse_args()

    if args.advance:
        payload = advance(args.advance, args.to or "DONE", args.note)
    elif args.init or args.force:
        payload = init_queue(force=args.force)
    else:
        payload = load_queue(today_slug()) or init_queue(force=False)
    print_status(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
