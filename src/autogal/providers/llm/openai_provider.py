import os
import json
import textwrap
from typing import Type
from openai import AsyncOpenAI
from autogal.providers.llm.base import LLMProvider, T

class OpenAICompatibleProvider(LLMProvider):
    def __init__(self, api_key: str = None, base_url: str = None, model: str = "qwen-max"):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.base_url = base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.model = model
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: Type[T],
        max_retries: int = 3
    ) -> T:
        last_error = None
        last_content = None

        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": textwrap.dedent(system_prompt).strip()},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )

                content = response.choices[0].message.content
                last_content = content
                clean_json = content.strip().replace("```json", "").replace("```", "")
                data = json.loads(clean_json)
                return response_model.model_validate(data)

            except Exception as e:
                last_error = e
                print(f"⚠️ 第 {attempt + 1} 次尝试失败: {e}")
                if attempt < max_retries - 1:
                    print("   正在重试...")

        print(f"\n❌ 重试 {max_retries} 次后仍然失败")
        print(f"\n📄 AI 原始输出:\n{last_content}")
        raise last_error