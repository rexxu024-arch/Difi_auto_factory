"""Dispatch Operation Shock & Awe V5 prompts to Midjourney one safe batch at a time."""

from __future__ import annotations

import argparse
import csv
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import mj_harvest

DEFAULT_QUEUE = PROJECT_ROOT / "Database" / "Shock_And_Awe_V5_MJ_Dispatch_Queue.csv"
QUEUE = DEFAULT_QUEUE
NY_TZ = ZoneInfo("America/New_York")
CONFIRM_TIMEOUT_SECONDS = 75
CONFIRM_POLL_SECONDS = 5
_IMAGINE_COMMAND_CACHE: dict | None = None


def clean_prompt(value: str) -> str:
    return " ".join(str(value or "").replace("\n", " ").replace("\r", " ").split()).strip()


def prompt_for_signature(prompt: str) -> str:
    """Use semantic text for confirmation, not volatile MJ image URLs.

    Midjourney often rewrites Discord/CDN image prompts into short s.mj.run
    links in the visible channel echo. Matching the full original URL therefore
    produces false unconfirmed states. Strip leading image URLs or local
    reference paths before computing the durable signature.
    """
    text = clean_prompt(prompt)
    parts = text.split(" ", 1)
    if len(parts) == 2:
        first = parts[0].lower()
        if first.startswith("http://") or first.startswith("https://") or first.endswith((".png", ".jpg", ".jpeg", ".webp")):
            return parts[1]
    return text


def read_rows(queue: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not queue.exists():
        raise FileNotFoundError(f"Missing queue: {queue}")
    with queue.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def write_rows(queue: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    needed = [
        "Dispatched_At_ET",
        "Dispatch_Response_Status",
        "Dispatch_Confirm_Message_ID",
        "Dispatch_Error",
    ]
    for field in needed:
        if field not in fields:
            fields.append(field)
    with queue.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build_payload(prompt: str) -> dict:
    command = get_imagine_command()
    data = {
        "version": mj_harvest.Config.MJ_VERSION,
        "id": mj_harvest.Config.MJ_ID,
        "name": "imagine",
        "type": 1,
        "options": [{"type": 3, "name": "prompt", "value": prompt}],
        "attachments": [],
    }
    if command:
        data["application_command"] = command
    return {
        "type": 2,
        "application_id": mj_harvest.Config.APP_ID,
        "guild_id": mj_harvest.Config.GUILD_ID,
        "channel_id": mj_harvest.Config.CHANNEL_ID,
        "session_id": mj_harvest.Config.SESSION_ID,
        "data": data,
        "nonce": str(int(time.time() * 1000)) + str(random.randint(100, 999)),
    }


def get_imagine_command() -> dict | None:
    global _IMAGINE_COMMAND_CACHE
    if _IMAGINE_COMMAND_CACHE is not None:
        return _IMAGINE_COMMAND_CACHE
    try:
        response = mj_harvest.requests.get(
            f"https://discord.com/api/v9/applications/{mj_harvest.Config.APP_ID}/commands",
            headers={"Authorization": mj_harvest.Config.TOKEN},
            timeout=12,
        )
        response.raise_for_status()
        for command in response.json():
            if str(command.get("name") or "") == "imagine":
                _IMAGINE_COMMAND_CACHE = command
                return command
    except Exception:
        pass
    _IMAGINE_COMMAND_CACHE = {}
    return None


def prompt_signature(prompt: str) -> str:
    return mj_harvest._prompt_signature(prompt_for_signature(prompt), length=140)


def confirm_discord_echo(
    prompt: str,
    timeout_seconds: int = CONFIRM_TIMEOUT_SECONDS,
    excluded_ids: set[str] | None = None,
) -> str:
    """Return the Discord message id if Midjourney Bot visibly accepted it.

    Discord's interaction endpoint can return a 2xx response while the command
    never becomes a visible Midjourney task. Treating 2xx as success created
    false positives in the production queue. A dispatch now needs a persistent
    Midjourney Bot channel echo before it is marked MJ_SUBMITTED. Transient
    command-invocation echoes can appear and disappear; those are deliberately
    ignored.
    """
    signature = prompt_signature(prompt)
    excluded_ids = excluded_ids or set()
    if not signature:
        return ""
    deadline = time.time() + max(10, timeout_seconds)
    while time.time() < deadline:
        try:
            messages = mj_harvest._fetch_recent_messages(100)
        except Exception:
            messages = []
        for message in messages if isinstance(messages, list) else []:
            author = str(message.get("author", {}).get("username") or "")
            if author.lower() != "midjourney bot":
                continue
            content = message.get("content", "")
            message_id = str(message.get("id") or "")
            if message_id in excluded_ids:
                continue
            if signature in mj_harvest._normalize_match_text(content):
                candidate = str(message.get("id") or "")
                time.sleep(12)
                try:
                    still_recent = mj_harvest._fetch_recent_messages(100)
                except Exception:
                    still_recent = []
                if any(str(item.get("id") or "") == candidate for item in still_recent if isinstance(still_recent, list)):
                    return candidate
        time.sleep(CONFIRM_POLL_SECONDS)
    return ""


def dispatch(limit: int, dry_run: bool = False, queue: Path = DEFAULT_QUEUE) -> int:
    mj_harvest._validate_runtime_config()
    rows, fields = read_rows(queue)
    ready = [row for row in rows if str(row.get("Dispatch_Status") or "").strip() == "READY_FOR_MJ"]
    if not ready:
        print("[SHOCK-MJ-IDLE] no READY_FOR_MJ rows")
        return 0

    sent = 0
    for row in rows:
        if sent >= limit:
            break
        if str(row.get("Dispatch_Status") or "").strip() != "READY_FOR_MJ":
            continue
        sku = str(row.get("Internal_SKU") or "").strip()
        prompt = clean_prompt(row.get("MJ_Master_Prompt") or "")
        if not prompt:
            row["Dispatch_Status"] = "MJ_DISPATCH_HOLD"
            row["Dispatch_Error"] = "empty prompt"
            continue
        output = PROJECT_ROOT / str(row.get("Output_Folder") or f"Output/Shock_And_Awe/V5/Zone2/{sku}")
        output.mkdir(parents=True, exist_ok=True)
        if dry_run:
            sent += 1
            print(f"[SHOCK-MJ-DRY] {sku} prompt_chars={len(prompt)}")
            continue
        try:
            try:
                before_messages = mj_harvest._fetch_recent_messages(100)
                before_ids = {str(item.get("id") or "") for item in before_messages if isinstance(before_messages, list)}
            except Exception:
                before_ids = set()
            response = mj_harvest._interaction(build_payload(prompt))
            if not response:
                raise RuntimeError("Discord interaction returned no response")
            row["Dispatched_At_ET"] = datetime.now(NY_TZ).strftime("%Y-%m-%d %I:%M:%S %p %Z")
            row["Dispatch_Response_Status"] = str(getattr(response, "status_code", ""))
            confirm_id = confirm_discord_echo(prompt, excluded_ids=before_ids)
            if not confirm_id:
                row["Dispatch_Status"] = "MJ_SUBMIT_UNCONFIRMED_RETRY"
                row["Dispatch_Confirm_Message_ID"] = ""
                row["Dispatch_Error"] = "Discord interaction returned 2xx but no Midjourney channel echo within confirmation window"
                print(f"[SHOCK-MJ-UNCONFIRMED] {sku} response={row['Dispatch_Response_Status']}")
                write_rows(queue, rows, fields)
                return 2
            row["Dispatch_Status"] = "MJ_SUBMITTED"
            row["Dispatch_Confirm_Message_ID"] = confirm_id
            row["Dispatch_Error"] = ""
            sent += 1
            print(f"[SHOCK-MJ-SUBMITTED] {sku} prompt_chars={len(prompt)} echo={confirm_id}")
            write_rows(queue, rows, fields)
            time.sleep(8)
        except Exception as exc:
            row["Dispatch_Status"] = "MJ_DISPATCH_FAILED"
            row["Dispatch_Error"] = repr(exc)[:500]
            print(f"[SHOCK-MJ-FAILED] {sku}: {exc}")
            write_rows(queue, rows, fields)
            return 1
    write_rows(queue, rows, fields)
    print(f"[SHOCK-MJ-DONE] submitted={sent}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Dispatch Shock & Awe V5 MJ prompts")
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return dispatch(max(1, args.limit), args.dry_run, Path(args.queue))


if __name__ == "__main__":
    raise SystemExit(main())
