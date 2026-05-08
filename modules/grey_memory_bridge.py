"""Grey Memory Bridge: repo memory -> Gemini API -> task recommendations."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import daily_sitrep_builder
from modules.grey_api_client import GreyApiError, extract_text, generate
from modules.grey_response_parser import parse as parse_grey_response

BRIDGE_DIR = PROJECT_ROOT / "Review_Packets" / "Gemini_Bridge"
CONSTITUTION = BRIDGE_DIR / "GREY_CONTEXT_CONSTITUTION.md"
TO_GREY = BRIDGE_DIR / "TO_GREY_latest.md"
FROM_GREY = BRIDGE_DIR / "FROM_GREY_latest.md"
STATE_JSON = PROJECT_ROOT / "Database" / "Grey_Bridge_State.json"
RUN_LOG = PROJECT_ROOT / "Database" / "Grey_Bridge_Run_Log.csv"


def _now() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")


def _read(path: Path, max_chars: int = 8000) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[-max_chars:]


def ensure_constitution() -> None:
    BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
    if CONSTITUTION.exists():
        return
    CONSTITUTION.write_text(
        """# Grey Context Constitution

## Role Split
- Rex is the business commander and requirement engineer.
- Grey/Gemini is the strategic advisor: direction, risk critique, market logic, and summary pressure tests.
- Codex is the execution officer and head engineer: code, QA, automation, local state, and safe operations.

## Current Mainline Priority
- Printify / eBay / Etsy POD factory is the active project.
- Fallback projects are R&D only until the POD factory is stable or Rex explicitly activates them.

## Business Goal
- Build a reliable semi-automatic money printer with low manual Rex intervention.
- Prioritize real traffic, low error rate, no account damage, and no loss-making products.

## Marketplace Guardrails
- eBay ads: Promoted Listings Standard / General only, fixed 2.0%; no Priority/PPC and no suggested-rate chasing.
- Etsy spend cap before signal: $2 per batch, $6 daily gray cap, $40-$60 early test ceiling, 200 listing experiment pool.
- Do not modify payment/billing settings, generate orders, or touch private credentials beyond reading project env/config.

## Browser Rule
- Marketplace/account UI must use dedicated Edge CDP 9223 only.
- Do not use Rex's daily Chrome for Etsy, Printify, eBay, Seller Hub, or account data gathering.
- Gemini Web strategic sync must use the existing Gemini chat thread named `Codex 自动化矩阵升级计划` only. API bridge traffic remains file/API based; web chat sync is low-frequency and advisory.

## Product / QA Standards
- Printify production design must match local Production_Design through visual QA.
- Cover Gate: live buyer-page image must be verified before retiring old listings or scaling.
- Gallery Integrity Gate: repeated buyer-facing gallery thumbnails and non-sticker custom detail galleries block publish/scale until repaired or isolated.
- Official Printify default mockups are allowed and often preferred for buyer context.
- Sticker custom U gallery mismatch is a blocker.
- Poster/Acrylic use full-image designs, not sticker cut logic.

## Strategy Notes
- Ads alone have not solved eBay 0-view; cover integrity, SEO intent, category fit, and product-market fit matter more.
- Poster/Acrylic showed better early signal than Sticker.
- Use Quiet Luxury, Smoky Jade, Reading Nook, Meditation Room, Study Room, Collector Shelf, and Deep Work intent language when suitable.
""",
        encoding="utf-8",
    )


def build_context(question: str = "") -> str:
    ensure_constitution()
    daily_sitrep_builder.build()
    report = _read(PROJECT_ROOT / "Review_Packets" / "Latest" / "morning_report_latest.md", 9000)
    backlog = _read(PROJECT_ROOT / "Database" / "Factory_Backlog.csv", 7000)
    progress = _read(PROJECT_ROOT / "PROGRESS_LOG.md", 9000)
    sitrep = _read(BRIDGE_DIR / "DAILY_SITREP_latest.md", 5000)
    prompt = f"""You are Grey, Rex's strategic advisor for OpenClaw.

Strict output requirement:
- Return concise Markdown plus a JSON block.
- The JSON block must include a top-level `tasks` array.
- Each task should include: title, priority, lane, rationale, command, risk.
- Do not request secrets. Do not recommend PPC/Priority ads. Do not recommend spending beyond caps.

## Constitution
{_read(CONSTITUTION, 9000)}

## Daily Sitrep
{sitrep}

## Latest Morning Report
{report}

## Current Backlog CSV
{backlog}

## Recent Progress Tail
{progress}

## Question / Decision Request
{question or "Review current state. Identify the next 3-7 highest ROI actions, risks, and any strategic correction. Keep Printify/POD as mainline."}
"""
    TO_GREY.write_text(prompt, encoding="utf-8")
    latest = BRIDGE_DIR / f"TO_GREY_{datetime.now(ZoneInfo('America/New_York')).strftime('%Y%m%d_%H%M')}.md"
    shutil.copyfile(TO_GREY, latest)
    return prompt


def _write_state(payload: dict) -> None:
    STATE_JSON.parent.mkdir(exist_ok=True)
    STATE_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _append_log(status: str, detail: str) -> None:
    exists = RUN_LOG.exists()
    RUN_LOG.parent.mkdir(exist_ok=True)
    with RUN_LOG.open("a", encoding="utf-8", newline="") as handle:
        import csv

        writer = csv.writer(handle)
        if not exists:
            writer.writerow(["Timestamp", "Status", "Detail"])
        writer.writerow([_now(), status, detail])


def send(question: str = "", dry_run: bool = False) -> dict:
    prompt = build_context(question)
    if dry_run:
        result = {"status": "DRY_RUN", "to_grey": str(TO_GREY), "chars": len(prompt)}
        _write_state(result)
        _append_log("DRY_RUN", f"chars={len(prompt)}")
        return result
    try:
        payload = generate(prompt)
        text = extract_text(payload)
        if not text:
            raise GreyApiError("EMPTY_GEMINI_RESPONSE")
        FROM_GREY.write_text(text, encoding="utf-8")
        latest = BRIDGE_DIR / f"FROM_GREY_{datetime.now(ZoneInfo('America/New_York')).strftime('%Y%m%d_%H%M')}.md"
        shutil.copyfile(FROM_GREY, latest)
        tasks = parse_grey_response(FROM_GREY)
        result = {
            "status": "OK",
            "to_grey": str(TO_GREY),
            "from_grey": str(FROM_GREY),
            "tasks": len(tasks),
            "response_chars": len(text),
        }
        _write_state(result)
        _append_log("OK", f"tasks={len(tasks)} response_chars={len(text)}")
        return result
    except Exception as exc:  # noqa: BLE001
        result = {"status": "ERROR", "error_type": type(exc).__name__, "detail": str(exc), "to_grey": str(TO_GREY)}
        _write_state(result)
        _append_log("ERROR", f"{type(exc).__name__}: {exc}")
        return result


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="OpenClaw Grey Memory Bridge")
    parser.add_argument("--question", default="")
    parser.add_argument("--prepare", action="store_true", help="Only create constitution, sitrep, and TO_GREY.")
    parser.add_argument("--dry-run", action="store_true", help="Build prompt without calling Gemini.")
    parser.add_argument("--parse-only", action="store_true", help="Parse existing FROM_GREY_latest.md into tasks.")
    args = parser.parse_args()
    if args.parse_only:
        print(json.dumps({"tasks": parse_grey_response(FROM_GREY)}, indent=2, ensure_ascii=False))
        return
    if args.prepare:
        prompt = build_context(args.question)
        result = {"status": "PREPARED", "to_grey": str(TO_GREY), "chars": len(prompt)}
    else:
        result = send(args.question, dry_run=args.dry_run)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
