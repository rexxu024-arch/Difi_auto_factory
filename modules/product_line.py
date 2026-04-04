import json
import requests
import time
from config import Config

def run_production_delivery():
    input_file = "Product_line_input.txt"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        print(f"📦 [Dispatcher] 成功加载 {len(tasks)} 组生产任务。")
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return

    headers = {
        "Authorization": f"Bearer {Config.Product_line_API_KEY}",
        "Content-Type": "application/json"
    }

    target_url = "https://api.dify.ai/v1/chat-messages"

    print("🚀 启动生产线物理对齐 [Category Enforcement Mode]...\n")

    for index, task in enumerate(tasks):
        # 提取当前任务的核心参数
        category = task.get('Category', 'Unknown')
        p_type = task.get('Product_Type', 'Item')
        num = task.get('Number_of_Designs', 10)

        # 构造“绝对指令”：防止模型模仿 System Prompt 里的 Zen 例子
        # 我们把指令直接怼到模型的“嘴边”
        mandatory_instruction = (
            f"### PRODUCTION ORDER ###\n"
            f"CURRENT CATEGORY: {category}\n"
            f"PRODUCT TYPE: {p_type}\n"
            f"QUANTITY: {num}\n"
            f"--------------------------\n"
            f"INSTRUCTION: Ignore all previous 'Zen' or 'Sticker' examples. "
            f"Generate content strictly for the '{category}' category. "
            f"Ensure the product style is a '{p_type}'. "
            f"Output exactly {num} designs now."
        )

        payload = {
            "inputs": {
                "Category": category,
                "Product_Type": p_type,
                "Number_of_Designs": num
            },
            "query": mandatory_instruction,  # 用 Query 覆盖 Inputs 的模糊性
            "response_mode": "blocking",
            "conversation_id": "",           # 强制每一轮都是全新的，杜绝 Zen 记忆
            "user": "Rex_Architect"
        }

        print(f"📡 [{index + 1}/{len(tasks)}] 正在切换生产线配置: {category}...")

        try:
            response = requests.post(
                target_url, 
                headers=headers, 
                json=payload, 
                timeout=150 # 增加超时，确保 10 个能写完
            )
            
            if response.status_code == 200:
                answer = response.json().get('answer', '')
                # 审计产出品类
                if category.lower() in answer.lower():
                    print(f"✅ 对齐成功：已进入 {category} 生产序列。")
                else:
                    print(f"❌ 对齐失败：模型仍输出旧品类。请检查 Dify 后台变量绑定。")
                
                # 打印开头和结尾确认完整性
                print(f"📝 产出头部: {answer[:100].strip()}...")
                print(f"📝 产出尾部: ...{answer[-100:].strip()}")
            else:
                print(f"⚠️ 状态码 {response.status_code}: {response.text}")

        except Exception as e:
            print(f"❌ 系统异常: {e}")

        time.sleep(Config.ACTION_DELAY)

if __name__ == "__main__":
    run_production_delivery()