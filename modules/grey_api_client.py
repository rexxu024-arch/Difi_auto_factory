"""Gemini API client for the Grey Memory Bridge.

The API key is read from config only and is never printed, logged, or committed.
"""

from __future__ import annotations

import json
import base64
import mimetypes
import sys
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config


class GreyApiError(RuntimeError):
    pass


def _key_for_tier(tier: str = "auto") -> str | None:
    tier = str(tier or "auto").lower()
    if tier == "paid":
        return Config.GEMINI_PAID_API_KEY or Config.GEMINI_API_KEY
    if tier == "free":
        return Config.GEMINI_FREE_API_KEY or Config.GEMINI_API_KEY
    return Config.GEMINI_FREE_API_KEY or Config.GEMINI_API_KEY or Config.GEMINI_PAID_API_KEY


def generate(prompt: str, *, model: str | None = None, timeout: int = 120, tier: str = "auto") -> dict:
    return _generate_parts([{"text": prompt}], model=model, timeout=timeout, tier=tier)


def generate_with_images(
    prompt: str,
    image_paths: list[str | Path],
    *,
    model: str | None = None,
    timeout: int = 180,
    tier: str = "auto",
) -> dict:
    parts: list[dict] = [{"text": prompt}]
    for image_path in image_paths:
        path = Path(image_path)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        if not path.exists():
            raise GreyApiError(f"IMAGE_NOT_FOUND: {path}")
        mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        parts.append({"inline_data": {"mime_type": mime_type, "data": data}})
    return _generate_parts(parts, model=model, timeout=timeout, tier=tier)


def _generate_parts(parts: list[dict], *, model: str | None = None, timeout: int = 120, tier: str = "auto") -> dict:
    api_key = _key_for_tier(tier)
    if not api_key:
        raise GreyApiError("MISSING_GEMINI_API_KEY")
    if model:
        model_name = model
    elif str(tier or "").lower() == "paid":
        model_name = Config.GEMINI_PAID_MODEL or Config.GEMINI_MODEL or "gemini-1.5-pro"
    elif str(tier or "").lower() == "free":
        model_name = Config.GEMINI_FREE_MODEL or Config.GEMINI_MODEL or "gemini-flash-latest"
    else:
        model_name = Config.GEMINI_MODEL or Config.GEMINI_FREE_MODEL or "gemini-flash-latest"
    url = f"{Config.GEMINI_BASE_URL.rstrip('/')}/models/{model_name}:generateContent"
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "X-goog-api-key": api_key,
        },
        json={
            "contents": [{"role": "user", "parts": parts}],
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
