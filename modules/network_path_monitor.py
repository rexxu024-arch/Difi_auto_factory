"""Lightweight network path monitor for OpenClaw.

Records whether Windows is actually using Ethernet or Wi-Fi as the active
default route. This is intentionally cheap: no continuous speed tests, only
adapter/route state plus optional alerting when the active path changes.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
STATE_PATH = DATABASE / "Network_Path_State.json"
LOG_PATH = DATABASE / "Network_Path_Monitor.csv"
ALERT_PATH = DATABASE / "Network_Path_Alerts.csv"


def now_et() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def powershell_json(script: str) -> Any:
    command = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        script,
    ]
    completed = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        timeout=30,
        check=True,
    )
    text = completed.stdout.strip()
    if not text:
        return []
    return json.loads(text)


def as_list(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, list):
        return [v for v in value if isinstance(v, dict)]
    if isinstance(value, dict):
        return [value]
    return []


def snapshot() -> dict[str, Any]:
    adapters = as_list(
        powershell_json(
            "Get-NetAdapter | Select-Object Name,InterfaceDescription,Status,LinkSpeed,ifIndex,MacAddress | ConvertTo-Json -Depth 3"
        )
    )
    routes = as_list(
        powershell_json(
            "Get-NetRoute -DestinationPrefix '0.0.0.0/0' | "
            "Select-Object ifIndex,InterfaceAlias,NextHop,RouteMetric,InterfaceMetric | ConvertTo-Json -Depth 3"
        )
    )
    profiles = as_list(
        powershell_json(
            "Get-NetConnectionProfile | Select-Object Name,InterfaceAlias,IPv4Connectivity,IPv6Connectivity | ConvertTo-Json -Depth 3"
        )
    )

    up_ifindexes = {
        int(a.get("ifIndex"))
        for a in adapters
        if str(a.get("Status") or "").lower() == "up" and str(a.get("ifIndex") or "").isdigit()
    }
    viable_routes = []
    for route in routes:
        try:
            ifindex = int(route.get("ifIndex"))
            route_metric = int(route.get("RouteMetric") or 0)
            iface_metric = int(route.get("InterfaceMetric") or 0)
        except Exception:
            continue
        if ifindex in up_ifindexes:
            viable_routes.append((route_metric + iface_metric, route))
    viable_routes.sort(key=lambda item: item[0])
    active_route = viable_routes[0][1] if viable_routes else {}
    active_alias = str(active_route.get("InterfaceAlias") or "")

    adapter_by_name = {str(a.get("Name") or ""): a for a in adapters}
    active_adapter = adapter_by_name.get(active_alias, {})
    profile = next((p for p in profiles if str(p.get("InterfaceAlias") or "") == active_alias), {})

    return {
        "timestamp": now_et(),
        "active_alias": active_alias,
        "active_description": active_adapter.get("InterfaceDescription", ""),
        "active_status": active_adapter.get("Status", ""),
        "active_link_speed": active_adapter.get("LinkSpeed", ""),
        "active_next_hop": active_route.get("NextHop", ""),
        "active_metric": (int(active_route.get("RouteMetric") or 0) + int(active_route.get("InterfaceMetric") or 0))
        if active_route
        else "",
        "network_name": profile.get("Name", ""),
        "ipv4": profile.get("IPv4Connectivity", ""),
        "ethernet_status": str(adapter_by_name.get("Ethernet 3", {}).get("Status", "")),
        "ethernet_link_speed": str(adapter_by_name.get("Ethernet 3", {}).get("LinkSpeed", "")),
        "wifi_status": str(adapter_by_name.get("Wi-Fi", {}).get("Status", "")),
        "wifi_link_speed": str(adapter_by_name.get("Wi-Fi", {}).get("LinkSpeed", "")),
    }


def read_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def append_csv(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def classify_alert(current: dict[str, Any], previous: dict[str, Any], expected_alias: str) -> str:
    active = str(current.get("active_alias") or "")
    prev = str(previous.get("active_alias") or "")
    ethernet_status = str(current.get("ethernet_status") or "")
    if expected_alias and active != expected_alias:
        return f"ACTIVE_PATH_NOT_EXPECTED:{active or 'NONE'}"
    if prev and active and active != prev:
        return f"ACTIVE_PATH_CHANGED:{prev}->{active}"
    if ethernet_status and ethernet_status.lower() != "up":
        return f"ETHERNET_NOT_UP:{ethernet_status}"
    if not active:
        return "NO_ACTIVE_DEFAULT_ROUTE"
    return ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Log and alert on Ethernet/Wi-Fi active path changes.")
    parser.add_argument("--expected-alias", default="Ethernet 3")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    previous = read_state()
    current = snapshot()
    alert = classify_alert(current, previous, args.expected_alias)
    current["alert"] = alert
    append_csv(LOG_PATH, current)
    if alert:
        append_csv(ALERT_PATH, current)
    STATE_PATH.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(current, ensure_ascii=False, indent=2) if args.json else f"{current['timestamp']} {current['active_alias']} {alert or 'OK'}")


if __name__ == "__main__":
    main()
