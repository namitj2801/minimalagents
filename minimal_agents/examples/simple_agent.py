import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from minimal_agents.agent import MinimalAgent
from minimal_agents.llm.ollama import OllamaProvider

llm = OllamaProvider(model="llama3")

agent = MinimalAgent(
    name="LocalOllamaAgent",
    instructions="You are a helpful AI agent running locally using Ollama.",
    llm=llm
)
print("Type 'exit' to quit.\n")

while True:
    query = input("You: ")
    if query.lower() in {"exit", "quit", "bye"}:
        break

    response = agent.run(query)
    print("\nAgent:", response, "\n")


