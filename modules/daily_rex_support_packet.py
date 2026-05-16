"""Build the daily Rex/Grey support packet.

This is the one place for "what Rex needs to do for Codex" so requirements do
not get scattered across chat, logs, and CSVs.
"""

from __future__ import annotations

import json
import sys
import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
GEMINI_BRIDGE = REVIEW / "Gemini_Bridge"
LATEST = REVIEW / "Rex_Action_Packet_latest.md"


def now_et() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    except Exception:
        return []


def money(value: object) -> float:
    try:
        return float(str(value or "0").replace("$", "").strip() or 0)
    except Exception:
        return 0.0


def write_packet() -> Path:
    etsy_status = read_json(DATABASE / "Etsy_API_Status.json")
    digital_next = read_json(DATABASE / "Etsy_Digital_Next_Batch_State.json")
    external_poll = read_json(DATABASE / "Etsy_Printify_External_Poll_State.json")
    fee_guard = read_json(DATABASE / "Etsy_Fee_Kill_Switch.json")
    fee_rows = read_csv(DATABASE / "Etsy_Fee_Ledger.csv")
    today = datetime.now(ZoneInfo("America/New_York")).date().isoformat()
    digital_spend = sum(money(row.get("Confirmed_Spent_USD")) for row in fee_rows if "DIGITAL" in str(row.get("Batch_ID", "")).upper())
    pod_spend = sum(money(row.get("Confirmed_Spent_USD")) for row in fee_rows if "POD" in str(row.get("Batch_ID", "")).upper())
    total_spend = sum(money(row.get("Confirmed_Spent_USD")) for row in fee_rows)
    today_spend = sum(
        money(row.get("Confirmed_Spent_USD"))
        for row in fee_rows
        if str(row.get("Timestamp", "")).startswith(today) and str(row.get("Status", "")).startswith("CONFIRMED")
    )
    pool = int(fee_guard.get("authorized_pool_listings") or 200)
    pool_budget = money(fee_guard.get("authorized_pool_budget_usd") or 40)
    daily_cap = money(fee_guard.get("daily_listing_fee_cap_usd") or 6)
    absolute_cap = money(fee_guard.get("absolute_no_result_spend_cap_usd") or 60)
    lines = [
        "# Rex Action Packet",
        "",
        f"Generated: {now_et()}",
        "",
        "## Need Rex / Account UI Cooperation",
        "",
        "1. Etsy OAuth authorize flow",
        "   - Status: API key is active, but OAuth authorization currently lands on Etsy `error.php` before callback.",
        "   - First thing to confirm in the Etsy developer app: this callback URL is allowed exactly:",
        "     `http://localhost:8765/etsy/oauth/callback`",
        "   - If Etsy does not allow that exact local URL, add the official tutorial fallback too:",
        "     `http://localhost:3003/oauth/redirect`",
        "   - After adding it, Codex can complete OAuth and store access/refresh tokens locally.",
        "",
        "2. eBay Developer keyset compliance",
        "   - Status: Production keyset is disabled until Marketplace Account Deletion compliance is satisfied.",
        "   - Preferred path: Cloudflare Worker HTTPS endpoint for deletion notifications, not exemption, because OpenClaw stores item/listing/performance data.",
        "   - Codex can prepare endpoint code; Rex only needs to deploy/fill final public HTTPS URL if Cloudflare login requires human verification.",
        "",
        "3. Etsy shop name follow-up",
        "   - Status: Option 02 / Quiet Relic Studio shell copy and logo are applied.",
        "   - Still visible: Etsy shop name remains `DriveFuel`; the shop-name custom input did not accept the automated write.",
        "   - Rex can either manually rename it to `QuietRelicStudio`, or leave it temporarily while Codex continues Etsy listing/data work.",
        "",
        "## No New Credentials Needed Right Now",
        "",
        "- Etsy keystring/shared secret are already in `.env` and ping succeeds.",
        "- Printify API key is present, and the Printify Etsy shop is linked as shop `24260389`.",
        "- Do not paste passwords into chat. If a login expires, use Edge manually or store credentials only in a password manager/browser profile.",
        "",
        "## Current Automated Work",
        "",
        "- Build Etsy listing experiment pool without spending unless publish path passes QA.",
        "- Keep Sticker expansion frozen until gallery/cover trust is solved.",
        "- Use Poster/Acrylic and Etsy Digital as the main near-term battlefield.",
        "- Etsy storefront shell is partially applied: copy/tagline/about/logo are live; only shop name remains `DriveFuel`.",
        "- Block Printify products whose official mockup gallery contains exact duplicate buyer-facing images until a safe de-duplication route exists.",
        "",
        "## Etsy API Pulse",
        "",
        f"- status: `{etsy_status.get('status', 'UNKNOWN')}`",
        f"- http_status: `{etsy_status.get('http_status', '')}`",
        f"- next: `{etsy_status.get('oauth_next_step', '')}`",
        "",
        "## Etsy Spend / Queue Pulse",
        "",
        f"- confirmed_digital_listing_spend: `${digital_spend:.2f}`",
        f"- confirmed_pod_listing_spend: `${pod_spend:.2f}`",
        f"- confirmed_total_etsy_listing_spend: `${total_spend:.2f}`",
        f"- today_confirmed_etsy_listing_spend: `${today_spend:.2f}` / daily cap `${daily_cap:.2f}`",
        f"- authorized_experiment_pool: `{pool}` listings / `${pool_budget:.2f}` pool budget / `${absolute_cap:.2f}` no-result hard ceiling",
        f"- next_digital_candidates_ready_no_spend: `{digital_next.get('ready', '')}`",
        f"- next_digital_projected_fee_if_published: `${float(digital_next.get('projected_fee_if_published_usd') or 0):.2f}`",
        f"- printify_etsy_external_pending_checked: `{external_poll.get('checked', '')}`",
        f"- printify_etsy_external_pending_resolved: `{external_poll.get('resolved', '')}`",
        "",
        "## For Gemini/Grey",
        "",
        f"The strategic ask is not whether to keep Etsy as a battlefield; Rex has approved a {pool}-listing test pool. The current tactical blocker is Etsy OAuth authorization returning Etsy error.php before callback, plus duplicate Printify official mockups on some POD products. Storefront shell is mostly applied, but the public shop name remains DriveFuel. Recommend strategy under these constraints: use Etsy Digital/direct API once OAuth is fixed, keep daily spend under `${daily_cap:.2f}`, and only use Printify POD listings when gallery QA passes.",
        "",
    ]
    REVIEW.mkdir(exist_ok=True)
    GEMINI_BRIDGE.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines)
    LATEST.write_text(text, encoding="utf-8")
    dated = REVIEW / f"Rex_Action_Packet_{datetime.now(ZoneInfo('America/New_York')):%Y%m%d}.md"
    dated.write_text(text, encoding="utf-8")
    (GEMINI_BRIDGE / "TO_GREY_rex_needs_latest.md").write_text(text, encoding="utf-8")
    print(f"[REX-PACKET] {LATEST}")
    return LATEST


if __name__ == "__main__":
    write_packet()
