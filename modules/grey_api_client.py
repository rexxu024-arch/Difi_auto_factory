"""Gemini API client for the Grey Memory Bridge.

The API key is read from config only and is never printed, logged, or committed.
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


class GreyApiError(RuntimeError):
    pass


def generate(prompt: str, *, model: str | None = None, timeout: int = 120) -> dict:
    if not Config.GEMINI_API_KEY:
        raise GreyApiError("MISSING_GEMINI_API_KEY")
    model_name = model or Config.GEMINI_MODEL or "gemini-flash-latest"
    url = f"{Config.GEMINI_BASE_URL.rstrip('/')}/models/{model_name}:generateContent"
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "X-goog-api-key": Config.GEMINI_API_KEY,
        },
        json={
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.35,
                "topP": 0.9,
                "maxOutputTokens": 4096,
            },
        },
        timeout=timeout,
    )
    try:
        payload = response.json()
    except Exception as exc:  # noqa: BLE001
        raise GreyApiError(f"NON_JSON_RESPONSE status={response.status_code}") from exc
    if not response.ok:
        message = json.dumps(payload, ensure_ascii=False)[:1000]
        raise GreyApiError(f"GEMINI_HTTP_{response.status_code}: {message}")
    return payload


def extract_text(payload: dict) -> str:
    chunks: list[str] = []
    for candidate in payload.get("candidates") or []:
        content = candidate.get("content") or {}
        for part in content.get("parts") or []:
            text = part.get("text")
            if text:
                chunks.append(str(text))
    return "\n".join(chunks).strip()
