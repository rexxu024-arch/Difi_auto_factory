"""Complete Etsy OAuth PKCE through the logged-in Edge browser.

This is a local credential bridge only. It does not create listings, change
billing, touch orders, or send messages.
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import sys
import threading
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import websockets

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.automation_browser import cdp_status, launch
from modules.etsy_auth import listen_callback, make_authorize_url, load_json
from config import Config

NY = ZoneInfo("America/New_York")
LOG_CSV = PROJECT_ROOT / "Database" / "Etsy_OAuth_Edge_Flow_Log.csv"
FIELDS = ["Timestamp", "Action", "Status", "Detail"]


def now_text() -> str:
    return datetime.now(NY).isoformat(timespec="seconds")


def append_log(action: str, status: str, detail: str = "") -> None:
    LOG_CSV.parent.mkdir(exist_ok=True)
    exists = LOG_CSV.exists()
    with LOG_CSV.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({"Timestamp": now_text(), "Action": action, "Status": status, "Detail": detail[:5000]})


def quote_url(url: str) -> str:
    return urllib.parse.quote(url, safe=":/?=&")


def http_json(url: str, method: str = "GET") -> dict:
    request = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(request, timeout=8) as response:
        return json.load(response)


def close_target(port: int, target_id: str | None) -> None:
    if not target_id:
        return
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/close/{target_id}", timeout=3).read()
    except Exception:
        pass


class ListenerThread(threading.Thread):
    def __init__(self, timeout: int):
        super().__init__(daemon=True)
        self.timeout = timeout
        self.error: str | None = None
        self.ok = False

    def run(self) -> None:
        try:
            listen_callback(timeout=self.timeout)
            self.ok = True
        except Exception as exc:  # noqa: BLE001 - durable log boundary
            self.error = str(exc)


class CdpPage:
    def __init__(self, port: int, url: str):
        self.port = port
        self.url = url
        self.target: dict | None = None
        self.ws = None
        self.seq = 0

    async def __aenter__(self) -> "CdpPage":
        self.target = http_json(f"http://127.0.0.1:{self.port}/json/new?{quote_url(self.url)}", method="PUT")
        self.ws = await websockets.connect(self.target["webSocketDebuggerUrl"], max_size=20_000_000)
        await self.send("Page.enable")
        await self.send("Runtime.enable")
        return self

    async def __aexit__(self, *_exc) -> None:
        if self.ws:
            await self.ws.close()
        close_target(self.port, (self.target or {}).get("id"))

    async def send(self, method: str, params: dict | None = None) -> dict:
        assert self.ws is not None
        self.seq += 1
        payload = {"id": self.seq, "method": method}
        if params is not None:
            payload["params"] = params
        await self.ws.send(json.dumps(payload))
        while True:
            data = json.loads(await self.ws.recv())
            if data.get("id") == self.seq:
                return data

    async def eval(self, expression: str, *, await_promise: bool = False) -> object:
        response = await self.send(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True, "awaitPromise": await_promise},
        )
        if response.get("result", {}).get("exceptionDetails"):
            return {"__exception__": response["result"]["exceptionDetails"].get("text", "Runtime exception")}
        return response.get("result", {}).get("result", {}).get("value")

    async def wait_body(self, seconds: int = 45) -> dict:
        snapshot: dict = {}
        for _ in range(seconds):
            value = await self.eval(
                r"""({url:location.href,title:document.title,text:(document.body&&document.body.innerText||'').slice(0,4000)})"""
            )
            if isinstance(value, dict):
                snapshot = value
                if len(value.get("text") or "") > 200:
                    return value
            await asyncio.sleep(1)
        return snapshot


async def authorize_in_edge(port: int, auth_url: str, timeout: int) -> dict:
    async with CdpPage(port, auth_url) as page:
        snapshot = await page.wait_body(seconds=timeout)
        append_log("AUTHORIZE_PAGE", "LOADED", json.dumps(snapshot, ensure_ascii=False))
        text = str(snapshot.get("text", ""))
        if "redirect_uri" in text and ("invalid" in text.lower() or "mismatch" in text.lower()):
            return {"ok": False, "status": "REDIRECT_URI_BLOCKED", "snapshot": snapshot}
        result = await page.eval(
            r"""(async () => {
              const words = ['Allow Access', 'Allow', 'Grant Access', 'Authorize', 'Connect', 'Continue'];
              const buttons = [...document.querySelectorAll('button,input[type=submit],a')]
                .filter(el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length));
              const button = buttons.find(el => words.some(w => ((el.innerText || el.value || el.getAttribute('aria-label') || '').trim()).includes(w)));
              if (!button) return {clicked:false, buttons: buttons.map(el => (el.innerText || el.value || el.getAttribute('aria-label') || '').trim()).filter(Boolean).slice(0,50), text:(document.body.innerText||'').slice(0,2000)};
              button.scrollIntoView({block:'center'});
              button.click();
              await new Promise(r => setTimeout(r, 2500));
              return {clicked:true, url:location.href, text:(document.body.innerText||'').slice(0,2000)};
            })()""",
            await_promise=True,
        )
        append_log("AUTHORIZE_CLICK", "CLICKED" if isinstance(result, dict) and result.get("clicked") else "NO_BUTTON", json.dumps(result, ensure_ascii=False))
        return result if isinstance(result, dict) else {"ok": False, "result": result}


async def run(port: int, timeout: int) -> int:
    if cdp_status(port).get("status") != "RUNNING":
        launch("edge", port, Path(r"C:\openclaw_edge_profile"), "about:blank", minimized=False)
    auth_url = make_authorize_url()
    listener = ListenerThread(timeout=timeout)
    listener.start()
    result = await authorize_in_edge(port, auth_url, timeout=min(timeout, 60))
    listener.join(timeout=timeout)
    token = load_json(Config.ETSY_TOKEN_FILE)
    status = {
        "authorize_result": result,
        "listener_ok": listener.ok,
        "listener_error": listener.error,
        "token_present": bool(token.get("access_token")),
        "refresh_present": bool(token.get("refresh_token")),
    }
    append_log("OAUTH_FLOW", "CONNECTED" if status["token_present"] else "FAILED", json.dumps(status, ensure_ascii=False))
    print(json.dumps({k: v for k, v in status.items() if k != "authorize_result"}, ensure_ascii=False, indent=2))
    return 0 if status["token_present"] else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Etsy OAuth in logged-in Edge.")
    parser.add_argument("--port", type=int, default=9223)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(run(args.port, args.timeout)))


if __name__ == "__main__":
    main()
