from abc import ABC, abstractmethod

class BaseAgent(ABC):

    @abstractmethod
    def chat(self, user_input: str) -> str:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    def __enter__(self) -> "BaseAgent":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.reset()