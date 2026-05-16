"""Build the end-of-day OpenClaw winddown report for Rex and Grey."""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
GEMINI = REVIEW / "Gemini_Bridge"
PROGRESS = PROJECT_ROOT / "PROGRESS_LOG.md"
CURRENT = PROJECT_ROOT / "CURRENT_TASK.md"


def now_et() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def read_text(path: Path, max_chars: int = 6000) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[-max_chars:]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def money(value: object) -> float:
    try:
        return float(str(value or "0").replace("$", "").strip() or 0)
    except Exception:
        return 0.0


def etsy_summary() -> dict:
    queue = read_csv(DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv")
    ledger = read_csv(DATABASE / "Etsy_Fee_Ledger.csv")
    today = now_et().date().isoformat()
    today_spend = sum(
        money(row.get("Confirmed_Spent_USD"))
        for row in ledger
        if str(row.get("Timestamp", "")).startswith(today) and str(row.get("Status", "")).startswith("CONFIRMED")
    )
    total_spend = sum(money(row.get("Confirmed_Spent_USD")) for row in ledger if str(row.get("Status", "")).startswith("CONFIRMED"))
    return {
        "queue_counts": Counter(row.get("Launch_Status") for row in queue),
        "published": sum(1 for row in queue if row.get("Launch_Status") == "PUBLISHED_UI_CONFIRMED"),
        "today_spend": today_spend,
        "total_spend": total_spend,
    }


def build() -> Path:
    REVIEW.mkdir(exist_ok=True)
    GEMINI.mkdir(parents=True, exist_ok=True)
    stamp = now_et()
    etsy = etsy_summary()
    fee_guard = read_json(DATABASE / "Etsy_Fee_Kill_Switch.json")
    etsy_status = read_json(DATABASE / "Etsy_API_Status.json")
    backlog = read_text(DATABASE / "Factory_Backlog.md", 5000)
    progress = read_text(PROGRESS, 8000)
    current = read_text(CURRENT, 4000)
    lines = [
        "# OpenClaw Winddown Report",
        "",
        f"Generated: {stamp:%Y-%m-%d %H:%M:%S %Z}",
        "",
        "## Bigger Picture",
        "",
        "- Main battlefield remains Etsy Digital plus clean Poster/Acrylic POD. Sticker remains frozen until create-time gallery is safe.",
        "- Today's Etsy Digital expansion is real and spend-controlled; marketplace publishing should continue only through fee guards.",
        "- Gemini free/paid bridge is now usable for strategic oversight; free handles routine critique, paid handles scale/spend/failure decisions.",
        "",
        "## Quant Snapshot",
        "",
        f"- Etsy Digital live confirmed: `{etsy['published']}`",
        f"- Etsy spend today: `${etsy['today_spend']:.2f}` / daily cap `${money(fee_guard.get('daily_listing_fee_cap_usd') or 6):.2f}`",
        f"- Etsy total confirmed listing-fee spend: `${etsy['total_spend']:.2f}`",
        f"- Etsy authorized pool: `{fee_guard.get('authorized_pool_listings', '')}` listings / `${money(fee_guard.get('authorized_pool_budget_usd') or 0):.2f}`",
        f"- Etsy API status: `{etsy_status.get('status', 'UNKNOWN')}` next `{etsy_status.get('oauth_next_step', '')}`",
        "",
        "## Core Problems",
        "",
        "- Etsy OAuth still reaches Etsy `error.php` before callback; likely app redirect/callback configuration issue.",
        "- eBay Developer production keyset is disabled until Marketplace Account Deletion compliance is completed.",
        "- Etsy shop public name still shows `DriveFuel`; Option 02 shell copy/logo applied but name update did not verify.",
        "- Printify -> Etsy physical POD smoke product still lacks external id; keep it isolated from scaling.",
        "- Sticker pipeline still has gallery/cover risk unless created with the safe mixed official+cover shape from the beginning.",
        "",
        "## Rex Needs To Handle",
        "",
        "1. Etsy developer app: confirm/add callback `http://localhost:8765/etsy/oauth/callback`; if rejected, add `http://localhost:3003/oauth/redirect`.",
        "2. eBay developer app: complete Marketplace Account Deletion compliance endpoint setup or let Codex prepare a Cloudflare Worker endpoint.",
        "3. Etsy shop name: manually rename `DriveFuel` to `QuietRelicStudio` if Etsy UI keeps rejecting automation.",
        "",
        "## Copy To Gemini / Grey",
        "",
        "Use this report plus `Review_Packets/Rex_Action_Packet_latest.md`. Ask Grey to critique Etsy Digital scaling, OAuth unblock priority, and whether to keep POD physical listings paused until external id and gallery QA are clean.",
        "",
        "## Current Task Tail",
        "",
        "```text",
        current[-2500:],
        "```",
        "",
        "## Progress Tail",
        "",
        "```text",
        progress[-4500:],
        "```",
        "",
        "## Backlog Tail",
        "",
        "```text",
        backlog[-3000:],
        "```",
        "",
    ]
    out = REVIEW / f"OpenClaw_Winddown_Report_{stamp:%Y%m%d}.md"
    latest = REVIEW / "OpenClaw_Winddown_Report_latest.md"
    text = "\n".join(lines)
    out.write_text(text, encoding="utf-8")
    latest.write_text(text, encoding="utf-8")
    (GEMINI / "TO_GREY_winddown_latest.md").write_text(text, encoding="utf-8")
    print(f"[WINDDOWN] {latest}")
    return latest


if __name__ == "__main__":
    build()
