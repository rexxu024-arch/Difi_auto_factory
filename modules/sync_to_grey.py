import os

# 配置：需要包含的文件后缀
INCLUDE_EXTENSIONS = {'.py', '.txt', '.json'}
# 排除文件夹：增加 .venv 防止混入库代码
EXCLUDE_DIRS = {'.git', '__pycache__', 'venv', '.venv', 'node_modules', 'output', 'temp_audit'}
# 排除敏感或无关文件：增加 .env 确保安全，排除脚本自身
EXCLUDE_FILES = {'.env', 'sync_to_grey.py', 'GREY_CONTEXT.txt'}

OUTPUT_FILE = "GREY_CONTEXT.txt"

def generate_snapshot():
    print("🛡️  正在生成安全审计快照（已物理隔离 .env 和 .venv）...")
    
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        # 1. 写入目录树
        out.write("### [1] PROJECT STRUCTURE (SECURITY FILTERED) ###\n")
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            level = root.replace(".", "").count(os.sep)
            indent = " " * 4 * level
            out.write(f"{indent}{os.path.basename(root)}/\n")
            sub_indent = " " * 4 * (level + 1)
            for f in files:
                if any(f.endswith(ext) for ext in INCLUDE_EXTENSIONS) and f not in EXCLUDE_FILES:
                    out.write(f"{sub_indent}{f}\n")
        
        out.write("\n" + "="*60 + "\n\n")
        
        # 2. 写入核心逻辑
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                if any(f.endswith(ext) for ext in INCLUDE_EXTENSIONS) and f not in EXCLUDE_FILES:
                    file_path = os.path.join(root, f)
                    out.write(f"### FILE: {file_path} ###\n")
                    try:
                        with open(file_path, "r", encoding="utf-8") as content:
                            out.write(content.read())
                    except Exception as e:
                        out.write(f"Error reading file: {e}")
                    out.write("\n\n" + "="*60 + "\n\n")

    print(f"✅ 安全快照生成完毕。请发送 '{OUTPUT_FILE}' 给 Grey 进行审计。")

if __name__ == "__main__":
    generate_snapshot()