from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
NY = ZoneInfo("America/New_York")


PRODUCTS = {
    "Acrylic Block": {
        "target_code": "Acrylic Blocks (user/Grey target 107)",
        "blueprint_id": 1471,
        "provider_id": 104,
        "variant_id": 106190,
        "variant": "5x7 vertical photo block",
        "print_area": "front:1538x2138",
        "cost": "$35.43",
        "shipping": "$15.99",
        "retail": "$289.00",
        "note": "Official Printify 1471 Photo Block. User/Grey code 107 is not a valid catalog blueprint in current API.",
    },
    "Framed Poster": {
        "target_code": "Premium Framed Canvas (user/Grey target 118)",
        "blueprint_id": 1236,
        "provider_id": 105,
        "variant_id": 93818,
        "variant": "12x18 vertical black-frame fine-art poster",
        "print_area": "front:3600x5400",
        "cost": "$22.00",
        "shipping": "$13.89",
        "retail": "$199.00",
        "note": "Official Printify 1236 Framed Paper Posters. User/Grey code 118 is not a valid catalog blueprint in current API.",
    },
    "Canvas": {
        "target_code": "Premium Framed Canvas / Canvas tower product",
        "blueprint_id": 1936,
        "provider_id": 72,
        "variant_id": 119906,
        "variant": "12x18 vertical 1.6in canvas art wrap",
        "print_area": "front:3592x5387",
        "cost": "$26.00",
        "shipping": "$16.29",
        "retail": "$229.00",
        "note": "Official Printify 1936 Canvas Art Wraps. Use when canvas texture matters more than frame.",
    },
}


ZONE2 = [
    {
        "batch": "2.1 Epic Mythology",
        "sku": "OC-NYC-EPIC-001",
        "name": "Frost Rune War Chalice",
        "product": "Acrylic Block",
        "private_copy": "北欧冰霜金属与暗金圣杯的混合体。不是游戏周边，而是一件像从失落王庭里挖出的桌面权力物。",
        "dm_pitch": "这款不是普通装饰画，更像一件桌面权力摆件。适合送给喜欢史诗感、收藏感和办公室气场的人，第一眼就能看出不是淘宝风。",
        "broker_hook": "纽约工作室哥们儿出的实验批次，这个冰霜圣杯质感很凶。不走公卖，想要这种桌面权力感的私我。",
        "emotional_value": "卖点不是杯子造型，而是把客户包装成有收藏癖、有史诗审美、有私人王座感的人。",
        "cultural_anchor": "借用北欧 rune stone 和圣杯遗物的西方文化记忆，但不指向任何具体 IP。冰霜金属、暗金和烟熏玉形成一种王权遗物感。",
        "buyer_profile": "适合喜欢史诗游戏、奇幻文学、男士办公室摆件、收藏型礼品的客户。",
        "placement_scene": "办公桌、书架、展示柜、私人酒柜旁；适合小面积但需要强气场的位置。",
        "objection_reply": "它不是大众装饰，而是小批量实验样板；价格买的是材质错觉、故事密度和独立工作室定制感。",
        "prompt": "ancient war chalice forged from frost-blackened steel and dark antique gold, abstract Nordic rune engravings glowing under ice, ruined gothic altar background, brutal mythic atmosphere without any known game character, cinematic Rembrandt light, smoky jade undertone, premium museum object photography, no text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "batch": "2.1 Epic Mythology",
        "sku": "OC-NYC-EPIC-002",
        "name": "Gothic Ember Reliquary",
        "product": "Canvas",
        "private_copy": "暗金色哥特圣龛，像一座燃尽后的贵族教堂。适合高管办公室或私域礼品里最压场的一档。",
        "dm_pitch": "如果对方家里或办公室已经有普通挂画，这款走的是更重、更暗、更贵的路线，适合做乔迁、开业或书房主视觉。",
        "broker_hook": "这张不是普通墙画，是那种暗金哥特圣龛的压场货。办公室、书房想做出点老钱阴影感，这款可以看。",
        "emotional_value": "卖点是让空间从普通装修变成像有历史、有阴影、有阶层记忆的私人会客厅。",
        "cultural_anchor": "哥特教堂、圣物匣和伦勃朗式暗部光线是西方高阶视觉语言；它表达的是灾后仍保留权威的贵族感。",
        "buyer_profile": "适合成熟客户、老板办公室、深色家装、喜欢暗黑学院和宗教建筑气质的人。",
        "placement_scene": "书房主墙、办公室沙发背墙、深色木质家具旁；不适合太童趣或极简白墙空间。",
        "objection_reply": "这类图不靠可爱或流行梗，而靠空间气质；越是安静、深色、有木质或皮革家具的环境越显贵。",
        "prompt": "dark gold gothic reliquary shrine after a sacred fire, molten brass ribs, obsidian ash, ember light leaking through broken cathedral tracery, high fantasy dark-souls emotional tone but fully original, impasto canvas texture, collector-grade wall art, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "2.1 Epic Mythology",
        "sku": "OC-NYC-EPIC-003",
        "name": "Runestone Gate of Winter Kings",
        "product": "Framed Poster",
        "private_copy": "冬王石门，符文、冰霜、金属裂纹都压在一个画面里。给想要史诗感但不想买廉价 IP 图的人。",
        "dm_pitch": "这张适合喜欢游戏、奇幻、北欧感，但又不想把具体 IP 挂在家里的人。它有那个气质，但不会显得幼稚或侵权。",
        "broker_hook": "喜欢北欧史诗感但不想挂游戏周边的，看这个。它有那个气质，但没有任何具体 IP，成年人空间也能挂。",
        "emotional_value": "卖点是把玩家审美升级成成年人也能挂出来的史诗空间符号。",
        "cultural_anchor": "参考北欧石碑、王陵入口和古代铭文的形式感，用抽象符文代替可读文字，保留神秘感同时避开版权和宗教直指。",
        "buyer_profile": "适合游戏玩家升级审美、奇幻小说读者、年轻高净值客户、公寓书房。",
        "placement_scene": "电竞房、阅读角、书桌旁、黑白灰或冷色调卧室。",
        "objection_reply": "它不是游戏海报，而是把那种史诗情绪抽象成家居艺术，所以不会显得像粉丝周边。",
        "prompt": "colossal original runestone gate of winter kings, frost metal plates, ancient runes as abstract light marks, cracked black basalt, brushed brass fracture seams, cinematic northern fog, museum-grade framed poster composition, epic mythology without recognizable IP, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "2.1 Epic Mythology",
        "sku": "OC-NYC-EPIC-004",
        "name": "Ashen Valkyrie Helm Relic",
        "product": "Acrylic Block",
        "private_copy": "没有人物，只有一顶像被神话战争留下的头盔。桌摆尺寸，但气场像一件私人收藏馆藏品。",
        "dm_pitch": "这款适合放办公桌、书架、展示柜。不是可爱摆件，而是让桌面显得有故事、有力量感的小型收藏品。",
        "broker_hook": "这不是可爱摆件，是桌面战利品。放书架或办公桌，懂的人一眼知道你不是在买普通装饰。",
        "emotional_value": "卖点是给桌面一个小型英雄叙事，让普通工作区有私人藏品和战利品的感觉。",
        "cultural_anchor": "Valkyrie 是北欧神话中选择勇士命运的符号，这里只保留头盔和战后遗物感，不出现人物，避免廉价 cosplay 感。",
        "buyer_profile": "适合送男士、创业者、车库/书房收藏区、偏硬核审美的人。",
        "placement_scene": "桌面、陈列架、音响旁、深色灯光下；亚克力块的通透感会强化收藏品错觉。",
        "objection_reply": "尺寸不大，但适合做视觉锚点；真正的价值是让桌面从普通办公用品变成有故事的私人角落。",
        "prompt": "original ashen valkyrie helm relic on black stone plinth, frost iron wings reduced to abstract geometry, antique gold scar lines, smoky jade shadow reflections, dramatic museum macro photography, refractive acrylic depth, no known character, no text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "batch": "2.2 Cyber-Fusion",
        "sku": "OC-NYC-CYBER-005",
        "name": "Holographic Mechanical Buddha Hand",
        "product": "Acrylic Block",
        "private_copy": "东方外壳，西方科幻内核。机械佛手被全息蓝光拆解，适合做私域样板里的视觉记忆点。",
        "dm_pitch": "这款比较适合年轻一点、喜欢科技感和东方符号的人。不是传统佛像，是赛博艺术摆件，放桌面很容易被问链接。",
        "broker_hook": "这款赛博佛手很适合年轻人桌面，东方壳、西方科幻芯。不是传统佛像，是未来感艺术摆件。",
        "emotional_value": "卖点是让客户既显得懂东方符号，又显得不老派，像把未来感和文化底子同时拿在手里。",
        "cultural_anchor": "取东方手印的仪式感，但不做人脸和神像；用钛合金关节、全息投影和烟熏玉核心把它转成未来艺术物。",
        "buyer_profile": "适合留学生、科技行业、设计师、喜欢东方符号但不想要传统宗教摆件的人。",
        "placement_scene": "显示器旁、工作站、电竞桌、现代公寓玄关。",
        "objection_reply": "它不是宗教商品，而是把东方仪式感转译成未来材质；适合想要有文化但不老气的客户。",
        "prompt": "mechanical Buddha hand as an original cybernetic sculpture, brushed titanium joints, holographic neon projection layers, smoky jade palm core, no religious icon face, refractive acrylic depth, black studio product photography, ultra-premium sci-fi artifact, no text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "batch": "2.2 Cyber-Fusion",
        "sku": "OC-NYC-CYBER-006",
        "name": "Titanium Cyber Bonsai",
        "product": "Canvas",
        "private_copy": "盆景不再是传统雅物，而是一棵用拉丝钛合金、霓虹电路和黑玉根系构成的权力植物。",
        "dm_pitch": "这款适合新房、办公室、创业者空间。它保留盆景的雅，但加了科技和黑玉质感，不会像传统中式那么老气。",
        "broker_hook": "赛博盆景这款我觉得很适合新办公室，不老气，但有东方秩序感。创业者、科技圈应该会吃这个。",
        "emotional_value": "卖点是把克制、自律、增长和掌控感做成一个空间符号，适合创业者自我投射。",
        "cultural_anchor": "盆景本来象征控制、耐心和空间修养；这里用赛博材质重做，变成创业者和科技行业能理解的现代权力植物。",
        "buyer_profile": "适合科技行业、创业者、喜欢新中式但怕老气的人、办公室软装客户。",
        "placement_scene": "会议室、办公室、工作室入口、现代客厅。",
        "objection_reply": "这不是传统盆景图，而是把盆景的秩序感改造成科技材质，适合更年轻、更现代的空间。",
        "prompt": "cyber bonsai sculpture built from brushed titanium branches, black jade roots, neon circuit sap, minimalist dark luxury background, cinematic product lighting, impasto canvas texture, east shell west sci-fi core, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "2.2 Cyber-Fusion",
        "sku": "OC-NYC-CYBER-007",
        "name": "Neon Sutra Data Shrine",
        "product": "Framed Poster",
        "private_copy": "不是经文，也不出现可读文字。它只保留仪式感与数据流，适合年轻高净值客户的赛博书房。",
        "dm_pitch": "这张适合不想挂字、不想挂人物的人。看起来像未来宗教装置，适合书房、电竞房或高端公寓玄关。",
        "broker_hook": "这张适合不想挂字、不想挂人物的人。像未来宗教装置，放书房或玄关，会显得空间很聪明。",
        "emotional_value": "卖点是神秘、安静和高智感，让客户的空间看起来不像消费品陈列，而像未来档案室。",
        "cultural_anchor": "把卷轴、经文、数据流三种符号拆开，只保留漂浮和秩序，不给出任何可读文字，让它更像未来博物馆里的装置。",
        "buyer_profile": "适合喜欢安静科技感、抽象艺术、AI/金融/工程背景的客户。",
        "placement_scene": "玄关、书房、服务器/工作站区域、高端公寓走廊。",
        "objection_reply": "它故意不写字，因为写字会把艺术感拉低；保留抽象秩序，反而更适合长期挂在空间里。",
        "prompt": "abstract cyber shrine of floating data ribbons arranged like sacred scrolls, no readable characters, smoky jade glass panels, titanium frame, neon cyan and antique gold light, high-end gallery poster, futuristic ritual atmosphere, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "batch": "2.3 Cultural Assassin",
        "sku": "OC-NYC-ASSASSIN-008",
        "name": "Smoky Jade Spartan Helm",
        "product": "Acrylic Block",
        "private_copy": "西方人看见斯巴达，华人看见玉质和黑钛金。它的价值在于两边都看得懂，但都说不完全。",
        "dm_pitch": "这款最适合做文化套利：西方史诗符号加东方玉质感。送人时不用解释太多，一看就是昂贵、硬核、很有品位。",
        "broker_hook": "这款是文化套利核心款：斯巴达轮廓加烟熏玉和黑钛金。送人不用解释，一眼就是贵、硬、懂。",
        "emotional_value": "卖点是身份压制：客户既拿到西方武德符号，又拿到东方材质隐喻，像一种不明说的圈层暗号。",
        "cultural_anchor": "斯巴达头盔是西方勇武与纪律的公共符号；烟熏玉和黑钛金则把它从古代兵器转成华人也能读懂的材质炫耀。",
        "buyer_profile": "适合男性礼品、办公室桌摆、健身/创业/金融圈层、喜欢硬核成功叙事的人。",
        "placement_scene": "办公桌、书柜、酒柜、会议室边柜。",
        "objection_reply": "它不是复制历史文物，而是用东西方材质语言重构一个权力符号；适合想要有气场但不俗的礼物。",
        "prompt": "ancient Spartan-inspired helmet reconstructed from smoky jade and black titanium, brushed gold fracture seams, no copyrighted design, no movie reference, museum plinth, intense Rembrandt lighting, premium collectible artifact photography, refractive acrylic block depth, no text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "batch": "2.3 Cultural Assassin",
        "sku": "OC-NYC-ASSASSIN-009",
        "name": "Black Titanium Greek Mask",
        "product": "Canvas",
        "private_copy": "古希腊戏剧面具被黑钛金和深玉重新铸造。适合需要文化压制感的客厅或会客室。",
        "dm_pitch": "这张更适合成熟客户，尤其是想让客厅显得有文化、有艺术馆感，但又不想买普通油画复制品的人。",
        "broker_hook": "古希腊面具这张更成熟，适合会客厅。不是油画复制品，是黑钛金和深玉重构出来的美术馆感。",
        "emotional_value": "卖点是让家里有一种不解释也能感到文化重量的美术馆气质。",
        "cultural_anchor": "古希腊戏剧面具背后是悲剧、命运和公共表演的传统；黑钛金与深玉让它变成一个更冷、更现代的美术馆物件。",
        "buyer_profile": "适合成熟家庭、会客厅、律师/咨询/艺术相关客户，以及想显得有文化但不想太张扬的人。",
        "placement_scene": "客厅、会客室、餐厅侧墙、深色画廊墙。",
        "objection_reply": "它不是普通古典复刻，而是把古典符号做成现代材质想象；懂的人会觉得有层次，不懂的人也会觉得贵。",
        "prompt": "classical Greek theater mask redesigned as black titanium and deep smoky jade, antique brass scars, dark museum wall, dramatic chiaroscuro, impasto canvas texture, original cultural fusion object, no exact historical replica, no text, no watermark --v 6.1 --ar 2:3 --style raw --no skin, person",
    },
    {
        "batch": "2.3 Cultural Assassin",
        "sku": "OC-NYC-ASSASSIN-010",
        "name": "Obsidian Laurel Victory Relic",
        "product": "Framed Poster",
        "private_copy": "胜利桂冠被做成黑曜石与烟熏玉的断裂标本。它不喊成功，但一眼就是赢家叙事。",
        "dm_pitch": "这款适合送给升职、开业、搬新办公室的人。它不直接写成功学，但整个画面就是胜利、克制和高级感。",
        "broker_hook": "升职、开业、搬办公室可以看这个。它不写成功学，但整个画面就是赢家叙事，比较克制。",
        "emotional_value": "卖点是克制的成功叙事，不喊口号，但让客户每天看到一种赢家身份确认。",
        "cultural_anchor": "桂冠来自古典世界的胜利象征；黑曜石和烟熏玉让它变成冷静、克制、可收藏的成功标本。",
        "buyer_profile": "适合开业、升职、乔迁、办公室礼品，以及不喜欢直白祝福语但想表达赢的人。",
        "placement_scene": "办公室、会议室、玄关、奖杯或证书旁。",
        "objection_reply": "它不像普通祝贺礼物那样直白，所以更耐看；对方每天看到的是胜利感，而不是一句廉价口号。",
        "prompt": "victory laurel relic made from obsidian leaves and smoky jade veins, brushed brass pins, archival museum specimen layout, dark luxury framed poster, old-world west shape with hidden east material logic, no readable labels, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
]


def payload(item: dict) -> dict:
    spec = PRODUCTS[item["product"]]
    return {
        "title": f"{item['name']} - OpenClaw NYC Private Atelier",
        "description": f"{item['private_copy']} 纽约独立工作室非量产实验批次；仅作私域展示、客户预览和未来 Printify 私域履约草稿。",
        "blueprint_id": spec["blueprint_id"],
        "print_provider_id": spec["provider_id"],
        "variants": [{"id": spec["variant_id"], "price": int(float(spec["retail"].strip("$")) * 100), "is_enabled": True, "sku": item["sku"]}],
        "print_areas": [{"variant_ids": [spec["variant_id"]], "placeholders": []}],
        "publish_policy": "PRINTIFY_PRIVATE_DRAFT_ONLY_DO_NOT_SYNC_EBAY_ETSY",
        "internal_sku": item["sku"],
    }


def build() -> None:
    DATABASE.mkdir(exist_ok=True)
    REVIEW.mkdir(exist_ok=True)
    rows = []
    for item in ZONE2:
        spec = PRODUCTS[item["product"]]
        rows.append(
            {
                "Internal_SKU": item["sku"],
                "Status": "CONCEPT_READY_WAITING_MJ",
                "Battlefield": item["batch"],
                "Concept_Name": item["name"],
                "Private_Copy": item["private_copy"],
                "Broker_Hook": item["broker_hook"],
                "DM_Pitch": item["dm_pitch"],
                "Emotional_Value": item["emotional_value"],
                "Cultural_Anchor": item["cultural_anchor"],
                "Buyer_Profile": item["buyer_profile"],
                "Placement_Scene": item["placement_scene"],
                "Objection_Reply": item["objection_reply"],
                "MJ_Master_Prompt": item["prompt"],
                "Product_Type": item["product"],
                "User_Target_Code": spec["target_code"],
                "Blueprint_ID": spec["blueprint_id"],
                "Provider_ID": spec["provider_id"],
                "Variant_ID": spec["variant_id"],
                "Variant": spec["variant"],
                "Print_Area": spec["print_area"],
                "Estimated_Cost_USD": spec["cost"],
                "Estimated_Shipping_USD": spec["shipping"],
                "Recommended_Retail_USD": spec["retail"],
                "Blueprint_Note": spec["note"],
                "Production_Image_Path": "",
                "Printify_Product_ID": "",
                "Payload_JSON": json.dumps(payload(item), ensure_ascii=False),
            }
        )

    csv_path = DATABASE / "Shock_And_Awe_V5_Zone2_Printify_Private_Queue.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_path = REVIEW / "OPERATION_SHOCK_AND_AWE_V5_ZONE2_CONCEPTS_20260509.md"
    lines = [
        "# Operation Shock and Awe V5 - Zone 2 Concept Preview",
        "",
        f"Generated: {datetime.now(NY).strftime('%Y-%m-%d %H:%M:%S %z')}",
        "",
        "Audience: private-channel partner demo. The goal is to impress Rex's partner with proof that OpenClaw can produce premium, culturally arbitraged visual products without requiring the partner to co-design.",
        "Scope: 战区二 10 个完整 Units。Each unit is decoupled into Block A prompt, Block B broker hook, Block C official spec sheet, and Block D Printify production vector.",
        "Policy: Printify private draft only. Do not sync eBay/Etsy. No direct copyrighted IP. No hardcore eastern mythology.",
        "",
        "## Blueprint Truth Check",
        "- Direct Printify API check: user/Grey ids 107, 118, 211, 1 return 404 in current catalog.",
        "- Direct Printify API check: 518 and 11 are apparel blueprints, not acrylic/canvas/mug targets.",
        "- Therefore this packet preserves user target codes but uses verified official fulfillment anchors: 1471 Photo Block, 1236 Framed Paper Posters, 1936 Canvas Art Wraps.",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['Internal_SKU']} - {row['Concept_Name']}",
                "",
                "### Block A: Midjourney Master Prompt",
                f"`{row['MJ_Master_Prompt']}`",
                "",
                "### Block B: The Broker's Hook",
                row["Broker_Hook"],
                "",
                "### Block C: The Studio Spec Sheet",
                f"- Internal SKU: {row['Internal_SKU']}",
                f"- Battlefield: {row['Battlefield']}",
                f"- Cultural Anchor: {row['Cultural_Anchor']}",
                f"- Material Illusion: {row['Emotional_Value']} {row['Private_Copy']}",
                f"- Spatial Recommendation: {row['Placement_Scene']}",
                f"- Best Buyer: {row['Buyer_Profile']}",
                f"- Objection Handling: {row['Objection_Reply']} 纽约排期满，走 Printify 全球供应链打样预计需 10-14 天。",
                "",
                "### Block D: Printify Production Vector",
                f"- Product: {row['Product_Type']} | {row['Variant']}",
                f"- Printify Anchor: blueprint {row['Blueprint_ID']} / provider {row['Provider_ID']} / variant {row['Variant_ID']}",
                f"- Base Cost + Shipping: {row['Estimated_Cost_USD']} + {row['Estimated_Shipping_USD']}",
                f"- Recommended Retail Price: {row['Recommended_Retail_USD']}",
                f"- Markup Note: priced as private-client high-margin showcase, not public marketplace commodity.",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8-sig")
    print(f"[SHOCK-V5] zone2_queue={csv_path}")
    print(f"[SHOCK-V5] concept_preview={md_path}")


if __name__ == "__main__":
    build()
