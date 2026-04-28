import os
from dotenv import load_dotenv

# 1. 物理定位与加载
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH, override=True)

class Config:
    """
    Grey 思维核心 - V18.0 严苛对齐协议
    [Rule]: 严禁任何形式的推测。完全镜像 .env 截图内容。
    """
    PROJECT_ROOT = BASE_DIR

    # --- [A] Printify 核心 (根据用户指示 ID=1) ---
    Printify_API_KEY = os.getenv("Printify_API_KEY")
    Printify_API_URL = "https://api.printify.com/v1"
    Printify_SHOP_ID = "26983633"  # 物理事实：第一个店铺

    # --- [B] Midjourney / Discord (镜像 .env 截图) ---
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD_ID = os.getenv("GUILD_ID")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    # --- [C] Dify / Product Line (镜像 .env 截图) ---
    Product_line_API_KEY = os.getenv("Product_line_API_KEY")
    Product_line_API_URL = os.getenv("Product_line_API_URL")
    
    # --- [D] DeepSeek 核心 (Stage 5 动力源) ---
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"

    # --- [E] Claude / Anthropic 核心 ---
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    CLAUDE_BASE_URL = os.getenv("CLAUDE_BASE_URL") or "https://api.anthropic.com"
   

    @classmethod
    def audit(cls):
        """全量审计：仅反馈 .env 中真实存在的键名读取状态"""
        print(f"\n📡 [V18.0 审计] 物理锚点: {ENV_PATH}")
        
        # 验证清单 (完全对应截图中的键名)
        checks = {
            "Printify_API_KEY": cls.Printify_API_KEY,
            "DISCORD_TOKEN": cls.DISCORD_TOKEN,
            "Product_line_API_KEY": cls.Product_line_API_KEY,
            "Printify_SHOP_ID (Manual)": cls.Printify_SHOP_ID
        }
        
        success = True
        for key, val in checks.items():
            if val:
                print(f"✅ {key:<25} | 已读取")
            else:
                print(f"❌ {key:<25} | 缺失 (EMPTY)")
                success = False
        return success
    @classmethod
    def validate(cls):
        """
        [启动校验协议]：对接 main.py 的启动检查
        执行全量审计并返回布尔值。
        """
        return cls.audit()

    @classmethod
    def audit(cls):
        """全量审计：反馈 .env 中真实存在的键名读取状态"""
        print(f"\n📡 [V18.0 审计] 物理锚点: {ENV_PATH}")
        
        # 验证清单 (完全对应你 .env 的核心变量)
        checks = {
            "Printify_API_KEY": cls.Printify_API_KEY,
            "DISCORD_TOKEN": cls.DISCORD_TOKEN,
            "Product_line_API_KEY": cls.Product_line_API_KEY,
            "GUILD_ID": cls.GUILD_ID,
            "CHANNEL_ID": cls.CHANNEL_ID
        }
        
        is_safe = True
        for key, val in checks.items():
            if val and len(str(val)) > 0:
                print(f"✅ {key:<25} | 已就绪")
            else:
                print(f"❌ {key:<25} | 缺失 (CRITICAL)")
                is_safe = False
        
        if is_safe:
            print("🚀 [CONFIG] 物理变量审计通过，生产环境就绪。")
        else:
            print("🛑 [CONFIG] 审计未通过，请检查 .env 文件。")
            
        return is_safe

if __name__ == "__main__":
    Config.audit()

CLAUDE_API_KEY = Config.CLAUDE_API_KEY
DEEPSEEK_API_KEY = Config.DEEPSEEK_API_KEY
BASE_URL = Config.CLAUDE_BASE_URL or Config.DEEPSEEK_BASE_URL
