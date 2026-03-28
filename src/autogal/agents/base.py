from abc import ABC, abstractmethod
from autogal.providers.llm.base import LLMProvider

# 把agent和provider关联起来

class BaseAgent(ABC):
    def __init__(self, llm: LLMProvider):
        self.llm = llm

    @abstractmethod
    async def execute(self, *args, **kwargs):
        """每个 Agent 必须实现的执行逻辑"""
        pass