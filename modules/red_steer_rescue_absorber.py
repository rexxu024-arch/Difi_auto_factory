"""Absorb failed/red Steer messages into the durable daily work-block queue.

Rex asked for a recovery path when Codex app Steer messages turn red and the
model never receives them. This module is intentionally small:

1. Read Database/Rex_Red_Steer_Rescue_Inbox.md.
2. Find sections headed "## NEW - ...".
3. Convert each section into a high-priority daily work block.
4. Mark the section "## ABSORBED - ..." with a timestamp.

It does not infer secrets, publish, spend, or execute the rescued content. It
only preserves the instruction as a model-readable work block.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = ROOT / "Database"
REVIEW_DIR = ROOT / "Review_Packets"
INBOX = DATABASE_DIR / "Rex_Red_Steer_Rescue_Inbox.md"
CURRENT_BLOCKS = DATABASE_DIR / "Daily_Work_Blocks_Current.json"
ET = ZoneInfo("America/New_York")


NEW_SECTION_RE = re.compile(
    r"^## NEW - (?P<label>.+?)\n(?P<body>.*?)(?=^## |\Z)",
    re.MULTILINE | re.DOTALL,
)


def now_et() -> datetime:
    return datetime.now(ET)


def today_slug() -> str:
    return now_et().strftime("%Y%m%d")


def queue_path(day: str) -> Path:
    return DATABASE_DIR / f"Daily_Work_Blocks_{day}.json"


def review_path(day: str) -> Path:
    return REVIEW_DIR / f"Daily_Work_Blocks_{day}.md"


def load_blocks() -> dict:
    if CURRENT_BLOCKS.exists():
        try:
            return json.loads(CURRENT_BLOCKS.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            pass
    from modules.daily_work_block_queue import init_queue

    return init_queue(force=False)


def write_blocks(payload: dict) -> None:
    day = payload.get("date") or today_slug()
    payload["updated_at_et"] = now_et().isoformat(timespec="seconds")
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    CURRENT_BLOCKS.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    queue_path(day).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        from modules.daily_work_block_queue import write_markdown

        write_markdown(payload, day)
    except Exception:
        review_path(day).write_text(
            "# Daily Work Blocks\n\n" + json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def build_block(label: str, body: str, index: int) -> dict:
    clean_body = body.strip()
    stamp = now_et().strftime("%H%M%S")
    return {
        "id": f"rescued_steer_{today_slug()}_{stamp}_{index}",
        "title": f"Rescued Rex Steer - {label.strip()[:80]}",
        "project": "Rex Rescue Steer",
        "priority": 110,
        "target_hours": 1.5,
        "task_class": "S/C hybrid",
        "objective": clean_body,
        "allowed_actions": [
            "Treat this as Rex-authored intent because it was copied from a failed Steer message",
            "Execute safely if reversible and inside existing guards",
            "If the rescued instruction is broad, decompose it into the active daily work blocks",
        ],
        "forbidden_actions": [
            "Do not publish, spend, upload, delete, or expose private data unless the rescued text and existing guards explicitly allow it",
            "Do not let this block erase newer delivered Rex chat instructions",
        ],
        "done_criteria": [
            "Instruction is executed, decomposed, or parked with a concrete blocker",
            "Any resulting durable task changes are written back to Daily_Work_Blocks_Current.json",
        ],
        "artifacts": [
            "Database/Rex_Red_Steer_Rescue_Inbox.md",
            "Database/Daily_Work_Blocks_Current.json",
        ],
        "rex_needed_policy": "If ambiguity or risk remains, park this rescued block visibly and continue the next safe block.",
        "status": "IN_PROGRESS",
        "notes": [f"absorbed_from_red_steer_at={now_et().isoformat(timespec='seconds')}"],
    }


def absorb(dry_run: bool = False) -> dict:
    if not INBOX.exists():
        return {"absorbed": 0, "reason": "inbox_missing"}
    text = INBOX.read_text(encoding="utf-8", errors="replace")
    matches = list(NEW_SECTION_RE.finditer(text))
    if not matches:
        return {"absorbed": 0, "reason": "no_NEW_sections"}

    payload = load_blocks()
    blocks = payload.setdefault("blocks", [])
    new_blocks = [build_block(match.group("label"), match.group("body"), i + 1) for i, match in enumerate(matches)]

    # Only one active block should remain active. If a rescued steer exists, it
    # is urgent because Rex explicitly copied it here after delivery failed.
    for block in blocks:
        if block.get("status") == "IN_PROGRESS":
            block["status"] = "PENDING"
    payload["blocks"] = new_blocks + blocks
    payload["policy"] = (
        payload.get("policy", "")
        + " Red Steer rescue inbox has priority over ordinary backlog and below newer delivered Rex messages."
    ).strip()

    absorbed_text = text
    for match in reversed(matches):
        section = match.group(0)
        replacement = section.replace("## NEW -", "## ABSORBED -", 1).rstrip()
        replacement += f"\n\nAbsorbed at {now_et().isoformat(timespec='seconds')} into Daily_Work_Blocks_Current.json.\n"
        absorbed_text = absorbed_text[: match.start()] + replacement + absorbed_text[match.end() :]

    if not dry_run:
        write_blocks(payload)
        INBOX.write_text(absorbed_text, encoding="utf-8")

    return {
        "absorbed": len(new_blocks),
        "dry_run": dry_run,
        "block_ids": [block["id"] for block in new_blocks],
        "current_block": new_blocks[0]["id"] if new_blocks else None,
    }


def selftest() -> dict:
    sample = "## NEW - 2026-05-18 09:30 ET\nContinue monthly tasks; test rescued steer.\n"
    matches = list(NEW_SECTION_RE.finditer(sample))
    block = build_block(matches[0].group("label"), matches[0].group("body"), 1) if matches else {}
    ok = bool(matches and block.get("objective") == "Continue monthly tasks; test rescued steer.")
    return {"status": "PASS" if ok else "FAIL", "matches": len(matches), "sample_block_id": block.get("id")}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    result = selftest() if args.selftest else absorb(dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") != "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
