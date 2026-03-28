from abc import ABC, abstractmethod

# 这里就是多模态——>图片的大模型抽象类
class ImageProvider(ABC):
    @abstractmethod
    async def text_to_image(self, prompt: str, save_path: str) -> str:
        """根据提示词生成图片并保存到本地，返回保存路径"""
        pass