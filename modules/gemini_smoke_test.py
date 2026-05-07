"""Gemini API availability probe for the Grey Memory Bridge.

The probe never prints or stores the API key. It checks three layers:
1. Config can load a key from .env.
2. Google can authenticate the key by listing models.
3. At least one low-cost generateContent model can produce a tiny response.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config

STATUS_JSON = PROJECT_ROOT / "Database" / "Gemini_API_Status.json"
REPORT_MD = PROJECT_ROOT / "Review_Packets" / "Gemini_Bridge" / "GEMINI_API_TEST_REPORT_latest.md"

DEFAULT_MODELS = [
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.5-flash",
]


def _extract_text(payload: dict) -> str:
    chunks: list[str] = []
    for candidate in payload.get("candidates") or []:
        content = candidate.get("content") or {}
        for part in content.get("parts") or []:
            text = part.get("text")
            if text:
                chunks.append(str(text))
    return "\n".join(chunks).strip()


def _safe_error(payload: dict) -> dict:
    error = payload.get("error", payload)
    return {
        "code": error.get("code"),
        "status": error.get("status"),
        "message": str(error.get("message", ""))[:800],
    }


def _classify(out: dict) -> str:
    if not out.get("key_loaded"):
        return "NO_KEY_LOADED"
    if not out.get("model_list_ok"):
        return "KEY_INVALID_OR_MODEL_LIST_BLOCKED"
    if any(test.get("ok") for test in out.get("tests", [])):
        return "GENERATE_OK"
    messages = " ".join(str(test.get("error_message", "")) for test in out.get("tests", [])).lower()
    if "prepayment credits are depleted" in messages:
        return "KEY_VALID_BUT_NO_PREPAY_CREDITS"
    if any(test.get("status_code") == 429 for test in out.get("tests", [])):
        return "KEY_VALID_BUT_RATE_OR_QUOTA_BLOCKED"
    return "KEY_VALID_BUT_GENERATE_BLOCKED"


def _write_report(out: dict) -> None:
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Gemini API Test Report",
        "",
        f"- Timestamp: {out.get('timestamp')}",
        f"- Key loaded by config: {out.get('key_loaded')}",
        f"- Model list status: {out.get('model_list_status_code')} / ok={out.get('model_list_ok')}",
        f"- Final status: {out.get('status')}",
        "",
        "## Generate Tests",
        "",
    ]
    for test in out.get("tests", []):
        lines.append(
            f"- {test.get('model')}: status={test.get('status_code')} ok={test.get('ok')} elapsed={test.get('elapsed_sec')}s"
        )
        if test.get("error_status") or test.get("error_message"):
            lines.append(f"  - error: {test.get('error_status')} | {test.get('error_message')}")
        elif test.get("response_preview"):
            lines.append(f"  - response: {test.get('response_preview')}")
    lines.extend(
        [
            "",
            "## Operator Meaning",
            "",
            "- If status is GENERATE_OK, the Grey Memory Bridge can send real tasks.",
            "- If status is KEY_VALID_BUT_NO_PREPAY_CREDITS, the key is configured but Google billing/prepay must be fixed before generation works.",
            "- The probe intentionally stops at tiny requests and does not retry aggressively.",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def run() -> dict:
    base_url = Config.GEMINI_BASE_URL.rstrip("/")
    out = {
        "timestamp": datetime.now(ZoneInfo("America/New_York")).isoformat(),
        "key_loaded": bool(Config.GEMINI_API_KEY),
        "base_url": base_url,
        "model_list_status_code": None,
        "model_list_ok": False,
        "tests": [],
    }
    if not Config.GEMINI_API_KEY:
        out["status"] = _classify(out)
        return out

    try:
        list_response = requests.get(
            f"{base_url}/models",
            headers={"X-goog-api-key": Config.GEMINI_API_KEY},
            timeout=60,
        )
        out["model_list_status_code"] = list_response.status_code
        out["model_list_ok"] = list_response.ok
        if not list_response.ok:
            try:
                out["model_list_error"] = _safe_error(list_response.json())
            except Exception:
                out["model_list_error"] = {"message": "NON_JSON_MODEL_LIST_RESPONSE"}
    except Exception as exc:  # noqa: BLE001
        out["model_list_error"] = {"type": type(exc).__name__, "message": str(exc)[:300]}

    if out["model_list_ok"]:
        for model in DEFAULT_MODELS:
            started = time.time()
            item = {"model": model, "ok": False}
            try:
                response = requests.post(
                    f"{base_url}/models/{model}:generateContent",
                    headers={
                        "Content-Type": "application/json",
                        "X-goog-api-key": Config.GEMINI_API_KEY,
                    },
                    json={
                        "contents": [{"parts": [{"text": "Reply exactly OK"}]}],
                        "generationConfig": {"maxOutputTokens": 128, "temperature": 0},
                    },
                    timeout=60,
                )
                item["status_code"] = response.status_code
                item["elapsed_sec"] = round(time.time() - started, 2)
                try:
                    payload = response.json()
                except Exception:
                    payload = {}
                item["ok"] = response.ok
                if response.ok:
                    text = _extract_text(payload)
                    item["response_preview"] = str(text).strip()[:80]
                    item["text_found"] = bool(text)
                else:
                    error = _safe_error(payload)
                    item["error_status"] = error["status"]
                    item["error_message"] = error["message"]
            except Exception as exc:  # noqa: BLE001
                item["elapsed_sec"] = round(time.time() - started, 2)
                item["exception"] = type(exc).__name__
                item["error_message"] = str(exc)[:300]
            out["tests"].append(item)
            if item.get("ok"):
                break

    out["status"] = _classify(out)
    STATUS_JSON.parent.mkdir(parents=True, exist_ok=True)
    STATUS_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    _write_report(out)
    return out


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(run(), indent=2, ensure_ascii=False))
