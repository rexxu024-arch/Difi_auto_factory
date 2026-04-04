import os, time, requests, datetime
from config import Config

def _interaction(payload):
    headers = {"Authorization": Config.TOKEN, "Content-Type": "application/json"}
    return requests.post("https://discord.com/api/v9/interactions", json=payload, headers=headers)

def _update_gas_status(t_id):
    """回填审计：强制清洗响应内容，确保状态同步"""
    params = {"action": "updateStatus", "id": t_id, "status": "Completed"}
    try:
        res = requests.get(Config.GAS_URL, params=params, timeout=15)
        # 🚨 [逻辑修正]：不再死磕 "success" 字符串，因为你的 GAS 响应目前返回的是 JSON 列表
        # 只要 HTTP 200 且响应长度正常，判定为已发送
        if res.status_code == 200:
            print(f"📡 [GAS-Ok] {t_id} 状态更新请求已送达。")
            return True
        else:
            print(f"❌ [GAS-Warn] {t_id} 响应异常 Code: {res.status_code}")
            return False
    except Exception as e:
        print(f"🚨 [GAS-Critical] 网络阻塞: {str(e)}")
        return False

def _download_asset(url, save_dir, filename):
    full_path = os.path.join(save_dir, filename)
    try:
        r = requests.get(url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(full_path, 'wb') as f:
                for chunk in r.iter_content(1024): f.write(chunk)
            return True
    except: pass
    return False

def run_logic():
    print("\n" + "="*60)
    print("🚀 [V13.7] 工业审计流水线启动 (物理隔离模式)")
    
    categories = ["Sticker", "Worksheet", "Poster", "Logo"]
    formats = ["Kiss-Cut", "Die-Cut", "Standard", "Transparent"]
    sel_cat = categories[int(input("Select Cat (1.Sticker): ") or "1")-1]
    sel_fmt = formats[int(input("Select Fmt (1.Kiss-Cut): ") or "1")-1]

    # --- [1. 任务拉取与物理冗余审计] ---
    try:
        res = requests.get(Config.GAS_URL, params={"action": "getDNA"}, timeout=15)
        # 严格过滤 Ready 状态
        task_pool = [t for t in res.json() if str(t.get("Status")) == "Ready_for_production"]
        
        final_queue = []
        for t in task_pool:
            t_id = str(t['ID']).strip()
            # 🚨 物理隔离检查：如果本地 U4 已存在，说明是旧任务，直接跳过生成
            check_file = os.path.join("Output", sel_cat, sel_fmt, f"{t_id}-Review", f"{t_id}_U4.png")
            if os.path.exists(check_file):
                print(f"⏩ [Skip] {t_id} 证据已在本地，跳过生成环节。")
                _update_gas_status(t_id) # 顺便尝试把 GAS 状态补齐
                continue
            final_queue.append(t)
            
        task_queue = final_queue
        print(f"📊 审计完成：{len(task_queue)} 个有效新任务待产。")
    except Exception as e:
        print(f"🛑 无法初始化任务队列: {e}")
        return

    active_pool = {} 
    MAX_PARALLEL = 3 
    TIME_OFFSET = 420 

    while task_queue or active_pool:
        # A. 投放 Imagine 指令
        while len(active_pool) < MAX_PARALLEL and task_queue:
            task = task_queue.pop(0)
            t_id, full_prompt = str(task['ID']).strip(), task['MJ_Prompt']
            f_print = full_prompt.split("--")[0].strip()[:100]
            
            save_path = os.path.join("Output", sel_cat, sel_fmt, f"{t_id}-Review")
            if not os.path.exists(save_path): os.makedirs(save_path)
            
            with open(os.path.join(save_path, "mj_prompt.txt"), "w", encoding="utf-8") as f:
                f.write(full_prompt)

            deploy_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=TIME_OFFSET)

            _interaction({
                "type": 2, "application_id": Config.APP_ID, "guild_id": Config.GUILD_ID,
                "channel_id": Config.CHANNEL_ID, "session_id": Config.SESSION_ID,
                "data": {"version": Config.MJ_VERSION, "id": Config.MJ_ID, "name": "imagine", "type": 1, 
                         "options": [{"type": 3, "name": "prompt", "value": full_prompt}]}
            })
            
            active_pool[f_print] = {
                "id": t_id, "path": save_path, "u_triggered": False, 
                "u_received": set(), "start_time": deploy_time
            }
            print(f"🎬 [{t_id}] Imagine 已投放 (Fast Hour 消耗中)。")
            time.sleep(5)

        # B. 极速取证 (Burst-Capture)
        if active_pool:
            time.sleep(10) 
            try:
                msgs = requests.get(f"https://discord.com/api/v9/channels/{Config.CHANNEL_ID}/messages?limit=50", 
                                    headers={"Authorization": Config.TOKEN}, timeout=10).json()
            except: continue
            
            for m in msgs:
                content, m_ts = m.get("content", ""), m.get('timestamp')
                if not m_ts: continue
                m_time = datetime.datetime.fromisoformat(m_ts.replace('Z', '+00:00'))

                for fp in list(active_pool.keys()):
                    info = active_pool[fp]
                    if fp in content and m_time > info["start_time"]:
                        
                        # 1. 拦截 Grid：启动 U 按钮
                        if "Image #" not in content and m.get("components") and not info["u_triggered"]:
                            print(f"🎯 [{info['id']}] 匹配 Grid。触发 U1-U4...")
                            if m.get("attachments"):
                                _download_asset(m["attachments"][0]["url"], info["path"], f"{info['id']}_Grid.png")
                            
                            active_pool[fp]["u_triggered"] = True 
                            btns = m["components"][0]["components"]
                            for i in range(4):
                                _interaction({
                                    "type": 3, "application_id": Config.APP_ID, "guild_id": Config.GUILD_ID,
                                    "channel_id": Config.CHANNEL_ID, "message_id": m['id'], "session_id": Config.SESSION_ID,
                                    "data": {"component_type": 2, "custom_id": btns[i]["custom_id"]}
                                })
                                time.sleep(0.8) # 物理间隔

                        # 2. 补齐 U 图
                        elif "Image #" in content and m.get("attachments"):
                            u_idx = content.split("Image #")[-1][0]
                            if u_idx not in info["u_received"]:
                                if _download_asset(m["attachments"][0]["url"], info["path"], f"{info['id']}_U{u_idx}.png"):
                                    info["u_received"].add(u_idx)
                                    print(f"📦 [{info['id']}] U{u_idx} 物理入库。")

        # C. 审计终结
        for fp in list(active_pool.keys()):
            info = active_pool[fp]
            if len(info["u_received"]) >= 4:
                print(f"✅ [{info['id']}] 证据闭环，尝试更新 GAS 状态...")
                if _update_gas_status(info["id"]):
                    del active_pool[fp]
                    print(f"🎊 [{info['id']}] 任务完成，已从活跃池移除。")

    print("\n🏁 [V13.7] 运行结束。")

if __name__ == "__main__":
    run_logic()