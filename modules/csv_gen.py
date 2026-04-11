import os
import pandas as pd
from openai import OpenAI
from modules.spec_registry import Registry
from config import Config

# --- DeepSeek 配置 ---
# 请确保你的 .env 中有 DEEPSEEK_API_KEY
client = OpenAI(api_key=Config.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def get_ds_seo_logic(prompt_data):
    """
    通过 DeepSeek 将 MJ 的技术 Prompt 转化为电商 Title 和 Tags
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a professional Etsy/eBay SEO expert. Translate MJ prompts into high-converting Product Titles and 13 Tags. Format: Title | Tag1, Tag2..."},
                {"role": "user", "content": f"Extract SEO from these prompts: {prompt_data}"}
            ],
            stream=False
        )
        res = response.choices[0].message.content
        return res.split("|") if "|" in res else [res, "stickers, art, zen"]
    except Exception as e:
        print(f"🚨 DeepSeek API 调用失败: {e}")
        return ["Premium Sticker Pack", "art, decor, gift"]

def run_logic():
    print(f"\n{'='*20} 📝 STAGE 5: CSV_GEN 启动 {'='*20}")
    
    # 1. 交互选择 (对齐 Registry)
    for k, v in Registry.CATALOG.items(): print(f"[{k}] {v.name}")
    type_key = input("选择大类 (1-4): ") or "1"
    product = Registry.CATALOG.get(type_key, Registry.STICKER)

    for i, s in enumerate(product.specs, 1): print(f"[{i}] {s}")
    spec_idx = int(input(f"选择 {product.name} 的制式 (1-3): ") or "1") - 1
    spec = product.specs[spec_idx]

    # 2. 路径对齐 (使用相对路径)
    # 扫描基准: Output/Sticker/Kiss-Cut
    rel_target_dir = os.path.join("Output", product.name, spec)
    # 结果存放在: Output/Sticker/Sticker_Kiss-Cut_Listings.csv
    csv_filename = f"{product.name}_{spec}_Listings.csv"
    csv_rel_path = os.path.join("Output", product.name, csv_filename)

    if not os.path.exists(rel_target_dir):
        print(f"❌ 找不到相对目录: {rel_target_dir}")
        return

    # 3. 扫描 _Completed 文件夹
    folders = [d for d in os.listdir(rel_target_dir) if d.endswith("_Completed")]
    print(f"📡 发现 {len(folders)} 个待录入 SKU")

    new_listings = []

    for folder in folders:
        # 路径全部转为相对路径存储
        folder_rel_path = os.path.join(rel_target_dir, folder)
        meta_file = os.path.join(folder_rel_path, "metadata.txt")
        
        if not os.path.exists(meta_file): continue

        # 提取 ID 和 Prompt
        with open(meta_file, "r", encoding="utf-8") as f:
            meta_content = f.read()
            # 简单提取 MASTER_ID
            m_id = folder.replace("_Completed", "")
            # 提取所有 Prompt 片段用于 DeepSeek 分析
            prompts = " ".join([p for p in meta_content.split("MJ_Prompt:") if "--ar" in p])

        print(f"⚙️ 正在精炼 SKU 数据: {m_id}...")
        seo = get_ds_seo_logic(prompts)
        
        # 4. 组装行数据
        # 图片名遵循我们在 Stage 4 定义的命名规范
        clean_id = m_id.replace("MASTER_", "")
        row = {
            "SKU": m_id,
            "Title": seo[0].strip(),
            "Keywords": seo[1].strip(),
            "Cover_Img_Name": f"COVER_Main_{clean_id}.jpg",
            "Ready_Img_Name": f"READY_6x6_{clean_id}.png",
            "Rel_Folder_Path": folder_rel_path,
            "Category": product.name,
            "Spec": spec,
            "Process_Date": pd.Timestamp.now().strftime('%Y-%m-%d')
        }
        new_listings.append(row)

    # 5. 增量写入 CSV (去重审计)
    if new_listings:
        new_df = pd.DataFrame(new_listings)
        if os.path.exists(csv_rel_path):
            old_df = pd.read_csv(csv_rel_path)
            # 根据 SKU 去重，保留最新的 DeepSeek 优化结果
            final_df = pd.concat([old_df, new_df]).drop_duplicates(subset=["SKU"], keep='last')
        else:
            final_df = new_df
        
        final_df.to_csv(csv_rel_path, index=False, encoding="utf-8-sig")
        print(f"✅ CSV 已更新: {csv_rel_path}")
    else:
        print("💡 没有新的 Completed 文件夹需要处理。")

if __name__ == "__main__":
    run_logic()