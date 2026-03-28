import os
from autogal.agents.writer.agent import WriterAgent
from autogal.agents.artist.agent import ArtistAgent
from autogal.agents.coder.agent import CoderAgent

class AutoGalOrchestrator:
    """
    项目协调器：负责调度不同的 Agent 完成从创意到游戏的完整转化。
    """
    def __init__(self, writer: WriterAgent, artist: ArtistAgent, coder: CoderAgent):
        self.writer = writer
        self.artist = artist
        self.coder = coder

    async def run(self, user_prompt: str, output_path: str, template_path: str):
        print(f"\n🚀 [Orchestrator] 启动项目生成流程：'{user_prompt}'")
        
        # --- 第一步：生成剧本 (Writer) ---
        # 结果是一个 Scenario Pydantic 对象
        scenario = await self.writer.execute(user_description=user_prompt)
        
        # --- 第二步：构建项目骨架与代码 (Coder) ---
        # 我们先运行 Coder，创建好文件夹结构，方便 Artist 存图
        await self.coder.execute(
            scenario=scenario, 
            template_path=template_path, 
            output_path=output_path
        )
        
        # --- 第三步：生成视觉资源 (Artist) ---
        # Artist 会根据剧本里的描述，把图画好直接存进 output_path/game/images
        await self.artist.execute(
            scenario=scenario, 
            output_dir=output_path
        )

        print(f"\n🎉 [Orchestrator] 恭喜！游戏项目已生成至: {output_path}")
        print("请打开 Ren'Py 引导器并指向该目录运行测试。")