import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from minimal_agents.agent import MinimalAgent
from minimal_agents.llm.groq import GroqProvider
from minimal_agents.tools.utilities.send_email import SendEmailTool
from minimal_agents.tools.utilities.weather_tool import WeatherTool
from minimal_agents.tools.utilities.translation import TranslationTool
from minimal_agents.tools.utilities.image_gen import ImageGenerationTool

load_dotenv()

llm = GroqProvider(model="llama-3.1-8b-instant")
send_email_tool = SendEmailTool()
weather_tool = WeatherTool()
translation_tool = TranslationTool()
image_tool = ImageGenerationTool()

agent = MinimalAgent(
    name="GroqAgent",
    instructions=(
        "You are a helpful AI agent powered by Groq. "
        "Only when explicitly asked to send an email, use the Send Email tool with a dict-like input "
        "containing to, subject, body, and optional from_email. "
        "If the user provides a sender email in their prompt, include it in from_email. "
        "When user asks for weather or current conditions for any place, use the Weather Tool. "
        "When user asks to translate text, use the Translation Tool. "
        "When user asks to generate or create an image, use the Image Generation Tool with the user's description."
    ),
    llm=llm,
    tools=[send_email_tool, weather_tool, translation_tool, image_tool],
    verbose=False,
    memory_file_path=os.path.join(os.path.dirname(__file__), "groq_agent_memory.jsonl"),
    memory_max_entries=20,
)
print("Type 'exit' to quit.\n")

while True:
    query = input("You: ")
    if query.lower() in {"exit", "quit", "bye"}:
        break

    response = agent.run(query)
    print("\nAgent:", response, "\n")

