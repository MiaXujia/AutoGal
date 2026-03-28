from autogal.agents.base import BaseAgent
from autogal.core.domain.scenario import Scenario
from autogal.providers.image.base import ImageProvider
import os

# ArtistAgent 的职责是遍历剧本，决定哪些需要画，并管理文件名
class ArtistAgent(BaseAgent):
    def __init__(self, image_provider: ImageProvider):
        self.img_hw = image_provider

    async def execute(self, scenario: Scenario, output_dir: str):
        """
        根据剧本生成所有必要的图像资产
        """
        image_folder = os.path.join(output_dir, "game", "images")
        os.makedirs(image_folder, exist_ok=True)

        # 1. 生成所有背景图
        for scene in scenario.scenes:
            bg_filename = f"bg_{scene.scene_id}.png"
            path = os.path.join(image_folder, bg_filename)
            if not os.path.exists(path):
                await self.img_hw.text_to_image(scene.bg_prompt, path)

        # 2. 生成所有角色立绘
        for char in scenario.characters:
            char_filename = f"char_{char.var_name}.png"
            path = os.path.join(image_folder, char_filename)
            if not os.path.exists(path):
                # 提示：立绘通常需要增加 "white background" 或 "transparent" 提示词
                prompt = f"{char.appearance_prompt}, standing, solo, simple background"
                await self.img_hw.text_to_image(prompt, path)
        
        print("✅ [ArtistAgent] 所有美术资产生成并保存完毕。")

'''
资产去重：我们在代码里加了 if not os.path.exists(path)。
如果一个角色在多个场景出现，我们只画一次，节省 API 额度和运行时间。

Prompt 自动增强：我们在生成立绘时自动添加了 standing, solo 等后缀。
这是 Agent 的“智能”体现，它知道 Ren'Py 的立绘需要什么样的构图。

目录规范：ArtistAgent 
直接按照 Ren'Py 的标准目录结构（game/images）进行保存，
方便 CoderAgent 直接引用
'''