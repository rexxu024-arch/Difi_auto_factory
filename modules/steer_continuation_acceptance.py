"""Acceptance test for the Steer-continuation recovery path.

This test answers one question: if a Steer message turns red and Rex copies it
into the rescue inbox, will the system recover it into the model-readable daily
work-block queue without destroying the existing queue?

The test is non-destructive: it backs up the inbox/queue, injects a temporary
NEW section, runs the absorber, verifies the resulting block, then restores the
original files.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = ROOT / "Database"
REPORTS_DIR = ROOT / "Reports"
AUTOMATION_DIR = Path.home() / ".codex" / "automations"
ET = ZoneInfo("America/New_York")

INBOX = DATABASE_DIR / "Rex_Red_Steer_Rescue_Inbox.md"
QUEUE = DATABASE_DIR / "Daily_Work_Blocks_Current.json"
RESULT_JSON = DATABASE_DIR / "Steer_Continuation_Acceptance.json"
RESULT_MD = REPORTS_DIR / "Steer_Continuation_Acceptance_latest.md"


def now_et() -> str:
    return datetime.now(ET).isoformat(timespec="seconds")


def today_queue_path() -> Path:
    return DATABASE_DIR / f"Daily_Work_Blocks_{datetime.now(ET).strftime('%Y%m%d')}.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def read_automation(automation_id: str) -> dict:
    path = AUTOMATION_DIR / automation_id / "automation.toml"
    if not path.exists():
        return {}
    with path.open("rb") as handle:
        return tomllib.load(handle)


def run_absorber() -> tuple[int, str]:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "modules" / "red_steer_rescue_absorber.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    return completed.returncode, (completed.stdout + completed.stderr).strip()


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    original_inbox = read_text(INBOX)
    original_queue = read_text(QUEUE)
    daily_queue = today_queue_path()
    original_daily_queue = read_text(daily_queue)
    marker = f"STEER_ACCEPTANCE_{datetime.now(ET).strftime('%Y%m%d_%H%M%S')}"
    checks: list[dict] = []

    try:
        injected = original_inbox.rstrip() + (
            f"\n\n## NEW - {now_et()} {marker}\n"
            "Test-only rescued steer: continue monthly tasks by doing a concrete Adobe Stock metadata QA chunk.\n"
            f"\n\n## NEW - {now_et()} {marker}_SECOND\n"
            "Test-only rescued steer: after the first block, continue to Etsy sticker bundle metadata prep.\n"
        )
        write_text(INBOX, injected)
        rc, output = run_absorber()
        checks.append({"name": "absorber_exit_zero", "ok": rc == 0, "detail": output[:500]})

        queue_payload = json.loads(read_text(QUEUE))
        blocks = queue_payload.get("blocks", [])
        first = blocks[0] if blocks else {}
        second = blocks[1] if len(blocks) > 1 else {}
        checks.append(
            {
                "name": "rescued_block_promoted",
                "ok": first.get("project") == "Rex Rescue Steer" and marker in first.get("title", ""),
                "detail": f"id={first.get('id')} title={first.get('title')}",
            }
        )
        checks.append(
            {
                "name": "multi_steer_order_preserved",
                "ok": second.get("project") == "Rex Rescue Steer" and f"{marker}_SECOND" in second.get("title", ""),
                "detail": f"second_id={second.get('id')} second_title={second.get('title')}",
            }
        )
        checks.append(
            {
                "name": "inbox_marked_absorbed",
                "ok": read_text(INBOX).count("## ABSORBED -") >= 2 and marker in read_text(INBOX),
                "detail": "temporary NEW sections became ABSORBED",
            }
        )

        heartbeat = read_automation("openclaw-current-thread-work-bridge")
        heartbeat_prompt = str(heartbeat.get("prompt", ""))
        checks.append(
            {
                "name": "heartbeat_uses_absorber",
                "ok": "red_steer_rescue_absorber.py" in heartbeat_prompt
                and "Daily_Work_Blocks_Current.json" in heartbeat_prompt,
                "detail": f"status={heartbeat.get('status')} rrule={heartbeat.get('rrule')}",
            }
        )

        worker = read_automation("openclaw-ai-supervised-long-work-block")
        worker_prompt = str(worker.get("prompt", ""))
        checks.append(
            {
                "name": "ai_worker_uses_absorber",
                "ok": worker.get("status") == "ACTIVE"
                and worker.get("reasoning_effort") == "xhigh"
                and "red_steer_rescue_absorber.py" in worker_prompt,
                "detail": f"status={worker.get('status')} model={worker.get('model')}",
            }
        )
    finally:
        write_text(INBOX, original_inbox)
        if original_queue:
            write_text(QUEUE, original_queue)
        if original_daily_queue:
            write_text(daily_queue, original_daily_queue)

    status = "PASS" if all(item["ok"] for item in checks) else "FAIL"
    payload = {"checked_at_et": now_et(), "status": status, "checks": checks}
    RESULT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Steer Continuation Acceptance",
        "",
        f"- checked_at_et: `{payload['checked_at_et']}`",
        f"- status: `{status}`",
        "",
    ]
    for item in checks:
        lines.append(f"- {'PASS' if item['ok'] else 'FAIL'}: {item['name']} - {item['detail']}")
    RESULT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(RESULT_MD.read_text(encoding="utf-8"))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
