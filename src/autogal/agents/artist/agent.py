import os
from PIL import Image          # 新增：用于读取和保存图片
from rembg import remove       # 新增：用于去除背景
from autogal.agents.base import BaseAgent
from autogal.core.domain.scenario import Scenario
from autogal.providers.image.base import ImageProvider

class ArtistAgent(BaseAgent):
    def __init__(self, image_provider: ImageProvider):
        self.img_hw = image_provider

    async def execute(self, scenario: Scenario, output_dir: str):
        """
        根据剧本生成所有必要的图像资产
        """
        image_folder = os.path.join(output_dir, "game", "images")
        os.makedirs(image_folder, exist_ok=True)

        # 1. 生成所有背景图 (背景图不需要抠图)
        for scene in scenario.scenes:
            bg_filename = f"bg_{scene.scene_id}.png"
            path = os.path.join(image_folder, bg_filename)
            if not os.path.exists(path):
                print(f"🎨 [ArtistAgent] 正在生成背景: {bg_filename}...")
                await self.img_hw.text_to_image(scene.bg_prompt, path)

        # 2. 生成所有角色立绘（含自动抠图处理）
        for char in scenario.characters:
            char_filename = f"char_{char.var_name}.png"
            path = os.path.join(image_folder, char_filename)
            
            if not os.path.exists(path):
                # 提示增强：加入 "simple white background"，让背景尽可能干净，提高 rembg 的抠图精度
                prompt = f"{char.appearance_prompt}, standing, solo, simple white background"
                print(f"🎨 [ArtistAgent] 正在生成立绘: {char_filename}...")
                
                # A. 先让 Provider 生成原图并保存到 path
                await self.img_hw.text_to_image(prompt, path)
                
                # B. --- 新增的抠图魔法 ---
                print(f"✂️ [ArtistAgent] 正在为 {char_filename} 去除背景...")
                try:
                    # 读取刚下载的带背景原图
                    input_image = Image.open(path)
                    
                    # 使用 rembg 移除背景 (返回一张带有 Alpha 透明通道的新图片)
                    output_image = remove(input_image)
                    
                    # 覆盖原来的文件，并明确指定保存为 PNG 格式（以保留透明度）
                    output_image.save(path, format="PNG")
                    print(f"✅ [ArtistAgent] {char_filename} 抠图成功，已保存为透明立绘！")
                    
                except Exception as e:
                    print(f"❌ [ArtistAgent] 抠图环节发生错误: {str(e)}。已保留原图。")
        
        print("✅ [ArtistAgent] 所有美术资产生成并处理完毕。")

'''
资产去重：我们在代码里加了 if not os.path.exists(path)。
如果一个角色在多个场景出现，我们只画一次，节省 API 额度和运行时间。

Prompt 自动增强：我们在生成立绘时自动添加了 standing, solo 等后缀。
这是 Agent 的“智能”体现，它知道 Ren'Py 的立绘需要什么样的构图。

目录规范：ArtistAgent 
直接按照 Ren'Py 的标准目录结构（game/images）进行保存，
方便 CoderAgent 直接引用
'''