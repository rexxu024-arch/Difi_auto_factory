import os
from dotenv import load_dotenv

# 强制加载 .env 物理环境
load_dotenv()

class Config:
    # --- 1. 基础通信接口 ---
    GAS_URL = os.getenv("GAS_URL")
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    # --- 2. 物理定位 (Discord 位点) ---
    GUILD_ID = os.getenv("GUILD_ID")
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    
    # --- 3. 交互协议参数 ---
    APP_ID = os.getenv("APPLICATION_ID")
    MJ_ID = os.getenv("MJ_ID")
    MJ_VERSION = os.getenv("MJ_VERSION")
    SESSION_ID = os.getenv("SESSION_ID")

    # --- 4. 物理规格矩阵 (Product Matrix V13.0) ---
    # 结构：Category -> Format -> Specific Specs
    PRODUCT_SPECS = {
        "Sticker": {
            "default_limit": 10, # 测试阶段物理限制
            "formats": {
                "Kiss-Cut": {"dpi": 300, "target_px": 832, "remove_bg": True, "suffix": "KC_3x3"},
                "Die-Cut":  {"dpi": 300, "target_px": 1024, "remove_bg": True, "suffix": "DC_ready"},
                "Standard": {"dpi": 300, "target_px": 832, "remove_bg": False, "suffix": "ST_ready"}
            }
        },
        "T-Shirt": {
            "default_limit": 999,
            "formats": {
                "Standard": {"dpi": 300, "target_px": 4500, "remove_bg": True, "suffix": "SHIRT_print"}
            }
        },
        "Poster": {
            "default_limit": 999,
            "formats": {
                "Standard": {"dpi": 300, "target_px": 5400, "remove_bg": False, "suffix": "POSTER_final"}
            }
        }
    }

    @classmethod
    def validate(cls):
        essential_keys = ["GAS_URL", "TOKEN", "GUILD_ID", "CHANNEL_ID", "APP_ID", "MJ_ID", "SESSION_ID"]
        missing = [key for key in essential_keys if not getattr(cls, key)]
        if missing:
            print(f"❌ [CONFIG ERROR] 物理变量缺失: {missing}")
            return False
        return True