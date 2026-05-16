"""Create performance lifecycle rules for marketplace experiments.

This is the missing middle layer between "publish listings" and "learn what
works." It does not modify marketplaces. It writes explicit rules for future
safe automation: when to observe, rewrite, promote, bundle, retire, or clone.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
OUT_RULES = DATABASE / "Performance_Lifecycle_Rules.csv"
OUT_MD = REVIEW / "Performance_Lifecycle_Autopilot.md"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

HEADERS = [
    "Platform",
    "Product_Lane",
    "Signal_Window",
    "Condition",
    "Action",
    "Guardrail",
    "Rex_Review_Needed",
]

RULES = [
    {
        "Platform": "Etsy",
        "Product_Lane": "POD Acrylic/Poster",
        "Signal_Window": "72 hours",
        "Condition": "0 views and no search impressions",
        "Action": "Rewrite title/tags toward buyer-intent room/use-case terms; do not publish more of same DNA.",
        "Guardrail": "No paid ads until listing is front-end visible and gallery has 5+ non-duplicate photos.",
        "Rex_Review_Needed": "No",
    },
    {
        "Platform": "Etsy",
        "Product_Lane": "POD Acrylic/Poster",
        "Signal_Window": "7 days",
        "Condition": "views > 20 but favorites = 0",
        "Action": "Replace cover/mockup and reduce conceptual wording; keep product live.",
        "Guardrail": "No price cut below cost + shipping + platform fee + 15% buffer.",
        "Rex_Review_Needed": "Only if image mismatch appears.",
    },
    {
        "Platform": "Etsy",
        "Product_Lane": "Digital bundle",
        "Signal_Window": "14 days",
        "Condition": "Fav/Visit < 1% and 0 carts/orders",
        "Action": "Retire to inactive, preserve metadata, do not renew automatically.",
        "Guardrail": "Never delete source ZIP until ledger and listing id are archived.",
        "Rex_Review_Needed": "No",
    },
    {
        "Platform": "Etsy",
        "Product_Lane": "Digital bundle",
        "Signal_Window": "14 days",
        "Condition": "Fav/Visit > 3% or any organic order",
        "Action": "Scale DNA into 20-50 variant mega-bundle queue and request Rex/Gemini review.",
        "Guardrail": "Spend cap still $50 normal / $60 hard until Rex expands budget.",
        "Rex_Review_Needed": "Yes before scale spend.",
    },
    {
        "Platform": "eBay",
        "Product_Lane": "Sticker",
        "Signal_Window": "Any",
        "Condition": "new sticker expansion request",
        "Action": "Freeze. Use existing sticker rows only for diagnostic history; no new sticker production.",
        "Guardrail": "eBay sticker market is too price-compressed for current POD cost structure.",
        "Rex_Review_Needed": "No",
    },
    {
        "Platform": "eBay",
        "Product_Lane": "Poster/Acrylic",
        "Signal_Window": "72 hours",
        "Condition": "views low but no account warning",
        "Action": "Run small ad-rate A/B after margin math; test 4%, 8%, 12% groups.",
        "Guardrail": "If ad rate makes net margin negative, raise Printify-side price or skip ad.",
        "Rex_Review_Needed": "No for dry-run; Yes for broad live changes until API route is reliable.",
    },
    {
        "Platform": "All",
        "Product_Lane": "First Audit / Studio",
        "Signal_Window": "Always",
        "Condition": "asset tagged First Audit or private-showcase",
        "Action": "Block public marketplace publish; only use release/lookbook/private pipeline.",
        "Guardrail": "Leak guard must run before public queues.",
        "Rex_Review_Needed": "Yes before any public use.",
    },
    {
        "Platform": "All",
        "Product_Lane": "Any",
        "Signal_Window": "Every morning 05:30 ET",
        "Condition": "permission, billing, OAuth, or account-policy blocker exists",
        "Action": "Append blocker to Rex Action Packet and Gemini/Grey packet.",
        "Guardrail": "Do not let permission-only blockers sit outside morning report.",
        "Rex_Review_Needed": "Yes",
    },
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def write_rules() -> None:
    DATABASE.mkdir(parents=True, exist_ok=True)
    with OUT_RULES.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(RULES)


def write_report() -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Performance Lifecycle Autopilot",
        "",
        f"Generated: {now_text()}",
        "",
        "This packet defines how OpenClaw should stop blind listing volume and turn marketplace signals into controlled next actions.",
        "",
        "## Non-Negotiable Guards",
        "",
        "- Sticker expansion is frozen unless Rex explicitly reopens it.",
        "- First Audit/private-showcase assets cannot leak into public marketplaces.",
        "- Paid actions must respect Etsy $50 normal / $60 hard cap and eBay margin math.",
        "- Permission/account blockers go into the morning Rex/Gemini packet.",
        "",
        "## Rule Table",
        "",
    ]
    for rule in RULES:
        lines.extend(
            [
                f"### {rule['Platform']} - {rule['Product_Lane']}",
                "",
                f"- Window: {rule['Signal_Window']}",
                f"- Condition: {rule['Condition']}",
                f"- Action: {rule['Action']}",
                f"- Guardrail: {rule['Guardrail']}",
                f"- Rex review: {rule['Rex_Review_Needed']}",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def append_progress() -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Built performance lifecycle autopilot rules; "
            f"rules={len(RULES)}; csv={OUT_RULES.relative_to(PROJECT_ROOT)}; packet={OUT_MD.relative_to(PROJECT_ROOT)}.\n"
        )


def main() -> None:
    write_rules()
    write_report()
    append_progress()
    print(f"[PERFORMANCE-LIFECYCLE] rules={len(RULES)} csv={OUT_RULES}")
    print(f"[PERFORMANCE-LIFECYCLE] packet={OUT_MD}")


if __name__ == "__main__":
    main()
