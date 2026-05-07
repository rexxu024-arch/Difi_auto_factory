"""Parse Grey/Gemini responses into local task recommendations."""

from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

BRIDGE_DIR = PROJECT_ROOT / "Review_Packets" / "Gemini_Bridge"
FROM_GREY = BRIDGE_DIR / "FROM_GREY_latest.md"
TASKS_CSV = PROJECT_ROOT / "Database" / "Grey_Bridge_Tasks.csv"
DECISIONS_JSON = BRIDGE_DIR / "GREY_DECISIONS_latest.json"


def _now() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")


def _extract_json(text: str) -> object | None:
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    candidates = [fence.group(1)] if fence else []
    candidates.append(text)
    for candidate in candidates:
        stripped = candidate.strip()
        start_positions = [idx for idx in (stripped.find("{"), stripped.find("[")) if idx >= 0]
        if not start_positions:
            continue
        start = min(start_positions)
        snippet = stripped[start:]
        for end in range(len(snippet), max(0, len(snippet) - 2000), -1):
            try:
                return json.loads(snippet[:end])
            except Exception:
                continue
    return None


def _normalize_tasks(parsed: object, raw_text: str) -> list[dict[str, str]]:
    tasks: list[dict[str, str]] = []
    if isinstance(parsed, dict):
        source = parsed.get("tasks") or parsed.get("actions") or parsed.get("recommendations") or []
        if isinstance(source, dict):
            source = [source]
        for item in source if isinstance(source, list) else []:
            if not isinstance(item, dict):
                continue
            tasks.append(
                {
                    "Title": str(item.get("title") or item.get("task") or item.get("action") or "Grey recommendation")[:160],
                    "Priority": str(item.get("priority") or item.get("rank") or "50"),
                    "Lane": str(item.get("lane") or item.get("category") or "grey"),
                    "Rationale": str(item.get("rationale") or item.get("reason") or "")[:800],
                    "Command": str(item.get("command") or "")[:400],
                    "Risk": str(item.get("risk") or "review")[:80],
                }
            )
    if tasks:
        return tasks
    bullet_lines = [
        re.sub(r"^[-*\d.\s]+", "", line).strip()
        for line in raw_text.splitlines()
        if re.match(r"^\s*([-*]|\d+[.)])\s+", line)
    ]
    for line in bullet_lines[:12]:
        if line:
            tasks.append({"Title": line[:160], "Priority": "50", "Lane": "grey", "Rationale": "", "Command": "", "Risk": "review"})
    return tasks


def parse(path: Path = FROM_GREY) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    parsed = _extract_json(text)
    DECISIONS_JSON.write_text(json.dumps(parsed or {"raw_text": text}, indent=2, ensure_ascii=False), encoding="utf-8")
    tasks = _normalize_tasks(parsed, text)
    exists = TASKS_CSV.exists()
    TASKS_CSV.parent.mkdir(exist_ok=True)
    with TASKS_CSV.open("a", encoding="utf-8", newline="") as handle:
        fieldnames = ["Timestamp", "Source", "Priority", "Lane", "Title", "Rationale", "Command", "Risk", "Status"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        for task in tasks:
            writer.writerow(
                {
                    "Timestamp": _now(),
                    "Source": str(path),
                    "Priority": task.get("Priority", "50"),
                    "Lane": task.get("Lane", "grey"),
                    "Title": task.get("Title", ""),
                    "Rationale": task.get("Rationale", ""),
                    "Command": task.get("Command", ""),
                    "Risk": task.get("Risk", "review"),
                    "Status": "GREY_RECOMMENDED",
                }
            )
    return tasks


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(parse(), indent=2, ensure_ascii=False))
