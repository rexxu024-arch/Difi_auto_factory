"""Create Rex-style long chat work blocks for the current day.

This is intentionally primitive. It does not try to be a daemon or planner AI.
It writes a simple route that the chat model and heartbeat prompts can read:
work the current block, then continue to the next block until heat, Rex, or
account guards genuinely block progress.
"""

from __future__ import annotations

import json
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "Database"
REVIEW = ROOT / "Review_Packets"
ET = ZoneInfo("America/New_York")

QUEUE_PATH = DATABASE / "Daily_Work_Blocks_Current.json"
THERMAL_PATH = DATABASE / "Thermal_Task_Schedule.json"
THERMAL_OVERRIDE_PATH = DATABASE / "Thermal_Override.json"
ROUTE_PATH = DATABASE / "Chat_Model_Work_Route_Current.json"


def now_et() -> datetime:
    return datetime.now(ET)


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}


def today_slug() -> str:
    return now_et().strftime("%Y%m%d")


def iso_at(hour: int, minute: int = 0, add_days: int = 0) -> str:
    base = now_et().date()
    dt = datetime.combine(base, time(hour, minute), ET)
    if add_days:
        dt = dt.replace(day=dt.day)  # keep lint-simple; timedelta not needed below
        from datetime import timedelta

        dt = dt + timedelta(days=add_days)
    return dt.isoformat(timespec="minutes")


def first_pending_block(queue: dict) -> str:
    for block in queue.get("blocks", []):
        if block.get("status") in {"IN_PROGRESS", "PENDING"}:
            return block.get("id", "adobe_stock_quality_batch")
    return "adobe_stock_quality_batch"


def build_route() -> dict:
    current = now_et()
    queue = read_json(QUEUE_PATH)
    thermal = read_json(THERMAL_PATH)
    override = read_json(THERMAL_OVERRIDE_PATH)
    ac_override = bool(override.get("ac_override_active"))

    # Rex's current priority: Adobe Stock first, sticker bundles second,
    # daily Etsy/eBay third. First Audit is deliberately late unless urgent.
    if ac_override:
        shutdown = "Rex/manual shutdown; ambient-weather shutdown disabled while AC override is active"
        blocks = [
            {
                "id": "steer_001_adobe_stock_quality_production",
                "source_block": "adobe_stock_quality_batch",
                "project": "Adobe Stock",
                "window_et": f"{current.isoformat(timespec='minutes')} -> Rex/manual stop",
                "thermal_mode": "AC_OVERRIDE_FULL_WORK_WITH_CPU_MEMORY_GUARDS",
                "target_hours": 6.0,
                "instruction": (
                    "Deeply participate as chat model. Produce Rex-trained Adobe Stock material assets: "
                    "market-DNA prompt refinement, MJ relaxed/source harvest when safe, local 4MP clarity QA, "
                    "metadata, upload-ready packaging, and /adobe-qa review queue. Do not use MJ Fast."
                ),
            },
            {
                "id": "steer_002_sticker_bundle_packaging",
                "source_block": "etsy_sticker_bundle_liquidation",
                "project": "Etsy Digital Warehouse",
                "window_et": "after steer_001 or if Adobe lane is Rex-blocked",
                "thermal_mode": "LIGHT_OR_NORMAL",
                "target_hours": 2.5,
                "instruction": (
                    "Package sticker remnants into Etsy-style digital bundles using 20/20/50 split ZIP logic, "
                    "buyer specs in description, watermarked previews, and no source deletion."
                ),
            },
            {
                "id": "steer_003_marketplace_drip_performance",
                "source_block": "marketplace_daily_drip_and_performance",
                "project": "Printify / Etsy / eBay",
                "window_et": "after steer_002 or if marketplace-safe guard opens",
                "thermal_mode": "LIGHT_OR_NORMAL",
                "target_hours": 2.0,
                "instruction": (
                    "Refresh Etsy/eBay performance, prepare high-quality POD-first listing candidates, and execute "
                    "only guard-approved daily drip. Park eBay/Etsy owner blockers visibly and continue safe prep."
                ),
            },
        ]
    else:
        shutdown = "weather/resource deadline; heavy work only in <80F or CPU-safe windows"
        blocks = [
            {
                "id": "steer_001_adobe_stock_morning_prep",
                "source_block": "adobe_stock_quality_batch",
                "project": "Adobe Stock",
                "window_et": f"{current.isoformat(timespec='minutes')} -> {iso_at(13, 0)}",
                "thermal_mode": "MORNING_MIXED: heavy only while <80F; then text/QA/metadata",
                "target_hours": 3.0,
                "instruction": (
                    "Deeply participate as chat model. Use the morning window for Adobe Stock DNA refinement, "
                    "prompt queue expansion, QA UI cleanup, metadata/title/keyword work, and source/clarity checks. "
                    "If ambient/CPU gets hot, switch to text/CSV only, not idle."
                ),
            },
            {
                "id": "steer_002_heat_zone_light_work",
                "source_block": "etsy_sticker_bundle_liquidation",
                "project": "Etsy Digital Warehouse + System",
                "window_et": f"{iso_at(13, 0)} -> {iso_at(17, 0)}",
                "thermal_mode": "RED_ZONE_LIGHT_ONLY_OR_PAUSE_IF_CPU_MEMORY_SPIKE",
                "target_hours": 2.0,
                "instruction": (
                    "If the laptop is safe, do only light work: sticker ZIP sizing, Etsy metadata, log cleanup, "
                    "HUD queue updates, and report skeletons. If CPU/memory/heat spikes, stop heavy operations and "
                    "sleep; do not burn hardware."
                ),
            },
            {
                "id": "steer_003_evening_marketplace_and_sticker",
                "source_block": "marketplace_daily_drip_and_performance",
                "project": "Printify / Etsy / eBay + Sticker",
                "window_et": f"{iso_at(17, 0)} -> {iso_at(20, 0)}",
                "thermal_mode": "LIGHT_TO_COOLING",
                "target_hours": 3.0,
                "instruction": (
                    "Do marketplace read/diagnosis, daily drip prep, POD-first candidate selection, and sticker bundle "
                    "final packaging. Publish/spend/upload only through existing guards and Rex budget."
                ),
            },
            {
                "id": "steer_004_night_adobe_stock_production",
                "source_block": "adobe_stock_quality_batch",
                "project": "Adobe Stock",
                "window_et": f"{iso_at(20, 0)} -> {iso_at(9, 0, add_days=1)}",
                "thermal_mode": "GREEN_ZONE_FULL_POWER_WITH_CPU_MEMORY_GUARDS",
                "target_hours": 8.0,
                "instruction": (
                    "Use the cool night window for Adobe Stock production: MJ relaxed dispatch/harvest if available, "
                    "local free super-resolution/downsample experiments, 4MP sharpness QA, upload-ready packaging, "
                    "and Rex review queue. Do not use MJ Fast for Stock."
                ),
            },
            {
                "id": "steer_005_low_priority_report_git_gemini",
                "source_block": "system_report_gemini_git",
                "project": "System / Gemini / Git",
                "window_et": "near final shutdown/report window only",
                "thermal_mode": "LOW_POWER",
                "target_hours": 1.0,
                "instruction": (
                    "Compress real progress into Gemini/report/git hygiene. Do not let reporting replace production "
                    "unless it is the end-of-day window or higher lanes are blocked."
                ),
            },
        ]

    route = {
        "date": today_slug(),
        "generated_at_et": current.isoformat(timespec="seconds"),
        "mode": "chat_model_steer_equivalent_route",
        "policy": (
            "These blocks are the durable replacement for unreliable/red Steer messages. "
            "A awakened chat-model turn should execute the current block as real work, not status-only reporting."
        ),
        "current_source_block": first_pending_block(queue),
        "thermal_summary": {
            "current_f": thermal.get("current_f"),
            "today_high_f": thermal.get("today_high_f"),
            "current_heavy_allowed": thermal.get("current_heavy_allowed"),
            "current_light_work_allowed": thermal.get("current_light_work_allowed"),
            "ac_override_active": ac_override,
            "shutdown_policy": shutdown,
        },
        "blocks": blocks,
        "validation": {
            "expected_behavior": "chat model works through blocks sequentially until Rex/guard/thermal stop",
            "heartbeat_role": "rescue and visibility only; it must not shrink work into a 20-second status check",
            "red_steer_fallback": "copy failed Steer text into Database/Rex_Red_Steer_Rescue_Inbox.md as NEW sections, then absorb",
        },
    }
    return route


def write_markdown(route: dict) -> Path:
    REVIEW.mkdir(parents=True, exist_ok=True)
    path = REVIEW / f"Daily_Steer_Route_{route['date']}.md"
    lines = [
        f"# Daily Steer Route {route['date']}",
        "",
        f"- generated_at_et: `{route['generated_at_et']}`",
        f"- mode: `{route['mode']}`",
        f"- policy: {route['policy']}",
        f"- shutdown_policy: `{route['thermal_summary'].get('shutdown_policy')}`",
        "",
        "## Blocks",
        "",
    ]
    for block in route["blocks"]:
        lines.extend(
            [
                f"### {block['id']}",
                "",
                f"- project: `{block['project']}`",
                f"- source_block: `{block['source_block']}`",
                f"- window_et: `{block['window_et']}`",
                f"- thermal_mode: `{block['thermal_mode']}`",
                f"- target_hours: `{block['target_hours']}`",
                "",
                "Steer-equivalent instruction:",
                "",
                block["instruction"],
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> int:
    DATABASE.mkdir(parents=True, exist_ok=True)
    route = build_route()
    ROUTE_PATH.write_text(json.dumps(route, ensure_ascii=False, indent=2), encoding="utf-8")
    review_path = write_markdown(route)
    print(
        json.dumps(
            {
                "status": "OK",
                "route_path": str(ROUTE_PATH),
                "review_path": str(review_path),
                "blocks": len(route["blocks"]),
                "current_first_block": route["blocks"][0]["id"] if route["blocks"] else None,
                "shutdown_policy": route["thermal_summary"].get("shutdown_policy"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
