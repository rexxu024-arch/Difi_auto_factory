"""Market evidence gate for revenue-facing OpenClaw products.

This module is deliberately lightweight: it records the mandatory evidence
sources, title/spec split rules, and launch checklist before a product line is
allowed to move from "we like it" into paid/public marketplace work.
It does not scrape, publish, spend, or call marketplace APIs.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_ROOT = PROJECT_ROOT / "Database" / "Market_Research"
REPORT_ROOT = PROJECT_ROOT / "Reports"


@dataclass(frozen=True)
class EvidenceSource:
    name: str
    url: str
    use_for: str
    caution: str


SOURCES = [
    EvidenceSource(
        "Etsy Help - Digital Listings",
        "https://help.etsy.com/hc/en-us/articles/115015628347-How-to-Manage-Your-Digital-Listings",
        "Official file-count, file-size, digital delivery, and buyer expectation constraints.",
        "Official policy source; treat as hard launch constraint.",
    ),
    EvidenceSource(
        "eRank",
        "https://erank.com/",
        "Keyword research, competitor titles/tags/prices/views, trend tracking, shop health checks.",
        "Third-party estimates; validate against Etsy search and our live shop stats.",
    ),
    EvidenceSource(
        "eRank Feature Docs",
        "https://help.erank.com/features",
        "Keyword Tool, Rank Checker, Traffic Stats, ROI calculator, and competitor listing inspection.",
        "Use for process design; exact search/sales values require live tool access.",
    ),
    EvidenceSource(
        "EverBee Product Analytics",
        "https://help.everbee.io/en/article/3-product-analytics",
        "Etsy listing demand estimates: sales, revenue, keyword rankings, search volume.",
        "Estimated data; do not treat as Etsy official truth.",
    ),
    EvidenceSource(
        "Sale Samurai",
        "https://salesamurai.io/",
        "Long-tail keyword search volume, competition, price spread, tags, and Etsy result export.",
        "Estimated/third-party data; use as one evidence layer only.",
    ),
]


TITLE_RULES = [
    {
        "rule": "etsy_first",
        "decision": "Lead with human Etsy intent and aesthetic, not eBay-style spec stacking.",
        "example": "Dark Academia Digital Stickers, Gothic Alchemy PNG Clipart for GoodNotes",
    },
    {
        "rule": "spec_teaser",
        "decision": "Keep only buyer-critical specs in the title when they improve expectation: 20+/50+, High Resolution, PNG, Bundle.",
        "example": "50+ High Resolution Digital Sticker PNG Bundle",
    },
    {
        "rule": "description_specs",
        "decision": "Move exact quantity, ZIP parts, pixel range, 300 DPI, transparency notes, license limits, and instant download terms into the description.",
        "example": "Quantity, format, transparent-background caveat, DPI metadata, ZIP part count, file-size limit compliance.",
    },
    {
        "rule": "tool_crosscheck",
        "decision": "Before paid public launch, compare at least 5-10 Etsy comps or one analytics export for phrasing, price, and tag shape.",
        "example": "eRank/EverBee/Sale Samurai/Etsy search screenshots or CSV references.",
    },
]


LAUNCH_CHECKLIST = [
    "Official platform constraints checked and written down.",
    "At least two non-identical market evidence sources consulted.",
    "Buyer expectation locked: file count, file type, delivery mode, license limits, and refund-sensitive caveats.",
    "Title is Etsy-native: aesthetic/use-case first, specs only where conversion-relevant.",
    "Description includes exact technical specs and no misleading claims.",
    "ZIP/file sizes comply with Etsy's 5 files / 20MB each instant-download constraint.",
    "Preview images communicate bundle value without leaking raw full-resolution assets.",
    "No First Audit/private-studio language leaks into low-price public digital archive products.",
    "Pricing is compared against competitor pack size, quality, and perceived value.",
    "If evidence is weak or contradictory, launch as tiny smoke test only.",
]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def render_report() -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    DATABASE_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    source_rows = [
        {
            "Name": item.name,
            "URL": item.url,
            "Use_For": item.use_for,
            "Caution": item.caution,
        }
        for item in SOURCES
    ]
    title_rows = [
        {
            "Rule": item["rule"],
            "Decision": item["decision"],
            "Example": item["example"],
        }
        for item in TITLE_RULES
    ]
    checklist_rows = [{"Step": str(index), "Requirement": item} for index, item in enumerate(LAUNCH_CHECKLIST, 1)]

    write_csv(DATABASE_ROOT / "Market_Evidence_Sources.csv", source_rows)
    write_csv(DATABASE_ROOT / "Etsy_Title_Spec_Split_Rules.csv", title_rows)
    write_csv(DATABASE_ROOT / "Revenue_Product_Launch_Checklist.csv", checklist_rows)

    report = REPORT_ROOT / "Market_Evidence_Gate_latest.md"
    lines = [
        "# Market Evidence Gate",
        "",
        f"Generated: {timestamp}",
        "",
        "## Rule",
        "",
        "Any product intended to make money on Etsy, eBay, Adobe Stock, or another public marketplace must pass this gate before title, price, metadata, or publishing decisions are treated as ready.",
        "",
        "## Required Evidence Sources",
        "",
    ]
    for item in SOURCES:
        lines.append(f"- **{item.name}**: {item.url}")
        lines.append(f"  - Use: {item.use_for}")
        lines.append(f"  - Caution: {item.caution}")
    lines.extend(
        [
            "",
            "## Etsy Digital Bundle Title Policy",
            "",
        ]
    )
    for item in TITLE_RULES:
        lines.append(f"- **{item['rule']}**: {item['decision']} Example: `{item['example']}`")
    lines.extend(
        [
            "",
            "## Launch Checklist",
            "",
        ]
    )
    for index, item in enumerate(LAUNCH_CHECKLIST, 1):
        lines.append(f"{index}. {item}")
    lines.extend(
        [
            "",
            "## Current Sticker Bundle Application",
            "",
            "- Titles should keep `20+` or `50+`, `High Resolution`, `Digital Sticker`, `PNG`, and the dominant aesthetic/use case.",
            "- Exact specs belong in the description: PNG, ZIP parts, 300 DPI metadata, approximate pixel range, transparent-background caveat, instant download, and no physical shipping.",
            "- Cyberpunk pack remains below launch threshold until enough qualifying U assets exist.",
            "- Zen Jade, Dark Academia, and Mega Vault can proceed only after preview/ZIP QA and market phrasing spot-check.",
        ]
    )
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main() -> int:
    report = render_report()
    print(f"market_evidence_gate_report={report}")
    print(f"sources_csv={DATABASE_ROOT / 'Market_Evidence_Sources.csv'}")
    print(f"title_rules_csv={DATABASE_ROOT / 'Etsy_Title_Spec_Split_Rules.csv'}")
    print(f"checklist_csv={DATABASE_ROOT / 'Revenue_Product_Launch_Checklist.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
