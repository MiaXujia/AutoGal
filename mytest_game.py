import openai
import os
import re

from dotenv import load_dotenv  # 添加这一行

# --- 加载 .env 文件中的环境变量 ---
load_dotenv()  # 这会读取项目根目录下的 .env 文件

# --- 配置区（从环境变量读取）---
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
PROJECT_PATH = os.getenv("PROJECT_PATH")

# 可选：设置默认值（如果 .env 中没有的话）
if not PROJECT_PATH:
    PROJECT_PATH = "D:/work-finding/my_test_game/My_first_test_game/game"

SCRIPT_FILE = os.path.join(PROJECT_PATH, "script.rpy")

client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)

def clean_ai_response(raw_content):
    """
    核心清洗函数：只保留真正的 Ren'Py 代码
    """
    # 1. 移除 Markdown 的代码块标记
    clean_code = re.sub(r"```[a-zA-Z]*", "", raw_content)
    clean_code = clean_code.replace("```", "").strip()
    
    # 2. 查找 label start: 的位置，把之前的废话全部切掉
    # 但要注意保留 define 和 default 语句
    lines = clean_code.split('\n')
    final_lines = []
    start_found = False
    
    for line in lines:
        # 保留定义语句和 label 之后的内容
        if line.strip().startswith(("define", "default", "image", "label", "init")):
            start_found = True
        if start_found:
            final_lines.append(line)
            
    return "\n".join(final_lines)

def generate_vibe_code(user_vibe):
    print("🚀 AI 正在构思 Vibe 代码...")
    
    # 结构化 Prompt：给 AI 一个填空题，而不是简答题
    prompt = f"""
    你是一个 Ren'Py 专家。请直接输出代码，不要任何解释文字。
    
    【必须遵守的结构】：
    1. 顶部定义区：使用 define 定义角色，default 定义变量。
    2. 图像区：使用 image 语句。
    3. 逻辑区：从 label start: 开始。
    
    【语法规则】：
    - 角色对话必须是：变量名 "内容"（严禁换行）。
    - 缩进：label 内逻辑缩进 4 个空格，menu 选项缩进 4 个空格，选项后内容再缩进 4 个空格。
    - 效果：仅使用 with fade, with dissolve, with vpunch。
    
    【剧本氛围】：
    {user_vibe}
    """
    
    try:
        response = client.chat.completions.create(
            model="qwen-plus", # 建议使用能力更强的模型
            messages=[{"role": "system", "content": "你是一个只输出 Ren'Py 代码的机器人。"},
                      {"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"# 错误: {str(e)}"

def update_renpy_script(code):
    clean_code = clean_ai_response(code)
    
    if not clean_code:
        print("❌ 警告：AI 返回了空内容或格式完全错误。")
        return

    with open(SCRIPT_FILE, "w", encoding="utf-8") as f:
        f.write(clean_code)
    
    print("-" * 30)
    print(clean_code) # 在控制台打印出来方便你检查
    print("-" * 30)
    print("✅ 脚本已更新！请回到 Ren'Py 窗口，按下 Shift+R 重载游戏。")

if __name__ == "__main__":
    print("=== Galgame Vibe Agent 已启动 ===")
    while True:
        vibe = input("\n[输入氛围描述] (或输入 'exit' 退出): ")
        if vibe.lower() == 'exit':
            break
        
        raw_ai_code = generate_vibe_code(vibe)
        update_renpy_script(raw_ai_code)