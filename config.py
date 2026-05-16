import os
from dotenv import dotenv_values, load_dotenv

# 1. 物理定位与加载
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH, override=True)


def _env_any(*names):
    def _norm(key):
        return "".join(ch for ch in str(key).lower() if ("a" <= ch <= "z") or ("0" <= ch <= "9"))

    for name in names:
        value = os.getenv(name)
        if value:
            return value
    wanted = {_norm(name) for name in names}
    for key, value in os.environ.items():
        normalized = _norm(key)
        if normalized in wanted and value:
            return value
    # Some Rex-provided .env keys use punctuation/non-ASCII characters that
    # python-dotenv can parse but may not export into os.environ as expected.
    for key, value in dotenv_values(ENV_PATH).items():
        normalized = _norm(key)
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
    GEMINI_FREE_API_KEY = _env_any(
        "GEMINI_FREE_API_KEY",
        "Gemini_free_api_key",
        "Gemnini_free_api_key",
        "GEMNINI_FREE_API_KEY",
        "Gemnini_free_api_key",
    )
    GEMINI_PAID_API_KEY = _env_any(
        "GEMINI_PAID_API_KEY",
        "Gemini_paid_api_key",
        "Gemini_paid_apid_key",
        "Gemini_paid_apikey",
        "Gemini_paid_key",
        "Gemini——paid_apid_key",
        "GEMINI_PAID_APID_KEY",
    )
    GEMINI_API_KEY = _env_any(
        "GEMINI_API_KEY",
        "Gemnini_api_key",
        "GEMNINI_API_KEY",
        "Gemni_api_key",
        "GEMNI_API_KEY",
        "Gemini_api_key",
        "GEMINI_KEY",
        "GOOGLE_API_KEY",
    ) or GEMINI_FREE_API_KEY or GEMINI_PAID_API_KEY
    GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta"
    GEMINI_MODEL = os.getenv("GEMINI_MODEL") or "gemini-flash-latest"
    GEMINI_FREE_MODEL = os.getenv("GEMINI_FREE_MODEL") or os.getenv("Gemini_free_model") or "gemini-flash-latest"
    GEMINI_PAID_MODEL = os.getenv("GEMINI_PAID_MODEL") or os.getenv("Gemini_paid_model") or os.getenv("GEMINI_PRO_MODEL") or "gemini-2.5-pro"

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
        "shops_r shops_w listings_r listings_w profile_r",
    )
    ETSY_TOKEN_FILE = os.getenv("ETSY_TOKEN_FILE") or os.path.join(BASE_DIR, "Database", ".etsy_oauth_tokens.json")
    ETSY_STATE_FILE = os.getenv("ETSY_STATE_FILE") or os.path.join(BASE_DIR, "Database", ".etsy_oauth_state.json")

    # --- eBay Developer / Sell APIs ---
    EBAY_SELLER_TOKEN = (
        os.getenv("EBAY_SELLER_OAUTH_TOKEN")
        or os.getenv("eBay_seller_oauth_token")
        or os.getenv("EBAY_SELLER_TOKEN")
        or os.getenv("eBay_seller_token")
        or os.getenv("EBAY_USER_TOKEN")
        or os.getenv("eBay_user_token")
    )
    EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID") or os.getenv("EBAY_APP_ID") or os.getenv("eBay_client_id")
    EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET") or os.getenv("EBAY_CERT_ID") or os.getenv("eBay_client_secret")
    EBAY_REDIRECT_URI = os.getenv("EBAY_REDIRECT_URI") or os.getenv("EBAY_RUNAME") or os.getenv("eBay_redirect_uri")
    EBAY_API_BASE_URL = os.getenv("EBAY_API_BASE_URL") or "https://api.ebay.com"
   

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
            "GEMINI_API_KEY": cls.GEMINI_API_KEY,
            "GEMINI_FREE_API_KEY": cls.GEMINI_FREE_API_KEY,
            "GEMINI_PAID_API_KEY": cls.GEMINI_PAID_API_KEY,
            "EBAY_SELLER_TOKEN": cls.EBAY_SELLER_TOKEN,
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
GEMINI_FREE_API_KEY = Config.GEMINI_FREE_API_KEY
GEMINI_PAID_API_KEY = Config.GEMINI_PAID_API_KEY
EBAY_SELLER_TOKEN = Config.EBAY_SELLER_TOKEN
BASE_URL = Config.CLAUDE_BASE_URL or Config.DEEPSEEK_BASE_URL
