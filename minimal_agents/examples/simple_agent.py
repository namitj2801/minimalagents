import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from minimal_agents.agent import MinimalAgent
from minimal_agents.llm.ollama import OllamaProvider
from minimal_agents.tools.utilities.send_email import SendEmailTool
from minimal_agents.tools.utilities.weather_tool import WeatherTool
from minimal_agents.tools.utilities.translation import TranslationTool
from minimal_agents.tools.utilities.image_gen import ImageGenerationTool
from minimal_agents.tools.utilities.github_documentation import GitHubDocumentationTool
from minimal_agents.tools.utilities.database_query_translator import DatabaseQueryTranslatorTool
from minimal_agents.tools.utilities.email_response_tool import EmailResponseTool

llm = OllamaProvider(model="llama3")
send_email_tool = SendEmailTool()
weather_tool = WeatherTool()
translation_tool = TranslationTool()
image_tool = ImageGenerationTool()
database_query_tool = DatabaseQueryTranslatorTool()
email_response_tool = EmailResponseTool()
github_docs_tool = GitHubDocumentationTool(
    default_repo_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
    default_output_file="minimal_agents/examples/simple_agent_codebase_docs.md",
)

agent = MinimalAgent(
    name="LocalOllamaAgent",
    instructions=(
        "You are a helpful AI agent running locally using Ollama. "
        "Only when explicitly asked to send an email, use the Send Email tool with a dict-like input "
        "containing to, subject, body, and optional from_email. "
        "If the user provides a sender email in their prompt, include it in from_email. "
        "When user asks for weather or current conditions for any place, use the Weather Tool. "
        "When user asks to translate text, use the Translation Tool. "
        "When user asks to generate or create an image, use the Image Generation Tool with the user's description. "
        "When user asks to generate repository or GitHub documentation, use the GitHub Documentation Generator. "
        "When user asks to translate natural language into SQL or MongoDB, use the Database Query Translator tool. "
        "When user asks to draft or curate a reply for an email, use the Email Response Tool."
    ),
    llm=llm,
    tools=[
        send_email_tool,
        weather_tool,
        translation_tool,
        image_tool,
        github_docs_tool,
        database_query_tool,
        email_response_tool,
    ],
)
print("Type 'exit' to quit.\n")

while True:
    query = input("You: ")
    if query.lower() in {"exit", "quit", "bye"}:
        break

    response = agent.run(query)
    print("\nAgent:", response, "\n")


