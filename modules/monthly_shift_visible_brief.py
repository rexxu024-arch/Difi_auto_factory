"""Build a concise visible progress brief for Rex.

This reads the primitive long-shift state file. It does not run tasks and does
not decide priorities; it only turns the background loop into a human-visible
counter so Rex can tell whether the shift is actually moving.

The visible message is intentionally ASCII-only. Windows/PowerShell/Codex
encoding occasionally garbles Chinese progress text, and Rex needs this brief
to be boringly readable every time.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import csv
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
STATE_FILE = DATABASE_DIR / "Monthly_Shift_Loop_State.md"
TRIGGER_FILE = DATABASE_DIR / "OpenClaw_Next_Action.trigger.json"
BRIEF_STATE_FILE = DATABASE_DIR / "Monthly_Shift_Visible_Brief_State.json"
BRIEF_FILE = DATABASE_DIR / "Monthly_Shift_Visible_Brief.md"
HOURLY_BRIEF_FILE = DATABASE_DIR / "Monthly_Shift_Hourly_Progress.md"
ET = ZoneInfo("America/New_York")

END_LINE_RE = re.compile(
    r"- (?P<stamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) EDT "
    r"\| END (?P<num>\d+) (?P<name>\S+) (?P<status>OK|RC=\d+|TIMEOUT)"
    r"(?: \| (?P<tail>.*))?$"
)
END_RE = re.compile(r"\| END (?P<num>\d+) (?P<name>\S+) (?P<status>OK|RC=\d+|TIMEOUT)")
STAMP_RE = re.compile(r"- (?P<stamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) EDT ")
START_RE = re.compile(
    r"- (?P<stamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) EDT "
    r"\| START (?P<num>\d+) (?P<name>\S+)"
)

COMMAND_PROJECT = {
    "adobe_stock_codex_ab_groups": "Adobe Stock factory",
    "adobe_stock_ab_mj_queue": "Adobe Stock factory",
    "adobe_stock_ab_mj_dispatch": "Adobe Stock factory",
    "etsy_external_poll": "Etsy/Printify reconciliation",
    "etsy_digital_packet": "Etsy V7 digital lab",
    "etsy_package_builder": "Etsy V7 digital lab",
    "etsy_preview_builder": "Etsy V7 digital lab",
    "etsy_pod_selector": "Etsy POD marketplace drip",
    "etsy_pod_publish_drip": "Etsy POD marketplace drip",
    "printify_gallery_duplicate_audit": "Printify QA",
    "printify_design_audit": "Printify QA",
    "ebay_traffic_diagnosis": "eBay recovery",
    "ebay_experiment_report": "eBay recovery",
    "project_mirror_scorecard": "Project Mirror DNA",
    "adobe_stock_scaffold": "Adobe Stock factory",
    "adobe_stock_mentor_expander": "Adobe Stock factory",
    "adobe_stock_pilot_queue": "Adobe Stock factory",
    "adobe_stock_two_layer_schema": "Adobe Stock factory",
    "adobe_stock_pilot_batch": "Adobe Stock factory",
    "adobe_stock_image_qa": "Adobe Stock factory",
    "adobe_stock_metadata_qa": "Adobe Stock factory",
    "adobe_stock_curated_pilot_pack": "Adobe Stock factory",
    "adobe_stock_upload_ready_pack": "Adobe Stock factory",
    "sticker_market_research_gate": "Sticker liquidation",
    "sticker_liquidation_builder": "Sticker liquidation",
    "first_audit_guard": "First Audit private studio",
    "first_audit_contact_sheet": "First Audit private studio",
    "first_audit_extension_specs": "First Audit private studio",
    "first_audit_lookbook": "First Audit private studio",
}


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    except OSError:
        return []


def count_rows(path: Path) -> int:
    return len(read_csv(path))


def count_status(path: Path, field: str, prefixes: tuple[str, ...]) -> int:
    total = 0
    for row in read_csv(path):
        value = str(row.get(field, ""))
        if value.startswith(prefixes):
            total += 1
    return total


def latest_csv_value(path: Path, field: str, default: str = "") -> str:
    rows = read_csv(path)
    if not rows:
        return default
    return str(rows[-1].get(field) or default)


def money(value: object) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def pct(done: float, total: float) -> int:
    if total <= 0:
        return 0
    return max(0, min(100, round((done / total) * 100)))


def project_dashboard() -> dict:
    fee_guard = load_json(DATABASE_DIR / "Etsy_Fee_Kill_Switch.json", {})
    risk = load_json(DATABASE_DIR / "Account_Risk_State.json", {}).get("states", {})

    fee_rows = read_csv(DATABASE_DIR / "Etsy_Fee_Ledger.csv")
    etsy_spend = sum(
        money(row.get("Confirmed_Spent_USD"))
        for row in fee_rows
        if str(row.get("Status", "")).startswith("CONFIRMED")
    )
    etsy_cap = money(fee_guard.get("authorized_pool_budget_usd") or 50)

    digital_live = read_csv(DATABASE_DIR / "Etsy_Digital_Gray_Launch_Queue.csv")
    digital_live_count = sum(1 for row in digital_live if row.get("Etsy_Listing_ID"))

    launch_log = read_csv(DATABASE_DIR / "Etsy_Printify_Launch_Log.csv")
    confirmed_pod = {
        row.get("ID")
        for row in launch_log
        if row.get("Action") in {"POLL", "PUBLISH"}
        and str(row.get("Status", "")).startswith(("EXTERNAL_CONFIRMED", "PUBLISHED_EXTERNAL_CONFIRMED"))
    }
    pod_launch_count = len([item for item in confirmed_pod if item])

    adobe_mentor = read_csv(DATABASE_DIR / "Adobe_Stock_Mentor_Hub.csv")
    adobe_expanded = count_rows(DATABASE_DIR / "Adobe_Stock_Mentor_DNA_Expanded.csv")
    adobe_daily_queue = count_rows(DATABASE_DIR / "Adobe_Stock_Daily_Production_Queue.csv")
    adobe_batch_rows = count_rows(DATABASE_DIR / "Adobe_Stock_Pilot_Batch.csv")
    adobe_image_pass = count_status(DATABASE_DIR / "Adobe_Stock_Pilot_Batch.csv", "QA_Status", ("QA_PASS",))
    adobe_metadata_pass = count_status(DATABASE_DIR / "Adobe_Stock_Metadata_QA.csv", "QA_Status", ("METADATA_QA_PASS",))
    adobe_upload_ready = count_status(
        DATABASE_DIR / "Adobe_Stock_Upload_Ready.csv",
        "Status",
        ("READY_FOR_ADOBE",),
    )
    adobe_curated_ready = count_status(
        DATABASE_DIR / "Adobe_Stock_Curated_Pilot_strict_premium.csv",
        "Status",
        ("READY_FOR_ADOBE",),
    )
    adobe_ui_status = latest_csv_value(DATABASE_DIR / "Adobe_Stock_UI_Upload_Status.csv", "Status", "")

    first_manifest = read_csv(DATABASE_DIR / "First_Audit_001_Asset_Manifest.csv")
    first_release_dirs = [p for p in (PROJECT_ROOT / "First_Audit_Release").glob("*") if p.is_dir()] if (PROJECT_ROOT / "First_Audit_Release").exists() else []
    first_done = max(len(first_manifest), len(first_release_dirs))

    v7_packet = read_csv(DATABASE_DIR / "Etsy_Darwinian_Lab_V7_Listing_Packet.csv")
    v7_ready = sum(
        1
        for row in v7_packet
        if str(row.get("Launch_Readiness", "")).startswith(("READY", "PUBLISHED"))
        or str(row.get("Packet_Status", "")).startswith(("READY", "PUBLISHED"))
    )

    ebay_rows = read_csv(DATABASE_DIR / "eBay_Traffic_Experiment_Report.csv")
    ebay_recent = len(ebay_rows)
    mirror_rows = read_csv(DATABASE_DIR / "Project_Mirror_AB_Scorecard.csv")
    mirror_pairs = len(mirror_rows)

    blockers: list[str] = []
    if risk.get("ebay", {}).get("paid_publish_allowed") is False:
        blockers.append("eBay publish frozen")
    if etsy_spend >= etsy_cap:
        blockers.append("Etsy budget cap reached")
    if adobe_batch_rows and adobe_image_pass == 0:
        blockers.append("Adobe waiting image QA")
    if adobe_upload_ready and adobe_ui_status == "NEEDS_ADOBE_LOGIN":
        blockers.append("Adobe Contributor login needed")
    rex_actions = rex_actions_from_blockers(blockers)

    printify_pct = pct(pod_launch_count + digital_live_count, 250)
    # Adobe progress is a staged first-submission readiness score, not lifetime
    # business completion. It should reflect the real current pipeline rather
    # than the older scaffold-only Production_Line row count.
    adobe_pct = round(
        (10 if adobe_expanded >= 200 else pct(adobe_expanded, 200) * 0.10)
        + (10 if adobe_daily_queue >= 50 else pct(adobe_daily_queue, 50) * 0.10)
        + (15 if adobe_batch_rows >= 50 else pct(adobe_batch_rows, 50) * 0.15)
        + pct(adobe_image_pass, 50) * 0.20
        + pct(adobe_metadata_pass, 50) * 0.15
        + pct(max(adobe_upload_ready, adobe_curated_ready), 15) * 0.15
        + (15 if adobe_ui_status in {"UPLOADED", "SUBMITTED", "SUBMISSION_READY"} else 0)
    )
    first_pct = pct(first_done, 30)
    etsy_pct = pct(digital_live_count + pod_launch_count, 250)
    ebay_pct = 55 if ebay_recent else 45
    mirror_pct = pct(mirror_pairs, 20) if mirror_pairs else 10

    return {
        "printify_pct": printify_pct,
        "adobe_pct": adobe_pct,
        "first_pct": first_pct,
        "etsy_pct": etsy_pct,
        "ebay_pct": ebay_pct,
        "mirror_pct": mirror_pct,
        "etsy_spend": etsy_spend,
        "etsy_cap": etsy_cap,
        "digital_live": digital_live_count,
        "pod_live": pod_launch_count,
        "adobe_rows": adobe_batch_rows,
        "adobe_mentor_rows": adobe_expanded or len(adobe_mentor),
        "adobe_base_mentor_rows": len(adobe_mentor),
        "adobe_expanded_rows": adobe_expanded,
        "adobe_daily_queue_rows": adobe_daily_queue,
        "adobe_image_pass": adobe_image_pass,
        "adobe_metadata_pass": adobe_metadata_pass,
        "adobe_upload_ready": adobe_upload_ready,
        "adobe_curated_ready": adobe_curated_ready,
        "adobe_ui_status": adobe_ui_status,
        "first_done": first_done,
        "mirror_pairs": mirror_pairs,
        "v7_ready": v7_ready,
        "blockers": blockers,
        "rex_actions": rex_actions,
    }


def rex_actions_from_blockers(blockers: list[str]) -> list[dict]:
    actions: list[dict] = []
    for blocker in blockers:
        if blocker == "eBay publish frozen":
            actions.append(
                {
                    "project": "eBay",
                    "severity": "warn",
                    "title": "eBay publish lane parked",
                    "rex_needed": "Business policy/API eligibility or Seller Hub safe cleanup may need owner-side review.",
                    "system_action": "Do not force publish; continue traffic diagnosis, candidate cleanup, title/ad planning, and safe UI notes.",
                }
            )
        elif blocker == "Etsy budget cap reached":
            actions.append(
                {
                    "project": "Printify/Etsy",
                    "severity": "bad",
                    "title": "Etsy fee cap reached",
                    "rex_needed": "Raise the Etsy budget cap or wait for the next budget window.",
                    "system_action": "Park paid writes; continue QA, packaging, metadata, read-only probes, and market evidence.",
                }
            )
        elif blocker == "Adobe waiting image QA":
            actions.append(
                {
                    "project": "Adobe Stock",
                    "severity": "warn",
                    "title": "Adobe image QA needed",
                    "rex_needed": "Review approved/rejected sample quality when available.",
                    "system_action": "Park upload; continue source research, DNA distillation, metadata, and non-upload prep.",
                }
            )
        elif blocker == "Adobe Contributor login needed":
            actions.append(
                {
                    "project": "Adobe Stock",
                    "severity": "warn",
                    "title": "Adobe Contributor login needed",
                    "rex_needed": "Log in to Adobe Contributor in Edge.",
                    "system_action": "Park upload; continue local production, metadata, and QA.",
                }
            )
        else:
            actions.append(
                {
                    "project": "OpenClaw",
                    "severity": "warn",
                    "title": blocker,
                    "rex_needed": "Owner review may be needed.",
                    "system_action": "Park only the blocked lane and continue the next safe monthly task.",
                }
            )
    return actions


def parse_stamp(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=ET)
    except ValueError:
        return None


def parse_iso_stamp(value: object) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=ET)
    return parsed.astimezone(ET)


def compact_tail(value: str, limit: int = 130) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def read_state_tail(max_bytes: int = 2_000_000) -> list[str]:
    """Read only the recent state window so visible briefs stay fast."""
    if not STATE_FILE.exists():
        return []
    try:
        with STATE_FILE.open("rb") as handle:
            handle.seek(0, 2)
            size = handle.tell()
            handle.seek(max(0, size - max_bytes))
            data = handle.read()
    except OSError:
        return []
    text = data.decode("utf-8", errors="ignore")
    lines = text.splitlines()
    if data and size > max_bytes and lines:
        lines = lines[1:]
    return lines


def parse_state() -> tuple[list[dict], dict | None]:
    if not STATE_FILE.exists():
        return [], None

    completed: list[dict] = []
    latest_start: dict | None = None
    for line in read_state_tail():
        start_match = START_RE.search(line)
        if start_match:
            latest_start = {
                "num": int(start_match.group("num")),
                "name": start_match.group("name"),
                "stamp": start_match.group("stamp"),
            }
            continue

        end_line_match = END_LINE_RE.search(line)
        if end_line_match:
            command = end_line_match.group("name")
            completed.append(
                {
                    "num": int(end_line_match.group("num")),
                    "name": command,
                    "status": end_line_match.group("status"),
                    "stamp": end_line_match.group("stamp"),
                    "project": COMMAND_PROJECT.get(command, "Other"),
                    "tail": compact_tail(end_line_match.group("tail") or ""),
                }
            )
            continue

        end_match = END_RE.search(line)
        if end_match:
            stamp_match = STAMP_RE.search(line)
            stamp_text = stamp_match.group("stamp") if stamp_match else ""
            command = end_match.group("name")
            completed.append({
                "num": int(end_match.group("num")),
                "name": command,
                "status": end_match.group("status"),
                "stamp": stamp_text,
                "project": COMMAND_PROJECT.get(command, "Other"),
                "tail": "",
            })
    return completed, latest_start


def recent_items(completed: list[dict], now: datetime, minutes: int) -> list[dict]:
    cutoff = now - timedelta(minutes=minutes)
    recent: list[dict] = []
    for item in completed:
        stamp = parse_stamp(str(item.get("stamp") or ""))
        if stamp and stamp >= cutoff:
            recent.append(item)
    return recent


def summarize_recent(completed: list[dict], latest_start: dict | None, now: datetime, minutes: int = 10, verbose: bool = False) -> str:
    recent = recent_items(completed, now, minutes)

    if not recent:
        if latest_start:
            project = COMMAND_PROJECT.get(str(latest_start.get("name")), "Other")
            return (
                f"last_{minutes}_min=no completed command yet; "
                f"in_progress={project}/{latest_start.get('name')} since {latest_start.get('stamp')}"
            )
        return f"last_{minutes}_min=no completed command yet"

    by_project: dict[str, list[dict]] = {}
    for item in recent:
        by_project.setdefault(str(item["project"]), []).append(item)

    if not verbose:
        parts = [f"{project}+{len(items)}" for project, items in by_project.items()]
        return f"last_{minutes}_min=" + ", ".join(parts)

    parts = []
    for project, items in by_project.items():
        names: list[str] = []
        for item in items:
            name = str(item["name"])
            if name not in names:
                names.append(name)
        detail = ", ".join(names[:4])
        if len(names) > 4:
            detail += f", +{len(names) - 4} more"
        parts.append(f"{project}: {len(items)} done ({detail})")
    return f"last_{minutes}_min=" + " | ".join(parts)


def progress_score(dashboard: dict) -> int:
    weighted = (
        dashboard["printify_pct"] * 0.30
        + dashboard["first_pct"] * 0.30
        + dashboard["adobe_pct"] * 0.20
        + dashboard["ebay_pct"] * 0.10
        + dashboard["mirror_pct"] * 0.10
    )
    return round(weighted)


def progress_line(dashboard: dict) -> str:
    return (
        f"OpenClaw {progress_score(dashboard)}% overall | "
        f"Printify/Etsy {dashboard['printify_pct']}% "
        f"(digital {dashboard['digital_live']}, POD {dashboard['pod_live']}, "
        f"spend ${dashboard['etsy_spend']:.2f}/${dashboard['etsy_cap']:.2f}) | "
        f"First Audit {dashboard['first_pct']}% ({dashboard['first_done']}/30) | "
        f"Adobe {dashboard['adobe_pct']}% "
        f"(DNA {dashboard['adobe_expanded_rows']}, batch {dashboard['adobe_rows']}, "
        f"QA {dashboard['adobe_image_pass']}/{dashboard['adobe_metadata_pass']}, "
        f"ready {dashboard['adobe_upload_ready']}, UI {dashboard['adobe_ui_status'] or 'not checked'}) | "
        f"eBay {dashboard['ebay_pct']}% | "
        f"Project Mirror {dashboard['mirror_pct']}% ({dashboard['mirror_pairs']} pairs)"
    )


def remaining_line(dashboard: dict) -> str:
    first_left = max(0, 30 - int(dashboard["first_done"]))
    etsy_left = max(0, 250 - int(dashboard["digital_live"]) - int(dashboard["pod_live"]))
    adobe_left = max(0, 50 - int(dashboard["adobe_image_pass"]))
    blocker_text = ", ".join(dashboard["blockers"]) if dashboard["blockers"] else "none"
    return (
        "Remaining estimate: "
        f"First Audit {first_left} premium folders left; "
        f"Etsy/Printify {etsy_left} listings left to the 250-test ceiling; "
        f"Adobe pilot about {adobe_left} QA-passed images left before daily 50 baseline; "
        f"Rex blockers={blocker_text}."
    )


def rex_action_line(dashboard: dict) -> str:
    actions = dashboard.get("rex_actions") or []
    if not actions:
        return "Rex action: none. Blocked lanes=0; safe lanes continue."
    titles = "; ".join(f"{item['project']}: {item['title']}" for item in actions)
    return f"Rex action: {titles}. Blocked lanes are parked; safe lanes continue."


def rex_action_block(dashboard: dict) -> str:
    actions = dashboard.get("rex_actions") or []
    if not actions:
        return "- No Rex action needed right now. Continue safe monthly tasks.\n"
    lines = []
    for item in actions:
        lines.append(
            f"- [{item['severity'].upper()}] {item['project']} - {item['title']}: "
            f"Rex needed: {item['rex_needed']} System action: {item['system_action']}"
        )
    return "\n".join(lines) + "\n"


def hourly_block(
    dashboard: dict,
    completed: list[dict],
    latest_start: dict | None,
    now: datetime,
    current_command: str,
    current_count: int,
) -> str:
    return (
        "HOURLY_PROGRESS:\n"
        f"- Progress: {progress_line(dashboard)}.\n"
        f"- Last 60m: {summarize_recent(completed, latest_start, now, minutes=60, verbose=True)}.\n"
        f"- Current: {current_command}; total_completed={current_count}.\n"
        f"- Remaining: {remaining_line(dashboard)}\n"
        f"- {rex_action_line(dashboard)}"
    )


def build_brief(hourly: bool = False) -> str:
    completed, latest_start = parse_state()
    trigger = load_json(TRIGGER_FILE, {})
    dashboard = project_dashboard()
    previous = load_json(BRIEF_STATE_FILE, {"last_completed": 0})
    previous_count = int(previous.get("last_completed") or 0)
    current_count = max((item["num"] for item in completed), default=0)
    delta = [item for item in completed if item["num"] > previous_count]

    now = datetime.now(ET)
    current_command = trigger.get("current_command") or (latest_start or {}).get("name") or "unknown"
    deadline = trigger.get("deadline_et", "unknown")
    blocker_text = rex_action_line(dashboard)

    if hourly:
        brief = hourly_block(dashboard, completed, latest_start, now, current_command, current_count)
    elif delta:
        brief = (
            f"10M_PROGRESS: {progress_line(dashboard)}. "
            f"{summarize_recent(completed, latest_start, now, minutes=10)}. "
            f"Current={current_command}; +{len(delta)} commands since last visible brief; {blocker_text}."
        )
        previous["last_completed"] = current_count
    else:
        started = ""
        if latest_start:
            started = f"; latest_start={latest_start['num']}:{latest_start['name']}@{latest_start['stamp']}"
        brief = (
            f"10M_PROGRESS: {progress_line(dashboard)}. "
            f"No new completion since last brief; current={current_command}{started}. "
            f"{summarize_recent(completed, latest_start, now, minutes=10)}; {blocker_text}."
        )

    if not hourly:
        last_hourly = parse_iso_stamp(previous.get("last_hourly_at_et"))
        if last_hourly is None or (now - last_hourly).total_seconds() >= 3600:
            brief = (
                brief
                + "\n"
                + hourly_block(dashboard, completed, latest_start, now, current_command, current_count)
            )
            previous["last_hourly_at_et"] = now.isoformat()

    previous["updated_at_et"] = now.isoformat()
    previous["deadline_et"] = deadline
    BRIEF_STATE_FILE.write_text(json.dumps(previous, indent=2), encoding="utf-8")
    BRIEF_FILE.write_text(
        "# Monthly Shift Visible Brief\n\n"
        f"- updated_at_et: {now.isoformat()}\n"
        f"- commands_completed: {current_count}\n"
        f"- current_command: {current_command}\n"
        f"- deadline_et: {deadline}\n\n"
        "## Project Dashboard\n\n"
        f"- Overall weighted progress: {progress_score(dashboard)}%\n"
        f"- Printify/Etsy pipeline: {dashboard['printify_pct']}% (live digital={dashboard['digital_live']}, live POD={dashboard['pod_live']})\n"
        f"- Adobe Stock pilot: {dashboard['adobe_pct']}% "
        f"(expanded_dna={dashboard['adobe_expanded_rows']}, daily_queue={dashboard['adobe_daily_queue_rows']}, "
        f"batch={dashboard['adobe_rows']}, image_QA={dashboard['adobe_image_pass']}, "
        f"metadata_QA={dashboard['adobe_metadata_pass']}, upload_ready={dashboard['adobe_upload_ready']}, "
        f"strict_curated={dashboard['adobe_curated_ready']}, UI={dashboard['adobe_ui_status'] or 'not checked'})\n"
        f"- First Audit: {dashboard['first_pct']}% ({dashboard['first_done']}/30 release assets)\n"
        f"- eBay recovery: {dashboard['ebay_pct']}%\n"
        f"- Project Mirror: {dashboard['mirror_pct']}% ({dashboard['mirror_pairs']} A/B pairs)\n"
        f"- Etsy spend: ${dashboard['etsy_spend']:.2f}/${dashboard['etsy_cap']:.2f}\n"
        f"- {rex_action_line(dashboard)}\n\n"
        "## Rex Action / Parked Lanes\n\n"
        f"{rex_action_block(dashboard)}\n"
        f"- Last 10 minutes: {summarize_recent(completed, latest_start, now)}\n\n"
        f"- Hourly detail: {summarize_recent(completed, latest_start, now, minutes=60, verbose=True)}\n"
        f"- Remaining: {remaining_line(dashboard)}\n\n"
        f"{brief}\n",
        encoding="utf-8",
    )
    if hourly:
        HOURLY_BRIEF_FILE.write_text(
            "# Monthly Shift Hourly Progress\n\n"
            f"- updated_at_et: {now.isoformat()}\n"
            f"- overall_progress: {progress_score(dashboard)}%\n"
            f"- current_command: {current_command}\n\n"
            f"{brief}\n",
            encoding="utf-8",
        )
    return brief


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hourly", action="store_true", help="Emit the detailed hourly progress line.")
    args = parser.parse_args()
    brief = build_brief(hourly=args.hourly)
    sys.stdout.buffer.write((brief + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
