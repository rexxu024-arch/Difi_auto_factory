import base64, requests, os, time
from config import Config

# --- 核心配置 ---
SHOP_ID = "26983633"
BLUEPRINT_ID = 400
PROVIDER_ID = 99
TARGET_VARIANT_ID = 45754  
UNIFIED_PRICE = 1600
BASE_PATH = os.path.join("Output", "Sticker", "Test_Production")

class EfficiencyAuditor:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {Config.Printify_API_KEY}", "Content-Type": "application/json"}

    def _log(self, msg):
        print(f"[{time.strftime('%H:%M:%S')}] ⚙️ {msg}")

    def global_pre_clean(self, folder_list):
        """一次性物理抹除：为新任务腾出逻辑空间"""
        self._log(f"启动全量预清理，涉及项目数: {len(folder_list)}...")
        p_res = requests.get(f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json", headers=self.headers)
        if p_res.status_code == 200:
            existing = p_res.json().get("data", [])
            for folder in folder_list:
                item_id = folder.split("-")[-1]
                for p in existing:
                    # 匹配 "Set 0002" 这种固定标识
                    if f"Set {item_id}" in p.get("title", ""):
                        requests.delete(f"https://api.printify.com/v1/shops/{SHOP_ID}/products/{p.get('id')}.json", headers=self.headers)
                        self._log(f"已清理旧 Listing 占用: {item_id}")
        
        self._log("预清理完成，预留 8s 同步时间...")
        time.sleep(8)

    def process_task(self, folder_name):
        item_id = folder_name.split("-")[-1]
        full_folder_path = os.path.join(BASE_PATH, folder_name)
        
        # --- SKU 盐值化：语义化设计 ---
        # 格式：ZEN-0002-171285xxxx (前4位时间戳足够区分版本)
        version_tag = str(int(time.time()))
        sku = f"ZEN-{item_id}-{version_tag}"
        
        # 1. 上传
        c_path = os.path.join(full_folder_path, f"COVER_Main_Sticker-Zen-{item_id}.jpg")
        r_path = os.path.join(full_folder_path, f"READY_6x6_Sticker-Zen-{item_id}.png")
        
        c_id = self.upload_image(c_path, item_id, version_tag)
        r_id = self.upload_image(r_path, item_id, version_tag)

        # 2. 创建骨架
        payload = {
            "title": f"Imperial Jade Zen Sticker Set {item_id} - Alchemical 6x6 Vinyl Decal",
            "blueprint_id": BLUEPRINT_ID,
            "print_provider_id": PROVIDER_ID,
            "variants": [{"id": TARGET_VARIANT_ID, "price": UNIFIED_PRICE, "is_enabled": True, "sku": sku}],
            "print_areas": [{"variant_ids": [TARGET_VARIANT_ID], "placeholders": [{"position": "front", "images": [{"id": r_id, "x": 0.5, "y": 0.5, "scale": 1, "angle": 0}]}]}],
            "images": [{"id": c_id, "is_default": True, "is_selected_for_publishing": True, "variant_ids": [TARGET_VARIANT_ID]}] if c_id else []
        }
        res = requests.post(f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json", headers=self.headers, json=payload)
        
        if res.status_code == 200:
            product_id = res.json().get("id")
            self._log(f"项目 [{item_id}] 骨架已建立。SKU: {sku}")
            self._log(f"等待后端渲染 25s...")
            time.sleep(25)
            
            # 发布
            requests.post(f"https://api.printify.com/v1/shops/{SHOP_ID}/products/{product_id}/publish.json", 
                          headers=self.headers, 
                          json={"title": True, "description": True, "images": True, "variants": True, "tags": True})
            self._log(f"✅ 项目 [{item_id}] 发布指令已发出。")
        else:
            self._log(f"❌ 骨架创建失败: {res.text}")

    def upload_image(self, path, item_id, version):
        if not os.path.exists(path): return None
        with open(path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
        # 素材库文件名同步：STK-0002-171285xxxx
        res = requests.post("https://api.printify.com/v1/uploads/images.json", 
                            headers=self.headers, 
                            json={"file_name": f"STK-{item_id}-{version}", "contents": img_b64})
        return res.json().get("id")

    def run(self):
        folders = sorted([f for f in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, f))])
        self.global_pre_clean(folders)
        
        for folder in folders:
            self.process_task(folder)
            self._log("-" * 60)
            time.sleep(2)

if __name__ == "__main__":
    EfficiencyAuditor().run()