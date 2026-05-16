import argparse
import csv
import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import etsy_api

DATABASE = PROJECT_ROOT / "Database"
REPORTS = PROJECT_ROOT / "Reports"
RELEASE = PROJECT_ROOT / "Release"
FIRST_AUDIT = PROJECT_ROOT / "First_Audit_Release"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"

LOW_VALUE_WORDS = (
    "sticker",
    "decal",
    "digital",
    "printable",
    "planner",
    "journal",
    "ephemera",
    "download",
    "bundle",
    "insert",
)

PROTECTED_WORDS = (
    "first audit",
    "studio relic",
    "optical acrylic",
    "executive office",
    "anchor",
    "masterwork",
)


def now_et() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def price_usd(listing: dict) -> float:
    raw = listing.get("price")
    if isinstance(raw, dict):
        amount = raw.get("amount") or raw.get("value") or 0
        divisor = raw.get("divisor") or 100
        try:
            return float(amount) / float(divisor)
        except Exception:
            return 0.0
    try:
        return float(raw)
    except Exception:
        return 0.0


def epoch_to_age_hours(value) -> float:
    if not value:
        return 0.0
    try:
        created = datetime.fromtimestamp(int(value), tz=timezone.utc)
    except Exception:
        return 0.0
    return max(0.0, (datetime.now(timezone.utc) - created).total_seconds() / 3600)


def is_low_value_pattern(listing: dict) -> bool:
    title_l = str(listing.get("title") or "").lower()
    listing_type = str(listing.get("type") or listing.get("listing_type") or "").lower()
    if listing_type == "download":
        return True
    return any(word in title_l for word in LOW_VALUE_WORDS)


def fetch_active_listings(limit: int = 100) -> list[dict]:
    shop_id = etsy_api.first_shop_id()
    offset = 0
    rows: list[dict] = []
    while True:
        data = etsy_api.request(
            "GET",
            f"/shops/{shop_id}/listings",
            params={"state": "active", "limit": limit, "offset": offset},
        )
        batch = data.get("results") or []
        rows.extend(batch)
        count = data.get("count")
        if len(batch) < limit:
            break
        offset += limit
        if count is not None and offset >= int(count):
            break
    return rows


def classify_candidate(
    listing: dict,
    *,
    max_price: float,
    min_age_hours: float,
    policy: str,
) -> tuple[bool, str]:
    title = str(listing.get("title") or "")
    title_l = title.lower()
    listing_type = str(listing.get("type") or listing.get("listing_type") or "").lower()
    views = int(listing.get("views") or 0)
    favs = int(listing.get("num_favorers") or 0)
    price = price_usd(listing)
    age_hours = epoch_to_age_hours(listing.get("created_timestamp") or listing.get("original_creation_timestamp"))

    if any(word in title_l for word in PROTECTED_WORDS):
        return False, "protected_title"

    if policy == "hard":
        if price < max_price and is_low_value_pattern(listing):
            return True, "v155_hard_low_price_digital_or_sticker"
        if views == 0 and favs == 0 and age_hours >= min_age_hours and any(word in title_l for word in LOW_VALUE_WORDS):
            return True, "v155_hard_zero_signal_non_pod_experiment"
        return False, "v155_hard_keep"

    if price >= max_price:
        return False, f"price_ge_{max_price:g}"
    if views != 0 or favs != 0:
        return False, f"has_signal_views_{views}_favs_{favs}"
    if age_hours < min_age_hours:
        return False, f"too_new_{age_hours:.1f}h"
    if listing_type == "download":
        return True, "download_under_price_zero_signal"
    if any(word in title_l for word in LOW_VALUE_WORDS):
        return True, "low_value_keyword_under_price_zero_signal"
    return False, "not_low_value_pattern"


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def audit_etsy_purge(max_price: float, min_age_hours: float, policy: str) -> tuple[list[dict], list[dict]]:
    listings = fetch_active_listings()
    audit_rows: list[dict] = []
    candidates: list[dict] = []
    ts = now_et()
    for listing in listings:
        is_candidate, reason = classify_candidate(
            listing,
            max_price=max_price,
            min_age_hours=min_age_hours,
            policy=policy,
        )
        row = {
            "audit_ts": ts,
            "policy": policy,
            "listing_id": listing.get("listing_id"),
            "state": listing.get("state"),
            "title": listing.get("title"),
            "listing_type": listing.get("type") or listing.get("listing_type"),
            "price_usd": f"{price_usd(listing):.2f}",
            "views": listing.get("views") or 0,
            "favorites": listing.get("num_favorers") or 0,
            "age_hours": f"{epoch_to_age_hours(listing.get('created_timestamp') or listing.get('original_creation_timestamp')):.1f}",
            "candidate": "YES" if is_candidate else "NO",
            "reason": reason,
            "url": listing.get("url") or "",
        }
        audit_rows.append(row)
        if is_candidate:
            candidates.append(row)
    fieldnames = [
        "audit_ts",
        "policy",
        "listing_id",
        "state",
        "title",
        "listing_type",
        "price_usd",
        "views",
        "favorites",
        "age_hours",
        "candidate",
        "reason",
        "url",
    ]
    write_csv(DATABASE / "V155_Etsy_Purge_Audit.csv", audit_rows, fieldnames)
    write_csv(DATABASE / "V155_Etsy_Purge_Candidates.csv", candidates, fieldnames)
    return audit_rows, candidates


def set_etsy_listing_state(listing_id: str, state: str) -> dict:
    shop_id = etsy_api.first_shop_id()
    # Etsy accepts application/x-www-form-urlencoded for updateListing reliably.
    return etsy_api.request(
        "PATCH",
        f"/shops/{shop_id}/listings/{listing_id}",
        data={"state": state},
    )


def execute_purge(candidates: list[dict], max_apply: int, sleep_seconds: float) -> list[dict]:
    results: list[dict] = []
    fieldnames = [
        "execution_ts",
        "listing_id",
        "title",
        "price_usd",
        "views",
        "favorites",
        "reason",
        "target_state",
        "result",
        "error",
    ]
    log_path = DATABASE / "V155_Etsy_Purge_Execution_Log.csv"
    existing = log_path.exists()
    with log_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not existing:
            writer.writeheader()
        for row in candidates[:max_apply]:
            listing_id = str(row["listing_id"])
            result = {
                "execution_ts": now_et(),
                "listing_id": listing_id,
                "title": row["title"],
                "price_usd": row["price_usd"],
                "views": row["views"],
                "favorites": row["favorites"],
                "reason": row["reason"],
                "target_state": "inactive",
                "result": "",
                "error": "",
            }
            try:
                updated = set_etsy_listing_state(listing_id, "inactive")
                result["result"] = str(updated.get("state") or "updated")
            except Exception as exc:
                result["result"] = "ERROR"
                result["error"] = str(exc)[:500]
            writer.writerow(result)
            f.flush()
            results.append(result)
            if sleep_seconds:
                time.sleep(sleep_seconds)
    return results


def choose_first_audit_source() -> Path:
    preferred = [
        FIRST_AUDIT / "001-06_烟玉斯巴达",
        FIRST_AUDIT / "001-07_黑曜桂冠",
        FIRST_AUDIT / "001-03_冰霜符文圣杯",
    ]
    for folder in preferred:
        if (folder / "01_Hero_Production.png").exists():
            return folder
    for folder in FIRST_AUDIT.iterdir():
        if folder.is_dir() and (folder / "01_Hero_Production.png").exists():
            return folder
    raise FileNotFoundError("No First Audit release source with 01_Hero_Production.png found.")


def build_weaponized_release() -> Path:
    source = choose_first_audit_source()
    target = RELEASE / "OC-V155-001-Executive-Jade-Desk-Gift"
    target.mkdir(parents=True, exist_ok=True)

    copy_map = {
        "01_Hero_Production.png": "01_Hero_Production.png",
        "02_Mockup_Luxury_Desk.jpg": "02_Mockup_Luxury_Desk.jpg",
        "03_Mockup_Art_Gallery.jpg": "03_Mockup_Art_Gallery.jpg",
    }
    for src_name, dst_name in copy_map.items():
        src = source / src_name
        if not src.exists():
            # Keep the folder complete even if an older source only has the hero.
            src = source / "01_Hero_Production.png"
        shutil.copy2(src, target / dst_name)

    narrative = f"""# OC-V155-001 | Executive Jade Desk Gift

Source Asset: {source.name}
Protocol: V15.5 Dual-Track / Executive Gift Entrance Tier
Carrier: Optical Acrylic Block, 5 x 7 vertical
Suggested Printify Anchor: Photo Block / Acrylic Block, official 5 x 7 vertical variant if available in connected shop
Retail Tier: $88 entrance gift object

## Gift SEO Title

Executive Office Gift Smoky Jade Spartan Relic Acrylic Block, Minimalist Boss Decor for Walnut Desk

## English Listing / Sales Description

This studio object is built for a desk, shelf, or private office where ordinary wall decor feels too soft. The image reads like a recovered martial relic: smoky jade, blackened metal, cold highlights, and a restrained gallery-grade composition designed for an optical acrylic block.

It is positioned as an executive gift rather than a novelty item: compact enough for a desk, visually heavy enough to anchor a room, and neutral enough to sit beside walnut, black glass, brushed steel, or a 2K monitor setup.

Only the main production image is the purchasable artwork. Additional images are context previews or detail studies to help the buyer understand scale, mood, and material presence.

## Cost / Price Guard

- Target retail: $88
- Tier: $48-$98 entrance product
- Pricing intent: high-quality business gift, not low-margin traffic bait
- Before public listing: recalculate exact Printify production, shipping, marketplace fee, payment fee, listing fee, and ad-rate lane.

## 中文私域话术矩阵

### 官方概念设定

《烟玉斯巴达》是 OpenClaw Design Studio 的第一批审计资产之一。它用冷玉、黑钛金和古典战盔的视觉结构，重构一种“现代办公桌上的精神甲胄”。不是普通装饰画，而是给办公室、书房和高管桌面压住气场的实体物。

### 公域 / 朋友圈诱饵

纽约工作室这批实物打样里，我最看好的就是这个。不是走大平台低价铺货的东西，适合放老板桌、书房、玄关，质感偏冷、硬、贵，想看实物场景图可以私我。

### 1v1 核心节点私信

这个不是送“可爱小摆件”的逻辑，是送一个有气场的桌面物件。普通奢侈品太容易撞，反而没意思；这种独立概念作品更像审美名片。你看一下我发你的办公桌和画廊场景图，如果你觉得这个气质对，就可以走小批量打样。

### 抗拒处理

这类不是现货仓库货。走 Printify 全球供应链打样通常需要 10-14 天；如果要做私域定制、组合套装或更大尺寸，需要单独排期。我们宁愿慢一点，也不做廉价感。
"""
    (target / "04_Narrative_Matrix.md").write_text(narrative, encoding="utf-8")
    return target


def write_report(audit_rows: list[dict], candidates: list[dict], executed: list[dict], release_dir: Path) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    removed = [r for r in executed if r.get("result") and r.get("result") != "ERROR"]
    report = f"""# V15.5 Great Purge And First Release

Timestamp: {now_et()}

## Etsy Purge

- Active listings scanned: {len(audit_rows)}
- Purge candidates found: {len(candidates)}
- First-wave inactive attempts: {len(executed)}
- First-wave successful/non-error: {len(removed)}
- Candidate table: `Database/V155_Etsy_Purge_Candidates.csv`
- Execution log: `Database/V155_Etsy_Purge_Execution_Log.csv`

Selection rule:

- `conservative`: price below threshold, zero lifetime views, zero favorites, old enough, and low-value digital/sticker/planner/printable pattern
- `hard`: all low-value digital/sticker assets below threshold, plus old zero-signal non-POD experiments
- protected Studio / First Audit titles excluded
- Etsy listing API exposes lifetime view/favorite counters here; true 48h traffic is not available through this endpoint, so 48h purges require Seller Hub export or a later analytics source.

## First Weaponized Folder

- Folder: `{release_dir}`
- Contains: hero production image, luxury desk mockup, gallery mockup, narrative matrix.
- Tier: $88 entrance executive gift object.
"""
    (REPORTS / "V155_Great_Purge_And_First_Release.md").write_text(report, encoding="utf-8")
    with PROGRESS_LOG.open("a", encoding="utf-8") as f:
        f.write(
            f"\n\n## {now_et()} - V15.5 purge/release\n"
            f"- Scanned Etsy active listings: {len(audit_rows)}.\n"
            f"- Purge candidates: {len(candidates)}; first-wave inactive attempts: {len(executed)}; non-error: {len(removed)}.\n"
            f"- Created V15.5 weaponized folder: {release_dir}.\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="V15.5 purge and first weaponized release builder.")
    parser.add_argument("--apply", action="store_true", help="Set selected Etsy candidates inactive.")
    parser.add_argument("--max-apply", type=int, default=20)
    parser.add_argument("--max-price", type=float, default=15.0)
    parser.add_argument("--min-age-hours", type=float, default=72.0)
    parser.add_argument("--sleep-seconds", type=float, default=2.0)
    parser.add_argument("--policy", choices=["conservative", "hard"], default="conservative")
    args = parser.parse_args()

    audit_rows, candidates = audit_etsy_purge(args.max_price, args.min_age_hours, args.policy)
    executed: list[dict] = []
    if args.apply and candidates:
        executed = execute_purge(candidates, args.max_apply, args.sleep_seconds)
    release_dir = build_weaponized_release()
    write_report(audit_rows, candidates, executed, release_dir)
    print(
        json.dumps(
            {
                "active_scanned": len(audit_rows),
                "purge_candidates": len(candidates),
                "policy": args.policy,
                "apply": args.apply,
                "executed": len(executed),
                "release_dir": str(release_dir),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
