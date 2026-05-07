from __future__ import annotations

import argparse
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
QUEUE_PATH = DATABASE_DIR / "Grunt_Task_Queue.jsonl"
NY = ZoneInfo("America/New_York")


@dataclass
class ModularTask:
    task_id: str
    title: str
    action: str
    status: str = "PENDING"
    priority: int = 50
    resource_class: str = "local_light"
    lane: str = "grunt"
    business: str = "openclaw"
    requires_network: bool = False
    requires_login: bool = False
    cost_cap_usd: float = 0.0
    command: str = ""
    timeout_seconds: int = 300
    attempts: int = 0
    max_attempts: int = 2
    inputs: dict = field(default_factory=dict)
    expected_outputs: list[str] = field(default_factory=list)
    qa_profile: str = "basic"
    created_at: str = field(default_factory=lambda: now_iso())
    updated_at: str = field(default_factory=lambda: now_iso())
    started_at: str = ""
    completed_at: str = ""
    last_error: str = ""
    result_summary: str = ""


def now_iso():
    return datetime.now(NY).isoformat(timespec="seconds")


def _task_from_dict(data):
    allowed = set(ModularTask.__dataclass_fields__.keys())
    clean = {key: value for key, value in data.items() if key in allowed}
    return ModularTask(**clean)


def load_tasks(path=QUEUE_PATH) -> list[ModularTask]:
    path = Path(path)
    if not path.exists():
        return []
    tasks = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            tasks.append(_task_from_dict(json.loads(line)))
    return tasks


def save_tasks(tasks: list[ModularTask], path=QUEUE_PATH) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as handle:
        for task in tasks:
            handle.write(json.dumps(asdict(task), ensure_ascii=False, sort_keys=True) + "\n")
    tmp.replace(path)


def enqueue_task(**kwargs) -> ModularTask:
    tasks = load_tasks()
    task_id = kwargs.get("task_id") or f"grunt-{datetime.now(NY):%Y%m%d%H%M%S}-{uuid.uuid4().hex[:8]}"
    task = ModularTask(task_id=task_id, **{k: v for k, v in kwargs.items() if k != "task_id"})
    tasks.append(task)
    save_tasks(tasks)
    return task


def seed_default_tasks(force=False) -> list[ModularTask]:
    tasks = load_tasks()
    active_keys = {
        (task.action, task.command)
        for task in tasks
        if task.status in {"PENDING", "RUNNING", "DEFERRED"}
    }
    specs = [
        {
            "title": "Hardware heartbeat sample",
            "action": "hardware_heartbeat",
            "priority": 100,
            "resource_class": "local_light",
            "command": "py modules\\hardware_heartbeat_monitor.py --once",
            "timeout_seconds": 90,
            "qa_profile": "log",
            "expected_outputs": ["Database/Hardware_Heartbeat_State.json"],
        },
        {
            "title": "Hardware cooldown guard",
            "action": "hardware_cooldown_guard",
            "priority": 98,
            "resource_class": "local_light",
            "command": "py modules\\hardware_cooldown_guard.py --json",
            "timeout_seconds": 120,
            "qa_profile": "log",
            "expected_outputs": ["Database/Hardware_Cooldown_State.json"],
        },
        {
            "title": "Factory local maintenance refresh",
            "action": "local_supervisor_refresh",
            "priority": 90,
            "resource_class": "report_batch",
            "command": "py modules\\factory_supervisor.py --execute-local --skip-network",
            "timeout_seconds": 240,
            "qa_profile": "log",
            "expected_outputs": ["Database/Factory_Autopilot_State.json"],
        },
        {
            "title": "Quality floor scan on recent Database outputs",
            "action": "quality_floor_scan",
            "priority": 82,
            "resource_class": "qa_batch",
            "command": "py modules\\quality_floor_guard.py --paths Database --limit 80",
            "timeout_seconds": 180,
            "qa_profile": "log",
            "expected_outputs": ["Database/Quality_Floor_Guard.csv"],
        },
        {
            "title": "eBay traffic experiment refresh",
            "action": "copy_signal_refresh",
            "priority": 70,
            "resource_class": "local_light",
            "command": "py modules\\ebay_experiment_report.py",
            "timeout_seconds": 120,
            "qa_profile": "log",
            "expected_outputs": ["Database/eBay_Traffic_Experiment_Report.csv"],
        },
        {
            "title": "Market signal queue refresh",
            "action": "market_signal_refresh",
            "priority": 68,
            "resource_class": "local_light",
            "command": "py modules\\market_signal_planner.py",
            "timeout_seconds": 180,
            "qa_profile": "log",
            "expected_outputs": ["Database/Market_Signal_Action_Queue.csv"],
        },
        {
            "title": "Multi-track marketplace experiment plan",
            "action": "multi_track_experiment_plan",
            "priority": 72,
            "resource_class": "queue_planning",
            "command": "py modules\\multi_track_experiment_planner.py --json",
            "timeout_seconds": 420,
            "qa_profile": "log",
            "expected_outputs": ["Database/Multi_Track_Experiment_Plan.csv", "Database/Multi_Track_Experiment_State.json"],
        },
        {
            "title": "Rest-window log compression plan",
            "action": "rest_log_compression_plan",
            "priority": 60,
            "resource_class": "rest_maintenance",
            "command": "py modules\\grunt_engine.py --maintenance-plan",
            "timeout_seconds": 120,
            "qa_profile": "log",
            "expected_outputs": ["Database/Grunt_Maintenance_Plan.json"],
        },
    ]
    added = []
    for spec in specs:
        if not force and (spec["action"], spec["command"]) in active_keys:
            continue
        task = ModularTask(task_id=f"grunt-{spec['action']}-{uuid.uuid4().hex[:8]}", **spec)
        tasks.append(task)
        added.append(task)
    save_tasks(tasks)
    return added


def claim_next(allowed_classes=None, allowed_actions=None, mutate: bool = True) -> ModularTask | None:
    allowed_classes = set(allowed_classes or [])
    allowed_actions = set(allowed_actions or [])
    tasks = load_tasks()
    candidates = []
    for idx, task in enumerate(tasks):
        if task.status not in {"PENDING", "DEFERRED"}:
            continue
        if task.attempts >= task.max_attempts:
            continue
        if allowed_classes and task.resource_class not in allowed_classes:
            continue
        if allowed_actions and task.action not in allowed_actions:
            continue
        candidates.append((idx, task))
    if not candidates:
        return None
    idx, task = sorted(candidates, key=lambda pair: (-pair[1].priority, pair[1].created_at))[0]
    if not mutate:
        return task
    task.status = "RUNNING"
    task.attempts += 1
    task.started_at = now_iso()
    task.updated_at = now_iso()
    tasks[idx] = task
    save_tasks(tasks)
    return task


def update_task(task_id: str, **updates) -> ModularTask | None:
    tasks = load_tasks()
    target = None
    for idx, task in enumerate(tasks):
        if task.task_id != task_id:
            continue
        for key, value in updates.items():
            if hasattr(task, key):
                setattr(task, key, value)
        task.updated_at = now_iso()
        if updates.get("status") in {"DONE", "FAILED", "QUARANTINED"} and not task.completed_at:
            task.completed_at = now_iso()
        tasks[idx] = task
        target = task
        break
    save_tasks(tasks)
    return target


def summarize():
    counts = {}
    by_class = {}
    for task in load_tasks():
        counts[task.status] = counts.get(task.status, 0) + 1
        by_class[task.resource_class] = by_class.get(task.resource_class, 0) + 1
    return {"status_counts": counts, "resource_class_counts": by_class, "queue": str(QUEUE_PATH)}


def main():
    parser = argparse.ArgumentParser(description="Portable JSONL task queue for the OpenClaw Grunt Engine.")
    parser.add_argument("--seed-default", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--enqueue-json", default="")
    args = parser.parse_args()
    if args.seed_default:
        added = seed_default_tasks(force=args.force)
        print(json.dumps({"added": [asdict(task) for task in added], "summary": summarize()}, indent=2))
        return
    if args.enqueue_json:
        task = enqueue_task(**json.loads(args.enqueue_json))
        print(json.dumps(asdict(task), indent=2))
        return
    if args.list:
        print(json.dumps([asdict(task) for task in load_tasks()], indent=2))
        return
    print(json.dumps(summarize(), indent=2))


if __name__ == "__main__":
    main()
