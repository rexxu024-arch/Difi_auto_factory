"""Portable OpenClaw factory core.

This package is intentionally marketplace-agnostic.  New businesses should be
able to reuse the same task contract, risk gate, quality gate, and resource
allocation shape without importing Printify/eBay/Etsy-specific modules.
"""

from .contracts import ExecutionDecision, FactoryTask, GateResult
from .portable_gates import GateStack, run_gate_stack

__all__ = [
    "ExecutionDecision",
    "FactoryTask",
    "GateResult",
    "GateStack",
    "run_gate_stack",
]
