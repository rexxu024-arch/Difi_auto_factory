"""Isolation guard for the Adobe Stock fallback line.

Adobe Stock may reuse OpenClaw code patterns, but it must not write into the
Mentor Hub, Production Line, Etsy, or eBay operating datasets.
"""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ADOBE_ALLOWED_NAMESPACES = {
    "Adobe_Stock",
    "adobe_stock",
}
FORBIDDEN_DATA_NAMES = {
    "Mentor_Hub.xlsx",
    "Production_Line.xlsx",
    "pending_tasks.txt",
    "Pending_design.txt",
}
FORBIDDEN_CROSS_NAMESPACE_MARKERS = {
    "Etsy_",
    "eBay_",
    "Printify_",
    "First_Audit",
}
FORBIDDEN_CORE_NAME_MARKERS = {
    "Product_Line",
    "Mentor_Hub",
}


def _normalize(path: Path) -> Path:
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()


def assert_adobe_write_path(path: Path) -> None:
    resolved = _normalize(path)
    try:
        relative = resolved.relative_to(PROJECT_ROOT)
    except ValueError as exc:
        raise ValueError(f"Adobe Stock write path is outside project root: {resolved}") from exc

    name_text = str(relative).replace("/", "\\")
    if resolved.name in FORBIDDEN_DATA_NAMES:
        raise ValueError(f"Adobe Stock cannot write core operating file: {relative}")
    if any(marker in name_text for marker in FORBIDDEN_CROSS_NAMESPACE_MARKERS):
        raise ValueError(f"Adobe Stock cannot write non-Adobe namespace: {relative}")
    if any(marker in name_text for marker in FORBIDDEN_CORE_NAME_MARKERS) and not resolved.name.startswith("Adobe_Stock_"):
        raise ValueError(f"Adobe Stock cannot write core operating namespace: {relative}")
    if not any(namespace in name_text for namespace in ADOBE_ALLOWED_NAMESPACES):
        raise ValueError(f"Adobe Stock write path must include Adobe_Stock namespace: {relative}")


def assert_adobe_write_paths(paths: list[Path] | tuple[Path, ...]) -> None:
    for path in paths:
        assert_adobe_write_path(path)
