from abc import ABC, abstractmethod
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class LLMProvider(ABC):
    @abstractmethod
    async def generate_structured(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        response_model: Type[T]
    ) -> T:
        """发送请求并直接返回解析好的 Pydantic 模型对象"""
        pass

'''
这段代码定义了一个统一的 LLM 调用接口：

LLMProvider：抽象基类，规定所有 LLM 必须实现的方法

generate_structured：核心方法，让 LLM 返回结构化的 Pydantic 模型

泛型 T：确保类型安全，返回你期望的模型类型

这样设计后，你可以：

轻松切换不同的 LLM（OpenAI ↔ Claude）

方便测试（用 Mock 代替真实 API）

所有 Agent 用统一的 API 调用 LLM

这是多 Agent 系统中基础设施层（Providers）的标准设计模式。

'''