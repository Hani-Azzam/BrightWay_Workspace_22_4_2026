from dataclasses import dataclass

from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from base.agent_base import BaseAgent


@dataclass
class LlmConfig:
    api_key: str
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.0


class LlmClient:
    def __init__(self, config: LlmConfig) -> None:
        if not config.api_key:
            raise ValueError("LlmClient.api_key key is required and cannot be None")
        if not config.model_name:
            raise ValueError("LlmClient.model_name name is required and cannot be None")
        if not config.temperature: # this can be improved to check if T is within range(0,2) instead
            raise ValueError("LlmClient.temperature is required and cannot be None")

        self._llm = ChatGoogleGenerativeAI(
            model=config.model_name,
            google_api_key=config.api_key,
            temperature=config.temperature,
        )
        self._parser = StrOutputParser()

    def build_chain(self, prompt_template: ChatPromptTemplate):
        return prompt_template | self._llm | self._parser

    def invoke(self, message: list[BaseMessage]) -> str:
        return self._parser.invoke(self._llm.invoke(message))



