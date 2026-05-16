"""Validate Adobe Stock draft metadata before any upload.

This is a local QA gate. It writes a separate report and does not upload,
submit, spend, or mutate marketplace state.
"""

from __future__ import annotations

import argparse
import csv
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from adobe_stock_isolation import assert_adobe_write_paths


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

BATCH = DATABASE / "Adobe_Stock_Pilot_Batch.csv"
QUEUE = DATABASE / "Adobe_Stock_Pilot_Queue.csv"
OUT_QA = DATABASE / "Adobe_Stock_Metadata_QA.csv"
OUT_REPORT = REVIEW / "Adobe_Stock_Metadata_QA_latest.md"

PUBLIC_BAN_TERMS = {
    "ai art",
    "ai generated",
    "ai-generated",
    "artificial intelligence",
    "created by ai",
    "created using ai",
    "created using generative ai",
    "dall-e",
    "dalle",
    "firefly",
    "generative ai",
    "machine learning",
    "neural network",
    "stable diffusion",
    "text to image",
    "sweatshop",
    "openclaw",
    "first audit",
    "rex",
    "grey",
    "gemini",
    "codex",
    "midjourney",
    "claude",
    "deepseek",
    "dify",
    "etsy",
    "ebay",
    "printify",
}

IP_RISK_TERMS = {
    "disney",
    "marvel",
    "dc comics",
    "star wars",
    "pokemon",
    "warhammer",
    "lego",
    "pixar",
    "studio ghibli",
    "banksy",
    "basquiat",
    "warhol",
    "haring",
    "kusama",
    "giger",
    "picasso",
    "matisse",
    "monet",
    "van gogh",
    "vangogh",
    "rembrandt",
    "da vinci",
    "dali",
    "frida kahlo",
    "kaws",
    "bearbrick",
    "supreme",
    "nike",
    "apple",
    "tesla",
    "google",
    "amazon",
    "netflix",
    "harry potter",
    "lord of the rings",
    "game of thrones",
    "batman",
    "spiderman",
    "spider-man",
    "unreal engine",
    "unity",
    "coca cola",
    "coca-cola",
    "mcdonald",
    "mcdonalds",
    "gucci",
    "prada",
    "louis vuitton",
    "chanel",
    "hermes",
    "rolex",
    "adobe",
    "firefly",
    "facebook",
    "instagram",
    "youtube",
    "tiktok",
    "xbox",
    "playstation",
    "nintendo",
    "mickey",
    "barbie",
    "hello kitty",
    "naruto",
    "one piece",
    "dragon ball",
    "matrix",
    "blade runner",
    "dune",
    "lotr",
    "lovecraft",
    "cthulhu",
}

KNOWN_PEOPLE_TERMS = {
    "elon musk",
    "taylor swift",
    "beyonce",
    "rihanna",
    "kim kardashian",
    "kanye",
    "trump",
    "biden",
    "obama",
    "putin",
    "xi jinping",
    "zelensky",
    "swiftie",
    "celebrity",
    "influencer",
}

GOVERNMENT_NEWS_TERMS = {
    "fbi",
    "cia",
    "nasa",
    "white house",
    "pentagon",
    "election",
    "war news",
    "breaking news",
    "news event",
    "real event",
    "terror attack",
}

STOPWORDS = {
    "and",
    "with",
    "the",
    "for",
    "a",
    "an",
    "of",
    "to",
    "in",
    "on",
}


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, str]]:
    rows = read_rows(BATCH)
    if rows:
        return rows
    return read_rows(QUEUE)


def split_keywords(value: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in re.split(r"[,;]", value):
        keyword = re.sub(r"\s+", " ", raw.strip().lower())
        if not keyword or keyword in seen:
            continue
        seen.add(keyword)
        out.append(keyword)
    return out


def contains_blocked_term(value: str) -> str:
    lowered = value.lower()
    for term in sorted(PUBLIC_BAN_TERMS | IP_RISK_TERMS | KNOWN_PEOPLE_TERMS | GOVERNMENT_NEWS_TERMS):
        if len(term) <= 3 and term.isalpha():
            if re.search(rf"\b{re.escape(term)}\b", lowered):
                return term
            continue
        if term in lowered:
            return term
    return ""


def prompt_may_have_positive_people(prompt: str) -> bool:
    lowered = prompt.lower()
    positive_terms = ("face", "portrait", "person", "people", "human", "model", "celebrity")
    for term in positive_terms:
        if not re.search(rf"\b{re.escape(term)}s?\b", lowered):
            continue
        negated = any(
            marker in lowered
            for marker in (
                f"no {term}",
                f"no {term}s",
                f"without {term}",
                f"without {term}s",
                f"avoid {term}",
                f"avoid {term}s",
                f"exclude {term}",
                f"exclude {term}s",
            )
        )
        if not negated:
            return True
    return False


def title_search_terms(title: str) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9]{2,}", title.lower())
    return [word for word in words if word not in STOPWORDS][:8]


def validate(row: dict[str, str]) -> tuple[str, list[str]]:
    issues: list[str] = []
    filename = row.get("Target_Filename") or row.get("Filename", "")
    title = row.get("Adobe_Title") or row.get("Title", "")
    keywords_text = row.get("Adobe_Keywords") or row.get("Keywords", "")
    category = row.get("Adobe_Category") or row.get("Category", "")
    created_using_ai = row.get("Created_Using_AI", "").lower()
    release_required = row.get("Release_Required", "").lower()

    if not filename:
        issues.append("missing_filename")
    elif len(filename) > 30:
        issues.append("filename_over_30_chars")
    elif not re.fullmatch(r"[A-Za-z0-9_.-]+", filename):
        issues.append("filename_not_ascii_safe")

    if not 10 <= len(title) <= 70:
        issues.append("title_length_outside_10_70")
    if "," in title:
        issues.append("title_contains_comma")
    blocked = contains_blocked_term(title)
    if blocked:
        issues.append(f"title_blocked_term:{blocked}")

    keywords = split_keywords(keywords_text)
    if len(keywords) < 35:
        issues.append("too_few_keywords")
    if len(keywords) > 50:
        issues.append("too_many_keywords")
    blocked = contains_blocked_term(keywords_text)
    if blocked:
        issues.append(f"keyword_blocked_term:{blocked}")
    prompt_blocked = contains_blocked_term(row.get("MJ_Prompt", ""))
    if prompt_blocked:
        issues.append(f"prompt_blocked_term:{prompt_blocked}")
    prompt = row.get("MJ_Prompt", "").lower()
    if "in the style of" in prompt or "style of " in prompt:
        issues.append("prompt_uses_style_of_artist_pattern")
    if prompt_may_have_positive_people(prompt):
        issues.append("prompt_may_require_model_release")
    if len(keywords) != len(set(keywords)):
        issues.append("duplicate_keywords")

    missing_title_terms = [term for term in title_search_terms(title) if term not in " ".join(keywords[:10])]
    if len(missing_title_terms) > 3:
        issues.append("title_terms_not_front_loaded_in_top_10_keywords")

    if category != "8":
        issues.append("category_not_graphic_resources_8")
    if created_using_ai != "true":
        issues.append("created_using_ai_not_true")
    if release_required not in {"false", ""}:
        issues.append("release_required_not_false")
    if any(term in title.lower() for term in ("logo", "trademark")):
        issues.append("title_implies_logo_or_brand")
    if any(term in keywords_text.lower() for term in ("logo", "trademark")):
        issues.append("keywords_imply_logo_or_brand")

    status = "METADATA_QA_PASS" if not issues else "METADATA_QA_HOLD"
    return status, issues


def run(limit: int) -> dict[str, int]:
    assert_adobe_write_paths((OUT_QA, OUT_REPORT))
    rows = source_rows()
    if not rows:
        raise RuntimeError("No Adobe Stock metadata rows found. Run adobe_stock_pilot_batch.py first.")
    checked_rows = rows[:limit] if limit else rows
    qa_rows: list[dict[str, str]] = []
    passed = held = 0
    for index, row in enumerate(checked_rows, start=1):
        status, issues = validate(row)
        if status == "METADATA_QA_PASS":
            passed += 1
        else:
            held += 1
        qa_rows.append(
            {
                "QA_ID": f"ADOBE-META-QA-{index:04d}",
                "Source_ID": row.get("Batch_ID") or row.get("Queue_ID") or row.get("ID") or row.get("Asset_ID", ""),
                "Family": row.get("Family", ""),
                "Target_Filename": row.get("Target_Filename") or row.get("Filename", ""),
                "Adobe_Title": row.get("Adobe_Title") or row.get("Title", ""),
                "Keyword_Count": str(len(split_keywords(row.get("Adobe_Keywords") or row.get("Keywords", "")))),
                "QA_Status": status,
                "Issues": ";".join(issues),
                "Next_Action": "READY_FOR_IMAGE_QA_OR_UPLOAD_APPROVAL" if status == "METADATA_QA_PASS" else "FIX_METADATA_BEFORE_UPLOAD",
            }
        )

    write_rows(OUT_QA, qa_rows)
    write_report(qa_rows, passed, held)
    append_progress(len(qa_rows), passed, held)
    return {"checked": len(qa_rows), "passed": passed, "held": held}


def write_report(qa_rows: list[dict[str, str]], passed: int, held: int) -> None:
    issue_counts: dict[str, int] = {}
    for row in qa_rows:
        for issue in row["Issues"].split(";"):
            if not issue:
                continue
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
    lines = [
        "# Adobe Stock Metadata QA",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Checked: {len(qa_rows)}",
        f"- Passed: {passed}",
        f"- Held: {held}",
        f"- QA CSV: `{OUT_QA.relative_to(PROJECT_ROOT)}`",
        "- Official guard: Adobe AI disclosure must be selected during submission, but public title/keywords must not contain AI or generative-AI labels.",
        "- Rights guard: public metadata and prompts are blocked if they contain living/public people, artist names, brands, franchises, protected characters, or government/news-event terms.",
        "- Similar-content guard: keep first submit small and visually diverse; do not flood near-duplicate material/background families.",
        "",
        "## Top Issues",
        "",
    ]
    if issue_counts:
        lines.extend(f"- {issue}: {count}" for issue, count in sorted(issue_counts.items(), key=lambda item: (-item[1], item[0]))[:20])
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Guard",
            "",
            "This QA pass only validates metadata. It does not approve upload unless image QA also passes and Rex/guard budget allows submission.",
        ]
    )
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def append_progress(checked: int, passed: int, held: int) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock metadata QA checked={checked}; passed={passed}; "
            f"held={held}; no upload/spend.\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    result = run(args.limit)
    print(f"[ADOBE-METADATA-QA] {result}")


if __name__ == "__main__":
    main()
