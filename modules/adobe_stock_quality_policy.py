"""Strict Adobe Stock production-quality gate.

This module is intentionally harsher than Adobe's official minimums. Adobe may
accept images above 4MP, but OpenClaw should only submit assets that are both
commercially useful and traceable to a real high-resolution production source.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ADOBE_OFFICIAL_MIN_PIXELS = 4_000_000
OPENCLAW_MIN_PIXELS = 8_000_000
OPENCLAW_TARGET_PIXELS = 10_000_000
OPENCLAW_MIN_SHORT_EDGE = 2200
OPENCLAW_MIN_LONG_EDGE = 3300
MIN_FILE_BYTES = 1_200_000

MACRO_DNA_TERMS = (
    "extreme macro photography",
    "dramatic studio side-lighting",
    "rich textural depth",
    "micro-details",
    "100mm macro lens",
    "ultra-photorealistic",
)

FORBIDDEN_PROMPT_TERMS = (
    "orthographic material scan",
    "flat-lay material plate",
    "flat lay",
    "4k stock material asset",
    "--ar 1:1",
)

UPSCALE_PROVENANCE_TERMS = (
    "mj_u_button",
    "midjourney_u_button",
    "2x_upscale",
    "u1",
    "u2",
    "u3",
    "u4",
    "upscaled",
    "upscale",
)


def _join_row_text(row: dict[str, str] | None, keys: tuple[str, ...]) -> str:
    if not row:
        return ""
    return " ".join((row.get(key) or "") for key in keys).lower()


def prompt_macro_status(row: dict[str, str] | None) -> tuple[bool, list[str]]:
    text = _join_row_text(row, ("MJ_Prompt", "Prompt_Fragment", "Prompt", "Generation_Prompt"))
    if not text:
        return False, ["missing macro prompt text"]
    missing = [term for term in MACRO_DNA_TERMS if term not in text]
    forbidden = [term for term in FORBIDDEN_PROMPT_TERMS if term in text]
    reasons: list[str] = []
    if missing:
        reasons.append("missing macro DNA: " + ", ".join(missing[:3]))
    if forbidden:
        reasons.append("forbidden flat draft term: " + ", ".join(forbidden[:3]))
    return not reasons, reasons


def provenance_status(path: Path, row: dict[str, str] | None) -> tuple[bool, list[str]]:
    text = _join_row_text(
        row,
        (
            "Source_Provenance",
            "Generation_Source",
            "Upscale_Status",
            "Source_Path",
            "Local_Path",
            "Status",
            "QA_Status",
        ),
    )
    text = f"{text} {path.name.lower()} {str(path.parent).lower()}"
    if any(term in text for term in UPSCALE_PROVENANCE_TERMS):
        return True, []
    return False, ["missing MJ U-button / 2x upscale provenance"]


def validate_adobe_production_image(
    path: Path,
    row: dict[str, str] | None = None,
    require_macro_prompt: bool = True,
    require_upscale_provenance: bool = True,
) -> tuple[bool, str, dict[str, str]]:
    """Return (ok, status, info) for a candidate Adobe Stock production file."""
    if not path.exists():
        return False, "HOLD_SOURCE_PATH_MISSING", {}
    file_bytes = path.stat().st_size
    if file_bytes < MIN_FILE_BYTES:
        return False, "HOLD_FILE_TOO_SMALL_FOR_STOCK", {"File_Bytes": str(file_bytes)}
    try:
        with Image.open(path) as image:
            width, height = image.size
            mode = image.mode
            fmt = image.format or ""
    except Exception as exc:
        return False, f"HOLD_IMAGE_READ_ERROR:{type(exc).__name__}", {}

    pixels = width * height
    short_edge = min(width, height)
    long_edge = max(width, height)
    info = {
        "Width": str(width),
        "Height": str(height),
        "Pixels": str(pixels),
        "Short_Edge": str(short_edge),
        "Long_Edge": str(long_edge),
        "Mode": mode,
        "Format": fmt,
        "File_Bytes": str(file_bytes),
    }
    if pixels < ADOBE_OFFICIAL_MIN_PIXELS:
        return False, "HOLD_BELOW_ADOBE_OFFICIAL_4MP_MINIMUM", info
    if pixels < OPENCLAW_MIN_PIXELS or short_edge < OPENCLAW_MIN_SHORT_EDGE or long_edge < OPENCLAW_MIN_LONG_EDGE:
        return False, "HOLD_BELOW_OPENCLAW_STOCK_RESOLUTION_REDLINE", info
    if mode not in {"RGB", "RGBA"}:
        return False, f"HOLD_UNEXPECTED_COLOR_MODE:{mode}", info
    if fmt.upper() not in {"JPEG", "JPG", "PNG"}:
        return False, f"HOLD_UNEXPECTED_FORMAT:{fmt}", info

    if require_macro_prompt:
        prompt_ok, prompt_reasons = prompt_macro_status(row)
        if not prompt_ok:
            info["Quality_Reasons"] = " | ".join(prompt_reasons)
            return False, "HOLD_PROMPT_NOT_MACRO_PHOTOGRAPHY_DNA", info

    if require_upscale_provenance:
        provenance_ok, provenance_reasons = provenance_status(path, row)
        if not provenance_ok:
            info["Quality_Reasons"] = " | ".join(provenance_reasons)
            return False, "HOLD_MISSING_REAL_UPSCALE_PROVENANCE", info

    return True, "QA_PASS_ADOBE_MACRO_UPSCALED_PRODUCTION", info


def macro_prompt(material_type: str) -> str:
    """Canonical Adobe Stock prompt spine for future generation queue rows."""
    return (
        f"Extreme macro photography of {material_type}, dramatic studio side-lighting, "
        "rich textural depth, micro-details, 8k resolution, shot on 100mm macro lens, "
        "ultra-photorealistic, commercial material background, no people, no logo, "
        "no text, no watermark --ar 3:2 --style raw --v 6.0"
    )
