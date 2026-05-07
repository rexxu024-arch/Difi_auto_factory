from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .contracts import ExecutionDecision, FactoryTask, GateResult


GateCallable = Callable[[FactoryTask], GateResult]


@dataclass
class GateStack:
    """Reusable risk/quality gate stack.

    Business-specific projects should register adapters here rather than
    hard-coding platform checks inside production modules.
    """

    risk_gates: list[GateCallable] = field(default_factory=list)
    quality_gates: list[GateCallable] = field(default_factory=list)
    cost_gates: list[GateCallable] = field(default_factory=list)

    def all_gates(self) -> list[GateCallable]:
        return [*self.risk_gates, *self.quality_gates, *self.cost_gates]


def run_gate_stack(task: FactoryTask, stack: GateStack) -> ExecutionDecision:
    results: list[GateResult] = []
    for gate in stack.all_gates():
        result = gate(task)
        results.append(result)
        if not result.allowed:
            return ExecutionDecision(
                task_id=task.task_id,
                decision="BLOCK",
                reason=f"{result.gate}: {result.reason}",
                gate_results=results,
            )
    warning = next((item for item in results if item.status.upper() == "WARN_ALLOW"), None)
    if warning:
        return ExecutionDecision(
            task_id=task.task_id,
            decision="RUN_CONSERVATIVE",
            reason=f"warning gate passed conservatively: {warning.gate}",
            gate_results=results,
            max_parallel=1,
            batch_size=1,
        )
    return ExecutionDecision(
        task_id=task.task_id,
        decision="RUN",
        reason="all gates passed",
        gate_results=results,
    )


def cost_cap_gate(task: FactoryTask) -> GateResult:
    requested_spend = float(task.inputs.get("planned_spend_usd") or 0)
    if task.cost_cap_usd and requested_spend > task.cost_cap_usd:
        return GateResult(
            gate="cost_cap",
            status="BLOCK",
            reason=f"planned spend ${requested_spend:.2f} exceeds cap ${task.cost_cap_usd:.2f}",
            score=0.0,
        )
    return GateResult("cost_cap", "PASS", "within task cost cap")


def no_customer_message_gate(task: FactoryTask) -> GateResult:
    if task.action.lower() in {"send_buyer_message", "reply_customer", "refund_order", "cancel_order"}:
        return GateResult("customer_boundary", "BLOCK", "buyer/order action requires Rex confirmation", score=0.0)
    return GateResult("customer_boundary", "PASS", "not a buyer/order action")
