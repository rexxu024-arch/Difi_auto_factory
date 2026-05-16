from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules.resilient_http import request_with_retry

NY_TZ = ZoneInfo("America/New_York")
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
RAW_DIR = DATABASE / "Printify_Catalog_Raw"


@dataclass(frozen=True)
class ProductSpec:
    key: str
    label: str
    blueprint_id: int
    provider_id: int
    variant_id: int
    fallback_cost_cents: int
    fallback_shipping_cents: int
    fallback_print_area: str
    payload_note: str


PRODUCT_SPECS = {
    "Acrylic Block": ProductSpec(
        key="Acrylic Block",
        label="5x7 vertical acrylic photo block",
        blueprint_id=1471,
        provider_id=104,
        variant_id=106190,
        fallback_cost_cents=3543,
        fallback_shipping_cents=1599,
        fallback_print_area="front:1538x2138",
        payload_note="Use one vertical full-frame production image; no sticker cut lines.",
    ),
    "Framed Poster": ProductSpec(
        key="Framed Poster",
        label="12x18 black-frame fine-art poster",
        blueprint_id=1236,
        provider_id=105,
        variant_id=93818,
        fallback_cost_cents=2200,
        fallback_shipping_cents=1389,
        fallback_print_area="front:3600x5400",
        payload_note="Use vertical edge-to-edge art; do not add cut contour or border.",
    ),
    "Canvas": ProductSpec(
        key="Canvas",
        label='12x18 premium 1.6" canvas art wrap',
        blueprint_id=1936,
        provider_id=72,
        variant_id=119906,
        fallback_cost_cents=2600,
        fallback_shipping_cents=1629,
        fallback_print_area="front:3592x5387",
        payload_note="Keep critical subject inside safe center; allow premium wrap margin.",
    ),
    "Premium Matte Poster": ProductSpec(
        key="Premium Matte Poster",
        label="12x18 premium matte vertical poster",
        blueprint_id=282,
        provider_id=99,
        variant_id=43138,
        fallback_cost_cents=600,
        fallback_shipping_cents=700,
        fallback_print_area="front:3600x5400",
        payload_note="Use as lower-cost private sample proof, not as the prestige hero.",
    ),
}


SHOWCASE = [
    {
        "batch": "A",
        "sku": "OC-NYC-JADE-001",
        "name": "Song Mountain in Smoky Jade",
        "product": "Framed Poster",
        "retail_cents": 19900,
        "narrative": "纽约独立工作室以烟熏玉重构宋代山水。远看是极简书房画，近看有玉层、雾脉与隐约金线，适合送给懂克制的人。",
        "prompt": "western minimalist geometric reconstruction of Song dynasty ink landscape, mountains carved from smoky jade slabs, subtle kintsugi gold vein repair, brushed brass horizon grid, negative space like a private collector study, museum-grade fine art paper texture, Rembrandt lighting, physical material illusion, quiet luxury apartment decor, no text, no signature --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "A",
        "sku": "OC-NYC-JADE-002",
        "name": "Scholar Stone Meridian",
        "product": "Acrylic Block",
        "retail_cents": 28900,
        "narrative": "一块像被时间压实的烟熏玉供石。内部有黄铜经纬线与云气折射，放在书桌或玄关像一个安静的身份暗号。",
        "prompt": "single scholar rock relic carved from smoky jade and cyber-obsidian, internal brushed brass meridian lines suspended inside translucent stone, refractive acrylic depth, soft internal glow, subtle mist trapped in layers, high-end object photography, black walnut desk shadow, gallery collectible, no text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "batch": "A",
        "sku": "OC-NYC-JADE-003",
        "name": "Ink Pavilion Geometry",
        "product": "Canvas",
        "retail_cents": 22900,
        "narrative": "亭台只剩结构，山水只剩气。用包豪斯几何压住东方意象，适合想要东方但不想显得土的人。",
        "prompt": "Bauhaus geometric abstraction of a Song dynasty riverside pavilion, ink wash atmosphere reduced into smoky jade planes, brushed brass contour architecture, impasto canvas texture, quiet old-money study room, restrained palette of jade black ivory and aged gold, cinematic side light, no text, no signature --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "A",
        "sku": "OC-NYC-JADE-004",
        "name": "Snow Pine Study Window",
        "product": "Framed Poster",
        "retail_cents": 18900,
        "narrative": "像纽约冬夜里的一扇东方书房窗。雪、松、玉色与铜框并置，低调但有家族书卷气。",
        "prompt": "minimal east-west study window composition, ancient pine silhouette behind frosted glass, smoky jade mountain reflection, brushed brass window frame, Song ink negative space, museum print texture, deep winter quiet, quiet luxury reading room decor, no text, no signature --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "B",
        "sku": "OC-NYC-OBS-005",
        "name": "Obsidian Guardian Field",
        "product": "Acrylic Block",
        "retail_cents": 29900,
        "narrative": "黑曜石神兽不露全形，只留下气场轮廓。适合办公室、玄关、合伙人开业礼，镇而不俗。",
        "prompt": "abstract guardian beast silhouette made of cyber-obsidian and smoky jade dust, barely visible mythic outline, faint neon blue qi field, brushed brass talisman geometry, refractive acrylic block depth, cinematic black background, elite office entrance object, no text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "batch": "B",
        "sku": "OC-NYC-QI-006",
        "name": "Bauhaus Taiji Meridian",
        "product": "Framed Poster",
        "retail_cents": 17900,
        "narrative": "太极被压缩成极简建筑语言。不是玄学装饰，而是办公室里能让人看懂气场的现代符号。",
        "prompt": "minimal Bauhaus taiji diagram as luxury architectural poster, smoky jade black and ivory fields, brushed brass meridian arcs, subtle paper grain, precise geometry, quiet executive office energy, negative space, museum-grade framed print composition, no Chinese characters, no text --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "B",
        "sku": "OC-NYC-GATE-007",
        "name": "Black Jade Threshold",
        "product": "Canvas",
        "retail_cents": 23900,
        "narrative": "一扇没有门牌的门。黑玉、铜线与微光构成入口感，给办公室和玄关一层不解释的压迫感。",
        "prompt": "abstract threshold gate made from black jade slabs and brushed brass seams, minimalist sacred architecture, faint cyan internal glow, cinematic fog, impasto canvas texture, high-status foyer wall art, no text, no logo, no figurative person --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "C",
        "sku": "OC-NYC-KID-008",
        "name": "Qilin Cub Study Lamp",
        "product": "Acrylic Block",
        "retail_cents": 24900,
        "narrative": "给孩子房间的文化火种：不是教材插图，而是一只像顶级动画电影道具的玉麒麟幼兽。",
        "prompt": "premium 3D animated film quality qilin cub curled beside a small scholar lamp, white jade horns, smoky jade mane, warm brass lantern glow, gentle mythology silhouette, collectible nursery-study object, no text, no branded character, ultra polished material detail, refractive acrylic presentation --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "batch": "C",
        "sku": "OC-NYC-KID-009",
        "name": "Azure Dragon Reading Cloud",
        "product": "Framed Poster",
        "retail_cents": 16900,
        "narrative": "一条不凶的青龙，藏在孩子阅读角的云层里。文化身份感足够强，但视觉依旧现代干净。",
        "prompt": "modern picture-book mythic azure dragon made of jade mist curling around a reading cloud, gentle premium children's study room art, soft Rembrandt-style warm light, minimal background, smoky jade and ivory palette, no text, no cartoon IP, museum paper texture --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "C",
        "sku": "OC-NYC-KID-010",
        "name": "Moon Rabbit Archive",
        "product": "Canvas",
        "retail_cents": 19900,
        "narrative": "月兔不再可爱化，而像一枚被收藏的家族徽章。适合学习房，也适合想留下东方记忆的家庭。",
        "prompt": "minimal mythic moon rabbit archive emblem, white jade rabbit silhouette inside smoky moonstone halo, brushed brass star map grid, soft impasto canvas texture, premium children's study room meets family heritage, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "D",
        "sku": "OC-NYC-GIFT-011",
        "name": "Abyss Blue Gold Strata",
        "product": "Canvas",
        "retail_cents": 25900,
        "narrative": "剥离所有东方符号，只留下深海蓝、金属层理和收藏级肌理。适合作为开业、乔迁的安全高端礼。",
        "prompt": "deep sea blue and antique gold abstract strata painting, thick impasto texture, brushed brass mineral veins, smoky translucent resin depth, large collector-grade canvas, quiet luxury penthouse decor, no symbols, no text, no signature --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "D",
        "sku": "OC-NYC-GIFT-012",
        "name": "Lithographic Tower Blueprint",
        "product": "Framed Poster",
        "retail_cents": 19900,
        "narrative": "像从建筑档案馆偷出的蓝图。光刻线、铜粉、深蓝纸面，给商务空间一种“懂行”的社交筹码。",
        "prompt": "academic photolithography architectural tower blueprint, dark navy archival paper, brushed brass ink lines, deconstructivist geometry, museum drafting table precision, luxury office wall art, no readable text, no numbers, no watermark --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "D",
        "sku": "OC-NYC-GIFT-013",
        "name": "Opening Vessel in Blue Brass",
        "product": "Acrylic Block",
        "retail_cents": 27900,
        "narrative": "为开业礼准备的抽象容器。像蓝金矿石里封着一口光，昂贵、干净、不会显得过度讨好。",
        "prompt": "abstract ceremonial vessel made from deep ocean blue mineral glass and brushed brass seams, internal amber light core, refractive acrylic depth, high-end corporate opening gift, museum object photography, black velvet background, no text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "batch": "E",
        "sku": "OC-NYC-BLOOD-014",
        "name": "Smoky Jade Venus Fragment",
        "product": "Acrylic Block",
        "retail_cents": 31900,
        "narrative": "西方人看见古典雕塑，华人看见玉质与断裂隐喻。它适合需要品味压制、但不想解释太多的场合。",
        "prompt": "classical torso fragment reminiscent of ancient museum sculpture, carved entirely from smoky jade and moonstone, broken edges repaired with subtle kintsugi gold, refractive acrylic depth, black museum plinth, Rembrandt lighting, no exact copyrighted artwork, no text, no signature --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "batch": "E",
        "sku": "OC-NYC-BLOOD-015",
        "name": "Rembrandt Scholar Heir",
        "product": "Framed Poster",
        "retail_cents": 22900,
        "narrative": "一张看似欧洲古典肖像的继承人画像，细节里却藏着玉扣、铜纹与东方书卷气。",
        "prompt": "fictional old-master inspired portrait of a young scholar heir, Rembrandt lighting, dark umber background, smoky jade collar clasp, brushed brass embroidery details, museum oil painting surface, original anonymous subject, no celebrity, no text, no signature --v 6.1 --ar 2:3 --style raw --no watermark",
    },
    {
        "batch": "E",
        "sku": "OC-NYC-BLOOD-016",
        "name": "Jade Apollo Study",
        "product": "Canvas",
        "retail_cents": 26900,
        "narrative": "希腊式形体，东方玉质骨相。放在客厅像欧洲美术馆，近看才露出东方材质的反击。",
        "prompt": "classical Apollo-like study bust as an original museum object, translucent smoky jade and aged marble composite, brushed brass fracture lines, impasto canvas reproduction texture, dramatic chiaroscuro, elite collector room decor, no exact copyrighted sculpture, no text --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "E",
        "sku": "OC-NYC-BLOOD-017",
        "name": "Provenance Portrait in Jade Light",
        "product": "Framed Poster",
        "retail_cents": 21900,
        "narrative": "像有出处的家族旧藏，但人物完全虚构。用欧洲画面秩序，装进东方材质密码。",
        "prompt": "fictional museum provenance portrait, anonymous aristocratic figure in dark velvet, smoky jade light reflecting from a scholar stone, brushed brass frame glow, old-master chiaroscuro, fine art paper grain, no real person, no artist imitation, no text --v 6.1 --ar 2:3 --style raw --no watermark",
    },
    {
        "batch": "F",
        "sku": "OC-NYC-VINT-018",
        "name": "1960s NYC Jazz Tunnel",
        "product": "Framed Poster",
        "retail_cents": 18900,
        "narrative": "给真正喜欢美国复古文化的人。不是廉价怀旧，而是纽约爵士、胶片颗粒和铜色灯光的高级复燃。",
        "prompt": "1960s New York jazz tunnel poster, cinematic film grain, smoky saxophone light without visible performers, wet brick, brushed brass subway reflections, elevated vintage aesthetic, museum poster composition, no readable text, no logo, no celebrity --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "F",
        "sku": "OC-NYC-VINT-019",
        "name": "Route 66 Neon Relic",
        "product": "Canvas",
        "retail_cents": 22900,
        "narrative": "美式公路文化被重新做成高级墙面艺术。霓虹、尘土、废墟，但没有廉价旅游纪念品感。",
        "prompt": "Route 66 neon ruin reconstructed as luxury vintage wall art, desert dusk, faded turquoise and amber neon, cracked chrome, cinematic dust, impasto canvas texture, elevated Americana, no readable signs, no brands, no watermark --v 6.1 --ar 2:3 --style raw --no skin, person, text",
    },
    {
        "batch": "F",
        "sku": "OC-NYC-VINT-020",
        "name": "Old Hollywood Rain Lot",
        "product": "Acrylic Block",
        "retail_cents": 26900,
        "narrative": "复古好莱坞不靠明星脸，而靠雨夜片场、灯架和玻璃反光。给懂电影感的人一个桌面藏品。",
        "prompt": "old Hollywood studio backlot in rain, no actors, no celebrities, vintage tungsten lights, wet black pavement, chrome camera silhouettes, smoky amber glow, refractive acrylic block depth, elevated film-noir collectible, no text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
]


def now_stamp() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %z")


def headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {Config.Printify_API_KEY}"}


def cached_get(path: str, cache_name: str) -> object:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    cache = RAW_DIR / cache_name
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    url = f"{Config.Printify_API_URL.rstrip('/')}{path}"
    response = request_with_retry("GET", url, headers=headers(), timeout=35, attempts=3)
    response.raise_for_status()
    data = response.json()
    cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def items(data: object, *keys: str) -> list[dict]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
    return []


def cost_for_variant(variant: dict, fallback: int) -> int:
    for key in ("cost", "price", "cost_cents"):
        value = variant.get(key)
        if isinstance(value, (int, float)) and value > 0:
            return int(value)
    return fallback


def print_area_for_variant(variant: dict, fallback: str) -> str:
    parts = []
    for item in variant.get("placeholders") or []:
        if isinstance(item, dict) and item.get("width") and item.get("height"):
            parts.append(f"{item.get('position') or 'front'}:{item['width']}x{item['height']}")
    return " | ".join(parts) or fallback


def shipping_for_variant(data: object, variant_id: int, fallback: int) -> int:
    for profile in items(data, "profiles", "shipping", "data"):
        variant_ids = {str(x) for x in profile.get("variant_ids") or []}
        if str(variant_id) not in variant_ids:
            continue
        first = profile.get("first_item") or {}
        value = first.get("cost")
        if isinstance(value, (int, float)) and value > 0:
            return int(value)
    return fallback


def load_product_vector(spec: ProductSpec) -> dict[str, object]:
    try:
        variants_data = cached_get(
            f"/catalog/blueprints/{spec.blueprint_id}/print_providers/{spec.provider_id}/variants.json",
            f"blueprint_{spec.blueprint_id}_provider_{spec.provider_id}_variants.json",
        )
        shipping_data = cached_get(
            f"/catalog/blueprints/{spec.blueprint_id}/print_providers/{spec.provider_id}/shipping.json",
            f"blueprint_{spec.blueprint_id}_provider_{spec.provider_id}_shipping.json",
        )
        variants = items(variants_data, "variants", "data")
        variant = next((x for x in variants if int(x.get("id") or 0) == spec.variant_id), {})
        unit_cost = cost_for_variant(variant, spec.fallback_cost_cents)
        shipping = shipping_for_variant(shipping_data, spec.variant_id, spec.fallback_shipping_cents)
        print_area = print_area_for_variant(variant, spec.fallback_print_area)
        title = variant.get("title") or spec.label
    except Exception:
        unit_cost = spec.fallback_cost_cents
        shipping = spec.fallback_shipping_cents
        print_area = spec.fallback_print_area
        title = spec.label
    return {
        "blueprint_id": spec.blueprint_id,
        "print_provider_id": spec.provider_id,
        "variant_id": spec.variant_id,
        "variant_title": title,
        "unit_cost_cents": unit_cost,
        "shipping_first_cents": shipping,
        "landed_cost_cents": unit_cost + shipping,
        "print_area": print_area,
        "payload_note": spec.payload_note,
    }


def usd(cents: int) -> str:
    return f"${cents / 100:.2f}"


def private_title(item: dict[str, object]) -> str:
    return f"{item['name']} - OpenClaw NYC Private Atelier"


def private_description(item: dict[str, object], row: dict[str, object]) -> str:
    return (
        f"{item['name']} is a private OpenClaw Design Studio showcase object, prepared for direct-client presentation rather than public marketplace SEO. "
        f"{item['narrative']} "
        f"Production is anchored to Printify {row['recommended_blueprint']} fulfillment, with a single full-frame artwork file matched to {row['print_area']}. "
        "This private draft is intended for client review, partner sales conversations, and future direct-order fulfillment."
    )


def build() -> None:
    DATABASE.mkdir(exist_ok=True)
    REVIEW.mkdir(exist_ok=True)
    vectors = {key: load_product_vector(spec) for key, spec in PRODUCT_SPECS.items()}
    rows = []
    for item in SHOWCASE:
        vector = vectors[item["product"]]
        landed = int(vector["landed_cost_cents"])
        min_400 = landed * 5
        retail = max(int(item["retail_cents"]), min_400)
        rows.append(
            {
                **item,
                "recommended_blueprint": item["product"],
                "blueprint_id": vector["blueprint_id"],
                "print_provider_id": vector["print_provider_id"],
                "variant_id": vector["variant_id"],
                "variant_title": vector["variant_title"],
                "print_area": vector["print_area"],
                "estimated_unit_cost_usd": usd(int(vector["unit_cost_cents"])),
                "estimated_shipping_usd": usd(int(vector["shipping_first_cents"])),
                "estimated_landed_cost_usd": usd(landed),
                "minimum_400_markup_usd": usd(min_400),
                "recommended_retail_usd": usd(retail),
            }
        )
        rows[-1]["printify_private_title"] = private_title(item)
        rows[-1]["printify_private_description"] = private_description(item, rows[-1])
        rows[-1]["payload_json"] = json.dumps(
            {
                "title": rows[-1]["printify_private_title"],
                "description": rows[-1]["printify_private_description"],
                "blueprint_id": vector["blueprint_id"],
                "print_provider_id": vector["print_provider_id"],
                "variants": [{"id": vector["variant_id"], "price": retail, "is_enabled": True, "sku": item["sku"]}],
                "print_areas": [{"variant_ids": [vector["variant_id"]], "placeholders": []}],
                "internal_sku": item["sku"],
                "publish_policy": "PRINTIFY_DRAFT_ONLY_DO_NOT_SYNC_MARKETPLACE",
                "note": vector["payload_note"],
            },
            ensure_ascii=False,
        )

    csv_path = DATABASE / "Shock_And_Awe_Showcase_Roster.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    queue_path = DATABASE / "Shock_And_Awe_Printify_Private_Queue.csv"
    queue_fields = [
        "Internal_SKU",
        "Status",
        "Printify_Private_Title",
        "Printify_Private_Description",
        "Product_Type",
        "Blueprint_ID",
        "Provider_ID",
        "Variant_ID",
        "Print_Area",
        "Recommended_Retail_USD",
        "Production_Image_Path",
        "Printify_Product_ID",
        "Payload_JSON",
    ]
    with queue_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=queue_fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "Internal_SKU": row["sku"],
                    "Status": "WAITING_FOR_MJ_IMAGE_QA",
                    "Printify_Private_Title": row["printify_private_title"],
                    "Printify_Private_Description": row["printify_private_description"],
                    "Product_Type": row["recommended_blueprint"],
                    "Blueprint_ID": row["blueprint_id"],
                    "Provider_ID": row["print_provider_id"],
                    "Variant_ID": row["variant_id"],
                    "Print_Area": row["print_area"],
                    "Recommended_Retail_USD": row["recommended_retail_usd"],
                    "Production_Image_Path": "",
                    "Printify_Product_ID": "",
                    "Payload_JSON": row["payload_json"],
                }
            )

    md_path = REVIEW / "OPERATION_SHOCK_AND_AWE_SPEC_SHEETS_20260509.md"
    lines = [
        "# Operation Shock and Awe - Private Showcase Spec Sheets",
        "",
        f"Generated: {now_stamp()}",
        "",
        "Scope: private-client showcase only. Do not generate eBay/Etsy public listing copy from this packet.",
        "Supply chain: Printify acrylic blocks, framed posters, and canvas products. China image API is intentionally out of scope for Phase 1.",
        "",
        "## Printify Anchors",
    ]
    for key, vector in vectors.items():
        lines.extend(
            [
                f"### {key}",
                f"- Blueprint / provider / variant: {vector['blueprint_id']} / {vector['print_provider_id']} / {vector['variant_id']}",
                f"- Variant: {vector['variant_title']}",
                f"- Print area: {vector['print_area']}",
                f"- Estimated unit + first shipping: {usd(int(vector['unit_cost_cents']))} + {usd(int(vector['shipping_first_cents']))} = {usd(int(vector['landed_cost_cents']))}",
                f"- Payload note: {vector['payload_note']}",
                "",
            ]
        )
    lines.append("## Studio Spec Sheets")
    for row in rows:
        lines.extend(
            [
                f"### {row['sku']} - {row['name']}",
                f"- Batch: {row['batch']}",
                f"- Concept Narrative: {row['narrative']}",
                f"- Printify Private Title: {row['printify_private_title']}",
                f"- Printify Private Description: {row['printify_private_description']}",
                f"- Midjourney Master Prompt: `{row['prompt']}`",
                "- Printify Production Vector:",
                f"  - Recommended Blueprint: {row['recommended_blueprint']} ({row['variant_title']})",
                f"  - Blueprint / provider / variant: {row['blueprint_id']} / {row['print_provider_id']} / {row['variant_id']}",
                f"  - Print area: {row['print_area']}",
                f"  - Estimated base + shipping: {row['estimated_unit_cost_usd']} + {row['estimated_shipping_usd']} = {row['estimated_landed_cost_usd']}",
                f"  - Recommended Retail Price: {row['recommended_retail_usd']} (minimum 400% markup guard: {row['minimum_400_markup_usd']})",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[SHOCK-AND-AWE] roster={csv_path}")
    print(f"[SHOCK-AND-AWE] private_printify_queue={queue_path}")
    print(f"[SHOCK-AND-AWE] specs={md_path}")


if __name__ == "__main__":
    build()
