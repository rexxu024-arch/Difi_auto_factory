"""Safe Gemini API smoke test for the Grey Memory Bridge.

This script never prints the API key. It only verifies that Config can read the
key and that Gemini returns a small response.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config


def run() -> dict:
    if not Config.GEMINI_API_KEY:
        return {
            "ok": False,
            "status": "MISSING_GEMINI_API_KEY",
            "detail": "Set GEMINI_API_KEY or Gemini_api_key in .env, then rerun.",
        }

    model = Config.GEMINI_MODEL or "gemini-flash-latest"
    url = f"{Config.GEMINI_BASE_URL.rstrip('/')}/models/{model}:generateContent"
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "X-goog-api-key": Config.GEMINI_API_KEY,
        },
        json={"contents": [{"parts": [{"text": "Reply exactly: OK"}]}]},
        timeout=60,
    )
    payload = response.json() if response.content else {}
    text = ""
    try:
        text = payload["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        text = ""
    return {
        "ok": response.ok and bool(text),
        "status_code": response.status_code,
        "model": model,
        "response_preview": text[:80],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False))
