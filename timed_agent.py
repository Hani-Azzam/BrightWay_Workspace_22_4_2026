import time

from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from base.agent_base import BaseAgent
from services.llm_client import LlmClient


class TimedAgent(BaseAgent):

    _SYSTEM ="You are helpful AI assistant specialising in agentic AI systems."

    def __init__(self, llm_client: LlmClient):
        self._llm = llm_client
        self._history: list[BaseMessage] = []
        self._prompt = ChatPromptTemplate.from_messages([
            ("system", self._SYSTEM),
            MessagesPlaceholder("history"),
            ("human", "{question}"),
        ])
        self._chain = llm_client.build_chain(self._prompt)
        # list of response time durations
        self._durations_list = []
        self._avg_duration : float = 0
        self._min_duration : float = float('inf')
        self._max_duration : float= 0
        self._durations_sum : float = 0 # used to compute avg
        # define threshold for how long a llm response can be in seconds before a warning is shown (for the Bonus requirement)
        self._slow_threshold_s: float = 3.0

    def chat(self, user_input: str) -> str:
        start = time.perf_counter() # start timer for duration
        response : str = self._chain.invoke(
            {"history": self._history, "question": user_input}
        )
        end = time.perf_counter() # stop timer for duration
        self._history.append(HumanMessage(content=user_input))
        self._history.append(AIMessage(content=response))
        # calc duration and add it to list and update average, min, max durations
        duration = end - start
        self._durations_list.append(duration)
        self._durations_sum += duration
        self._avg_duration = self._durations_sum / len(self._durations_list)
        self._min_duration = min(self._min_duration, duration)
        self._max_duration = max(self._max_duration, duration)
        # check if duration threshold has been surpassed (for the Bonus requirement)
        if duration > self._slow_threshold_s:
            warning_msg = "[WARNING: response took " + str(duration) + "s — threshold is " + str(self._slow_threshold_s) + "s]"
            response = response + "\n\n" + warning_msg
        return response

    def reset(self) -> None:
        self._history.clear()
        self._durations_list.clear() # clear durations list
        self._avg_duration = 0
        self._min_duration = float('inf')
        self._max_duration = 0
        self._durations_sum = 0

    def history_text(self) -> str:
        if not self._history:
            return "(no history)"
        lines = []
        for msg in self._history:
            role = "You" if isinstance(msg, HumanMessage) else "Agent"
            lines.append(f" [{role}] {msg.content[:100]}")
        return "\n".join(lines)

    def stats(self) -> dict:
        if not self._durations_list:
            return {"turns": 0, "avg_s": 0.0, "min_s": 0.0, "max_s": 0.0}
        return {"turns": len(self._durations_list), "avg_s": self._avg_duration, "min_s": self._min_duration, "max_s": self._max_duration}

