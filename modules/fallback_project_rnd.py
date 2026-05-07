from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATABASE_DIR = PROJECT_ROOT / "Database"
REVIEW_DIR = PROJECT_ROOT / "Review_Packets"
NY = ZoneInfo("America/New_York")

MULTI_TRACK_PATH = DATABASE_DIR / "Multi_Track_Experiment_Plan.csv"
DIGITAL_INDEX_PATH = DATABASE_DIR / "Digital_Printable_Pack_Index.csv"
EVAL_CSV = DATABASE_DIR / "Fallback_Project_Evaluation.csv"
PINTEREST_QUEUE = DATABASE_DIR / "Pinterest_Pin_Queue.csv"
MICROSTOCK_QUEUE = DATABASE_DIR / "Microstock_Export_Queue.csv"
STATE_PATH = DATABASE_DIR / "Fallback_Project_RnD_State.json"


@dataclass
class ProjectOption:
    option: str
    name: str
    roi_rank: int
    deploy_hours: str
    cash_cost: str
    success_probability: str
    expected_revenue_stability: str
    technical_bottleneck: str
    ban_risk: str
    decision: str
    first_code_step: str


def now_text() -> str:
    return datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S %z")


def slug(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text.strip().lower())
    return re.sub(r"-+", "-", text).strip("-")[:80] or "asset"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def option_matrix() -> list[ProjectOption]:
    return [
        ProjectOption(
            option="B",
            name="Pinterest visual traffic engine",
            roi_rank=1,
            deploy_hours="8-16h for queue + official API prototype after account/app access",
            cash_cost="$0-$5/mo if using free/cheap image hosting; no listing fees",
            success_probability="Medium: best fit for visual assets, but traffic is indirect and needs 2-4 weeks of pin history",
            expected_revenue_stability="Medium if pins index; weak short-term conversion, useful as free traffic layer",
            technical_bottleneck="Pinterest requires official API access/boards plus publicly reachable image URLs; local files cannot be posted directly",
            ban_risk="Medium-low only if official API, slow pacing, unique pins; high if browser/session automation or duplicate spam",
            decision="BUILD_FIRST",
            first_code_step="Generate Pinterest_Pin_Queue.csv with board taxonomy, UTM destination, public-image placeholder, jitter, and idempotency key.",
        ),
        ProjectOption(
            option="A",
            name="Microstock FTP/CSV export matrix",
            roi_rank=2,
            deploy_hours="6-10h for metadata/export pack; 12-24h for first platform FTP adapter after credentials",
            cash_cost="$0 direct; optional stock keyword tools or hosting not required",
            success_probability="Low-medium: assets can be reused, but AI-stock review, similarity, and low royalties make payoff slow",
            expected_revenue_stability="Low early, medium only after hundreds/thousands accepted across platforms",
            technical_bottleneck="Different agency requirements; Freepik FTP is locked until contributor level; review queues can take weeks",
            ban_risk="Medium if near-duplicates/AI disclosure wrong; low if platform-specific QA and slow submissions",
            decision="BUILD_SECOND_AS_METADATA_ONLY",
            first_code_step="Generate Microstock_Export_Queue.csv and per-platform CSV schemas; defer FTP until accounts/requirements are verified.",
        ),
        ProjectOption(
            option="C",
            name="B2B indie studio cold email crawler",
            roi_rank=3,
            deploy_hours="15-30h for prototype; 40h+ for compliant deliverability/CRM pipeline",
            cash_cost="$20-$100/mo for domain/inbox/warmup/verifier if done seriously",
            success_probability="Low short-term, high variance; direct-ticket upside exists but needs portfolio, offer proof, and human sales follow-up",
            expected_revenue_stability="Very unstable until a trust funnel exists",
            technical_bottleneck="Email discovery accuracy, spam filtering, opt-out compliance, domain reputation, manual objection handling",
            ban_risk="High: spam complaints, sender-domain damage, platform scraping blocks, privacy/compliance exposure",
            decision="DEFER",
            first_code_step="Only create a hand-reviewed lead research schema later; do not scrape/send at scale now.",
        ),
    ]


def build_pinterest_queue(limit: int = 30) -> list[dict[str, object]]:
    source_rows = read_csv(MULTI_TRACK_PATH)
    rows: list[dict[str, object]] = []
    seen: set[str] = set()
    for row in source_rows:
        if len(rows) >= limit:
            break
        if row.get("QA_Status") != "READY":
            continue
        source_path = row.get("Source_Path", "")
        if not source_path or source_path in seen:
            continue
        seen.add(source_path)
        primary = row.get("Primary_Search_Intent") or "quiet luxury decor"
        title = f"{row.get('Product_Type', 'Art')} idea for {primary}".strip()
        board = "Reading Nook Decor" if "reading" in primary.lower() else "Quiet Luxury Wall Art"
        destination = row.get("eBay_Item_ID") or row.get("Etsy_Listing_ID") or "TO_FILL_AFTER_PUBLIC_URL"
        rows.append(
            {
                "Timestamp": now_text(),
                "Queue_ID": f"PIN-{len(rows)+1:04d}-{slug(row.get('ID', 'asset'))}",
                "Source_ID": row.get("ID", ""),
                "Track": row.get("Track", ""),
                "Board_Name": board,
                "Pin_Title": title[:100],
                "Pin_Description": (
                    f"{primary} with smoky jade, quiet luxury, and deep work room styling. "
                    "Fresh OpenClaw visual, staged for decor discovery."
                )[:500],
                "Alt_Text": f"{row.get('Category', '')} {row.get('Product_Type', '')} decor concept for {primary}".strip()[:500],
                "Local_Image_Path": source_path,
                "Public_Image_URL": "",
                "Destination_URL": destination,
                "UTM_Source": "pinterest",
                "Jitter_Minutes": row.get("Jitter_Minutes") or 37,
                "Risk_Status": "HOLD_UNTIL_OFFICIAL_API_AND_PUBLIC_IMAGE_URL",
                "Idempotency_Key": f"pinterest::{row.get('ID','')}::{slug(primary)}",
            }
        )
    return rows


def build_microstock_queue(limit: int = 40) -> list[dict[str, object]]:
    source_rows = read_csv(DIGITAL_INDEX_PATH)
    rows: list[dict[str, object]] = []
    for row in source_rows:
        if len(rows) >= limit:
            break
        source_path = row.get("Source_Path", "")
        if not source_path:
            continue
        title = re.sub(r"\b(12x18|5x7|4pc|Vinyl|Sticker)\b", "", row.get("Title", ""), flags=re.I)
        title = re.sub(r"\s+", " ", title).strip()[:180]
        keywords = [
            "quiet luxury",
            "dark academia",
            "smoky jade",
            "reading nook",
            "meditation room",
            "home office decor",
            "wabi sabi",
            "wall art",
            "interior design",
            "moody decor",
            "study room",
            "luxury apartment",
            "visual asset",
        ]
        rows.append(
            {
                "Timestamp": now_text(),
                "Queue_ID": f"STOCK-{len(rows)+1:04d}-{slug(row.get('ID','asset'))}",
                "Source_ID": row.get("ID", ""),
                "Local_Image_Path": source_path,
                "Stock_Title": title,
                "Keywords": ", ".join(keywords),
                "Adobe_Generative_AI_Flag": "REQUIRED_IF_SUBMITTED",
                "Shutterstock_CSV_Ready": "YES_METADATA_ONLY",
                "Freepik_FTP_Status": "BLOCKED_UNTIL_500_PUBLISHED_FILES",
                "Wirestock_Status": "MANUAL_PORTAL_OR_UNVERIFIED_API",
                "Risk_Status": "HOLD_FOR_PLATFORM_SPECIFIC_QA",
                "Notes": "Metadata/export only. Do not FTP-submit until agency account status and AI disclosure fields are verified.",
            }
        )
    return rows


def write_report(options: list[ProjectOption], pin_rows: list[dict[str, object]], stock_rows: list[dict[str, object]]) -> Path:
    report_path = REVIEW_DIR / f"FALLBACK_PROJECTS_ENGINEERING_EVAL_{datetime.now(NY):%Y%m%d_%H%M}.md"
    lines: list[str] = []
    lines.append("# Fall-back Projects Engineering Evaluation")
    lines.append("")
    lines.append(f"Generated: {now_text()} America/New_York")
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append("Build 1: Pinterest visual traffic queue, using official API only, no browser/session automation.")
    lines.append("Build 2: Microstock metadata/export matrix, but keep it metadata-only until contributor account requirements are verified.")
    lines.append("Defer: B2B cold-email crawler. It has the highest legal/deliverability risk and requires a human sales funnel before automation.")
    lines.append("")
    lines.append("## Cold Engineering Matrix")
    lines.append("")
    lines.append("| Rank | Option | Time to Deploy | Cash Cost | Success / Stability | Bottleneck | Ban Risk | Decision |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for opt in sorted(options, key=lambda item: item.roi_rank):
        lines.append(
            f"| {opt.roi_rank} | {opt.option}: {opt.name} | {opt.deploy_hours} | {opt.cash_cost} | "
            f"{opt.success_probability}; {opt.expected_revenue_stability} | {opt.technical_bottleneck} | "
            f"{opt.ban_risk} | {opt.decision} |"
        )
    lines.append("")
    lines.append("## First Code Framework")
    lines.append("")
    lines.append(f"- Pinterest queue generated: `{PINTEREST_QUEUE}` ({len(pin_rows)} rows).")
    lines.append(f"- Microstock export queue generated: `{MICROSTOCK_QUEUE}` ({len(stock_rows)} rows).")
    lines.append(f"- Evaluation matrix generated: `{EVAL_CSV}`.")
    lines.append("")
    lines.append("### Pinterest Engine Skeleton")
    lines.append("")
    lines.append("1. Read `Pinterest_Pin_Queue.csv`.")
    lines.append("2. QA: source image exists, non-low-res, non-duplicate, unique board/destination cadence.")
    lines.append("3. Host the image at a public HTTPS URL; Pinterest cannot fetch local laptop file paths.")
    lines.append("4. Use official Pinterest API after app approval and `pins:write`; one worker, token bucket, jitter, per-board pacing.")
    lines.append("5. Write pin_id and analytics back to the unified registry; never use session-cookie scraping.")
    lines.append("")
    lines.append("### Microstock Export Skeleton")
    lines.append("")
    lines.append("1. Read `Microstock_Export_Queue.csv`.")
    lines.append("2. Run image QA and similarity/dedup filter.")
    lines.append("3. Embed/emit metadata per platform: filename, title/description, keywords, category, AI disclosure.")
    lines.append("4. Export per-platform CSV and staging folders; FTP only after account credentials and platform requirements are verified.")
    lines.append("")
    lines.append("## Source-Aware Risk Notes")
    lines.append("")
    lines.append("- Pinterest supports creating/managing Pins/Boards through its API, but its own guidance says bulk creation must obey spam/abuse rules; Trial access pins may be sandbox-only until Standard access.")
    lines.append("- Pinterest policy warns against unapproved automation and repetitive/deceptive money-making content. So we use official API, slow pacing, unique pins, and no session-cookie botting.")
    lines.append("- Freepik official contributor docs say FTP upload is only available after 500 published files. This blocks a new-account FTP matrix there.")
    lines.append("- Shutterstock contributor docs support FTP/FTPS uploads and CSV metadata. That makes it a realistic first stock adapter once account status exists.")
    lines.append("- Adobe Stock accepts generative AI content only with proper rights, AI labeling, and strict quality/legal standards; near-duplicate spam is dangerous.")
    lines.append("- FTC CAN-SPAM guidance covers B2B commercial email too and requires truthful headers, non-deceptive subject, ad disclosure, physical postal address, opt-out, and honoring opt-outs. This makes cold email unsuitable for unsupervised automation now.")
    lines.append("")
    lines.append("## Primary Source Links")
    lines.append("")
    lines.append("- Pinterest content API/use case: https://developers.pinterest.com/usecase/content/")
    lines.append("- Pinterest access tiers: https://developers.pinterest.com/docs/key-concepts/access-tiers/")
    lines.append("- Pinterest developer guidelines: https://policy.pinterest.com/developer-guidelines")
    lines.append("- Freepik contributor upload levels: https://support.freepik.com/s/article/Contributor-Level-Upload")
    lines.append("- Freepik content submission requirements: https://support.freepik.com/s/article/What-can-I-sell-on-Freepik")
    lines.append("- Shutterstock FTPS upload help entry: https://support.submit.shutterstock.com/s/article/How-do-I-upload-content-via-FTPS")
    lines.append("- Adobe Stock generative AI content rules: https://helpx.adobe.com/stock/contributor/help/generative-ai-content.html")
    lines.append("- FTC CAN-SPAM compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business")
    lines.append("")
    lines.append("## Recommendation")
    lines.append("")
    lines.append("Highest ROI next sprint: Pinterest queue first, because it attacks the current zero-view problem without new listing fees and reuses existing visual assets.")
    lines.append("Second sprint: Microstock metadata/export, because it creates a zero-marginal-cost asset distribution backlog without touching marketplace accounts.")
    lines.append("Do not build the cold-email crawler until there is a portfolio landing page, compliant sender identity, opt-out handling, and hand-reviewed lead scoring.")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    latest = REVIEW_DIR / "Latest" / "fallback_projects_engineering_eval_latest.md"
    latest.parent.mkdir(exist_ok=True)
    latest.write_text(report_path.read_text(encoding="utf-8"), encoding="utf-8")
    return report_path


def run(pin_limit: int = 30, stock_limit: int = 40) -> dict[str, object]:
    options = option_matrix()
    write_csv(EVAL_CSV, [asdict(opt) for opt in options], list(asdict(options[0]).keys()))
    pin_rows = build_pinterest_queue(limit=pin_limit)
    stock_rows = build_microstock_queue(limit=stock_limit)
    write_csv(PINTEREST_QUEUE, pin_rows, list(pin_rows[0].keys()) if pin_rows else ["Timestamp"])
    write_csv(MICROSTOCK_QUEUE, stock_rows, list(stock_rows[0].keys()) if stock_rows else ["Timestamp"])
    report = write_report(options, pin_rows, stock_rows)
    state = {
        "timestamp": now_text(),
        "recommendations": ["B:Pinterest visual traffic engine", "A:Microstock metadata/export matrix"],
        "deferred": ["C:B2B cold email crawler"],
        "pinterest_queue_rows": len(pin_rows),
        "microstock_queue_rows": len(stock_rows),
        "evaluation_csv": str(EVAL_CSV),
        "pinterest_queue": str(PINTEREST_QUEUE),
        "microstock_queue": str(MICROSTOCK_QUEUE),
        "report": str(report),
        "spend_now": 0.0,
        "public_actions": 0,
    }
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    return state


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate and stage zero-marginal-cost fall-back projects.")
    parser.add_argument("--pin-limit", type=int, default=30)
    parser.add_argument("--stock-limit", type=int, default=40)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    state = run(pin_limit=args.pin_limit, stock_limit=args.stock_limit)
    if args.json:
        print(json.dumps(state, indent=2, ensure_ascii=False))
    else:
        print(f"[FALLBACK-RND] report={state['report']}")
        print(f"[FALLBACK-RND] pinterest_rows={state['pinterest_queue_rows']} microstock_rows={state['microstock_queue_rows']}")


if __name__ == "__main__":
    main()
