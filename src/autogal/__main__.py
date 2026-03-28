import asyncio
import os
from dotenv import load_dotenv

# 导入我们的组件
from autogal.providers.llm.openai_provider import OpenAICompatibleProvider
from autogal.providers.image.wanxiang_provider import WanxiangProvider
from autogal.agents.writer.agent import WriterAgent
from autogal.agents.artist.agent import ArtistAgent
from autogal.agents.coder.agent import CoderAgent
from autogal.agents.orchestrator import AutoGalOrchestrator

async def main():
    # 0. 初始化配置
    load_dotenv()
    
    # 获取路径
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    template_path = os.path.join(base_dir, "templates", "base_game")
    output_path = os.path.join(base_dir, "outputs", "my_first_ai_game")

    # 1. 组装 Provider (底层工具)
    # 假设你用通义千问兼容 OpenAI 的端点
    llm_provider = OpenAICompatibleProvider(
        model="qwen-plus" # qwen-max 对嵌套 JSON 支持不好
    )
    img_provider = WanxiangProvider()

    # 2. 实例化 Agent (员工)
    writer = WriterAgent(llm=llm_provider)
    artist = ArtistAgent(image_provider=img_provider)
    coder = CoderAgent(llm=None) # Coder 目前是纯逻辑，不需要 LLM

    # 3. 启动协调器 (经理)
    orchestrator = AutoGalOrchestrator(writer, artist, coder)
    
    # 4. 执行！
    prompt = "那天雨很大，撑着伞的我看到了淋成落汤鸡的前女友。她穿着一身碎花裙，微卷的头发因雨水贴在了额头上。"
    await orchestrator.run(prompt, output_path, template_path)

if __name__ == "__main__":
    asyncio.run(main())