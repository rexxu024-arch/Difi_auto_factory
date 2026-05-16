"""Build review-ready spec sheets for First Audit extension candidates.

This does not promote assets into the protected manifest. It turns candidates
that already passed the carrier/product gate into private-sales review copy so
Rex/Grey can judge whether they deserve THE FIRST AUDIT numbering.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "Database"
OUT_DIR = ROOT / "Review_Packets" / "First_Audit_001"
IN_CSV = DATABASE / "First_Audit_001_Extension_Candidates.csv"
OUT_MD = OUT_DIR / "FIRST_AUDIT_EXTENSION_SPEC_SHEETS.md"
OUT_CSV = DATABASE / "First_Audit_001_Extension_Specs.csv"

ET = ZoneInfo("America/New_York")


@dataclass
class ExtensionSpec:
    rank: int
    sku: str
    concept: str
    medium: str
    tier: str
    rrp: int
    source_file: str
    production_file: str
    printify_product_id: str
    broker_hook: str
    cultural_anchor: str
    material_illusion: str
    spatial_recommendation: str
    objection_handling: str


THEMES = {
    "AUSPICIOUS": {
        "anchor": "A secular prosperity talisman: not folk ornament, but the museum-case version of good fortune as a machine.",
        "material": "Smoky jade glow, brushed chrome housing, and refractive acrylic depth are treated like an industrial object study.",
        "space": "Best on a walnut desk, shelf niche, or entry console where it reads as a contained lucky engine.",
    },
    "CYBER": {
        "anchor": "A post-Bauhaus shrine object: bonsai discipline translated into circuitry, glass, and controlled neon.",
        "material": "Brushed titanium, cyan phosphor light, smoky glass refraction, and architectural negative space.",
        "space": "Best for a dark office, studio shelf, gaming room, or modern apartment with black metal accents.",
    },
    "EPIC": {
        "anchor": "Northern reliquary language without direct IP: frost metal, rune logic, and chapel-scale mythic pressure.",
        "material": "Frosted steel, worn brass, kintsugi-like fracture lines, and heavy chiaroscuro shadow volume.",
        "space": "Best beside books, speakers, a black desk lamp, or an executive shelf that can carry a heavier mood.",
    },
    "ARCHIVE": {
        "anchor": "A New York archive fragment: jazz-cellar light, film grain, and old-room warmth without postcard nostalgia.",
        "material": "Amber emulsion, smoky varnish, matte paper tooth, and low-saturation cinematic fog.",
        "space": "Best for a listening corner, record shelf, hallway vignette, or warm-toned reading room.",
    },
}


def clean(value: object) -> str:
    return str(value or "").strip()


def tier_and_price(vector: str) -> tuple[str, int]:
    v = vector.lower()
    if "acrylic" in v:
        return "Core optical relic", 128
    if "framed" in v or "poster" in v or "canvas" in v:
        return "Entrance studio print", 48
    return "Review object", 48


def theme_for_sku(sku: str) -> dict[str, str]:
    for key, theme in THEMES.items():
        if key in sku:
            return theme
    return {
        "anchor": "A private Studio object selected for material mood, cultural tension, and room presence.",
        "material": "Controlled contrast, premium surface illusion, and physical-product readability.",
        "space": "Best in a study, shelf niche, office corner, or quiet apartment wall where the object has breathing room.",
    }


def broker_hook(sku: str, concept: str, medium: str) -> str:
    if "AUSPICIOUS" in sku:
        return f"纽约这边刚筛出来的一个发财系实验件，{concept}，不是普通招财小摆件，是那种放桌上有点压场的质感。"
    if "CYBER" in sku:
        return f"这张是赛博书房线的候选，{concept}，适合那种不想买廉价装饰、但又想要一点未来感的人。"
    if "EPIC" in sku:
        return f"这件偏硬核，{concept}，不是游戏周边，是把那种史诗感抽出来做成办公室/书房里的物件。"
    return f"这件是工作室候选，{concept}，更像内部审稿里挑出来的空间物件，不走普通公卖。"


def broker_hook(sku: str, concept: str, medium: str) -> str:  # type: ignore[no-redef]
    """Private-sales hook in clean Chinese copy.

    This second definition intentionally overrides the legacy mojibake strings
    above without touching candidate parsing.
    """
    if "AUSPICIOUS" in sku:
        return f"纽约这边刚筛出来的发财系实验件，{concept}。不是普通招财小摆件，是那种放在桌上会有压场感的质感。"
    if "CYBER" in sku:
        return f"这张是赛博书房线的候选，{concept}。适合那种不想买廉价装饰、但又想要一点未来感和冷质感的人。"
    if "EPIC" in sku:
        return f"这件偏硬核，{concept}。不是游戏周边，是把那种史诗感抽出来，做成办公室或书房里能压住空间的物件。"
    return f"这件是工作室候选，{concept}。更像内部审稿里挑出来的空间物件，不走普通公卖。"


def read_candidates() -> list[ExtensionSpec]:
    if not IN_CSV.exists():
        raise FileNotFoundError(IN_CSV)
    specs: list[ExtensionSpec] = []
    with IN_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if clean(row.get("Gate_Status")) != "FIRST_AUDIT_EXTENSION_READY":
                continue
            sku = clean(row.get("SKU"))
            concept = clean(row.get("Concept")) or sku
            vector = clean(row.get("Product_Vector"))
            tier, rrp = tier_and_price(vector)
            theme = theme_for_sku(sku)
            rank = int(float(clean(row.get("Candidate_Rank")) or 0))
            specs.append(
                ExtensionSpec(
                    rank=rank,
                    sku=sku,
                    concept=concept,
                    medium=vector,
                    tier=tier,
                    rrp=rrp,
                    source_file=clean(row.get("Selected_File")),
                    production_file=clean(row.get("Production_Design_File")),
                    printify_product_id=clean(row.get("Printify_Product_ID")),
                    broker_hook=broker_hook(sku, concept, vector),
                    cultural_anchor=theme["anchor"],
                    material_illusion=theme["material"],
                    spatial_recommendation=theme["space"],
                    objection_handling="This is a candidate for THE FIRST AUDIT numbering. It should stay private until Rex/Grey approve promotion; fulfillment would use Printify sample production with an expected 10-14 day physical turnaround.",
                )
            )
    return sorted(specs, key=lambda s: s.rank)


def write_csv(specs: list[ExtensionSpec]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = list(ExtensionSpec.__dataclass_fields__.keys())
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for spec in specs:
            writer.writerow(spec.__dict__)


def write_md(specs: list[ExtensionSpec]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(ET).strftime("%Y-%m-%d %H:%M:%S %Z")
    lines = [
        "# First Audit Extension Spec Sheets",
        "",
        f"Generated: {now}",
        "",
        "Purpose: convert the strongest extension candidates into private-review sales/spec copy without promoting them into THE FIRST AUDIT manifest yet.",
        "",
        "Rules:",
        "- Not for Etsy/eBay public listings.",
        "- Not yet final numbered Studio inventory.",
        "- Promote only after Rex/Grey visual approval.",
        "- Keep all assets out of low-price Etsy archive until downgraded explicitly.",
        "",
    ]
    for spec in specs:
        lines.extend(
            [
                f"## {spec.rank}. {spec.sku} - {spec.concept}",
                "",
                f"- **Medium:** {spec.medium}",
                f"- **Tier / RRP:** {spec.tier} / ${spec.rrp}",
                f"- **Printify Draft:** {spec.printify_product_id or 'pending'}",
                f"- **Source:** `{spec.source_file}`",
                f"- **Production Design:** `{spec.production_file}`",
                "",
                "### Broker Hook",
                spec.broker_hook,
                "",
                "### Studio Spec Sheet",
                f"- **Internal SKU:** {spec.sku}",
                f"- **Cultural Anchor:** {spec.cultural_anchor}",
                f"- **Material Illusion:** {spec.material_illusion}",
                f"- **Spatial Recommendation:** {spec.spatial_recommendation}",
                f"- **Objection Handling:** {spec.objection_handling}",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def main() -> None:
    specs = read_candidates()
    write_csv(specs)
    write_md(specs)
    print(f"[FIRST-AUDIT-EXTENSION-SPECS] specs={len(specs)} md={OUT_MD}")
    print(f"[FIRST-AUDIT-EXTENSION-SPECS] csv={OUT_CSV}")


if __name__ == "__main__":
    main()
