import os, io, shutil
from PIL import Image
from rembg import remove
from config import Config

def process_final_image(t_id, cat, fmt, folder, main_idx):
    """物理加工协议：RemoveBG -> Resize -> DPI 300"""
    spec = Config.PRODUCT_SPECS.get(cat, {}).get("formats", {}).get(fmt)
    if not spec: spec = {"dpi": 300, "target_px": 1024, "remove_bg": False, "suffix": "READY"}

    for i in range(1, 5):
        raw_file = os.path.join(folder, f"{t_id}_U{i}.png")
        if not os.path.exists(raw_file): continue

        if i == main_idx:
            print(f"⚙️  Processing MAIN Asset: {t_id}_U{i}...")
            with open(raw_file, 'rb') as f:
                img_data = f.read()
                # 1. 去背景
                processed = remove(img_data) if spec["remove_bg"] else img_data
                img = Image.open(io.BytesIO(processed))
                # 2. 物理缩放
                if img.width != spec["target_px"]:
                    img = img.resize((spec["target_px"], spec["target_px"]), Image.Resampling.LANCZOS)
                # 3. DPI 注入
                output_name = f"{t_id}_{spec['suffix']}.png"
                img.save(os.path.join(folder, output_name), "PNG", dpi=(spec["dpi"], spec["dpi"]))
            os.remove(raw_file)
        else:
            # 归档概念图
            os.rename(raw_file, os.path.join(folder, f"{t_id}_Concept_{i}.png"))

def run_logic():
    print("🔍 Scanning for '-Review' folders...")
    queue = [os.path.join(r, d) for r, ds, _ in os.walk("Output") for d in ds if d.endswith("-Review")]

    if not queue:
        print("📭 No folders ready for audit.")
        return

    for folder in queue:
        parts = folder.split(os.sep)
        # 兼容 Windows/Linux 路径
        sel_cat, sel_fmt, t_id = parts[-3], parts[-2], parts[-1].replace("-Review", "")
        
        print(f"\n🔎 Auditing: {t_id} | Format: {sel_fmt}")
        grid_path = os.path.join(folder, "Grid.png")
        if os.path.exists(grid_path): os.startfile(grid_path)

        choice = input("🏆 Select MAIN (1-4), '5' DELETE, 's' SKIP: ").strip()

        if choice in ['1', '2', '3', '4']:
            process_final_image(t_id, sel_cat, sel_fmt, folder, int(choice))
            # 清理
            prompt_file = os.path.join(folder, "mj_prompt.txt")
            if os.path.exists(prompt_file): os.remove(prompt_file)
            if os.path.exists(grid_path): os.remove(grid_path)
            # 归档
            os.rename(folder, folder.replace("-Review", "-Ready"))
            print(f"✅ [{t_id}] Audit Success & Archived.")
        elif choice == '5':
            shutil.rmtree(folder)
            print(f"🗑️  [{t_id}] Deleted.")
    
    print("\n🏁 [IRON_AUDIT CYCLE FINISHED] Returning to Console...")