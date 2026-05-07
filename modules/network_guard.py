import argparse
import json
import re
import statistics
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = ["api.printify.com", "www.etsy.com", "discord.com"]


@dataclass
class TargetHealth:
    target: str
    sent: int = 0
    received: int = 0
    loss_percent: float = 100.0
    min_ms: float | None = None
    max_ms: float | None = None
    avg_ms: float | None = None
    jitter_ms: float | None = None
    ok: bool = False


def _run_ping(target, count=6, timeout=20):
    return subprocess.run(
        ["ping", "-n", str(count), target],
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    ).stdout


def _parse_ping(target, text):
    packet = re.search(
        r"Packets:\s*Sent\s*=\s*(\d+),\s*Received\s*=\s*(\d+),\s*Lost\s*=\s*(\d+)\s*\((\d+)%\s*loss\)",
        text,
        re.I,
    )
    times = []
    for value in re.findall(r"time[=<]\s*(\d+)ms", text, re.I):
        try:
            times.append(float(value))
        except ValueError:
            pass
    health = TargetHealth(target=target)
    if packet:
        health.sent = int(packet.group(1))
        health.received = int(packet.group(2))
        health.loss_percent = float(packet.group(4))
    if times:
        health.min_ms = min(times)
        health.max_ms = max(times)
        health.avg_ms = sum(times) / len(times)
        health.jitter_ms = statistics.pstdev(times) if len(times) > 1 else 0.0
    health.ok = health.received > 0 and health.loss_percent <= 2.0 and (health.avg_ms or 9999) < 200
    return health


def check_network(targets=None, count=6):
    results = []
    for target in targets or DEFAULT_TARGETS:
        try:
            results.append(_parse_ping(target, _run_ping(target, count=count)))
        except Exception:
            results.append(TargetHealth(target=target))
    return results


def choose_strategy(results):
    if not results or any(item.received == 0 for item in results):
        return {"mode": "pause", "max_parallel": 0, "batch_size": 0, "reason": "endpoint unreachable"}
    worst_loss = max(item.loss_percent for item in results)
    worst_avg = max(item.avg_ms or 9999 for item in results)
    worst_jitter = max(item.jitter_ms or 9999 for item in results)
    if worst_loss > 5 or worst_avg > 350:
        return {"mode": "pause", "max_parallel": 0, "batch_size": 0, "reason": f"loss={worst_loss:.1f}% avg={worst_avg:.0f}ms"}
    if worst_loss > 0 or worst_avg > 120 or worst_jitter > 60:
        return {"mode": "conservative", "max_parallel": 1, "batch_size": 1, "reason": f"loss={worst_loss:.1f}% avg={worst_avg:.0f}ms jitter={worst_jitter:.0f}ms"}
    return {"mode": "full_throughput", "max_parallel": 3, "batch_size": 8, "reason": f"wired/healthy; avg={worst_avg:.0f}ms"}


def report(count=6, targets=None):
    results = check_network(targets=targets, count=count)
    return {"results": [asdict(item) for item in results], "strategy": choose_strategy(results)}


def main():
    parser = argparse.ArgumentParser(description="Preflight network guard for OpenClaw batch jobs.")
    parser.add_argument("--count", type=int, default=6)
    parser.add_argument("--targets", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    targets = [item.strip() for item in args.targets.split(",") if item.strip()] or DEFAULT_TARGETS
    payload = report(count=args.count, targets=targets)
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    for item in payload["results"]:
        print(
            f"[NET] {item['target']} received={item['received']}/{item['sent']} "
            f"loss={item['loss_percent']:.1f}% avg={item['avg_ms']}ms max={item['max_ms']}ms jitter={item['jitter_ms']}ms"
        )
    strategy = payload["strategy"]
    print(
        f"[NET-STRATEGY] mode={strategy['mode']} max_parallel={strategy['max_parallel']} "
        f"batch_size={strategy['batch_size']} reason={strategy['reason']}"
    )
    if strategy["mode"] == "pause":
        sys.exit(2)


if __name__ == "__main__":
    main()
