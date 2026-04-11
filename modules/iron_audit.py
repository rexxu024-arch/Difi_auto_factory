import os
import io
import shutil
from PIL import Image
from rembg import remove
from modules.spec_registry import Registry

# --- 物理参数审计 (Sticker Kiss-Cut 专用) ---
STICKER_KISS_CUT_CONFIG = {
    "canvas_size": 1800,
    "thumb_prod": 400,
    "thumb_cover": 520,
    "elements_count": 8
}

def process_sticker_kiss_cut(folder_path):
    """
    具体的 Sticker Kiss-Cut 图像算法：8合1 抠图、READY合成与COVER渲染
    """
    master_id = os.path.basename(folder_path).replace("MASTER_", "").replace("_Completed", "")
    grid_files = sorted([f for f in os.listdir(folder_path) if f.endswith(("_Grid.png", "_Grid.jpg"))])
    
    if len(grid_files) < 2:
        print(f"  ❌ 数据不完整: {master_id} 缺少 Grid 文件")
        return False

    all_elements = []
    cfg = STICKER_KISS_CUT_CONFIG

    # 1. AI 抠图阶段
    for g_idx, g_file in enumerate(grid_files):
        img = Image.open(os.path.join(folder_path, g_file)).convert("RGBA")
        w, h = img.size
        mid_x, mid_y = w // 2, h // 2
        boxes = [(0, 0, mid_x, mid_y), (mid_x, 0, w, mid_y), (0, mid_y, mid_x, h), (mid_x, mid_y, w, h)]
        
        for b_idx, box in enumerate(boxes):
            element = img.crop(box)
            img_byte_arr = io.BytesIO()
            element.save(img_byte_arr, format='PNG')
            print(f"    ⏳ 正在处理图像资产 (G{g_idx+1}-E{b_idx+1})...", end="\r")
            element_no_bg = remove(img_byte_arr.getvalue())
            all_elements.append(Image.open(io.BytesIO(element_no_bg)))
    
    if len(all_elements) < cfg["elements_count"]:
        return False

    # 2. 生成 READY_6x6 (生产底稿)
    canvas_prod = Image.new("RGBA", (cfg["canvas_size"], cfg["canvas_size"]), (255, 255, 255, 0))
    x_gap_p = (cfg["canvas_size"] - 2 * cfg["thumb_prod"]) // 3
    y_gap_p = (cfg["canvas_size"] - 4 * cfg["thumb_prod"]) // 5

    for idx, sticker in enumerate(all_elements[:8]):
        temp = sticker.copy()
        temp.thumbnail((cfg["thumb_prod"], cfg["thumb_prod"]), Image.Resampling.LANCZOS)
        row, col = idx // 2, idx % 2
        pos = (x_gap_p + col * (cfg["thumb_prod"] + x_gap_p), y_gap_p + row * (cfg["thumb_prod"] + y_gap_p))
        canvas_prod.paste(temp, pos, temp)
    
    canvas_prod.save(os.path.join(folder_path, f"READY_6x6_{master_id}.png"), "PNG", dpi=(300, 300))

    # 3. 生成 COVER_Main (营销封面)
    white_bg = Image.new("RGBA", (cfg["canvas_size"], cfg["canvas_size"]), (255, 255, 255, 255))
    x_gap_c = (cfg["canvas_size"] - 2 * cfg["thumb_cover"]) // 3
    y_gap_c = (cfg["canvas_size"] - 4 * cfg["thumb_cover"]) // 5

    for idx, sticker in enumerate(all_elements[:8]):
        temp_c = sticker.copy()
        temp_c.thumbnail((cfg["thumb_cover"], cfg["thumb_cover"]), Image.Resampling.LANCZOS)
        shadow = Image.new("RGBA", temp_c.size, (0, 0, 0, 35))
        pos_c = (x_gap_c + (idx%2)*(cfg["thumb_cover"]+x_gap_c), y_gap_c + (idx//2)*(cfg["thumb_cover"]+y_gap_c))
        white_bg.paste(shadow, (pos_c[0]+8, pos_c[1]+8), temp_c)
        white_bg.paste(temp_c, pos_c, temp_c)
    
    white_bg.convert("RGB").save(os.path.join(folder_path, f"COVER_Main_{master_id}.jpg"), "JPEG", quality=95)
    return True

def run_logic():
    """
    由 main.py 直接调用的入口函数
    """
    print("\n--- 🔧 正在初始化 IRON_AUDIT 执行环境 ---")
    
    # 1. 内部引导选择（复用 Registry 逻辑）
    for k, v in Registry.CATALOG.items(): print(f"[{k}] {v.name}")
    type_choice = input("确认审计大类 (默认1): ") or "1"
    product = Registry.CATALOG.get(type_choice, Registry.STICKER)

    for i, s in enumerate(product.specs, 1): print(f"[{i}] {s}")
    spec_idx = int(input(f"确认 {product.name} 审计制式 (默认1): ") or "1") - 1
    spec = product.specs[spec_idx]

    # 2. 路径对齐
    target_dir = os.path.join("Output", product.name, spec)
    if not os.path.exists(target_dir):
        print(f"❌ 路径不存在，跳过审计: {target_dir}")
        return

    # 3. 扫描并执行
    print(f"📡 正在扫描待处理资产: {target_dir}")
    subfolders = [d for d in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, d))]
    
    active_tasks = [f for f in subfolders if "MASTER_" in f and not f.endswith("_Completed")]
    print(f"📦 待处理 SKU 总数: {len(active_tasks)}")

    for folder_name in active_tasks:
        old_path = os.path.join(target_dir, folder_name)
        
        # 根据大类和制式路由逻辑
        if product.name == "Sticker" and spec == "Kiss-Cut":
            if process_sticker_kiss_cut(old_path):
                # 状态闭环：重命名文件夹
                new_path = old_path + "_Completed"
                shutil.move(old_path, new_path)
                print(f"✅ [SUCCESS] {folder_name} -> 已归档为 _Completed")
        else:
            print(f"⚠️  当前版本暂未录入 {product.name}-{spec} 的审计算法，请补充子函数。")