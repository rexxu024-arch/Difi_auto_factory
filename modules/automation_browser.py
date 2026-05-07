"""Launch or check a dedicated browser profile for OpenClaw automation.

This keeps marketplace/account automation out of Rex's daily Chrome/Edge
windows. The browser is still visible if a login challenge needs human action,
but normal script work should use this isolated remote-debugging profile and
close tabs after each task.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path


DEFAULT_PORT = int(os.getenv("OPENCLAW_CDP_PORT") or "9223")
DEFAULT_PROFILE = Path(os.getenv("OPENCLAW_AUTOMATION_PROFILE") or r"C:\openclaw_edge_profile")


def browser_path(browser: str) -> Path:
    candidates = []
    if browser == "edge":
        candidates = [
            Path(os.getenv("ProgramFiles", r"C:\Program Files")) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
            Path(os.getenv("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
        ]
    else:
        candidates = [
            Path(os.getenv("ProgramFiles", r"C:\Program Files")) / "Google" / "Chrome" / "Application" / "chrome.exe",
            Path(os.getenv("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Google" / "Chrome" / "Application" / "chrome.exe",
        ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"Could not find {browser} executable.")


def cdp_status(port: int) -> dict:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=3) as response:
            payload = json.load(response)
        return {"status": "RUNNING", "port": port, "browser": payload.get("Browser", ""), "webSocketDebuggerUrl": payload.get("webSocketDebuggerUrl", "")}
    except Exception as exc:  # noqa: BLE001
        return {"status": "NOT_RUNNING", "port": port, "error": str(exc)}


def launch(browser: str, port: int, profile: Path, url: str, minimized: bool = True) -> dict:
    current = cdp_status(port)
    if current["status"] == "RUNNING":
        return current
    profile.mkdir(parents=True, exist_ok=True)
    exe = browser_path(browser)
    args = [
        str(exe),
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile}",
        "--no-first-run",
        "--disable-background-mode",
        "--disable-features=Translate",
        url,
    ]
    if minimized:
        args.insert(-1, "--start-minimized")
    subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(20):
        time.sleep(0.5)
        current = cdp_status(port)
        if current["status"] == "RUNNING":
            current["profile"] = str(profile)
            current["browser_exe"] = str(exe)
            return current
    raise RuntimeError(f"Browser did not expose CDP on port {port}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch/check OpenClaw dedicated automation browser.")
    parser.add_argument("--browser", choices=["edge", "chrome"], default=os.getenv("OPENCLAW_AUTOMATION_BROWSER", "edge"))
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--profile", default=str(DEFAULT_PROFILE))
    parser.add_argument("--url", default="about:blank")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--no-minimize", action="store_true")
    args = parser.parse_args()
    if args.check:
        result = cdp_status(args.port)
    else:
        result = launch(args.browser, args.port, Path(args.profile), args.url, minimized=not args.no_minimize)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
