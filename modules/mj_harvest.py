import os, time, requests, datetime, shutil, re, json
from pathlib import Path
from openpyxl import load_workbook
from config import Config
from modules.spec_registry import Registry

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_LINE_PATH = PROJECT_ROOT / "Database" / "Production_Line.xlsx"
PRODUCTION_HEADERS = ["ID", "Timestamp", "Category", "Product_Type", "Style", "Title", "MJ_Prompt", "SEO_Hook", "Status"]

# --- 1. 核心通讯 (保持 V15.9 稳定性) ---
def _interaction(payload):
    headers = {"Authorization": Config.TOKEN, "Content-Type": "application/json"}
    try:
        return requests.post("https://discord.com/api/v9/interactions", json=payload, headers=headers, timeout=10)
    except: return None

def _load_production_workbook():
    wb = load_workbook(PRODUCTION_LINE_PATH)
    ws = wb.active
    headers = [ws.cell(1, c).value for c in range(1, len(PRODUCTION_HEADERS) + 1)]
    if headers != PRODUCTION_HEADERS:
        wb.close()
        raise RuntimeError(f"Production_Line.xlsx header mismatch: {headers}")
    return wb, ws, {name: idx + 1 for idx, name in enumerate(PRODUCTION_HEADERS)}

def _read_ready_tasks(product_type):
    wb, ws, cols = _load_production_workbook()
    tasks = []
    try:
        for row in range(2, ws.max_row + 1):
            row_status = str(ws.cell(row, cols["Status"]).value or "").strip()
            row_product = str(ws.cell(row, cols["Product_Type"]).value or "").strip()
            if row_status != "Ready_for_production":
                continue
            if row_product.lower() != str(product_type).lower():
                continue
            task = {header: ws.cell(row, cols[header]).value for header in PRODUCTION_HEADERS}
            task["_row"] = row
            tasks.append(task)
    finally:
        wb.close()
    return tasks

def _update_status_via_excel_com(t_id, status):
    import pythoncom
    import win32com.client

    pythoncom.CoInitialize()
    excel = None
    workbook = None
    created_excel = False
    abs_path = str(PRODUCTION_LINE_PATH)
    try:
        try:
            workbook = win32com.client.GetObject(abs_path)
            excel = workbook.Application
        except Exception:
            excel = win32com.client.DispatchEx("Excel.Application")
            created_excel = True
            excel.DisplayAlerts = False
            workbook = excel.Workbooks.Open(abs_path)

        ws = workbook.Worksheets(1)
        headers = [ws.Cells(1, c).Value for c in range(1, len(PRODUCTION_HEADERS) + 1)]
        if headers != PRODUCTION_HEADERS:
            raise RuntimeError(f"Production_Line.xlsx header mismatch: {headers}")

        max_row = ws.UsedRange.Rows.Count
        for row in range(2, max_row + 1):
            if str(ws.Cells(row, 1).Value or "").strip() == str(t_id).strip():
                ws.Cells(row, 9).Value = status
                workbook.Save()
                return True
        return False
    finally:
        if created_excel and workbook is not None:
            workbook.Close(SaveChanges=True)
        if created_excel and excel is not None:
            excel.Quit()
        pythoncom.CoUninitialize()

def _update_product_line_status(t_id, status="Completed"):
    try:
        wb, ws, cols = _load_production_workbook()
        try:
            for row in range(2, ws.max_row + 1):
                if str(ws.cell(row, cols["ID"]).value or "").strip() == str(t_id).strip():
                    ws.cell(row, cols["Status"]).value = status
                    try:
                        wb.save(PRODUCTION_LINE_PATH)
                    except PermissionError:
                        wb.close()
                        if _update_status_via_excel_com(t_id, status):
                            return
                        print(f"[WARN] ID:{t_id} not found in Production_Line.xlsx; status not updated.")
                        return
                    return
            print(f"[WARN] ID:{t_id} not found in Production_Line.xlsx; status not updated.")
        finally:
            try:
                wb.close()
            except Exception:
                pass
    except Exception as exc:
        print(f"[WARN] Failed to update Production_Line.xlsx status for ID:{t_id}: {exc}")

def _download_asset(url, save_dir, filename):
    full_path = os.path.join(save_dir, filename)
    try:
        r = requests.get(url, stream=True, timeout=20)
        if r.status_code == 200:
            with open(full_path, 'wb') as f:
                for chunk in r.iter_content(4096): f.write(chunk)
            return True
    except: pass
    return False

def _purge_asset(path, t_id, status="Defeated_Prompt"):
    if path and os.path.exists(path): shutil.rmtree(path)
    _update_product_line_status(t_id, status)
    print(f"🗑️ [ID:{t_id}] 清理并标记为 {status}")

def save_dual_metadata(save_path, task_a, task_b=None):
    if task_b:
        content = f"MASTER_ID: {task_a.get('ID')}\n[PART A] ID: {task_a.get('ID')}\nMJ_Prompt: {task_a.get('MJ_Prompt')}\n[PART B] ID: {task_b.get('ID')}\nMJ_Prompt: {task_b.get('MJ_Prompt')}\n"
    else:
        content = f"ID: {task_a.get('ID')}\nTitle: {task_a.get('Title')}\nMJ_Prompt: {task_a.get('MJ_Prompt')}\n"
    with open(os.path.join(save_path, "metadata.txt"), "w", encoding="utf-8") as f: f.write(content)

# --- 2. 生产引擎 ---
def run_logic():
    print(f"\n{'='*20} V18.3 FULL COVERAGE MODE {'='*20}")
    
    # 模式选择
    for key, obj in Registry.CATALOG.items(): print(f"[{key}] {obj.name}")
    type_key = input("大类: ") or "1"
    selected_prod = Registry.CATALOG.get(type_key, Registry.STICKER)
    for i, spec in enumerate(selected_prod.specs, 1): print(f"[{i}] {spec}")
    spec_idx = int(input("制式: ") or "1") - 1
    sel_cat, sel_spec = selected_prod.name, selected_prod.specs[spec_idx]
    is_kiss_cut = (sel_cat == "Sticker" and "Kiss-Cut" in sel_spec)

    # 任务初始化
    try:
        raw_list = _read_ready_tasks(sel_cat)
        style_map = {}
        for t in raw_list:
            s = t.get("Style", "Default"); style_map.setdefault(s, []).append(t)
        
        batch_queue = []
        for style, tasks in style_map.items():
            while tasks:
                if is_kiss_cut:
                    if len(tasks) >= 2:
                        batch_queue.append([tasks.pop(0), tasks.pop(0)])
                    else:
                        # 妥善处理末尾孤儿
                        orphan = tasks.pop(0)
                        _update_product_line_status(orphan['ID'], "Defeated_Orphan")
                        print(f"⚠️ [Orphan] {orphan['ID']} 样式配对失败，已排除。")
                else:
                    batch_queue.append([tasks.pop(0)])
        print(f"📦 预备批次: {len(batch_queue)}")
    except Exception as exc:
        print(f"[ERROR] Failed to load Production_Line.xlsx tasks: {exc}")
        return

    active_pool = {}
    MAX_PARALLEL = 3

    while batch_queue or active_pool:
        # A. 投放逻辑
        while len(active_pool) < MAX_PARALLEL and batch_queue:
            current_batch = batch_queue.pop(0)
            for task in current_batch:
                tid = str(task['ID'])
                save_path = os.path.join("Output", sel_cat, sel_spec, f"{tid}-Review")
                if not os.path.exists(save_path): os.makedirs(save_path)
                p = task['MJ_Prompt'].strip()
                # 强制参数对齐
                full_p = f"{p.split('--')[0].strip()} ID_{tid} --{p.split('--', 1)[1]}" if "--" in p else f"{p} ID_{tid}"
                
                if _interaction({"type": 2, "application_id": Config.APP_ID, "guild_id": Config.GUILD_ID, "channel_id": Config.CHANNEL_ID, "session_id": Config.SESSION_ID, "data": {"version": Config.MJ_VERSION, "id": Config.MJ_ID, "name": "imagine", "type": 1, "options": [{"type": 3, "name": "prompt", "value": full_p}]}}):
                    active_pool[tid] = {"path": save_path, "u_triggered": False, "u_received": set(), "start_time": time.time(), "task_obj": task, "batch": current_batch, "grid_done": False}
                    print(f"🎬 [{tid}] Deployed.")
                time.sleep(5)

        # B. 监听与物理收割
        if active_pool:
            time.sleep(20)
            try:
                msgs = requests.get(f"https://discord.com/api/v9/channels/{Config.CHANNEL_ID}/messages?limit=50", headers={"Authorization": Config.TOKEN}, timeout=10).json()
            except: continue

            now = time.time()
            for tid in list(active_pool.keys()):
                # 核心修复：检查 ID 是否还在池子中
                if tid not in active_pool: continue
                
                info = active_pool[tid]
                if now - info["start_time"] > 600:
                    _purge_asset(info["path"], tid, "Defeated_Timeout"); del active_pool[tid]; continue

                for m in msgs:
                    content = m.get("content", "")
                    if f"ID_{tid}" in content:
                        # Grid 捕获
                        if "Image #" not in content and m.get("attachments") and not info["grid_done"]:
                            if _download_asset(m["attachments"][0]["url"], info["path"], f"{tid}_Grid.png"):
                                info["grid_done"] = True
                                if not is_kiss_cut and not info["u_triggered"]:
                                    btns = m.get("components", [{}])[0].get("components", [])
                                    for i in range(min(4, len(btns))):
                                        _interaction({"type": 3, "application_id": Config.APP_ID, "guild_id": Config.GUILD_ID, "channel_id": Config.CHANNEL_ID, "message_id": m['id'], "session_id": Config.SESSION_ID, "data": {"component_type": 2, "custom_id": btns[i]["custom_id"]}})
                                        time.sleep(2)
                                    info["u_triggered"] = True
                        # U图 捕获
                        if not is_kiss_cut and "Image #" in content and m.get("attachments"):
                            u_idx = content.split("Image #")[-1][0]
                            if u_idx not in info["u_received"]:
                                if _download_asset(m["attachments"][0]["url"], info["path"], f"{tid}_U{u_idx}.png"):
                                    info["u_received"].add(u_idx)

                # 判定完成
                success = info["grid_done"] if is_kiss_cut else (info["grid_done"] and len(info["u_received"]) >= 4)
                if success:
                    if is_kiss_cut:
                        partner_id = next((t['ID'] for t in info['batch'] if str(t['ID']) != tid), None)
                        if partner_id in active_pool and active_pool[partner_id]["grid_done"]:
                            p_info = active_pool[partner_id]
                            m_path = os.path.join("Output", sel_cat, sel_spec, f"MASTER_{tid}")
                            os.makedirs(m_path, exist_ok=True)
                            shutil.move(os.path.join(info["path"], f"{tid}_Grid.png"), m_path)
                            shutil.move(os.path.join(p_info["path"], f"{partner_id}_Grid.png"), m_path)
                            shutil.rmtree(info["path"]); shutil.rmtree(p_info["path"])
                            save_dual_metadata(m_path, info['task_obj'], p_info['task_obj'])
                            _update_product_line_status(tid); _update_product_line_status(partner_id)
                            print(f"💎 [MASTER] {tid} & {partner_id} PAIRED.")
                            del active_pool[tid]
                            del active_pool[partner_id]
                    else:
                        save_dual_metadata(info["path"], info['task_obj'])
                        _update_product_line_status(tid); print(f"✅ [DONE] {tid}"); del active_pool[tid]

    print("\n🏁 全覆盖流程结束。")

if __name__ == "__main__":
    run_logic()
