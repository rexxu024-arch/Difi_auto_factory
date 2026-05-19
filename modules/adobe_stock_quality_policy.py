"""Strict Adobe Stock production-quality gate.

This module is intentionally stricter than Adobe's official minimums, but it
does not require expensive Midjourney Fast or creative upscale for stock assets.
OpenClaw stock files must be commercially useful, clear, and traceable to a
real selected U-button / full-resolution source rather than a sliced grid crop.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageFilter, ImageStat


ADOBE_OFFICIAL_MIN_PIXELS = 4_000_000
OPENCLAW_MIN_PIXELS = 4_000_000
OPENCLAW_TARGET_PIXELS = 4_800_000
OPENCLAW_MIN_SHORT_EDGE = 1700
OPENCLAW_MIN_LONG_EDGE = 2400
SOFT_MIN_FILE_BYTES = 1_200_000
MIN_UPSCALED_EDGE_SCORE = 6.0
MIN_NATIVE_EDGE_SCORE = 12.0
MIN_SHARP_TILE_COVERAGE = 0.45
SHARP_TILE_EDGE_THRESHOLD = 6.0

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
    "u_button",
    "selected_u",
    "full_res_u",
    "mj_full_res",
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
    return False, ["missing MJ U-button/full-resolution provenance"]


def edge_detail_score(path: Path) -> float:
    with Image.open(path) as image:
        gray = image.convert("L")
        edges = gray.filter(ImageFilter.FIND_EDGES)
        return float(ImageStat.Stat(edges).mean[0])


def sharp_tile_coverage(path: Path, grid: tuple[int, int] = (12, 8)) -> float:
    """Estimate how much of the frame carries usable texture detail.

    Adobe will accept intentional shallow depth of field in some photos, but
    OpenClaw's first stock batches are material/background assets. Buyers need
    broad crop-safe sharpness, so low coverage is treated as a hold.
    """
    with Image.open(path) as image:
        edges = image.convert("L").filter(ImageFilter.FIND_EDGES)
        width, height = edges.size
        cols, rows = grid
        sharp = 0
        total = cols * rows
        for row in range(rows):
            for col in range(cols):
                crop = edges.crop(
                    (
                        col * width // cols,
                        row * height // rows,
                        (col + 1) * width // cols,
                        (row + 1) * height // rows,
                    )
                )
                if float(ImageStat.Stat(crop).mean[0]) >= SHARP_TILE_EDGE_THRESHOLD:
                    sharp += 1
        return sharp / max(total, 1)


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
    if file_bytes < SOFT_MIN_FILE_BYTES:
        info["File_Size_Warning"] = (
            f"soft warning only: file is {file_bytes} bytes; Adobe has no 4MB minimum, "
            "but visually inspect for over-compression or weak detail"
        )
    if pixels < ADOBE_OFFICIAL_MIN_PIXELS:
        return False, "HOLD_BELOW_ADOBE_OFFICIAL_4MP_MINIMUM", info
    if pixels < OPENCLAW_MIN_PIXELS or short_edge < OPENCLAW_MIN_SHORT_EDGE or long_edge < OPENCLAW_MIN_LONG_EDGE:
        return False, "HOLD_BELOW_OPENCLAW_STOCK_4MP_RESOLUTION_REDLINE", info
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
            return False, "HOLD_MISSING_SELECTED_U_FULL_RES_PROVENANCE", info

    edge_score = edge_detail_score(path)
    info["Edge_Detail_Score"] = f"{edge_score:.2f}"
    sharp_coverage = sharp_tile_coverage(path)
    info["Sharp_Tile_Coverage"] = f"{sharp_coverage:.3f}"
    provenance_text = _join_row_text(row, ("Source_Provenance", "Status", "QA_Status", "Upscale_Status"))
    if "local" in provenance_text or "local_resolution" in provenance_text:
        if edge_score < MIN_UPSCALED_EDGE_SCORE:
            info["Quality_Reasons"] = f"local-upscaled source lacks detail; edge score {edge_score:.2f} < {MIN_UPSCALED_EDGE_SCORE:.2f}"
            return False, "HOLD_LOCAL_UPSCALE_DETAIL_TOO_LOW", info
    elif edge_score < MIN_NATIVE_EDGE_SCORE:
        info["Quality_Reasons"] = f"native source lacks detail; edge score {edge_score:.2f} < {MIN_NATIVE_EDGE_SCORE:.2f}"
        return False, "HOLD_NATIVE_DETAIL_TOO_LOW", info
    if sharp_coverage < MIN_SHARP_TILE_COVERAGE:
        info["Quality_Reasons"] = (
            f"too much shallow depth/blurred area for first Adobe material batch; "
            f"sharp tile coverage {sharp_coverage:.3f} < {MIN_SHARP_TILE_COVERAGE:.2f}"
        )
        return False, "HOLD_SHALLOW_DOF_OR_LOW_SHARP_AREA", info

    return True, "QA_PASS_ADOBE_MACRO_FULL_RES_PRODUCTION", info


def macro_prompt(material_type: str) -> str:
    """Canonical Adobe Stock prompt spine for future generation queue rows."""
    return (
        f"Extreme macro photography of {material_type}, dramatic studio side-lighting, "
        "rich textural depth, micro-details, 8k resolution, shot on 100mm macro lens, "
        "ultra-photorealistic, commercial material background, deep focus across the material plane, "
        "broad crop-safe sharp texture coverage, no shallow depth of field, no bokeh, "
        "no blurred foreground, no blurred background, no people, no logo, no text, no watermark "
        "--ar 3:2 --style raw --v 6.0 --chaos 12 --relax"
    )
