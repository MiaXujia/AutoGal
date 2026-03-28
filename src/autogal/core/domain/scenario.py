from pydantic import BaseModel, Field
from typing import List, Optional
from autogal.core.domain.character import Character


# 剧本结构

## 台词 对白
class Dialogue(BaseModel):
    speaker_var: Optional[str] = Field(None, description="说话人的变量名")
    text: str = Field(..., description="对话文本")
    emotion: str = Field(default="neutral", description="角色情绪状态")


## 场景
class Scene(BaseModel):
    scene_id: str = Field(..., description="场景ID")
    bg_prompt: str = Field(..., description="场景背景描述词")
    dialogues: List[Dialogue]

class Scenario(BaseModel):
    title: str
    characters: List[Character]
    scenes: List[Scene]