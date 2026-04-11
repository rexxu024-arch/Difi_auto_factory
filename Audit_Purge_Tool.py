import requests
import json
import time

# 配置你的 GAS URL
GAS_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbwPyI_nd21Cn0exMaa9BC6AiTTuDt-NyN6siw9CockmaPLgufRKNMLT5-PsC0RI32SQNw/exec"

# 审计黑名单关键词
TARGET_KEYWORDS = ["Vergil", "Raiden", "雷电", "Jack the Ripper"]

def run_purge_audit():
    print(f"🚀 启动工业审计：物理抹除程序...")
    print(f"🎯 目标关键词: {TARGET_KEYWORDS}")
    
    # --- 1. 拉取当前 Production_Line 的所有 DNA 数据 ---
    try:
        # 假设你的 GAS 支持 action=getDNA 参数来获取全量 JSON
        res = requests.get(GAS_WEBAPP_URL, params={"action": "getDNA"}, timeout=20)
        all_tasks = res.json()
    except Exception as e:
        print(f"🛑 无法拉取数据: {e}")
        return

    purged_count = 0
    
    # --- 2. 遍历并匹配关键词 ---
    for task in all_tasks:
        t_id = str(task.get('ID', '')).strip()
        # 扫描 ID、Title、MJ_Prompt
        content_to_scan = f"{t_id} {task.get('Title', '')} {task.get('MJ_Prompt', '')}".lower()
        
        # 检查是否命中关键词
        if any(kw.lower() in content_to_scan for kw in TARGET_KEYWORDS):
            print(f"🚨 审计命中: [{t_id}]")
            
            # --- 3. 发送 PURGE 指令执行物理删除 ---
            # 构造 V52.0 协议 payload
            payload = {
                "id": t_id,
                "status": "PURGE"  # 触发 GAS 中的 sheetB.deleteRow 逻辑
            }
            
            try:
                response = requests.post(GAS_WEBAPP_URL, data=json.dumps(payload), timeout=20)
                if "Purged 1" in response.text:
                    print(f"   🔥 表格行已物理抹除。")
                    purged_count += 1
                else:
                    print(f"   ⚠️ GAS 响应异常: {response.text}")
            except Exception as e:
                print(f"   ❌ 发送销毁指令失败: {e}")
            
            # 避免请求频率过高
            time.sleep(0.5)

    print(f"\n🏁 审计结束。共从 Production_Line 抹除了 {purged_count} 行违规数据。")

if __name__ == "__main__":
    run_purge_audit()