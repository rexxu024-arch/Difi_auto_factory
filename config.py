import os
from dotenv import load_dotenv

# 1. 物理定位与加载
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH, override=True)


def _env_any(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    wanted = {"".join(ch for ch in name.lower() if ch.isalnum()) for name in names}
    for key, value in os.environ.items():
        normalized = "".join(ch for ch in key.lower() if ch.isalnum())
        if normalized in wanted and value:
            return value
    return None


class Config:
    """
    Grey 思维核心 - V18.0 严苛对齐协议
    [Rule]: 严禁任何形式的推测。完全镜像 .env 截图内容。
    """
    PROJECT_ROOT = BASE_DIR

    # --- [A] Printify 核心 (根据用户指示 ID=1) ---
    Printify_API_KEY = os.getenv("Printify_API_KEY")
    Printify_API_URL = "https://api.printify.com/v1"
    Printify_EBAY_SHOP_ID = os.getenv("Printify_EBAY_SHOP_ID") or "26983633"
    Printify_ETSY_SHOP_ID = os.getenv("Printify_ETSY_SHOP_ID") or "24260389"
    Printify_SHOP_ID = "26983633"  # 物理事实：第一个店铺
    PRINTIFY_LOGIN_EMAIL = os.getenv("PRINTIFY_LOGIN_EMAIL") or os.getenv("Printify_LOGIN_EMAIL") or ""

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

    # --- Gemini / Grey Advisor Bridge ---
    GEMINI_API_KEY = _env_any(
        "GEMINI_API_KEY",
        "Gemini_api_key",
        "GEMINI_KEY",
        "GOOGLE_API_KEY",
    )
    GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta"
    GEMINI_MODEL = os.getenv("GEMINI_MODEL") or "gemini-flash-latest"

    # --- [F] Etsy Open API / OAuth 2.0 PKCE ---
    ETSY_KEYSTRING = (
        os.getenv("ETSY_KEYSTRING")
        or os.getenv("ETSY_KEY_STRING")
        or os.getenv("ETSY_CLIENT_ID")
        or os.getenv("Etsy_Key_string")
    )
    ETSY_SHARED_SECRET = (
        os.getenv("ETSY_SHARED_SECRET")
        or os.getenv("ETSY_SECRET")
        or os.getenv("Etsy_shared_secret")
    )
    ETSY_REDIRECT_URI = os.getenv("ETSY_REDIRECT_URI") or "http://localhost:8765/etsy/oauth/callback"
    ETSY_SCOPES = os.getenv(
        "ETSY_SCOPES",
        "shops_r shops_w listings_r listings_w profile_r transactions_r",
    )
    ETSY_TOKEN_FILE = os.getenv("ETSY_TOKEN_FILE") or os.path.join(BASE_DIR, "Database", ".etsy_oauth_tokens.json")
    ETSY_STATE_FILE = os.getenv("ETSY_STATE_FILE") or os.path.join(BASE_DIR, "Database", ".etsy_oauth_state.json")
   

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
            "CHANNEL_ID": cls.CHANNEL_ID,
            "ETSY_KEYSTRING": cls.ETSY_KEYSTRING,
            "ETSY_SHARED_SECRET": cls.ETSY_SHARED_SECRET,
            "GEMINI_API_KEY": cls.GEMINI_API_KEY
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
GEMINI_API_KEY = Config.GEMINI_API_KEY
BASE_URL = Config.CLAUDE_BASE_URL or Config.DEEPSEEK_BASE_URL
