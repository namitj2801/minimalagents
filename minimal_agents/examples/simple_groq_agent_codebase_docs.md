# minimalagents - Automated Documentation

- Generated: 2026-05-07T22:16:40
- Total tracked files: 45
- Python files: 36
- Markdown files: 9

## Project Tree (Top-Level)

- `.env`
- `.gitignore`
- `INTERMEDIATE_RESULTS_AND_DISCUSSIONS.md`
- `MODULE_DESCRIPTION.md`
- `PUBLICATION_STATUS.md`
- `README.md`
- `WORK_COMPLETED.md`
- `file_structure.txt`
- `minimal_agents/`
- `minimal_agents.egg-info/`
- `setup.py`
- `test_gemini.py`
- `test_groq.py`

## Python Module Index

### `minimal_agents/__init__.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/agent.py`

- Purpose: Core agent implementation for MinimalAgents framework.
- Classes: MinimalAgent

### `minimal_agents/examples/custom_tools.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/examples/simple_agent.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/examples/simple_groq_agent.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/examples/tool_composition.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/llm/__init__.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/llm/base.py`

- Classes: OllamaProvider

### `minimal_agents/llm/gemini.py`

- Classes: GeminiProvider

### `minimal_agents/llm/groq.py`

- Classes: GroqProvider

### `minimal_agents/llm/ollama.py`

- Classes: OllamaProvider

### `minimal_agents/llm/openai.py`

- Purpose: OpenAI LLM provider implementation.
- Classes: OpenAIProvider

### `minimal_agents/tools/__init__.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/tools/base.py`

- Purpose: Base tool interface for all tools in the MinimalAgents framework.
- Classes: Tool

### `minimal_agents/tools/code/__init__.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/tools/code/python_repl.py`

- Purpose: Python REPL tool for executing Python code.
- Classes: PythonREPL

### `minimal_agents/tools/data/__init__.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/tools/data/file_reader.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/tools/data/pdf_extraction.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/tools/utilities/__init__.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/tools/utilities/calculator.py`

- Classes: CalculatorTool

### `minimal_agents/tools/utilities/github_documentation.py`

- Classes: GitHubDocumentationTool

### `minimal_agents/tools/utilities/image_gen.py`

- Classes: ImageGenerationTool

### `minimal_agents/tools/utilities/send_email.py`

- Classes: SendEmailTool

### `minimal_agents/tools/utilities/translation.py`

- Classes: TranslationTool

### `minimal_agents/tools/utilities/weather_tool.py`

- Classes: WeatherTool

### `minimal_agents/tools/utilities/wolfram.py`

- Classes: WolframTool

### `minimal_agents/tools/web/__init__.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/tools/web/scraper.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/tools/web/search.py`

- Purpose: Web search tool implementation.
- Classes: WebSearch

### `minimal_agents/utils/__init__.py`

- Purpose: (No module-level docstring found)

### `minimal_agents/utils/parsing.py`

- Purpose: Utility functions for parsing LLM responses.
- Functions: extract_tool_calls, extract_final_answer, extract_chat_response, extract_observations, extract_thoughts

### `minimal_agents/utils/prompts.py`

- Purpose: Default prompt templates for MinimalAgents framework.

### `setup.py`

- Purpose: Setup configuration for minimal_agents package.

### `test_gemini.py`

- Purpose: (No module-level docstring found)

### `test_groq.py`

- Purpose: (No module-level docstring found)

## Suggested Next Steps

- Keep this file updated via the GitHub Documentation Generator tool after major architecture or API changes.
- Add deeper docs for high-complexity modules and tool workflows.
