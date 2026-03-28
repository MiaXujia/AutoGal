import os
import httpx
from autogal.providers.image.base import ImageProvider

# 这是一个通义万相的大模型Provider，用于图片生成，它实现了多模态图片抽象类
'''
通义万相（Wanxiang）目前在阿里 DashScope 中也有 OpenAI 兼容端点
但为了更精细地控制参数（如比例、风格）
我们通常使用官方 SDK 或简单的 HTTP 请求。
'''

import asyncio
import httpx
import os

class WanxiangProvider(ImageProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        # 提交任务的地址
        self.submit_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
        # 查询任务的地址（需要拼上 task_id）
        self.status_url = "https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"

    async def text_to_image(self, prompt: str, save_path: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable"
        }
        
        payload = {
            "model": "wanx-v1",
            "input": {"prompt": prompt},
            "parameters": {"style": "<anime>", "size": "1280*720"}
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            # --- 1. 提交任务 ---
            resp = await client.post(self.submit_url, headers=headers, json=payload)
            submit_data = resp.json()
            if "output" not in submit_data:
                raise Exception(f"提交失败: {submit_data}")
            
            task_id = submit_data["output"]["task_id"]
            print(f"🎨 [Artist] 任务已提交 ID: {task_id}")

            # --- 2. 轮询状态 ---
            max_retries = 30 # 最多等待约 60 秒
            image_url = None
            
            for i in range(max_retries):
                # 拿着 task_id 去查状态
                status_resp = await client.get(
                    self.status_url.format(task_id=task_id), 
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                status_data = status_resp.json()
                task_status = status_data["output"]["task_status"]

                if task_status == "SUCCEEDED":
                    image_url = status_data["output"]["results"][0]["url"]
                    print(f"✨ [Artist] 图片生成成功！开始下载...")
                    break
                elif task_status == "FAILED":
                    raise Exception(f"图片生成失败: {status_data['output']['message']}")
                
                # 每 2 秒查一次
                await asyncio.sleep(2)
            
            if not image_url:
                raise Exception("图片生成超时")

            # --- 3. 下载并保存 ---
            img_resp = await client.get(image_url)
            if img_resp.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(img_resp.content)
                print(f"💾 [Artist] 图片已保存至: {save_path}")
                return save_path
            else:
                raise Exception("图片下载失败")