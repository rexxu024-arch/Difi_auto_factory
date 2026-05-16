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
        "blueprint_id": 1471,
        "provider_id": 104,
        "variant_id": 106190,
        "variant": "5x7 vertical photo block",
        "print_area": "front:1538x2138",
        "cost": "$35.43",
        "shipping": "$15.99",
        "retail": "$289.00",
        "note": "High-end private desk object. Keep subject centered and materially dense.",
    },
    "Framed Poster": {
        "blueprint_id": 1236,
        "provider_id": 105,
        "variant_id": 93818,
        "variant": "12x18 vertical black-frame fine-art poster",
        "print_area": "front:3600x5400",
        "cost": "$22.00",
        "shipping": "$13.89",
        "retail": "$199.00",
        "note": "Ready-to-hang premium wall art. Best for private-client spatial storytelling.",
    },
    "Canvas": {
        "blueprint_id": 1936,
        "provider_id": 72,
        "variant_id": 119906,
        "variant": "12x18 vertical 1.6in canvas art wrap",
        "print_area": "front:3592x5387",
        "cost": "$26.00",
        "shipping": "$16.29",
        "retail": "$229.00",
        "note": "Use when visible texture and painterly tactility matter.",
    },
    "Notebook": {
        "blueprint_id": 5634,
        "provider_id": 99,
        "variant_id": 252281,
        "variant": "5.5x8.5 dotted spiral notebook",
        "print_area": "front:1725x2625 | back:1725x2625",
        "cost": "$6.80",
        "shipping": "$12.09",
        "retail": "$79.00",
        "note": "Private-channel lower-ticket artifact. Best for student, study-room, and gift bundles.",
    },
    "Mug": {
        "blueprint_id": 478,
        "provider_id": 28,
        "variant_id": 65216,
        "variant": "11oz ceramic mug",
        "print_area": "front:2475x1155 wrap",
        "cost": "$4.40",
        "shipping": "$6.39",
        "retail": "$49.00",
        "note": "Requires horizontal wrap prompt. Keep central motif repeatable and handle-safe.",
    },
}


UNITS = [
    {
        "sku": "OC-NYC-ARCHIVE-011",
        "battlefield": "1.1 NYC Archive",
        "name": "Art Deco Crown Blueprint",
        "product": "Framed Poster",
        "hook": "这张走的是纽约老钱建筑感，不是旅游纪念品。适合那种想让书房看起来像懂建筑、懂城市史的人。",
        "cultural": "Art Deco 在纽约不是装饰风格，而是金融资本和机械时代共同制造出的垂直神话。",
        "material": "青铜线稿、旧档案纸、烟熏玉阴影，把摩天楼做成一张像从建筑事务所保险柜里拿出来的图。",
        "scene": "胡桃木书桌后方、律师办公室、城市景观公寓玄关。",
        "objection": "它不靠地标明信片感，靠的是纽约建筑秩序和档案气质；越安静的空间越显贵。",
        "prompt": "archival Art Deco skyscraper crown blueprint inspired by 1930s New York geometry, brushed brass drafting lines on aged ivory paper, smoky jade shadow wash, precise architectural annotations as abstract unreadable marks, museum-grade framed poster, quiet luxury study decor, no readable text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-ARCHIVE-012",
        "battlefield": "1.1 NYC Archive",
        "name": "Brooklyn Cable Nocturne",
        "product": "Acrylic Block",
        "hook": "布鲁克林桥钢缆做成桌面藏品，很纽约但不俗。不是游客照，是城市骨架。",
        "cultural": "Brooklyn Bridge 是工业时代的信仰工程；钢缆本身比天际线更能代表纽约的硬度。",
        "material": "黑钛金钢缆、冷雾、琥珀街灯和亚克力折射，让它像一块封存城市夜色的样本。",
        "scene": "办公室桌面、书架、深色音响旁、城市公寓边柜。",
        "objection": "小件不是弱点，它适合做桌面的城市身份暗号，离近看才有层次。",
        "prompt": "macro close-up of Brooklyn Bridge steel cables at midnight, black titanium tension lines, amber sodium light, cold river fog, smoky jade reflections, premium urban artifact photography, refractive acrylic depth, no skyline postcard feeling, no text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-ARCHIVE-013",
        "battlefield": "1.1 NYC Archive",
        "name": "Sixties Jazz Cellar Amber",
        "product": "Canvas",
        "hook": "60 年代纽约爵士地下室，不出现人物，只留烟、铜管和琥珀灯。懂的人会觉得很有味道。",
        "cultural": "爵士俱乐部是纽约夜生活的地下礼拜堂；真正高级的是场域，不是明星脸。",
        "material": "胶片颗粒、暗红皮革、拉丝黄铜、烟雾层次，做成有年代感的画布。",
        "scene": "酒柜、客厅侧墙、音乐房、咖啡角。",
        "objection": "没有人物反而更耐看，也避开肖像和版权风险，留下的是氛围和阶层感。",
        "prompt": "1960s New York jazz cellar interior with no people, empty brass saxophone on dark red leather chair, amber low light, cigarette smoke atmosphere, vintage film grain, Rembrandt shadows, impasto canvas texture, private club mood, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-ARCHIVE-014",
        "battlefield": "1.1 NYC Archive",
        "name": "Subway Tile Oracle",
        "product": "Notebook",
        "hook": "把老纽约地铁瓷砖做成学习本封面，低调但很有城市味。适合学生和写作者。",
        "cultural": "纽约地铁瓷砖是城市公共记忆，粗糙、耐用、真实，比旅游图更像本地人的纽约。",
        "material": "裂釉白瓷、煤灰边缘、旧铜绿线条，给日常用品加一点档案感。",
        "scene": "课堂、咖啡店、阅读角、随身礼物。",
        "objection": "它不是高价主产品，而是私域礼品池里的入门款，适合搭配大件销售。",
        "prompt": "old New York subway ceramic tile pattern redesigned as quiet luxury notebook cover, cracked white glaze, patinated brass trim, smoky graphite shadows, abstract station geometry with no readable words, premium stationery product art, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-AMERICANA-015",
        "battlefield": "1.2 Elevated Americana",
        "name": "Route 66 Neon Reliquary",
        "product": "Framed Poster",
        "hook": "Route 66 不是做成廉价复古牌子，而是做成霓虹遗迹。适合喜欢美国公路文化但不想土的人。",
        "cultural": "美国公路文化的高级版本不是车标，而是废墟、霓虹和离开的自由感。",
        "material": "褪色霓虹、沙尘玻璃、锈蚀钢架和伦勃朗式夜光。",
        "scene": "男士书房、车库 lounge、复古主题空间。",
        "objection": "不使用具体品牌或车款，保留公路情绪，避免廉价周边感。",
        "prompt": "Route 66 roadside neon relic in desert twilight, no brand names, broken motel sign reduced to abstract geometry, rusted steel, dusty glass, Rembrandt light, cinematic Americana nostalgia, museum-grade framed poster, no readable text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-AMERICANA-016",
        "battlefield": "1.2 Elevated Americana",
        "name": "Hollywood Backlot Ghost Light",
        "product": "Canvas",
        "hook": "复古好莱坞不是明星海报，而是一盏空舞台的 ghost light。更像懂行的人会买的东西。",
        "cultural": "Ghost light 是剧场空场后的守夜灯，象征舞台仍然活着。",
        "material": "黑幕、暖钨丝灯、灰尘颗粒和胶片划痕，形成怀旧但不俗的画面。",
        "scene": "影音室、客厅、工作室、表演艺术爱好者空间。",
        "objection": "没有明星肖像，所以不会过时，也没有版权风险；卖的是幕后气质。",
        "prompt": "vintage Hollywood backlot stage with a single ghost light, no actors, no famous set, warm tungsten bulb, black velvet curtains, dust particles, 35mm film grain, painterly canvas texture, cinematic nostalgia, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-AMERICANA-017",
        "battlefield": "1.2 Elevated Americana",
        "name": "Gas Station After Rain",
        "product": "Acrylic Block",
        "hook": "雨后老加油站做成亚克力桌摆，灯光折进去会很好看。复古但不廉价。",
        "cultural": "Mid-century roadside architecture 是美国大众梦的残影，适合做年轻客户的怀旧入口。",
        "material": "湿柏油反光、铬金属边、琥珀灯和深蓝夜色。",
        "scene": "桌面、车库陈列、复古游戏/影音角。",
        "objection": "没有品牌字样，不是汽油广告；只是保留美式夜路的情绪。",
        "prompt": "mid-century American roadside gas station after rain, no brand signs, chrome trim, wet asphalt reflections, amber canopy light, deep blue night, cinematic product-photo depth, acrylic block refraction, elevated vintage Americana, no readable text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-MUSEUM-018",
        "battlefield": "1.3 Pure Museum",
        "name": "Celestial Anatomy Folio",
        "product": "Framed Poster",
        "hook": "十九世纪星象和解剖手稿的混合感，挂在书房比普通星图更有压迫力。",
        "cultural": "维多利亚时代的科学图谱把求知、殖民博物馆和私人书房绑定在一起。",
        "material": "旧羊皮纸、细铜版线、星尘蓝和骨白墨迹。",
        "scene": "书房、阅读角、学院风卧室、咨询室。",
        "objection": "图中不出现真实人体器官细节，保留学术感但不造成不适。",
        "prompt": "19th century celestial anatomy folio, astronomical instruments and abstract bone-like geometry, copperplate engraving lines, aged parchment, starlight blue ink, dark academia museum poster, no readable text, no gore, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-MUSEUM-019",
        "battlefield": "1.3 Pure Museum",
        "name": "Rembrandt Scholar Without Face",
        "product": "Canvas",
        "hook": "伦勃朗光影的人物感，但不做具体人脸。适合想要古典肖像气质又不想挂陌生人的客户。",
        "cultural": "荷兰黄金时代肖像的核心是光线、布料和阶层姿态，不一定需要脸。",
        "material": "深棕背景、旧黑袍、羊皮纸和黄金边光。",
        "scene": "书房、办公室、会客室、深色墙面。",
        "objection": "没有可识别人脸，不涉及肖像版权，也更适合长期挂在私人空间。",
        "prompt": "Rembrandt-lit faceless scholar silhouette, dark velvet robe, gloved hands holding blank parchment, no visible face, old master chiaroscuro, impasto oil texture, pure museum wall art, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, watermark",
    },
    {
        "sku": "OC-NYC-MUSEUM-020",
        "battlefield": "1.3 Pure Museum",
        "name": "Orrery of the Silent House",
        "product": "Acrylic Block",
        "hook": "古典星象仪做成桌面亚克力，像私人图书馆里的小型天体装置。",
        "cultural": "Orrery 是启蒙时代的知识玩具，代表把宇宙缩小到书桌上的权力。",
        "material": "黄铜轨道、黑曜石底座、烟熏玻璃星球和微弱蓝光。",
        "scene": "书桌、书柜、学习房、办公室角落。",
        "objection": "它不是儿童天文玩具，而是知识阶层的桌面符号。",
        "prompt": "antique orrery of the silent house, brass orbital rings, obsidian base, smoky glass planets, faint starlight jade glow, private library object photography, acrylic block refraction, no readable labels, no text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-CYBERPOP-021",
        "battlefield": "3.1 Cyber-Pop",
        "name": "Acid Chrome Toy Panther",
        "product": "Notebook",
        "hook": "给留学生和年轻客户的低门槛潮牌感：酸性色、铬金属、玩具豹，但不碰任何现成 IP。",
        "cultural": "潮玩的价值不在角色，而在材质、轮廓和可展示的社交货币。",
        "material": "酸性绿色、液态铬、透明树脂眼和故障霓虹。",
        "scene": "课堂、宿舍、咖啡店、朋友圈晒图。",
        "objection": "这是走量入口款，不追求严肃文化，而追求第一眼够亮、够记忆点。",
        "prompt": "original cyber-pop toy panther, acid green and liquid chrome body, translucent resin eyes, glitch neon sticker-bomb background, premium notebook cover composition, no existing character, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-CYBERPOP-022",
        "battlefield": "3.1 Cyber-Pop",
        "name": "Hot Pink Signal Bunny",
        "product": "Notebook",
        "hook": "高饱和兔形潮玩，但完全原创。适合学生、礼物和低价试水。",
        "cultural": "用可爱外壳承载赛博信号，让低门槛产品也有一点未来感。",
        "material": "热粉、玻璃纤维、LED 边缘光、透明塑料质感。",
        "scene": "宿舍、书包、社交平台图文。",
        "objection": "不碰暴力熊或任何已知角色，只提取潮玩情绪和材质语言。",
        "prompt": "original cyber-pop bunny mascot sculpture, hot pink fiberglass shell, LED rim light, transparent plastic ears, acid design background, high-saturation youth streetwear energy, notebook cover art, no existing toy IP, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-CYBERPOP-023",
        "battlefield": "3.1 Cyber-Pop",
        "name": "Neon Vending Shrine",
        "product": "Mug",
        "hook": "杯子用横向 wrap：霓虹自动贩卖机神龛，适合年轻客群和礼物。",
        "cultural": "便利店、自动贩卖机、夜行灯牌，是亚洲年轻人的城市神龛。",
        "material": "霓虹紫、玻璃反光、铬边框和糖果色塑料。",
        "scene": "宿舍、办公室杯、礼品组合。",
        "objection": "Mug 必须做横向连续构图，避免把竖图硬塞导致生产图裁切。",
        "prompt": "continuous panoramic wrap-around design of an original neon vending machine shrine, cyberpunk candy colors, chrome frame, glowing beverage silhouettes with no readable labels, seamless mug art, handle-safe center composition, no text, no logo --v 6.1 --ar 2:1 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-CYBERPOP-024",
        "battlefield": "3.1 Cyber-Pop",
        "name": "Chrome Skate Relic",
        "product": "Framed Poster",
        "hook": "不是滑板品牌海报，而是铬金属滑板遗物。适合年轻潮牌感空间。",
        "cultural": "街头文化的高级化路径，是把用品变成像博物馆标本一样的图像。",
        "material": "刮痕铬面、酸性贴纸残影、黑色背景和边缘霓虹。",
        "scene": "宿舍、游戏房、潮牌集合店、年轻办公室。",
        "objection": "无品牌、无 logo、无具体 IP，只保留滑板文化的速度和磨损感。",
        "prompt": "original chrome skateboard relic floating on black gallery background, acid sticker residue as abstract shapes, scratched metal, neon magenta rim light, youth streetwear art poster, no brands, no readable text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-CYBERPOP-025",
        "battlefield": "3.1 Cyber-Pop",
        "name": "Glitch Mascot Totem",
        "product": "Canvas",
        "hook": "留学生潮牌向的视觉核弹：高饱和、强轮廓、没有侵权角色。",
        "cultural": "互联网世代的图腾不是神像，而是可识别、可转发、可做头像的抽象角色。",
        "material": "酸性黄、电子蓝、软胶玩具质感和像素故障。",
        "scene": "宿舍主墙、游戏房、潮玩展示区。",
        "objection": "它是战区三的流量款，不跟高冷款抢定位，负责拉年轻人注意力。",
        "prompt": "original glitch mascot totem, high-saturation acid yellow and electric blue, soft vinyl toy material, pixel distortion aura, aggressive cyber-pop composition, canvas texture, no known character, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-AUSPICIOUS-026",
        "battlefield": "3.2 Neo-Auspicious",
        "name": "Chrome Lucky Cat Engine",
        "product": "Acrylic Block",
        "hook": "招财猫不做土味，做成铬金属引擎猫。认知门槛低，但质感可以很贵。",
        "cultural": "招财符号适合下沉私域，但必须用工业材质重绘，避开廉价感。",
        "material": "液态铬、红色树脂核心、金色机械铃铛和透明亚克力深度。",
        "scene": "收银台、办公室桌面、开业礼物。",
        "objection": "保留招财逻辑，但不写发财字、不做传统龙凤，避免土味。",
        "prompt": "original lucky cat engine sculpture, liquid chrome body, red resin power core, antique gold mechanical bell, premium product photography, refractive acrylic block depth, neo-auspicious but not traditional, no text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-AUSPICIOUS-027",
        "battlefield": "3.2 Neo-Auspicious",
        "name": "Fortune Coin Circuit",
        "product": "Mug",
        "hook": "横向杯图：金币变成电路板，不写发财，但一眼知道是好运和钱。",
        "cultural": "把财运从土味文字转成视觉符号，更适合年轻客户和办公室礼品。",
        "material": "金属金币、黑色 PCB、绿玉光点、连续 wrap。",
        "scene": "办公室杯、礼物、开业小件。",
        "objection": "杯子是低价入口，不需要讲太深，核心是好看、好送、不亏。",
        "prompt": "continuous seamless panoramic mug wrap of fortune coins transforming into black circuit board traces, jade green indicator lights, antique gold metal, no readable symbols, modern neo-auspicious gift design, handle-safe composition, no text, no logo --v 6.1 --ar 2:1 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-AUSPICIOUS-028",
        "battlefield": "3.2 Neo-Auspicious",
        "name": "Red Envelope Data Vault",
        "product": "Notebook",
        "hook": "红包变成数据保险库，适合学生和年轻上班族。喜庆但不俗。",
        "cultural": "红包是华人最直接的财富符号，用赛博保险库重写后更适合海外年轻人。",
        "material": "深红磨砂纸、金属锁芯、数据光线和玉石按钮。",
        "scene": "学习本、礼品、春节/开学季。",
        "objection": "不写中文，不做传统纹样堆叠，只留下财富和好运的现代感。",
        "prompt": "red envelope redesigned as a cyber data vault, matte crimson paper planes, brushed gold lock mechanism, jade security light, premium notebook cover, neo-auspicious modern Chinese diaspora gift energy, no readable text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-AUSPICIOUS-029",
        "battlefield": "3.2 Neo-Auspicious",
        "name": "Jade Prosperity Capsule",
        "product": "Acrylic Block",
        "hook": "发财不写出来，做成一枚玉质能量舱。适合开业和办公桌。",
        "cultural": "把传统愿望压缩成未来科技容器，能跨过土味门槛。",
        "material": "半透明玉、黑钛框架、金色能量芯和冷白背景。",
        "scene": "办公桌、开业礼、收银台、玄关。",
        "objection": "如果客户觉得太抽象，就用开业礼物、好运桌摆来解释。",
        "prompt": "translucent jade prosperity capsule inside black titanium frame, gold energy core, premium sci-fi gift object, clean studio lighting, acrylic block depth, modern lucky artifact without words, no text, no logo --v 6.1 --ar 5:7 --style raw --no skin, person, watermark",
    },
    {
        "sku": "OC-NYC-AUSPICIOUS-030",
        "battlefield": "3.2 Neo-Auspicious",
        "name": "Neon Shop Guardian",
        "product": "Framed Poster",
        "hook": "小店守护神做成霓虹抽象雕塑，不用龙凤，不用字，也能有开业气场。",
        "cultural": "华人开业礼需要吉利，但海外审美不能太直白；这个负责折中。",
        "material": "霓虹红、暗金、黑曜石底座和玻璃光。",
        "scene": "小店、工作室、收银台后方、办公室入口。",
        "objection": "它不是宗教神像，也不是传统年画；只是一个现代好运守护符号。",
        "prompt": "abstract neon shop guardian sculpture, no animal dragon or phoenix, obsidian plinth, red neon halo, antique gold protective geometry, modern diaspora opening-gift wall art, framed poster composition, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark",
    },
]


def product_payload(unit: dict) -> dict:
    spec = PRODUCTS[unit["product"]]
    return {
        "title": f"{unit['name']} - OpenClaw NYC Private Atelier",
        "description": f"{unit['hook']} 纽约独立工作室私域样板；仅作客户预览与未来 Printify 私域履约草稿，不同步公域平台。",
        "blueprint_id": spec["blueprint_id"],
        "print_provider_id": spec["provider_id"],
        "variants": [
            {
                "id": spec["variant_id"],
                "price": int(float(spec["retail"].strip("$")) * 100),
                "is_enabled": True,
                "sku": unit["sku"],
            }
        ],
        "print_areas": [{"variant_ids": [spec["variant_id"]], "placeholders": []}],
        "publish_policy": "PRINTIFY_PRIVATE_DRAFT_ONLY_DO_NOT_SYNC_EBAY_ETSY",
        "internal_sku": unit["sku"],
    }


def build() -> None:
    DATABASE.mkdir(exist_ok=True)
    REVIEW.mkdir(exist_ok=True)
    rows: list[dict[str, str]] = []
    for unit in UNITS:
        spec = PRODUCTS[unit["product"]]
        rows.append(
            {
                "Internal_SKU": unit["sku"],
                "Status": "CONCEPT_READY_WAITING_MJ",
                "Battlefield": unit["battlefield"],
                "Concept_Name": unit["name"],
                "Broker_Hook": unit["hook"],
                "Cultural_Anchor": unit["cultural"],
                "Material_Illusion": unit["material"],
                "Spatial_Recommendation": unit["scene"],
                "Objection_Handling": unit["objection"],
                "MJ_Master_Prompt": unit["prompt"],
                "Product_Type": unit["product"],
                "Blueprint_ID": str(spec["blueprint_id"]),
                "Provider_ID": str(spec["provider_id"]),
                "Variant_ID": str(spec["variant_id"]),
                "Variant": spec["variant"],
                "Print_Area": spec["print_area"],
                "Estimated_Cost_USD": spec["cost"],
                "Estimated_Shipping_USD": spec["shipping"],
                "Recommended_Retail_USD": spec["retail"],
                "Blueprint_Note": spec["note"],
                "Payload_JSON": json.dumps(product_payload(unit), ensure_ascii=False),
            }
        )

    csv_path = DATABASE / "Shock_And_Awe_V5_Zones1_3_Printify_Private_Queue.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_path = REVIEW / "OPERATION_SHOCK_AND_AWE_V5_ZONES1_3_CONCEPTS_20260509.md"
    lines = [
        "# Operation Shock and Awe V5 - Zones 1 and 3 Concept Packet",
        "",
        f"Generated: {datetime.now(NY).strftime('%Y-%m-%d %H:%M:%S %z')}",
        "",
        "Purpose: complete the remaining 20 private-channel demo concepts after the Zone 2 tower batch.",
        "Policy: Printify private draft only; no eBay/Etsy listing text; no direct copyrighted IP; no hardcore eastern mythology.",
        "",
    ]
    for unit in UNITS:
        spec = PRODUCTS[unit["product"]]
        lines.extend(
            [
                f"## {unit['sku']} - {unit['name']}",
                "",
                "### Block A: Midjourney Master Prompt",
                f"`{unit['prompt']}`",
                "",
                "### Block B: The Broker's Hook",
                unit["hook"],
                "",
                "### Block C: The Studio Spec Sheet",
                f"- Internal SKU: {unit['sku']}",
                f"- Battlefield: {unit['battlefield']}",
                f"- Cultural Anchor: {unit['cultural']}",
                f"- Material Illusion: {unit['material']}",
                f"- Spatial Recommendation: {unit['scene']}",
                f"- Objection Handling: {unit['objection']} 纽约排期满，走 Printify 全球供应链打样预计需 10-14 天。",
                "",
                "### Block D: Printify Production Vector",
                f"- Product: {unit['product']} | {spec['variant']}",
                f"- Printify Anchor: blueprint {spec['blueprint_id']} / provider {spec['provider_id']} / variant {spec['variant_id']}",
                f"- Base Cost + Shipping: {spec['cost']} + {spec['shipping']}",
                f"- Recommended Retail Price: {spec['retail']}",
                f"- Note: {spec['note']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[SHOCK-V5-REMAINING] rows={len(rows)} csv={csv_path} packet={md_path}")


if __name__ == "__main__":
    build()
