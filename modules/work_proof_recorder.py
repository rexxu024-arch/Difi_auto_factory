"""Append a small auditable proof that a work block did real work.

This is intentionally primitive. Rex needs to distinguish "the loop is alive"
from "actual project work happened."  Every supervised work block should leave
one JSONL row plus a latest Markdown summary with concrete artifacts.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = ROOT / "Database"
REPORTS_DIR = ROOT / "Reports"
LOG_FILE = DATABASE_DIR / "Work_Proof_Log.jsonl"
LATEST_JSON = DATABASE_DIR / "Work_Proof_Latest.json"
LATEST_MD = REPORTS_DIR / "Work_Proof_Latest.md"
ET = ZoneInfo("America/New_York")


def now_iso() -> str:
    return datetime.now(ET).isoformat(timespec="seconds")


def main() -> int:
    parser = argparse.ArgumentParser(description="Record OpenClaw work proof.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--status", default="COMPLETED")
    parser.add_argument("--project", default="OpenClaw")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--started-at", default="")
    parser.add_argument("--ended-at", default="")
    parser.add_argument("--duration-sec", type=float, default=0.0)
    args = parser.parse_args()

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    row = {
        "recorded_at_et": now_iso(),
        "source": args.source,
        "status": args.status,
        "project": args.project,
        "summary": args.summary,
        "artifacts": args.artifact,
        "started_at_et": args.started_at or "",
        "ended_at_et": args.ended_at or now_iso(),
        "duration_sec": args.duration_sec,
    }

    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    LATEST_JSON.write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
    artifact_lines = "\n".join(f"- `{item}`" for item in row["artifacts"]) or "- none"
    LATEST_MD.write_text(
        "\n".join(
            [
                "# Latest Work Proof",
                "",
                f"- recorded_at_et: `{row['recorded_at_et']}`",
                f"- source: `{row['source']}`",
                f"- status: `{row['status']}`",
                f"- project: `{row['project']}`",
                f"- summary: {row['summary']}",
                f"- duration_sec: `{row['duration_sec']}`",
                "- artifacts:",
                artifact_lines,
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"[WORK-PROOF] {row['source']} {row['status']} {row['project']}: {row['summary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
