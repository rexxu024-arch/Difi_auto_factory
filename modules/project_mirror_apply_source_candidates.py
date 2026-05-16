"""Apply vetted starter source URLs to Project Mirror source slots.

This only seeds candidates for review. It does not download images or reuse
source media. Accepted samples still require later quality review.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
INDEX_CSV = DATABASE_DIR / "Aesthetic_DNA_Pool_Index.csv"
SOURCE_CANDIDATES_CSV = DATABASE_DIR / "Aesthetic_DNA_Source_Candidates.csv"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"


def now_et() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], headers: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


def apply_candidates() -> dict[str, int]:
    rows = read_csv(INDEX_CSV)
    candidates = read_csv(SOURCE_CANDIDATES_CSV)
    if not rows:
        raise FileNotFoundError(f"Missing or empty {INDEX_CSV}")
    if not candidates:
        raise FileNotFoundError(f"Missing or empty {SOURCE_CANDIDATES_CSV}")

    headers = list(rows[0].keys())
    applied_by_niche: dict[str, int] = {}
    used_urls = {row.get("Source_URL", "") for row in rows if row.get("Source_URL")}

    for candidate in candidates:
        niche = candidate.get("Niche", "")
        url = candidate.get("Source_URL", "")
        if not niche or not url or url in used_urls:
            continue
        for row in rows:
            if row.get("Niche") != niche:
                continue
            if row.get("Source_URL"):
                continue
            row["Status"] = "SOURCE_CANDIDATE_REVIEW"
            row["Source_Target"] = candidate.get("Source_Title", row.get("Source_Target", ""))
            row["Source_URL"] = url
            row["Vision_Status"] = "WAITING_ACCEPTED_IMAGE"
            row["Notes"] = (
                f"{candidate.get('Why_Useful', '')} | use mode: {candidate.get('Use_Mode', '')} | "
                f"guard: {candidate.get('Do_Not_Do', '')}"
            )
            applied_by_niche[niche] = applied_by_niche.get(niche, 0) + 1
            used_urls.add(url)
            break

    write_csv(INDEX_CSV, rows, headers)
    return applied_by_niche


def append_progress(applied_by_niche: dict[str, int]) -> None:
    total = sum(applied_by_niche.values())
    msg = (
        f"\n## {now_et().strftime('%Y-%m-%d %H:%M ET')} - Project Mirror Source Candidate Seeding\n"
        f"- Seeded {total} vetted source-candidate URLs into `{INDEX_CSV.name}` for review-only DNA extraction.\n"
        f"- By niche: {applied_by_niche}.\n"
        "- No image download, marketplace publish, or source redistribution occurred.\n"
    )
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(msg)


def main() -> int:
    applied_by_niche = apply_candidates()
    append_progress(applied_by_niche)
    print({"applied_total": sum(applied_by_niche.values()), "by_niche": applied_by_niche})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
