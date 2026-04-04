import sys
from modules import mentor_hub, product_line, mj_harvest, iron_audit
from config import Config

def print_stage(num, title, desc):
    print(f"\n{'='*60}\n🎬 [STAGE {num}] - {title}\n📌 {desc}\n{'='*60}")

def main():
    if not Config.validate(): 
        sys.exit("❌ [CONFIG ERROR] 物理变量缺失，请检查 .env 文件。")

    while True:
        print("\n" + "💎"*25)
        print("🏛️  [GREY ARCHITECT V13.0] - PRODUCTION HUB")
        print("💎"*25)
        print("1️⃣ [MENTOR_HUB]      - 策略大脑 (Niche Analysis)")
        print("2️⃣ [PRODUCT_LINE]    - DNA 生成 (GAS DNA Sync)")
        print("3️⃣ [MJ_HARVEST]      - 钢铁收割 (Imagine & Auto-Un)")
        print("4️⃣ [IRON_AUDIT]      - 物理审计 (Edit & Archive)")
        print("0️⃣ [EXIT]            - 系统关闭")
        
        choice = input("\n👉 请选择执行阶段 (0-4): ").strip()

        if choice == '1':
            print_stage(1, "MENTOR_HUB", "分析市场 Niche 与 Prompt 逻辑架构...")
            mentor_hub.run_logic()
        elif choice == '2':
            print_stage(2, "PRODUCT_LINE", "同步 GAS 任务数据，准备生产位点...")
            product_line.run_logic()
        elif choice == '3':
            print_stage(3, "MJ_HARVEST", "启动异步收割：批量发送指令并追踪图片落地...")
            mj_harvest.run_logic()
            print("\n✅ [STAGE 3 COMPLETE] 所有任务已触发 Un 并验证下载。")
        elif choice == '4':
            print_stage(4, "IRON_AUDIT", "启动物理加工：去背景、DPI 注入与归档...")
            iron_audit.run_logic()
            print("\n✅ [STAGE 4 COMPLETE] 审计完成，任务已移至 -Ready。")
        elif choice == '0':
            print("👋 逻辑核心已离线。")
            break
        else:
            print("⚠️ 无效输入，请遵循 V13.0 协议流程。")

if __name__ == "__main__":
    main()