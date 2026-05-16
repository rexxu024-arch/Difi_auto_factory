"""Apply the Etsy shop shell through the logged-in Edge UI.

This module deliberately avoids payment, order, message, and ad settings. It
only touches shop appearance/copy fields that Rex already approved for the
Option 02 / Quiet Relic Studio shell.
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import sys
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

NY = ZoneInfo("America/New_York")
DATABASE = PROJECT_ROOT / "Database"
LOG_CSV = DATABASE / "Etsy_Shop_Shell_Apply_Log.csv"
BRAND_SHELL = DATABASE / "Etsy_brand_shell.md"
INFO_URL = "https://www.etsy.com/your/shops/me?ref=seller-platform-mcnav"
SHOP_BASICS_URL = "https://www.etsy.com/your/shops/me/settings/your-shop/shop-basics?ref=seller-platform-mcnav"
SHOP_HOME_EDITOR_URL = "https://www.etsy.com/shop/me/edit"
SHOP_NAME = "QuietRelicStudio"
LOGO_PATH = PROJECT_ROOT / "Output" / "Brand" / "Etsy" / "20260504_180120" / "previews" / "Option_02_shop_icon_500.png"
BANNER_PATH = PROJECT_ROOT / "Output" / "Brand" / "Etsy" / "20260504_180120" / "previews" / "Option_02_big_banner_1600x400.png"


FIELDS = ["Timestamp", "Action", "Status", "URL", "Detail"]


SHOP_ANNOUNCEMENT = (
    "Quiet Relic Studio creates small-batch wall art, acrylic display objects, "
    "and printable study-room pieces inspired by jade textures, scholar rooms, "
    "quiet ritual objects, kintsugi detail, and wabi-sabi calm. Each physical "
    "piece is produced on demand through trusted production partners."
)

BUYER_NOTE = (
    "Thank you for ordering from Quiet Relic Studio. Physical items are made "
    "on demand through a production partner, so small color or finish "
    "differences can happen between screen previews and the final piece. If a "
    "production issue arrives, please send clear photos so it can be reviewed."
)

DIGITAL_BUYER_NOTE = (
    "Thank you for choosing a Quiet Relic Studio digital download. No physical "
    "item will be shipped for digital listings. Your files are prepared for "
    "personal use and may not be resold, redistributed, or used as a competing "
    "commercial file set."
)

TAGLINE = "Quiet luxury jade art and study room decor"

ABOUT_TEXT = (
    "Quiet Relic Studio is a small-batch visual object shop for readers, desk "
    "dwellers, and quiet-room aesthetes. The collection blends dark academia, "
    "zen minimalism, jade mineral textures, kintsugi repair, and surreal object "
    "design into wall art, acrylic display pieces, and printable decor. Physical "
    "items are produced on demand rather than mass stocked; digital pieces are "
    "curated and prepared as downloadable print files."
)


def js_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def now_text() -> str:
    return datetime.now(NY).isoformat(timespec="seconds")


def append_log(action: str, status: str, url: str = "", detail: str = "") -> None:
    LOG_CSV.parent.mkdir(exist_ok=True)
    exists = LOG_CSV.exists()
    with LOG_CSV.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow(
            {
                "Timestamp": now_text(),
                "Action": action,
                "Status": status,
                "URL": url,
                "Detail": detail[:6000],
            }
        )


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
        await self.wait_ready()
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
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": await_promise,
            },
        )
        if response.get("result", {}).get("exceptionDetails"):
            return {
                "__exception__": response["result"]["exceptionDetails"].get("text", "Runtime exception"),
                "__raw__": response["result"]["exceptionDetails"],
            }
        result = response.get("result", {}).get("result", {})
        return result.get("value")

    async def wait_ready(self) -> None:
        for _ in range(45):
            value = await self.eval("({ready:document.readyState,len:(document.body&&document.body.innerText||'').length,url:location.href})")
            if isinstance(value, dict) and value.get("len", 0) > 300 and value.get("ready") in {"interactive", "complete"}:
                return
            await asyncio.sleep(1)

    async def wait_for(self, expression: str, seconds: int = 45) -> bool:
        for _ in range(seconds):
            value = await self.eval(expression)
            if value:
                return True
            await asyncio.sleep(1)
        return False

    async def set_file_input(self, selector: str, file_path: Path) -> bool:
        doc = await self.send("DOM.getDocument", {"depth": -1, "pierce": True})
        root_id = doc.get("result", {}).get("root", {}).get("nodeId")
        if not root_id:
            return False
        node = await self.send("DOM.querySelector", {"nodeId": root_id, "selector": selector})
        node_id = node.get("result", {}).get("nodeId")
        if not node_id:
            return False
        await self.send("DOM.setFileInputFiles", {"nodeId": node_id, "files": [str(file_path)]})
        return True


async def apply_info_page(port: int, dry_run: bool = False) -> bool:
    async with CdpPage(port, INFO_URL) as page:
        before = await page.eval(
            r"""(() => ({
              url: location.href,
              title: document.title,
              text: (document.body&&document.body.innerText||'').slice(0,2000),
              fields: {
                announcement: document.querySelector('#shop-announcement')?.value || '',
                sale: document.querySelector('#shop-sale-message')?.value || '',
                digital: document.querySelector('#digital-shop-sale-message')?.value || ''
              }
            }))()"""
        )
        if not isinstance(before, dict) or "Info & Appearance" not in str(before.get("text", "")):
            append_log("INFO_PAGE_TEXT", "LOGIN_OR_PAGE_UNEXPECTED", str(before.get("url", "")), json.dumps(before, ensure_ascii=False))
            return False
        if dry_run:
            append_log("INFO_PAGE_TEXT", "DRY_RUN_READY", str(before.get("url", "")), json.dumps(before.get("fields", {}), ensure_ascii=False))
            return True
        payload = json.dumps(
            {
                "announcement": SHOP_ANNOUNCEMENT,
                "sale": BUYER_NOTE,
                "digital": DIGITAL_BUYER_NOTE,
            },
            ensure_ascii=False,
        )
        result = await page.eval(
            rf"""(async () => {{
              const payload = {payload};
              const setValue = (selector, value) => {{
                const el = document.querySelector(selector);
                if (!el) return false;
                el.focus();
                el.value = value;
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return true;
              }};
              const ok = [
                setValue('#shop-announcement', payload.announcement),
                setValue('#shop-sale-message', payload.sale),
                setValue('#digital-shop-sale-message', payload.digital),
              ];
              const submit = [...document.querySelectorAll('input[type=submit],button')].find(el => ((el.value || el.innerText || '').trim()).includes('Save Changes'));
              if (!submit) return {{ ok, clicked: false, reason: 'no_save_button' }};
              submit.click();
              await new Promise(r => setTimeout(r, 4500));
              return {{
                ok,
                clicked: true,
                url: location.href,
                title: document.title,
                text: (document.body&&document.body.innerText||'').slice(0,1200),
                fields: {{
                  announcement: document.querySelector('#shop-announcement')?.value || '',
                  sale: document.querySelector('#shop-sale-message')?.value || '',
                  digital: document.querySelector('#digital-shop-sale-message')?.value || ''
                }}
              }};
            }})()""",
            await_promise=True,
        )
        success = isinstance(result, dict) and all(result.get("ok") or []) and result.get("clicked")
        append_log("INFO_PAGE_TEXT", "UPDATED" if success else "FAILED", INFO_URL, json.dumps(result, ensure_ascii=False))
        if success:
            return True
    verified = await verify_info_page(port)
    append_log(
        "INFO_PAGE_TEXT",
        "UPDATED_VERIFIED_AFTER_NAVIGATION" if verified else "FAILED_VERIFY_AFTER_NAVIGATION",
        INFO_URL,
        "",
    )
    return verified


async def verify_info_page(port: int) -> bool:
    async with CdpPage(port, INFO_URL) as page:
        fields = await page.eval(
            r"""(() => ({
              announcement: document.querySelector('#shop-announcement')?.value || '',
              sale: document.querySelector('#shop-sale-message')?.value || '',
              digital: document.querySelector('#digital-shop-sale-message')?.value || ''
            }))()"""
        )
    return (
        isinstance(fields, dict)
        and fields.get("announcement") == SHOP_ANNOUNCEMENT
        and fields.get("sale") == BUYER_NOTE
        and fields.get("digital") == DIGITAL_BUYER_NOTE
    )


async def click_section_action(page: CdpPage, section_id: str, action_text: str | None = None) -> dict:
    return await page.eval(
        rf"""(() => {{
          const section = document.querySelector({js_string('#' + section_id)});
          if (!section) return {{ clicked: false, reason: 'missing_section' }};
          const candidates = [...section.querySelectorAll('button,clg-button,clg-text-button,[role="button"]')]
            .filter(el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length));
          const wanted = {js_string(action_text or '')};
          const el = wanted
            ? candidates.find(e => ((e.innerText || e.getAttribute('aria-label') || '').trim()).includes(wanted))
            : candidates[0];
          if (!el) return {{ clicked: false, reason: 'missing_action', actions: candidates.map(e => (e.innerText || e.getAttribute('aria-label') || '').trim()) }};
          el.scrollIntoView({{block:'center'}});
          el.click();
          return {{ clicked: true, section: {js_string(section_id)}, action: (el.innerText || el.getAttribute('aria-label') || '').trim() }};
        }})()""",
        await_promise=False,
    )


async def save_visible_editor(page: CdpPage) -> dict:
    return await page.eval(
        r"""(async () => {
          const buttons = [...document.querySelectorAll('button,clg-button,clg-text-button,[role="button"],input[type=submit]')]
            .filter(el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length));
          const save = buttons.find(el => {
            const text = ((el.innerText || el.value || el.getAttribute('aria-label') || '').trim()).toLowerCase();
            return text === 'save' || text === 'save changes' || text.includes('save');
          });
          if (!save) return {saved:false, reason:'missing_save', buttons:buttons.map(el => (el.innerText || el.value || el.getAttribute('aria-label') || '').trim()).slice(0,40)};
          save.scrollIntoView({block:'center'});
          save.click();
          await new Promise(r => setTimeout(r, 3500));
          return {saved:true, url:location.href, text:(document.body.innerText||'').slice(0,1500)};
        })()""",
        await_promise=True,
    )


async def apply_text_section(port: int, section_id: str, action_text: str, value: str, verify_text: str) -> bool:
    async with CdpPage(port, SHOP_BASICS_URL) as page:
        ready = await page.wait_for(rf"!!document.querySelector({js_string('#' + section_id)})", seconds=60)
        if not ready:
            snapshot = await page.eval(r"""({url:location.href,title:document.title,text:(document.body.innerText||'').slice(0,2000)})""")
            append_log(f"SHOP_BASICS_{section_id}", "FAILED_SECTION_TIMEOUT", SHOP_BASICS_URL, json.dumps(snapshot, ensure_ascii=False))
            return False
        clicked = await click_section_action(page, section_id, action_text)
        if not isinstance(clicked, dict) or not clicked.get("clicked"):
            append_log(f"SHOP_BASICS_{section_id}", "FAILED_CLICK", SHOP_BASICS_URL, json.dumps(clicked, ensure_ascii=False))
            return False
        await asyncio.sleep(1.2)
        filled = await page.eval(
            rf"""(() => {{
              const section = document.querySelector({js_string('#' + section_id)});
              const scope = section || document;
              const fields = [...scope.querySelectorAll('input:not([type=file]),textarea,clg-text-input,clg-textarea,[contenteditable="true"]')]
                .filter(el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length));
              const el = fields.find(e => (e.tagName === 'TEXTAREA') || (e.tagName === 'INPUT') || e.tagName.startsWith('CLG-') || e.getAttribute('contenteditable') === 'true') || fields[0];
              if (!el) return {{ filled:false, reason:'missing_field', html:(scope.outerHTML||'').slice(0,1200) }};
              el.focus();
              const value = {js_string(value)};
              const inner = el.shadowRoot?.querySelector('input,textarea');
              if (el.getAttribute('contenteditable') === 'true') {{
                el.innerText = value;
              }} else if (inner) {{
                inner.value = value;
                inner.dispatchEvent(new Event('input', {{ bubbles:true, composed:true }}));
                inner.dispatchEvent(new Event('change', {{ bubbles:true, composed:true }}));
              }} else {{
                el.value = value;
                el.setAttribute('value', value);
              }}
              el.dispatchEvent(new Event('input', {{ bubbles:true, composed:true }}));
              el.dispatchEvent(new Event('change', {{ bubbles:true, composed:true }}));
              el.dispatchEvent(new KeyboardEvent('keyup', {{ bubbles:true, composed:true, key:'a' }}));
              return {{ filled:true, tag:el.tagName, section:{js_string(section_id)}, value }};
            }})()"""
        )
        if not isinstance(filled, dict) or not filled.get("filled"):
            append_log(f"SHOP_BASICS_{section_id}", "FAILED_FILL", SHOP_BASICS_URL, json.dumps(filled, ensure_ascii=False))
            return False
        saved = await save_visible_editor(page)
        await asyncio.sleep(1.0)
        verified = await page.eval(
            rf"""(() => {{
              const section = document.querySelector({js_string('#' + section_id)});
              const text = (section?.innerText || document.body.innerText || '');
              return {{ ok: text.includes({js_string(verify_text)}), text: text.slice(0,800), saved: {json.dumps(saved, ensure_ascii=False)} }};
            }})()"""
        )
        ok = isinstance(verified, dict) and verified.get("ok")
        append_log(f"SHOP_BASICS_{section_id}", "UPDATED" if ok else "FAILED_VERIFY", SHOP_BASICS_URL, json.dumps(verified, ensure_ascii=False))
        return bool(ok)


async def apply_tagline_section(port: int) -> bool:
    async with CdpPage(port, SHOP_BASICS_URL) as page:
        ready = await page.wait_for("!!document.querySelector('#shopTagline')", seconds=60)
        if not ready:
            snapshot = await page.eval(r"""({url:location.href,title:document.title,text:(document.body.innerText||'').slice(0,2000)})""")
            append_log("SHOP_BASICS_shopTagline", "FAILED_SECTION_TIMEOUT", SHOP_BASICS_URL, json.dumps(snapshot, ensure_ascii=False))
            return False
        section_text = await page.eval("(document.querySelector('#shopTagline')?.innerText || '')")
        if isinstance(section_text, str) and TAGLINE in section_text:
            append_log("SHOP_BASICS_shopTagline", "ALREADY_SET", SHOP_BASICS_URL, section_text[:500])
            return True
        action = "Edit" if isinstance(section_text, str) and "Edit" in section_text else "Add"
        clicked = await click_section_action(page, "shopTagline", action)
        if not isinstance(clicked, dict) or not clicked.get("clicked"):
            append_log("SHOP_BASICS_shopTagline", "FAILED_CLICK", SHOP_BASICS_URL, json.dumps(clicked, ensure_ascii=False))
            return False
        await asyncio.sleep(1.2)
        rect = await page.eval(
            r"""(() => {
              const el = document.querySelector('#shopTagline clg-text-input, #shopTagline input');
              if (!el) return null;
              const r = el.getBoundingClientRect();
              return {x:r.left + r.width/2, y:r.top + r.height/2, width:r.width, height:r.height};
            })()"""
        )
        if not isinstance(rect, dict):
            append_log("SHOP_BASICS_shopTagline", "FAILED_INPUT_RECT", SHOP_BASICS_URL, json.dumps(rect, ensure_ascii=False))
            return False
        await page.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": rect["x"], "y": rect["y"], "button": "left", "clickCount": 1})
        await page.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": rect["x"], "y": rect["y"], "button": "left", "clickCount": 1})
        await asyncio.sleep(0.3)
        await page.send("Input.dispatchKeyEvent", {"type": "keyDown", "modifiers": 2, "windowsVirtualKeyCode": 65, "code": "KeyA", "key": "a"})
        await page.send("Input.dispatchKeyEvent", {"type": "keyUp", "modifiers": 2, "windowsVirtualKeyCode": 65, "code": "KeyA", "key": "a"})
        await page.send("Input.insertText", {"text": TAGLINE})
        await asyncio.sleep(0.8)
        saved = await save_visible_editor(page)
        await asyncio.sleep(1.2)
        verified = await page.eval(
            rf"""(() => {{
              const section = document.querySelector('#shopTagline');
              const text = (section?.innerText || document.body.innerText || '');
              return {{ ok: text.includes({js_string(TAGLINE)}), text: text.slice(0,700), saved: {json.dumps(saved, ensure_ascii=False)} }};
            }})()"""
        )
        ok = isinstance(verified, dict) and verified.get("ok")
        append_log("SHOP_BASICS_shopTagline", "UPDATED" if ok else "FAILED_VERIFY", SHOP_BASICS_URL, json.dumps(verified, ensure_ascii=False))
        return bool(ok)


async def apply_shop_name_section(port: int) -> bool:
    async with CdpPage(port, SHOP_BASICS_URL) as page:
        ready = await page.wait_for("!!document.querySelector('#shopName')", seconds=60)
        if not ready:
            append_log("SHOP_BASICS_shopName", "FAILED_SECTION_TIMEOUT", SHOP_BASICS_URL, "")
            return False
        section_text = await page.eval("(document.querySelector('#shopName')?.innerText || '')")
        if isinstance(section_text, str) and SHOP_NAME in section_text:
            append_log("SHOP_BASICS_shopName", "ALREADY_SET", SHOP_BASICS_URL, section_text[:500])
            return True
        if isinstance(section_text, str) and "Save" not in section_text:
            clicked = await click_section_action(page, "shopName", "Edit")
            if not isinstance(clicked, dict) or not clicked.get("clicked"):
                append_log("SHOP_BASICS_shopName", "FAILED_CLICK", SHOP_BASICS_URL, json.dumps(clicked, ensure_ascii=False))
                return False
            await asyncio.sleep(1.2)
        rect = await page.eval(
            rf"""(() => {{
              const section = document.querySelector('#shopName');
              const el = section?.querySelector('clg-text-input,input:not([type=file])');
              if (!el) return {{ok:false, html:(section?.outerHTML||'').slice(0,1600)}};
              const inner = el.shadowRoot?.querySelector('input,textarea');
              const target = inner || el;
              target.focus();
              target.select?.();
              const r = target.getBoundingClientRect();
              return {{
                ok:true,
                before: target.value || el.value || el.getAttribute('value') || '',
                x:r.left + r.width/2,
                y:r.top + r.height/2,
                width:r.width,
                height:r.height,
                tag:el.tagName
              }};
            }})()"""
        )
        if not isinstance(rect, dict) or not rect.get("ok"):
            append_log("SHOP_BASICS_shopName", "FAILED_INPUT_RECT", SHOP_BASICS_URL, json.dumps(rect, ensure_ascii=False))
            return False
        await page.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": rect["x"], "y": rect["y"], "button": "left", "clickCount": 1})
        await page.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": rect["x"], "y": rect["y"], "button": "left", "clickCount": 1})
        await asyncio.sleep(0.25)
        await page.send("Input.dispatchKeyEvent", {"type": "keyDown", "modifiers": 2, "windowsVirtualKeyCode": 65, "code": "KeyA", "key": "a"})
        await page.send("Input.dispatchKeyEvent", {"type": "keyUp", "modifiers": 2, "windowsVirtualKeyCode": 65, "code": "KeyA", "key": "a"})
        await asyncio.sleep(0.15)
        await page.send("Input.insertText", {"text": SHOP_NAME})
        await asyncio.sleep(0.7)
        filled = await page.eval(
            r"""(() => {
              const section = document.querySelector('#shopName');
              const el = section?.querySelector('clg-text-input,input:not([type=file])');
              const inner = el?.shadowRoot?.querySelector('input,textarea');
              const target = inner || el;
              target?.dispatchEvent(new Event('input', { bubbles:true, composed:true }));
              target?.dispatchEvent(new Event('change', { bubbles:true, composed:true }));
              el?.dispatchEvent(new Event('input', { bubbles:true, composed:true }));
              el?.dispatchEvent(new Event('change', { bubbles:true, composed:true }));
              return {
                filled: !!target,
                value: target?.value || '',
                hostValue: el?.value || el?.getAttribute('value') || '',
                html:(section?.outerHTML||'').slice(0,1600)
              };
            })()"""
        )
        if not isinstance(filled, dict) or filled.get("value") != SHOP_NAME:
            append_log("SHOP_BASICS_shopName", "FAILED_FILL", SHOP_BASICS_URL, json.dumps({"rect": rect, "filled": filled}, ensure_ascii=False))
            return False
        await asyncio.sleep(0.8)
        saved = await save_visible_editor(page)
        await asyncio.sleep(2.0)
        verified = await page.eval(
            rf"""(() => {{
              const pageText = document.body.innerText || '';
              const section = document.querySelector('#shopName');
              const text = (section?.innerText || pageText || '');
              return {{ ok: text.includes({js_string(SHOP_NAME)}), text: text.slice(0,1000), pageText: pageText.slice(0,1600), saved: {json.dumps(saved, ensure_ascii=False)} }};
            }})()"""
        )
        ok = isinstance(verified, dict) and verified.get("ok")
        status = "UPDATED" if ok else "FAILED_VERIFY_OR_NAME_UNAVAILABLE"
        append_log("SHOP_BASICS_shopName", status, SHOP_BASICS_URL, json.dumps(verified, ensure_ascii=False))
        return bool(ok)


async def apply_logo_section(port: int) -> bool:
    if not LOGO_PATH.exists():
        append_log("SHOP_BASICS_shopIcon", "FAILED_MISSING_LOGO_FILE", SHOP_BASICS_URL, str(LOGO_PATH))
        return False
    async with CdpPage(port, SHOP_BASICS_URL) as page:
        ready = await page.wait_for("!!document.querySelector('#shopIcon')", seconds=60)
        if not ready:
            append_log("SHOP_BASICS_shopIcon", "FAILED_SECTION_TIMEOUT", SHOP_BASICS_URL, "")
            return False
        clicked = await click_section_action(page, "shopIcon", "Edit")
        if not isinstance(clicked, dict) or not clicked.get("clicked"):
            append_log("SHOP_BASICS_shopIcon", "FAILED_CLICK", SHOP_BASICS_URL, json.dumps(clicked, ensure_ascii=False))
            return False
        await asyncio.sleep(1.2)
        removed = await page.eval(
            r"""(() => {
              const section = document.querySelector('#shopIcon');
              const remove = [...section.querySelectorAll('button,clg-button,clg-text-button,[role="button"]')]
                .find(el => ((el.innerText || el.getAttribute('aria-label') || '').trim()).includes('Remove'));
              if (remove) { remove.click(); return true; }
              return false;
            })()"""
        )
        await asyncio.sleep(1.2)
        has_input = await page.wait_for("!!document.querySelector('#shopIcon input[type=file], input[type=file][accept*=image]')", seconds=8)
        if not has_input:
            await click_section_action(page, "shopIcon", "Cancel")
            append_log("SHOP_BASICS_shopIcon", "FAILED_NO_FILE_INPUT_AFTER_EDIT", SHOP_BASICS_URL, json.dumps({"removed": removed}, ensure_ascii=False))
            return False
        uploaded = await page.set_file_input("#shopIcon input[type=file], input[type=file][accept*=image]", LOGO_PATH)
        await asyncio.sleep(2.5)
        if not uploaded:
            await click_section_action(page, "shopIcon", "Cancel")
            append_log("SHOP_BASICS_shopIcon", "FAILED_SET_FILE", SHOP_BASICS_URL, str(LOGO_PATH))
            return False
        saved = await save_visible_editor(page)
        await asyncio.sleep(2.5)
        verified = await page.eval(
            rf"""(() => {{
              const section = document.querySelector('#shopIcon');
              return {{
                ok: !!section && (section.innerText || '').includes('Edit'),
                text: (section?.innerText || '').slice(0,700),
                imgs: [...(section?.querySelectorAll('img') || [])].map(img => img.src).slice(0,5),
                saved: {json.dumps(saved, ensure_ascii=False)}
              }};
            }})()"""
        )
        ok = isinstance(verified, dict) and verified.get("ok")
        append_log("SHOP_BASICS_shopIcon", "UPDATED" if ok else "FAILED_VERIFY", SHOP_BASICS_URL, json.dumps(verified, ensure_ascii=False))
        return bool(ok)


async def apply_about_section(port: int) -> bool:
    async with CdpPage(port, SHOP_BASICS_URL) as page:
        ready = await page.wait_for("!!document.querySelector('#shopStory')", seconds=60)
        if not ready:
            snapshot = await page.eval(r"""({url:location.href,title:document.title,text:(document.body.innerText||'').slice(0,2000)})""")
            append_log("SHOP_BASICS_shopStory", "FAILED_SECTION_TIMEOUT", SHOP_BASICS_URL, json.dumps(snapshot, ensure_ascii=False))
            return False
        section_text = await page.eval("(document.querySelector('#shopStory')?.innerText || '')")
        if isinstance(section_text, str) and "Quiet Relic Studio is a small-batch visual object shop" in section_text:
            append_log("SHOP_BASICS_shopStory", "ALREADY_SET", SHOP_BASICS_URL, section_text[:500])
            return True
        action = "Edit" if isinstance(section_text, str) and "Edit" in section_text else "Add"
        clicked = await click_section_action(page, "shopStory", action)
        if not isinstance(clicked, dict) or not clicked.get("clicked"):
            append_log("SHOP_BASICS_shopStory", "FAILED_CLICK", SHOP_BASICS_URL, json.dumps(clicked, ensure_ascii=False))
            return False
        await asyncio.sleep(1.2)
        filled = await page.eval(
            rf"""(() => {{
              const section = document.querySelector('#shopStory');
              const setField = (el, value) => {{
                if (!el) return false;
                el.focus?.();
                const inner = el.shadowRoot?.querySelector('input,textarea');
                if (inner) {{
                  inner.value = value;
                  inner.dispatchEvent(new Event('input', {{ bubbles:true, composed:true }}));
                  inner.dispatchEvent(new Event('change', {{ bubbles:true, composed:true }}));
                }}
                if ('value' in el) el.value = value;
                el.setAttribute('value', value);
                el.dispatchEvent(new Event('input', {{ bubbles:true, composed:true }}));
                el.dispatchEvent(new Event('change', {{ bubbles:true, composed:true }}));
                el.dispatchEvent(new KeyboardEvent('keyup', {{ bubbles:true, composed:true, key:'a' }}));
                return true;
              }};
              const fields = [...section.querySelectorAll('input:not([type=file]),textarea,clg-text-input,clg-textarea,[contenteditable="true"]')]
                .filter(el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length));
              const headline = fields.find(el => el.getAttribute('name') === 'storyHeadline') || fields[0];
              const body = fields.find(el => el.getAttribute('name') === 'story') || fields.find(el => el.tagName === 'TEXTAREA' || el.tagName === 'CLG-TEXTAREA') || fields[1];
              return {{
                headline: setField(headline, 'Quiet Relic Studio'),
                body: setField(body, {js_string(ABOUT_TEXT)}),
                fields: fields.map(el => ({{tag:el.tagName,name:el.getAttribute('name'),type:el.getAttribute('type'),value:el.value||el.getAttribute('value')||''}})),
                html: section.outerHTML.slice(0,1500)
              }};
            }})()"""
        )
        if not isinstance(filled, dict) or not filled.get("headline") or not filled.get("body"):
            append_log("SHOP_BASICS_shopStory", "FAILED_FILL", SHOP_BASICS_URL, json.dumps(filled, ensure_ascii=False))
            return False
        saved = await save_visible_editor(page)
        await asyncio.sleep(1.0)
        verified = await page.eval(
            rf"""(() => {{
              const section = document.querySelector('#shopStory');
              const text = (section?.innerText || document.body.innerText || '');
              return {{ ok: text.includes('Quiet Relic Studio') || text.includes('small-batch visual object shop'), text: text.slice(0,1000), saved: {json.dumps(saved, ensure_ascii=False)} }};
            }})()"""
        )
        ok = isinstance(verified, dict) and verified.get("ok")
        append_log("SHOP_BASICS_shopStory", "UPDATED" if ok else "FAILED_VERIFY", SHOP_BASICS_URL, json.dumps(verified, ensure_ascii=False))
        return bool(ok)


async def probe_asset_section(port: int, section_id: str, action_text: str) -> dict:
    async with CdpPage(port, SHOP_BASICS_URL) as page:
        await page.wait_for(rf"!!document.querySelector({js_string('#' + section_id)})", seconds=60)
        clicked = await click_section_action(page, section_id, action_text)
        await asyncio.sleep(1.5)
        result = await page.eval(
            rf"""(() => ({{
              clicked: {json.dumps(clicked, ensure_ascii=False)},
              url: location.href,
              text: (document.body.innerText || '').slice(0,3000),
              inputs: [...document.querySelectorAll('input')].map((e,i)=>({{i,type:e.type,accept:e.accept,multiple:e.multiple,visible:!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length),name:e.name,id:e.id}})).slice(0,60),
              buttons: [...document.querySelectorAll('button,clg-button,clg-text-button,[role="button"]')].map((e,i)=>({{i,tag:e.tagName,text:(e.innerText||e.getAttribute('aria-label')||'').trim(),visible:!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length)}})).filter(x=>x.visible).slice(0,80)
            }}))()"""
        )
        append_log(f"SHOP_BASICS_{section_id}_ASSET_PROBE", "PROBED", SHOP_BASICS_URL, json.dumps(result, ensure_ascii=False))
        return result if isinstance(result, dict) else {}


async def probe_shop_basics(port: int) -> dict:
    async with CdpPage(port, SHOP_BASICS_URL) as page:
        await page.wait_for("!!document.querySelector('#shopName')", seconds=60)
        result = await page.eval(
            r"""(() => ({
              url: location.href,
              title: document.title,
              text: (document.body&&document.body.innerText||'').slice(0,4000),
              buttons: [...document.querySelectorAll('button')].map((b,i)=>({i,text:(b.innerText||b.getAttribute('aria-label')||'').trim(),disabled:b.disabled,visible:!!(b.offsetWidth||b.offsetHeight||b.getClientRects().length)})).filter(x=>x.visible&&x.text).slice(0,80),
              links: [...document.querySelectorAll('a')].map((a,i)=>({i,text:(a.innerText||a.getAttribute('aria-label')||'').trim(),href:a.href,visible:!!(a.offsetWidth||a.offsetHeight||a.getClientRects().length)})).filter(x=>x.visible&&(x.text||x.href)).slice(0,80)
            }))()"""
        )
        append_log("SHOP_BASICS_PROBE", "PROBED", SHOP_BASICS_URL, json.dumps(result, ensure_ascii=False))
        return result if isinstance(result, dict) else {}


async def run(port: int, dry_run: bool = False, probe_assets: bool = False) -> int:
    if cdp_status(port).get("status") != "RUNNING":
        launch("edge", port, Path(r"C:\openclaw_edge_profile"), "about:blank", minimized=False)
    info_ok = await apply_info_page(port, dry_run=dry_run)
    shop_name_ok = False
    tagline_ok = False
    about_ok = False
    logo_ok = False
    asset_probes: dict[str, dict] = {}
    if not dry_run:
        shop_name_ok = await apply_shop_name_section(port)
        tagline_ok = await apply_tagline_section(port)
        about_ok = await apply_about_section(port)
        logo_ok = await apply_logo_section(port)
        if probe_assets:
            asset_probes["shopIcon"] = await probe_asset_section(port, "shopIcon", "Edit")
            asset_probes["shopPhotos"] = await probe_asset_section(port, "shopPhotos", "Add")
    basics = await probe_shop_basics(port)
    print(json.dumps({
        "info_page_text": info_ok,
        "shop_name": shop_name_ok,
        "tagline": tagline_ok,
        "about": about_ok,
        "logo": logo_ok,
        "asset_probes": {k: bool(v) for k, v in asset_probes.items()},
        "shop_basics_title": basics.get("title"),
        "quiet_relic_visible": "Quiet Relic" in str(basics.get("text", "")),
        "shop_name_visible": "DriveFuel" in str(basics.get("text", "")),
    }, ensure_ascii=False, indent=2))
    return 0 if dry_run or (info_ok and tagline_ok and about_ok) else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply approved Etsy shop shell fields.")
    parser.add_argument("--port", type=int, default=9223)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--probe-assets", action="store_true")
    args = parser.parse_args()
    raise SystemExit(asyncio.run(run(args.port, dry_run=args.dry_run, probe_assets=args.probe_assets)))


if __name__ == "__main__":
    main()
