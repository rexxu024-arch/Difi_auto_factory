"""Compliant metadata separation helpers.

OpenClaw uses two metadata layers:
- production metadata for Printify/product creation: neutral, accurate, and low-noise;
- marketplace metadata for eBay/Etsy: richer SEO copy that is still accurate.

This module explicitly rejects deceptive "vanilla" labels that describe a
different subject than the product. The goal is account hygiene and operational
clarity, not bypassing platform or print-provider review.
"""

from __future__ import annotations

import re


_PRODUCT_LABELS = {
    "Sticker": "Vinyl Sticker Sheet",
    "Poster": "Matte Wall Art Print",
    "Acrylic": "Acrylic Photo Block",
    "Canvas": "Canvas Wall Art",
    "T-shirt": "Graphic Tee",
    "Mug": "Ceramic Mug",
}

_STYLE_WORDS = {
    "academia": "Vintage Study",
    "zen": "Quiet Minimal",
    "grimdark": "Moody Collector",
    "gothic": "Moody Architectural",
    "cyber": "Modern Luminous",
    "jade": "Jade Tone",
    "floral": "Floral",
}

_MISLEADING_SUBJECTS = {
    "floral": {"flower", "floral", "botanical", "rose", "lotus", "blossom"},
    "animal": {"cat", "dog", "bird", "raven", "koi", "lion", "beast"},
    "portrait": {"portrait", "face", "person", "figure"},
}


def clean_text(value: object, limit: int | None = None) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    text = re.sub(r"[^\x20-\x7E]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if limit and len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0].strip() or text[:limit].strip()
    return text


def product_type(row: dict) -> str:
    raw = clean_text(row.get("Product_Type") or row.get("Product") or "Art")
    for key in _PRODUCT_LABELS:
        if raw.lower().startswith(key.lower()):
            return key
    return raw or "Art"


def main_category(row: dict) -> str:
    raw = clean_text(row.get("Category") or row.get("Style") or row.get("Title") or "Art")
    return raw.split("-")[0].split()[0].title() if raw else "Art"


def infer_style(row: dict) -> str:
    blob = " ".join(
        clean_text(row.get(key))
        for key in ("Title", "Category", "Style", "SEO_Hook", "MJ_Prompt")
    ).lower()
    for key, label in _STYLE_WORDS.items():
        if key in blob:
            return label
    return main_category(row)


def production_safe_title(row: dict) -> str:
    ptype = product_type(row)
    product_label = _PRODUCT_LABELS.get(ptype, f"{ptype} Art")
    style = infer_style(row)
    title = f"{style} {product_label}"
    return clean_text(title, limit=80)


def production_safe_description(row: dict) -> str:
    ptype = product_type(row)
    product_label = _PRODUCT_LABELS.get(ptype, f"{ptype} product")
    style = infer_style(row)
    return clean_text(
        f"Made-to-order {product_label.lower()} with a {style.lower()} visual style. "
        "Production metadata is intentionally concise; marketplace-facing copy is managed separately and must remain accurate.",
        limit=500,
    )


def is_misleading_internal_title(internal_title: str, public_title: str) -> bool:
    internal = clean_text(internal_title).lower()
    public = clean_text(public_title).lower()
    for label, terms in _MISLEADING_SUBJECTS.items():
        internal_claims = label in internal or any(term in internal for term in terms)
        public_supports = label in public or any(term in public for term in terms)
        if internal_claims and not public_supports:
            return True
    return False


def printify_metadata_payload(row: dict) -> dict[str, str]:
    public_title = clean_text(row.get("Title"))
    title = clean_text(row.get("Printify_Internal_Title")) or production_safe_title(row)
    description = clean_text(row.get("Printify_Internal_Description")) or production_safe_description(row)
    if is_misleading_internal_title(title, public_title):
        raise ValueError(
            f"Misleading Printify internal title rejected: internal={title!r} public={public_title!r}"
        )
    return {"title": title, "description": description}
