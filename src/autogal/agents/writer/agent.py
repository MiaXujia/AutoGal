import json
from autogal.agents.base import BaseAgent
from autogal.core.domain.scenario import Scenario

class WriterAgent(BaseAgent):
    async def execute(self, user_description: str) -> Scenario:
        example_json = {
            "title": "上海之梦",
            "characters": [
                {
                    "name": "晓晓",
                    "var_name": "xiao",
                    "color": "#ffffff",
                    "appearance_prompt": "a girl in school uniform"
                }
            ],
            "scenes": [
                {
                    "scene_id": "scene_1",
                    "bg_prompt": "a futuristic park at sunset",
                    "dialogues": [
                        {"speaker_var": "xiao", "text": "你好呀。", "emotion": "happy"},
                        {"speaker_var": None, "text": "她轻轻招了招手。", "emotion": "neutral"}
                    ]
                }
            ]
        }

        system_prompt = """你是一个专业的视觉小说编剧。请将用户的描述转化为详细的剧本。

【输出格式要求】：
必须输出有效的 JSON，不要包含任何 Markdown 或其他文字。

【JSON 结构说明】：
- scenes 是一个数组，每个元素代表一个场景
- 每个 scene 必须包含: scene_id, bg_prompt, dialogues
- dialogues 是一个数组，包含该场景中的所有对话
- 每个 dialogue 包含一个字典类型 对应的键有三个: speaker_var (可为 null), text, emotion

【重要】：
- scenes 数组的元素是 scene 对象，不是 dialogue 对象
- dialogues 必须嵌套在 scene 对象内部
- 不要把 dialogue 直接放在 scenes 数组里

【正确示例】：
""" + json.dumps(example_json, ensure_ascii=False, indent=2)

        user_prompt = f"""请根据以下描述生成剧本，严格按照 JSON 格式输出：

{user_description}

记住：scenes 里每个元素必须有 scene_id、bg_prompt 和 dialogues 三个字段。"""

        scenario = await self.llm.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=Scenario
        )
        return scenario