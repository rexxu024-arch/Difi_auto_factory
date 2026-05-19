"""Harvest Midjourney outputs for Operation Shock & Awe V5.

This module is intentionally separate from the production-line harvester because
the private showcase prompts were submitted as concept prompts, not normal
Production_Line IDs. Matching therefore uses a prompt signature plus Discord
message references instead of ID_* tags.
"""

from __future__ import annotations

import argparse
import csv
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
NY_TZ = ZoneInfo("America/New_York")
EXTRA_FIELDS = [
    "Harvest_Status",
    "Grid_Message_ID",
    "Grid_File",
    "U1_File",
    "U2_File",
    "U3_File",
    "U4_File",
    "Last_Harvest_ET",
    "Harvest_Error",
    "Grid_Wait_First_ET",
    "Grid_Wait_Attempts",
]
TERMINAL_HARVEST_STATES = {
    "READY_FOR_VISUAL_QA",
    "VISUAL_QA_PASSED",
    "GRID_FOUND",
    "GRID_TIMEOUT_HOLD",
    "HARVEST_HOLD",
    "HARVEST_HOLD_DUPLICATE_GRID_ID",
    "VISUAL_QA_HOLD_IDENTITY_DRIFT",
}
GRID_WAIT_MAX_ATTEMPTS = 12
GRID_WAIT_MAX_MINUTES = 45
DISCORD_HISTORY_SCAN_LIMIT = 600


def clean(value: object) -> str:
    return str(value or "").strip()


def prompt_for_signature(prompt: str) -> str:
    """Use semantic text for matching, not volatile image-reference URLs."""
    text = " ".join(clean(prompt).replace("\n", " ").replace("\r", " ").split())
    parts = text.split(" ", 1)
    if len(parts) == 2:
        first = parts[0].lower()
        if first.startswith("http://") or first.startswith("https://") or first.endswith((".png", ".jpg", ".jpeg", ".webp")):
            return parts[1]
    return text


def now_et_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %I:%M:%S %p %Z")


def parse_et(value: str) -> datetime | None:
    raw = clean(value)
    if not raw:
        return None
    tz_hint = None
    if raw.endswith(" EDT"):
        raw = raw[:-4]
        tz_hint = NY_TZ
    elif raw.endswith(" EST"):
        raw = raw[:-4]
        tz_hint = NY_TZ
    for fmt in ("%Y-%m-%d %I:%M:%S %p %Z", "%Y-%m-%d %I:%M:%S %p", "%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M:%S %Z"):
        try:
            parsed = datetime.strptime(raw, fmt)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=tz_hint or NY_TZ)
            return parsed.astimezone(NY_TZ)
        except ValueError:
            continue
    try:
        parsed = datetime.fromisoformat(raw)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=NY_TZ)
        return parsed.astimezone(NY_TZ)
    except ValueError:
        return None


def minutes_since(value: str) -> int:
    parsed = parse_et(value)
    if not parsed:
        return 0
    return int((datetime.now(NY_TZ) - parsed).total_seconds() // 60)


def increment_grid_wait(row: dict[str, str]) -> tuple[int, int]:
    first_seen = clean(row.get("Grid_Wait_First_ET"))
    if not first_seen:
        row["Grid_Wait_First_ET"] = now_et_text()
        first_seen = row["Grid_Wait_First_ET"]
    try:
        attempts = int(clean(row.get("Grid_Wait_Attempts")) or "0") + 1
    except ValueError:
        attempts = 1
    row["Grid_Wait_Attempts"] = str(attempts)
    age_candidates = [
        minutes_since(first_seen),
        minutes_since(clean(row.get("Dispatched_At_ET"))),
        minutes_since(clean(row.get("Created_At_ET"))),
    ]
    age_minutes = max(age_candidates)
    return attempts, age_minutes


def read_rows(queue: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not queue.exists():
        raise FileNotFoundError(f"Missing queue: {queue}")
    with queue.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        for field in EXTRA_FIELDS:
            if field not in fields:
                fields.append(field)
        return list(reader), fields


def write_rows(queue: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with queue.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def output_dir(row: dict[str, str]) -> Path:
    sku = clean(row.get("Internal_SKU"))
    raw = clean(row.get("Output_Folder")) or f"Output/Shock_And_Awe/V5/Zone2/{sku}"
    path = PROJECT_ROOT / raw
    path.mkdir(parents=True, exist_ok=True)
    return path


def min_upscale_dim(row: dict[str, str]) -> int:
    product_type = clean(row.get("Product_Type")).lower()
    prompt = clean(row.get("MJ_Master_Prompt")).lower()
    # 2:1 mug wraps from Midjourney commonly resolve to 1536x768. That is
    # acceptable for a concept/demo wrap and should not be rejected by the
    # vertical poster/acrylic short-edge gate.
    if product_type == "mug" or "--ar 2:1" in prompt or "panoramic mug wrap" in prompt:
        return 700
    return 850


def prompt_signature(row: dict[str, str]) -> str:
    prompt = clean(row.get("MJ_Master_Prompt"))
    return mj_harvest._prompt_signature(prompt_for_signature(prompt), length=140)


def message_text(message: dict) -> str:
    return mj_harvest._normalize_match_text(message.get("content", ""))


def message_has_signature(message: dict, signature: str) -> bool:
    return bool(signature and signature in message_text(message))


def id_after(message_id: str, anchor_id: str) -> bool:
    """Discord snowflakes increase over time; use them to avoid old prompt matches."""
    if not anchor_id:
        return True
    try:
        return int(clean(message_id)) > int(clean(anchor_id))
    except ValueError:
        return True


def find_grid_message(messages: list[dict], row: dict[str, str], excluded_ids: set[str] | None = None) -> dict | None:
    excluded_ids = excluded_ids or set()
    grid_id = clean(row.get("Grid_Message_ID"))
    confirm_id = clean(row.get("Dispatch_Confirm_Message_ID"))
    signature = prompt_signature(row)
    for message in messages:
        message_id = clean(message.get("id"))
        if message_id in excluded_ids:
            continue
        if (grid_id and message_id == grid_id) or (confirm_id and message_id == confirm_id):
            if message.get("attachments") and not mj_harvest._is_incomplete_midjourney_message(message):
                return message
            continue
    for message in messages:
        message_id = clean(message.get("id"))
        if message_id in excluded_ids:
            continue
        if not message.get("attachments"):
            continue
        if "Image #" in clean(message.get("content")):
            continue
        if mj_harvest._is_incomplete_midjourney_message(message):
            continue
        if confirm_id and not id_after(message_id, confirm_id):
            continue
        if message_has_signature(message, signature):
            return message
    return None


def fetch_recent_messages_paged(total_limit: int = DISCORD_HISTORY_SCAN_LIMIT) -> list[dict]:
    """Fetch recent Discord messages across pages.

    Discord only returns up to 100 messages per request. Shock & Awe prompts can
    be hours old by the time the cruise loop harvests them, so a single recent
    page is not enough and causes false grid-missing holds.
    """
    messages: list[dict] = []
    before = ""
    while len(messages) < total_limit:
        limit = min(100, total_limit - len(messages))
        url = f"https://discord.com/api/v9/channels/{mj_harvest.Config.CHANNEL_ID}/messages?limit={limit}"
        if before:
            url += f"&before={before}"
        response = mj_harvest.requests.get(
            url,
            headers={"Authorization": mj_harvest.Config.TOKEN},
            timeout=12,
        )
        response.raise_for_status()
        page = response.json()
        if not isinstance(page, list) or not page:
            break
        messages.extend(page)
        before = clean(page[-1].get("id"))
        if len(page) < limit or not before:
            break
        time.sleep(0.35)
    return messages


def fetch_message_by_id(message_id: str) -> dict | None:
    mid = clean(message_id)
    if not mid:
        return None
    response = mj_harvest.requests.get(
        f"https://discord.com/api/v9/channels/{mj_harvest.Config.CHANNEL_ID}/messages/{mid}",
        headers={"Authorization": mj_harvest.Config.TOKEN},
        timeout=12,
    )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        return None
    if not data.get("attachments") or mj_harvest._is_incomplete_midjourney_message(data):
        return None
    return data


def resolve_grid_message(messages: list[dict], row: dict[str, str], excluded_ids: set[str] | None = None) -> dict | None:
    excluded_ids = excluded_ids or set()
    grid = find_grid_message(messages, row, excluded_ids=excluded_ids)
    if grid:
        return grid
    grid_id = clean(row.get("Grid_Message_ID"))
    if not grid_id or grid_id in excluded_ids:
        return None
    try:
        grid = fetch_message_by_id(grid_id)
        if grid and grid.get("attachments") and clean(grid.get("id")) not in excluded_ids:
            return grid
    except Exception as exc:
        row["Harvest_Error"] = f"Grid_Message_ID fetch failed: {repr(exc)[:220]}"
    return None


def u_index(message: dict) -> str:
    content = clean(message.get("content"))
    marker = "Image #"
    if marker not in content:
        return ""
    tail = content.split(marker, 1)[1].strip()
    return tail[:1] if tail[:1] in {"1", "2", "3", "4"} else ""


def find_u_messages(messages: list[dict], row: dict[str, str]) -> dict[str, dict]:
    grid_id = clean(row.get("Grid_Message_ID"))
    signature = prompt_signature(row)
    found: dict[str, dict] = {}
    for message in messages:
        idx = u_index(message)
        if not idx or not message.get("attachments"):
            continue
        if grid_id and clean(mj_harvest._message_reference_id(message)) == grid_id:
            found[idx] = message
            continue
        if grid_id:
            # Once a concrete grid message is known, U images must be tied to
            # that Discord reference. Signature fallback is useful only before
            # a grid id exists; otherwise similar stock prompts can steal older
            # U-buttons and silently duplicate prior assets.
            continue
        if message_has_signature(message, signature):
            found[idx] = message
    return found


def harvest(limit: int, queue: Path = DEFAULT_QUEUE, trigger_upscales: bool = False) -> int:
    mj_harvest._validate_runtime_config()
    rows, fields = read_rows(queue)
    candidates = [
        row
        for row in rows
        if clean(row.get("Dispatch_Status")) == "MJ_SUBMITTED"
        and clean(row.get("Harvest_Status")) not in TERMINAL_HARVEST_STATES
        and not clean(row.get("Harvest_Status")).startswith("VISUAL_QA_HOLD")
    ]
    if not candidates:
        print("[SHOCK-HARVEST-IDLE] no submitted rows needing harvest")
        return 0

    messages = fetch_recent_messages_paged(DISCORD_HISTORY_SCAN_LIMIT)
    touched = 0
    assigned_grid_ids = {
        clean(existing.get("Grid_Message_ID"))
        for existing in rows
        if clean(existing.get("Grid_Message_ID"))
    }
    used_grid_ids: set[str] = set()
    for row in candidates[: max(1, limit)]:
        sku = clean(row.get("Internal_SKU"))
        out = output_dir(row)
        try:
            current_grid_id = clean(row.get("Grid_Message_ID"))
            other_assigned_grid_ids = {gid for gid in assigned_grid_ids if gid and gid != current_grid_id}
            grid = resolve_grid_message(messages, row, excluded_ids=used_grid_ids | other_assigned_grid_ids)
            if not grid:
                attempts, age_minutes = increment_grid_wait(row)
                if attempts >= GRID_WAIT_MAX_ATTEMPTS or age_minutes >= GRID_WAIT_MAX_MINUTES:
                    row["Harvest_Status"] = "GRID_TIMEOUT_HOLD"
                    row["Harvest_Error"] = (
                        f"No matching grid after {attempts} attempts / {age_minutes} minutes; "
                        "held so cruise can continue."
                    )
                    if "Visual_QA_Status" in fields:
                        row["Visual_QA_Status"] = "HOLD_GRID_NOT_FOUND"
                    print(f"[SHOCK-HARVEST-HOLD] {sku} grid not found attempts={attempts} age={age_minutes}m")
                else:
                    row["Harvest_Status"] = "WAITING_FOR_GRID"
                    row["Harvest_Error"] = (
                        f"No matching grid in recent Discord messages; attempts={attempts}; age={age_minutes}m"
                    )
                    print(f"[SHOCK-HARVEST-WAIT] {sku} grid not found attempts={attempts} age={age_minutes}m")
                continue

            row["Grid_Message_ID"] = clean(grid.get("id"))
            assigned_grid_ids.add(row["Grid_Message_ID"])
            used_grid_ids.add(row["Grid_Message_ID"])
            row_min_dim = min_upscale_dim(row)
            grid_file = out / f"{sku}_Grid.png"
            if not grid_file.exists() and grid.get("attachments"):
                ok = mj_harvest._download_asset(grid["attachments"][0], str(out), grid_file.name, row_min_dim, "Grid")
                if ok:
                    row["Grid_File"] = str(grid_file.relative_to(PROJECT_ROOT))
            elif grid_file.exists():
                row["Grid_File"] = str(grid_file.relative_to(PROJECT_ROOT))

            if trigger_upscales and clean(row.get("Harvest_Status")) not in {"UPSCALES_REQUESTED", "READY_FOR_VISUAL_QA"}:
                if mj_harvest._has_upscale_buttons(grid):
                    mj_harvest._trigger_upscales(grid)
                    row["Harvest_Status"] = "UPSCALES_REQUESTED"
                    print(f"[SHOCK-HARVEST-UPSCALE] {sku} grid={row['Grid_Message_ID']}")
                    time.sleep(2)

            u_messages = find_u_messages(messages, row)
            for idx, message in u_messages.items():
                field = f"U{idx}_File"
                filename = f"{sku}_U{idx}.png"
                target = out / filename
                if target.exists():
                    row[field] = str(target.relative_to(PROJECT_ROOT))
                    continue
                ok = mj_harvest._download_asset(message["attachments"][0], str(out), filename, row_min_dim, f"U{idx}")
                if ok:
                    row[field] = str(target.relative_to(PROJECT_ROOT))

            got_u = sum(1 for idx in "1234" if clean(row.get(f"U{idx}_File")))
            if got_u >= 4:
                row["Harvest_Status"] = "READY_FOR_VISUAL_QA"
            elif clean(row.get("Grid_File")) and clean(row.get("Harvest_Status")) not in {"UPSCALES_REQUESTED", "READY_FOR_VISUAL_QA"}:
                row["Harvest_Status"] = "GRID_FOUND"
            row["Last_Harvest_ET"] = now_et_text()
            row["Harvest_Error"] = ""
            touched += 1
            print(f"[SHOCK-HARVEST] {sku} status={row.get('Harvest_Status')} u={got_u}/4")
        except Exception as exc:
            row["Harvest_Status"] = "HARVEST_ERROR"
            row["Harvest_Error"] = repr(exc)[:500]
            print(f"[SHOCK-HARVEST-ERROR] {sku}: {exc}")
        finally:
            write_rows(queue, rows, fields)
    print(f"[SHOCK-HARVEST-DONE] touched={touched}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Harvest Shock & Awe V5 MJ outputs")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE), help="Shock/Awe MJ dispatch queue CSV to harvest")
    parser.add_argument("--request-upscales", action="store_true", help="Explicitly request MJ U1-U4 upscales. Default is grid-only drafting.")
    parser.add_argument("--no-upscale", action="store_true", help="Deprecated compatibility flag; grid-only drafting is already the default.")
    args = parser.parse_args()
    return harvest(max(1, args.limit), queue=PROJECT_ROOT / args.queue, trigger_upscales=bool(args.request_upscales and not args.no_upscale))


if __name__ == "__main__":
    raise SystemExit(main())
