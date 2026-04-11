import os
import io
from PIL import Image
from rembg import remove

def prepare_test_main_asset():
    """
    针对当前目录下 Output/Test 路径下的第一个子文件夹进行物理加工
    """
    # 设定相对路径
    base_path = "Output"
    test_path = os.path.join(base_path, "Test")

    if not os.path.exists(test_path):
        print(f"❌ 找不到路径: {test_path}，请确保在 openclaw_difi 目录下运行此脚本")
        return

    # 获取第一个子文件夹
    subfolders = [d for d in os.listdir(test_path) if os.path.isdir(os.path.join(test_path, d))]
    if not subfolders:
        print(f"📭 {test_path} 中没有子文件夹")
        return

    target_subfolder = os.path.join(test_path, subfolders[0])
    print(f"📁 选定测试目标文件夹: {target_subfolder}")

    # 寻找原图：支持 ID_U1.png 格式或简单的 U1.png
    files = [f for f in os.listdir(target_subfolder) if f.endswith("_U1.png") or f == "U1.png"]
    if not files:
        # 备选：找任何带 _U 的 png
        files = [f for f in os.listdir(target_subfolder) if "_U" in f and f.endswith(".png")]
    
    if not files:
        print(f"❌ 在 {target_subfolder} 中找不到任何 U 系原图")
        return
    
    raw_file_name = files[0]
    raw_path = os.path.join(target_subfolder, raw_file_name)
    
    # 构造输出文件名：保持 ID 并加上 _MAIN 标记
    t_id = raw_file_name.split("_U")[0] if "_U" in raw_file_name else "Sticker"
    output_path = os.path.join(target_subfolder, f"{t_id}_MAIN.png")

    print(f"🚀 开始加工原件: {raw_file_name}...")

    try:
        with open(raw_path, 'rb') as i:
            input_data = i.read()
            
            # 1. 物理去背景 (RemBG)
            print("🎨 执行 RemBG 深度去背景...")
            no_bg_data = remove(input_data)
            img = Image.open(io.BytesIO(no_bg_data))

            # 2. 尺寸标准化 (2048px 是 Printify 的高画质安全线)
            target_size = 2048
            if img.width != target_size or img.height != target_size:
                print(f"📏 缩放至 {target_size}x{target_size} (LANCZOS 采样)...")
                img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)

            # 3. 注入 300 DPI 
            print(f"💾 注入 300 DPI 并保存...")
            img.save(output_path, "PNG", dpi=(300, 300))

        print(f"✨ 加工成功！")
        print(f"📍 最终样板位置: {output_path}")
        print(f"\n👉 明天请使用这个带 '_MAIN' 的文件进行全流程肉身实测。")
        
    except Exception as e:
        print(f"💥 处理失败，错误原因: {e}")

if __name__ == "__main__":
    prepare_test_main_asset()