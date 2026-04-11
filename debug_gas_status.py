import requests
import json
import time

# 确认这是你部署后的 URL
GAS_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbwPyI_nd21Cn0exMaa9BC6AiTTuDt-NyN6siw9CockmaPLgufRKNMLT5-PsC0RI32SQNw/exec" 

def debug_update_status():
    print("🚀 正在执行 V43.0 原位覆盖测试...")
    
    test_cases = [
        {"id": "Sticker-Zen-0001", "status": "defeat this"},   # 预期: Defeated_Prompt
        {"id": "Sticker-Zen-0002", "status": "please revise"}, # 预期: Revised_Prompt
        {"id": "Sticker-Zen-0003", "status": "completed"}      # 预期: Completed
    ]

    for case in test_cases:
        print(f"📡 正在对标 ID: {case['id']} -> {case['status']}")
        try:
            # 此时 payload 非常简单，只需这两个字段
            response = requests.post(GAS_WEBAPP_URL, data=json.dumps(case), timeout=20)
            print(f"📥 GAS 响应: {response.text}")
        except Exception as e:
            print(f"❌ 错误: {e}")
        time.sleep(0.5)

if __name__ == "__main__":
    debug_update_status()