"""Build the First Audit Cyber-Renaissance draft queue.

This queue is for concept-grid review only. It does not create marketplace
listings, does not publish to Printify, and does not authorize Midjourney
upscale. Rex must visually promote a grid result before any hero production
or luxury mockup work happens.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "Database"
REVIEW_DIR = ROOT / "Review_Packets" / "First_Audit_001"
OUT_CSV = DATABASE / "First_Audit_Cyber_Renaissance_Draft_Queue.csv"
OUT_MD = REVIEW_DIR / "FIRST_AUDIT_CYBER_RENAISSANCE_DRAFT_QUEUE.md"
ET = ZoneInfo("America/New_York")


@dataclass
class DraftConcept:
    id: str
    code_name_cn: str
    battlefield: str
    product_vector: str
    blueprint_id: int
    provider_id: int
    variant_id: int
    studio_tier: str
    rrp_usd: int
    cultural_frame: str
    material_thesis: str
    broker_hook_cn: str
    private_dm_cn: str
    mj_prompt: str
    status: str = "READY_FOR_MJ_DRAFT_GRID_ONLY_NO_UPSCALE"
    upscale_policy: str = "NO_UPSCALE_UNTIL_REX_TOP1_APPROVAL"


ANCHORS = {
    "acrylic": ("Optical Acrylic Block 5x7", 1471, 104, 106190, "Core optical relic", 128),
    "poster": ("Archival Framed Studio Print 12x18", 1236, 105, 93818, "Entrance studio print", 48),
    "canvas": ("Gallery Canvas Art Wrap 12x18", 1936, 72, 119906, "Anchor study canvas", 295),
}


RAW_CONCEPTS = [
    ("FA-CR-010", "巴别塔冷玉核心", "Classical Ruin / Babel", "acrylic", "the Tower of Babel as an unfinished algorithmic ziggurat, cold jade core visible through fractured stone, liquid chrome scaffolding, tiny unreadable brass drafting marks"),
    ("FA-CR-011", "维特鲁威铬骨架", "Da Vinci Manuscript / Anatomy", "poster", "Vitruvian proportional diagram rebuilt as brushed titanium and unpolished jade armature, Renaissance notebook geometry, no readable letters"),
    ("FA-CR-012", "达芬奇水力机关", "Da Vinci Manuscript / Engineering", "poster", "Leonardo-style hydraulic engine reimagined as smoky glass pistons and jade pressure chambers, sepia vellum field, abstract engineering marks"),
    ("FA-CR-013", "拉奥孔液态线圈", "Classical Sculpture / Tension", "canvas", "Laocoon group tension abstracted into liquid chrome coils around a cracked marble torso silhouette, chiaroscuro fog, museum darkness"),
    ("FA-CR-014", "帕台农雨夜控制台", "Greek Architecture / Control Room", "poster", "Parthenon triglyph geometry fused with a rain-lit cybernetic console, smoky jade indicators, black titanium rails, no letters"),
    ("FA-CR-015", "卡拉瓦乔棱镜礼拜堂", "Baroque Light / Chapel", "acrylic", "Caravaggio chiaroscuro chapel interior containing a levitating refractive prism reliquary, cold jade light, heavy optical glass depth"),
    ("FA-CR-016", "皮拉内西数据监牢", "Piranesi / Imaginary Prison", "poster", "Piranesi imaginary prison rebuilt as a data archive, impossible staircases, brushed brass railings, jade fog nodes, architectural engraving texture"),
    ("FA-CR-017", "枯山水铬石庭", "Rock Garden / Minimal Authority", "acrylic", "karesansui rock garden translated into black titanium raked lines and unpolished jade monoliths, silent executive object, gallery-grade negative space"),
    ("FA-CR-018", "荷兰静物反应堆", "Dutch Still Life / Wealth Signal", "canvas", "Dutch golden age still life composition with fruit replaced by smoky jade vessels and liquid chrome pearls, candlelit Rembrandt shadows, no text"),
    ("FA-CR-019", "美第奇星象室", "Medici Observatory / Power", "acrylic", "private Medici observatory cabinet, brass astrolabe rings, cold jade celestial lens, refractive glass dome, aristocratic science aura"),
    ("FA-CR-020", "罗塞塔霓虹碑", "Ancient Tablet / Translation", "poster", "Rosetta stone silhouette reconstructed as translucent obsidian slab with cyan neon strata, no readable script, museum artifact lighting"),
    ("FA-CR-021", "拜占庭电路圣像", "Byzantine Icon / Circuitry", "acrylic", "Byzantine icon panel without human figure, halo geometry rebuilt from gold circuit traces and smoky jade enamel, black glass shrine depth"),
    ("FA-CR-022", "炼金炉玻璃心脏", "Alchemy / Furnace", "acrylic", "Renaissance alchemical furnace with a heavy refractive glass heart, kintsugi cracks, blue-green internal glow, brushed brass valves"),
    ("FA-CR-023", "哥特唱诗算法", "Gothic Cathedral / Sound", "poster", "gothic choir vaults translated into waveform architecture, black stone ribs, jade resonance nodes, cinematic fog diffusion"),
    ("FA-CR-024", "阿特拉斯冷玉负重", "Atlas / Burden", "canvas", "Atlas myth reduced to a monumental jade sphere pressing into a titanium plinth, no human body, only weight and shadow, severe gallery composition"),
    ("FA-CR-025", "俄耳甫斯黑镜琴", "Orpheus / Music Relic", "acrylic", "Orpheus lyre abstracted into a black mirror instrument, liquid chrome strings, smoky jade resonance chamber, no figure, private music-room relic"),
    ("FA-CR-026", "阿波罗冷光镜", "Apollo / Solar Order", "poster", "Apollo sun order rebuilt as a cold optical lens array, brushed titanium rays, unpolished jade center, precise museum poster composition"),
    ("FA-CR-027", "西西弗斯工作台", "Sisyphus / Executive Burden", "poster", "Sisyphus myth translated into an empty executive workstation, massive jade sphere half-lit on black walnut, no person, philosophical office pressure"),
    ("FA-CR-028", "记忆女神档案柜", "Mnemosyne / Archive", "acrylic", "Mnemosyne memory archive as stacked translucent glass drawers, smoky jade catalog cores, brass index rails, quiet luxury study object"),
    ("FA-CR-029", "贝尼尼雾化衣褶", "Baroque Sculpture / Vapor", "canvas", "Bernini-like marble drapery abstracted into frozen fog and liquid chrome folds, cold jade shadow veins, dramatic gallery spotlight"),
    ("FA-CR-030", "水星凌日标本柜", "Astronomy / Transit", "acrylic", "Mercury transit specimen cabinet, black glass astronomical plate, brushed brass orbit arcs, tiny jade planet glow, no readable numbers"),
]


def lens_suffix(product: str) -> str:
    if product == "acrylic":
        return "shot on 85mm lens, f/8, ultra-sharp focus, object photography, high refractive depth"
    return "shot on 85mm lens, f/8, ultra-sharp focus, gallery-grade flat artwork capture"


def build_prompt(subject: str, product: str) -> str:
    aspect = "5:7" if product == "acrylic" else "2:3"
    return (
        f"{subject}, Cyber-Renaissance private atelier artwork, 2026 digital computation physically reconstructing classical civilization, "
        "brushed titanium finish, unpolished smoky jade, liquid chrome, kintsugi hairline fractures, cinematic fog diffusion, "
        "chiaroscuro lighting, dappled museum light, physically plausible surfaces, no cheap fantasy, no anime, "
        f"{lens_suffix(product)}, draft concept grid only, no upscale --v 6.1 --ar {aspect} --style raw --stylize 700 --chaos 35 "
        "--no readable text, typography, watermark, logo, signature, skin, person, face, blurry edges"
    )


def concepts() -> list[DraftConcept]:
    out: list[DraftConcept] = []
    for row in RAW_CONCEPTS:
        ident, cn, battlefield, product, subject = row
        vector, blueprint, provider, variant, tier, rrp = ANCHORS[product]
        out.append(
            DraftConcept(
                id=ident,
                code_name_cn=cn,
                battlefield=battlefield,
                product_vector=vector,
                blueprint_id=blueprint,
                provider_id=provider,
                variant_id=variant,
                studio_tier=tier,
                rrp_usd=rrp,
                cultural_frame=battlefield,
                material_thesis="冷玉、液态铬、拉丝钛金与加厚光学亚克力/典藏版画语言融合，目标是智力优越感与物理材质错觉同时成立。",
                broker_hook_cn=f"这件走的是赛博古典线，{cn}。不是便宜装饰，是把古典文明的骨架重新压进冷玉和金属里的工作室实验件。",
                private_dm_cn=f"这个我会建议你先看场景图：{cn} 不是烂大街奢侈品逻辑，它更像一个有典故的空间物件。适合放在书房、玄关或办公室，靠气场而不是 logo 说话。",
                mj_prompt=build_prompt(subject, product),
            )
        )
    return out


def write_csv(rows: list[DraftConcept]) -> None:
    DATABASE.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_md(rows: list[DraftConcept]) -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(ET).strftime("%Y-%m-%d %H:%M:%S %Z")
    lines = [
        "# First Audit Cyber-Renaissance Draft Queue",
        "",
        f"Generated: {now}",
        "",
        "Purpose: fill the First Audit concept pool toward 30 units without spending Midjourney upscale minutes.",
        "",
        "Hard rules:",
        "- Draft grids only. Do not run Upscale Creative/Subtle until Rex promotes a Top 1% image.",
        "- No Etsy/eBay listing text. These are private Studio candidates.",
        "- Product vectors are restricted to Acrylic Block, Framed Studio Print, or Canvas Art Wrap.",
        "- Prompts must use historical/classical composition plus cold jade/liquid chrome/cyber-classical material logic.",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row.id} - {row.code_name_cn}",
                "",
                f"- **Battlefield:** {row.battlefield}",
                f"- **Product Vector:** {row.product_vector}",
                f"- **Printify:** blueprint {row.blueprint_id}, provider {row.provider_id}, variant {row.variant_id}",
                f"- **Tier / RRP:** {row.studio_tier} / ${row.rrp_usd}",
                f"- **Status:** {row.status}",
                "",
                "### Broker Hook",
                row.broker_hook_cn,
                "",
                "### 1v1 Private DM",
                row.private_dm_cn,
                "",
                "### MJ Master Prompt",
                row.mj_prompt,
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def main() -> None:
    rows = concepts()
    write_csv(rows)
    write_md(rows)
    print(f"[FIRST-AUDIT-CYBER-RENAISSANCE] draft_concepts={len(rows)}")
    print(f"[FIRST-AUDIT-CYBER-RENAISSANCE] csv={OUT_CSV}")
    print(f"[FIRST-AUDIT-CYBER-RENAISSANCE] md={OUT_MD}")


if __name__ == "__main__":
    main()
