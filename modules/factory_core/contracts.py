from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class FactoryTask:
    """Portable unit of work for any future AI-labor factory."""

    task_id: str
    business: str
    lane: str
    action: str
    priority: int
    risk_level: str = "medium"
    cost_cap_usd: float = 0.0
    resource_class: str = "local_light"
    requires_network: bool = False
    requires_login: bool = False
    inputs: dict[str, Any] = field(default_factory=dict)
    expected_outputs: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))


@dataclass
class GateResult:
    gate: str
    status: str
    reason: str
    score: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def allowed(self) -> bool:
        return self.status.upper() in {"PASS", "ALLOW", "WARN_ALLOW"}


@dataclass
class ExecutionDecision:
    task_id: str
    decision: str
    reason: str
    max_parallel: int = 1
    batch_size: int = 1
    cooldown_minutes: int = 0
    gate_results: list[GateResult] = field(default_factory=list)
    resource_snapshot: dict[str, Any] = field(default_factory=dict)

    @property
    def runnable(self) -> bool:
        return self.decision.upper() in {"RUN", "RUN_CONSERVATIVE"}
