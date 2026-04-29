# modules/spec_registry.py

class ProductDef:
    """产品定义类"""
    def __init__(self, name, specs):
        self.name = name          # 产品大类名：如 Sticker
        self.specs = specs        # 生产制式列表：如 Kiss-Cut

class Registry:
    # --- 1. 硬编码固定顺序与产品制式 (按你的要求排序) ---
    STICKER = ProductDef("Sticker", ["Kiss-Cut", "Die-Cut", "Standard"])
    POSTER = ProductDef("Poster", ["Premium-Matte-Vertical", "Fine-Art-Print", "Blueprint-Texture", "Laminated"])
    ACRYLIC = ProductDef("Acrylic", ["Photo-Block", "Acrylic-Mount"])
    TSHIRT = ProductDef("T-Shirt", ["DTG-Print", "Screen-Print"])
    WALL_ART = ProductDef("Wall Art", ["Canvas-Wrapped", "Acrylic-Mount"])

    # 映射表：确保用户按 1, 2, 3, 4 选择时永远对应正确的产品
    CATALOG = {
        "1": STICKER,
        "2": POSTER,
        "3": ACRYLIC,
        "4": TSHIRT,
        "5": WALL_ART
    }

    @staticmethod
    def get_processing_logic(product_type, spec):
        """
        预留接口：大流程四（审核+图像处理）的调用逻辑
        目前返回空字典，之后我们针对每种 spec 补齐具体参数
        """
        # 逻辑示例：logic_key = "sticker_kiss_cut"
        return {}
