"""Low-frequency Gemini web chat sync through the dedicated Edge profile.

This module is intentionally separate from the high-frequency Gemini API bridge.
The API bridge is the normal path. This web sync is only for daily strategic
handoff into Rex/Grey's persistent Gemini chat.

Write path safety:
- Default mode is dry-run.
- Marketplace/account Chrome is never used.
- Edge CDP is used only to open/focus the Gemini thread and the input box.
- Message text is written through the OS clipboard and submitted with OS-level
  keyboard events, not DOM value injection.
- If Rex is actively using the computer, execution waits/skips unless --force.
"""

from __future__ import annotations

import argparse
import csv
import ctypes
import json
import random
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import websockets

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import automation_browser, daily_sitrep_builder

try:
    import win32clipboard
    import win32con
    import win32gui
except Exception:  # pragma: no cover - Windows-only runtime dependency
    win32clipboard = None
    win32con = None
    win32gui = None


BRIDGE_DIR = PROJECT_ROOT / "Review_Packets" / "Gemini_Bridge"
CHAT_PAYLOAD = BRIDGE_DIR / "DAILY_SITREP_FOR_GEMINI_CHAT_latest.md"
CHAT_REPLY = BRIDGE_DIR / "FROM_GEMINI_CHAT_latest.md"
STATE_JSON = PROJECT_ROOT / "Database" / "Gemini_Chat_Sync_State.json"
RUN_LOG = PROJECT_ROOT / "Database" / "Gemini_Chat_Sync_Log.csv"

DEFAULT_CHAT_URL = "https://gemini.google.com/app/d2ab3afa2778aa9e"
DEFAULT_THREAD_NAME = "Codex 自动化矩阵升级计划"
DEFAULT_PORT = 9223
DEFAULT_MIN_IDLE_SECONDS = 120

SECRET_PATTERNS = [
    "AIza",
    "x-goog-api-key",
    "bearer ",
    "shared_secret",
    "password=",
    "access_token",
    "refresh_token",
]


@dataclass
class CdpPage:
    id: str
    url: str
    title: str
    websocket_url: str


def now_text() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")


def write_state(payload: dict) -> None:
    STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
    STATE_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def append_log(status: str, detail: str) -> None:
    exists = RUN_LOG.exists()
    RUN_LOG.parent.mkdir(exist_ok=True)
    with RUN_LOG.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        if not exists:
            writer.writerow(["Timestamp", "Status", "Detail"])
        writer.writerow([now_text(), status, detail[:1200]])


def get_idle_seconds() -> float:
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    info = LASTINPUTINFO()
    info.cbSize = ctypes.sizeof(info)
    if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(info)):
        return 0.0
    tick = ctypes.windll.kernel32.GetTickCount()
    return max(0.0, (tick - info.dwTime) / 1000.0)


def build_payload(include_free_tier_eval: bool = True) -> str:
    BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
    sitrep = daily_sitrep_builder.build()
    free_eval = ""
    eval_path = BRIDGE_DIR / "GEMINI_FREE_TIER_EVALUATION.md"
    if include_free_tier_eval and eval_path.exists():
        free_eval = eval_path.read_text(encoding="utf-8", errors="replace")
    grey_state = ""
    state_path = PROJECT_ROOT / "Database" / "Grey_Bridge_State.json"
    if state_path.exists():
        grey_state = state_path.read_text(encoding="utf-8", errors="replace")[:2500]
    text = "\n\n".join(
        part
        for part in [
            "[DAILY_SITREP_TO_GREY_CHAT]",
            f"Timestamp: {now_text()}",
            "Thread: Codex automation matrix upgrade plan",
            "Purpose: low-frequency strategic sync from Codex local factory to Grey/Gemini chat.",
            sitrep,
            "## Grey API Bridge State\n\n```json\n" + grey_state + "\n```" if grey_state else "",
            "## Gemini Free Tier Evaluation\n\n" + free_eval if free_eval else "",
            "## Request To Grey\n\nReview the current state at strategic level only. Return concise priorities, risks, and any correction. Do not request secrets. Do not suggest PPC/Priority ads. Do not exceed fee caps.",
        ]
        if part
    )
    validate_no_secret(text)
    CHAT_PAYLOAD.write_text(text, encoding="utf-8")
    return text


def validate_no_secret(text: str) -> None:
    lower = text.lower()
    for pattern in SECRET_PATTERNS:
        if pattern.lower() in lower:
            raise RuntimeError(f"Refusing to sync payload: possible secret marker `{pattern}`.")


def list_pages(port: int) -> list[CdpPage]:
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=5) as response:
        payload = json.load(response)
    pages = []
    for item in payload:
        if item.get("type") != "page":
            continue
        pages.append(
            CdpPage(
                id=str(item.get("id", "")),
                url=str(item.get("url", "")),
                title=str(item.get("title", "")),
                websocket_url=str(item.get("webSocketDebuggerUrl", "")),
            )
        )
    return pages


def ensure_edge(port: int, url: str) -> dict:
    status = automation_browser.cdp_status(port)
    if status["status"] == "RUNNING":
        return status
    return automation_browser.launch("edge", port, automation_browser.DEFAULT_PROFILE, url, minimized=False)


def get_or_open_thread(port: int, url: str, thread_name: str) -> CdpPage:
    pages = list_pages(port)
    for page in pages:
        if url in page.url or thread_name in page.title:
            return page
    encoded = urllib.parse.quote(url, safe="")
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/new?{encoded}", timeout=5) as response:
            payload = json.load(response)
        return CdpPage(
            id=str(payload.get("id", "")),
            url=str(payload.get("url", "")),
            title=str(payload.get("title", "")),
            websocket_url=str(payload.get("webSocketDebuggerUrl", "")),
        )
    except Exception:
        status = automation_browser.cdp_status(port)
        browser_ws = status.get("webSocketDebuggerUrl", "")
        if browser_ws:
            import asyncio

            asyncio.run(browser_cdp_call(browser_ws, "Target.createTarget", {"url": url}))
            time.sleep(4)
            pages = list_pages(port)
            for page in pages:
                if url in page.url or "gemini.google.com" in page.url:
                    return page
        automation_browser.launch("edge", port, automation_browser.DEFAULT_PROFILE, url, minimized=False)
        time.sleep(4)
        pages = list_pages(port)
        for page in pages:
            if url in page.url or "gemini.google.com" in page.url:
                return page
    raise RuntimeError("Could not open Gemini chat thread in Edge CDP.")


async def cdp_call(page: CdpPage, method: str, params: dict | None = None) -> dict:
    async with websockets.connect(page.websocket_url, max_size=20_000_000) as websocket:
        seq = 1

        async def send(method_name: str, method_params: dict | None = None) -> dict:
            nonlocal seq
            message = {"id": seq, "method": method_name}
            if method_params is not None:
                message["params"] = method_params
            await websocket.send(json.dumps(message))
            current = seq
            seq += 1
            while True:
                reply = json.loads(await websocket.recv())
                if reply.get("id") == current:
                    return reply

        return await send(method, params)


async def browser_cdp_call(browser_ws: str, method: str, params: dict | None = None) -> dict:
    async with websockets.connect(browser_ws, max_size=20_000_000) as websocket:
        message = {"id": 1, "method": method}
        if params is not None:
            message["params"] = params
        await websocket.send(json.dumps(message))
        while True:
            reply = json.loads(await websocket.recv())
            if reply.get("id") == 1:
                return reply


async def focus_gemini_input(page: CdpPage) -> dict:
    await cdp_call(page, "Page.bringToFront")
    expression = r"""
(() => {
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 10 && r.height > 10 && s.visibility !== 'hidden' && s.display !== 'none';
  };
  const selectors = [
    'rich-textarea div[contenteditable="true"]',
    'div[contenteditable="true"][role="textbox"]',
    'div[contenteditable="true"]',
    'textarea'
  ];
  for (const selector of selectors) {
    const elements = [...document.querySelectorAll(selector)].filter(visible);
    const el = elements[elements.length - 1];
    if (el) {
      el.scrollIntoView({block: 'center'});
      el.focus();
      return {ok: true, selector, title: document.title, url: location.href};
    }
  }
  return {ok: false, title: document.title, url: location.href, body: document.body.innerText.slice(0, 700)};
})()
"""
    reply = await cdp_call(
        page,
        "Runtime.evaluate",
        {"expression": expression, "returnByValue": True, "awaitPromise": False},
    )
    value = ((reply.get("result") or {}).get("result") or {}).get("value") or {}
    if not value.get("ok"):
        raise RuntimeError(f"Gemini input not found: {value}")
    return value


async def capture_latest_response(page: CdpPage, wait_seconds: int = 180) -> dict:
    expression = r"""
(() => {
  const selectors = [
    'message-content',
    'div[class*="model-response"]',
    'div[data-test-id*="response"]',
    'div.markdown',
    'div[class*="markdown"]'
  ];
  const candidates = [];
  for (const selector of selectors) {
    for (const el of document.querySelectorAll(selector)) {
      const text = (el.innerText || '').trim();
      const rect = el.getBoundingClientRect();
      if (text.length > 40 && rect.width > 50 && rect.height > 10) {
        candidates.push({selector, text, length: text.length});
      }
    }
  }
  candidates.sort((a, b) => a.length - b.length);
  const last = candidates[candidates.length - 1];
  const body = (document.body.innerText || '').trim();
  return {
    ok: !!last,
    title: document.title,
    url: location.href,
    selector: last ? last.selector : '',
    text: last ? last.text.slice(0, 12000) : body.slice(Math.max(0, body.length - 12000)),
    length: last ? last.length : body.length
  };
})()
"""
    deadline = time.time() + max(5, wait_seconds)
    last_value: dict = {}
    while time.time() < deadline:
        reply = await cdp_call(
            page,
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True, "awaitPromise": False},
        )
        value = ((reply.get("result") or {}).get("result") or {}).get("value") or {}
        last_value = value
        text = str(value.get("text") or "").strip()
        if value.get("ok") and len(text) > 80:
            CHAT_REPLY.write_text(text, encoding="utf-8")
            return {**value, "saved_to": str(CHAT_REPLY)}
        time.sleep(3)
    text = str(last_value.get("text") or "").strip()
    if text:
        CHAT_REPLY.write_text(text, encoding="utf-8")
        return {**last_value, "saved_to": str(CHAT_REPLY), "timed_out": True}
    return {"ok": False, "timed_out": True, "saved_to": ""}


def set_clipboard_text(text: str) -> None:
    if win32clipboard is None or win32con is None:
        raise RuntimeError("pywin32 clipboard modules are unavailable.")
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
    finally:
        win32clipboard.CloseClipboard()


def activate_edge_window(title_hint: str = "Gemini") -> bool:
    if win32gui is None:
        return False
    matches: list[int] = []

    def callback(hwnd: int, _: object) -> None:
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)
        if title_hint.lower() in title.lower() or "gemini" in title.lower():
            matches.append(hwnd)

    win32gui.EnumWindows(callback, None)
    if not matches:
        return False
    hwnd = matches[0]
    try:
        win32gui.ShowWindow(hwnd, 5)
        win32gui.SetForegroundWindow(hwnd)
        return True
    except Exception:
        return False


def press_key(vk: int, up: bool = False) -> None:
    flags = 0x0002 if up else 0
    ctypes.windll.user32.keybd_event(vk, 0, flags, 0)


def os_hotkey_ctrl_v_then_enter(text_length: int) -> None:
    vk_ctrl = 0x11
    vk_v = 0x56
    vk_enter = 0x0D
    press_key(vk_ctrl)
    time.sleep(random.uniform(0.02, 0.05))
    press_key(vk_v)
    time.sleep(random.uniform(0.01, 0.03))
    press_key(vk_v, up=True)
    press_key(vk_ctrl, up=True)
    sleep_time = 2.0 + random.uniform(0.5, 3.0) + (text_length / 1000.0) * 0.5
    time.sleep(sleep_time)
    press_key(vk_enter)
    time.sleep(random.uniform(0.2, 0.7))
    press_key(vk_enter, up=True)


def run(
    *,
    execute: bool = False,
    force: bool = False,
    port: int = DEFAULT_PORT,
    url: str = DEFAULT_CHAT_URL,
    thread_name: str = DEFAULT_THREAD_NAME,
    min_idle_seconds: int = DEFAULT_MIN_IDLE_SECONDS,
    wait_response_seconds: int = 180,
) -> dict:
    payload = build_payload()
    idle_seconds = get_idle_seconds()
    result = {
        "timestamp": now_text(),
        "execute": execute,
        "port": port,
        "url": url,
        "thread_name": thread_name,
        "payload_path": str(CHAT_PAYLOAD),
        "payload_chars": len(payload),
        "idle_seconds": round(idle_seconds, 1),
    }
    if not execute:
        result["status"] = "DRY_RUN_READY"
        write_state(result)
        append_log(result["status"], f"payload_chars={len(payload)}")
        return result
    if idle_seconds < min_idle_seconds and not force:
        result["status"] = "WAIT_USER_ACTIVE"
        result["detail"] = f"idle_seconds={idle_seconds:.1f} below min_idle_seconds={min_idle_seconds}"
        write_state(result)
        append_log(result["status"], result["detail"])
        return result
    edge_status = ensure_edge(port, url)
    page = get_or_open_thread(port, url, thread_name)
    import asyncio

    focus_result = asyncio.run(focus_gemini_input(page))
    set_clipboard_text(payload)
    foreground = activate_edge_window("Gemini")
    time.sleep(random.uniform(0.4, 1.2))
    os_hotkey_ctrl_v_then_enter(len(payload))
    response_result: dict = {}
    if wait_response_seconds > 0:
        response_result = asyncio.run(capture_latest_response(page, wait_seconds=wait_response_seconds))
    result.update(
        {
            "status": "SUBMITTED",
            "edge_status": edge_status.get("status"),
            "page_title": page.title,
            "focus_selector": focus_result.get("selector"),
            "foreground_activated": foreground,
            "response_saved_to": response_result.get("saved_to", ""),
            "response_ok": response_result.get("ok"),
            "response_selector": response_result.get("selector", ""),
        }
    )
    write_state(result)
    append_log(result["status"], f"chars={len(payload)} selector={focus_result.get('selector')}")
    return result


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Sync daily OpenClaw sitrep into Gemini Chat via Edge.")
    parser.add_argument("--execute", action="store_true", help="Actually paste and submit through Edge.")
    parser.add_argument("--force", action="store_true", help="Bypass idle check. Use only when Rex explicitly allows focus steal.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--url", default=DEFAULT_CHAT_URL)
    parser.add_argument("--thread-name", default=DEFAULT_THREAD_NAME)
    parser.add_argument("--min-idle-seconds", type=int, default=DEFAULT_MIN_IDLE_SECONDS)
    parser.add_argument("--wait-response-seconds", type=int, default=180)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                execute=args.execute,
                force=args.force,
                port=args.port,
                url=args.url,
                thread_name=args.thread_name,
                min_idle_seconds=args.min_idle_seconds,
                wait_response_seconds=args.wait_response_seconds,
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
