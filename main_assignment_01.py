import os
import sys

from dotenv import load_dotenv

from agents.timed_agent import TimedAgent
from services.llm_client import LlmClient, LlmConfig

load_dotenv()

config = LlmConfig(
    api_key=os.getenv("GEMINI_API_KEY"),
    model_name=os.getenv("GEMINI_MODEL_NAME"),
    temperature=float(os.getenv("GEMINI_TEMPERATURE"))
)


with TimedAgent(LlmClient(config)) as agent:
    while True:
        try:
            user_input = input("You: ").strip()
        except(KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            sys.exit(0)

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("\nGoodbye!")
            sys.exit(0)
        if user_input.lower() == "reset":
            agent.reset()
            print("Session cleared.\n")
            continue
        if user_input.lower() == "history":
            print(agent.history_text() + "\n")
            continue
        if user_input.lower() == "stats":
            print(agent.stats())
            continue

        print(f"\nAgent: {agent.chat(user_input)}\n")