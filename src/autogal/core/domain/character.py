from pydantic import BaseModel,Field
'''
Pydantic 是 Python 中最流行的数据验证和设置管理库。
它利用 Python 类型提示来验证输入数据、解析数据格式，
并提供优秀的 IDE 支持。
'''

# 初步定义角色
'''
用途1：在 agent 或 pipeline 中直接创建角色
alice = Character(
    name="艾丽丝",
    var_name="alice",
    color="#ff88aa",
    appearance_prompt="anime style, cute girl, long blonde hair, blue eyes, wearing white dress"
)

用途2： Writer Agent 让 LLM 生成角色，返回 JSON
llm_response = """
{
    "name": "艾丽丝",
    "var_name": "alice",
    "color": "#ff88aa",
    "appearance_prompt": "anime style, cute girl, long blonde hair, blue eyes"
}
"""

# 自动验证和解析
alice = Character.model_validate_json(llm_response)

用途3： 
Agent之间传递，比如剧本Agent收到一个角色，
或者创建一个角色，它把这个角色传递给美术agent
然后Builder Agent也可以收到它们的角色json串，从而生成Ren'Py代码

'''

# 角色数据结构

class Character(BaseModel):
    name: str = Field(..., description="角色的显示名称")
    var_name: str = Field(..., description="Ren'Py 变量名，如 'e'")
    color: str = Field(default="#ffffff", description="名字颜色")
    appearance_prompt: str = Field(..., description="绘画用英文描述词")