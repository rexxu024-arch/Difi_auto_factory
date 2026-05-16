"""Route OpenClaw Grey/Gemini work between free and paid API keys."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
POLICY_JSON = PROJECT_ROOT / "Database" / "Gemini_Tier_Routing_Policy.json"
POLICY_MD = PROJECT_ROOT / "Review_Packets" / "Gemini_Bridge" / "GEMINI_TIER_ROUTING_POLICY.md"


POLICY = {
    "updated_at": datetime.now(ZoneInfo("America/New_York")).isoformat(timespec="seconds"),
    "default_tier": "free",
    "free_tier_uses": [
        "Daily sitrep summarization and Rex/Grey action packet compression",
        "Low-risk market hypothesis critique",
        "Backlog prioritization suggestions",
        "SEO wording variants for unpublished/local rows",
        "Non-urgent failure triage where no paid action is pending",
    ],
    "paid_tier_uses": [
        "High-value strategic decisions involving spend, ads, or scaling beyond current caps",
        "Complex postmortems after repeated API/UI failures",
        "Winner DNA expansion requests before increasing Etsy listing budget",
        "Major architecture/refactor planning for the OpenClaw factory",
        "Any prompt that includes large context slices where context caching or paid data handling matters",
    ],
    "never_send": [
        "Raw API keys, passwords, OAuth refresh tokens, payment data, or buyer private messages",
        "Unredacted credential files",
        "Orders or customer support data unless explicitly summarized and privacy-scrubbed",
    ],
    "cost_guard": {
        "paid_default_model": "gemini-flash-latest",
        "paid_heavy_model": "gemini-2.5-flash",
        "paid_pro_requires_reason": True,
        "prefer_batch_for_nonurgent_large_jobs": True,
        "daily_paid_soft_cap_usd": 1.0,
        "daily_paid_hard_cap_usd": 3.0,
        "escalate_to_rex_before_hard_cap": True,
    },
    "routing_rules": [
        {
            "if": "question mentions spend, scale, ads, buyer signal, expansion request, account risk, or repeated failures",
            "tier": "paid",
        },
        {
            "if": "local-only report compression, daily status, small SEO ideation, or backlog grooming",
            "tier": "free",
        },
        {
            "if": "free tier returns quota/rate error and the task is time-sensitive",
            "tier": "paid",
        },
        {
            "if": "free tier returns acceptable quality but task is not urgent",
            "tier": "free",
        },
    ],
}


def write_policy() -> None:
    POLICY_JSON.parent.mkdir(parents=True, exist_ok=True)
    POLICY_JSON.write_text(json.dumps(POLICY, indent=2, ensure_ascii=False), encoding="utf-8")
    POLICY_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Gemini Tier Routing Policy",
        "",
        f"- Updated: {POLICY['updated_at']}",
        f"- Default tier: `{POLICY['default_tier']}`",
        "",
        "## Free Tier",
        *[f"- {item}" for item in POLICY["free_tier_uses"]],
        "",
        "## Paid Tier",
        *[f"- {item}" for item in POLICY["paid_tier_uses"]],
        "",
        "## Never Send",
        *[f"- {item}" for item in POLICY["never_send"]],
        "",
        "## Cost Guard",
        *[f"- `{key}`: `{value}`" for key, value in POLICY["cost_guard"].items()],
        "",
        "## Routing Rules",
        *[f"- If {rule['if']} -> `{rule['tier']}`" for rule in POLICY["routing_rules"]],
        "",
    ]
    POLICY_MD.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    write_policy()
    print(json.dumps({"policy_json": str(POLICY_JSON), "policy_md": str(POLICY_MD)}, indent=2))
