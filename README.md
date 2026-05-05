# MinimalAgents

A lightweight Python framework for building tool-enabled LLM agents.

## Overview

MinimalAgents provides a small, extensible agent layer that coordinates:

- LLM providers for model calls
- tool execution for structured actions
- prompt formatting and response parsing
- basic memory and iteration control

The library is designed to keep abstractions minimal while making it easy to add new tools and new model providers.

## What is included

- `minimal_agents.agent.MinimalAgent` — core orchestration for model + tools
- `minimal_agents.llm` providers for OpenAI, Gemini, Groq, and Ollama
- `minimal_agents.tools` built-in tool implementations
- `minimal_agents.utils` helpers for prompts and response parsing
- `minimal_agents/examples` sample scripts for starting agents quickly

## Installation

Install from the repository root:

```bash
python -m pip install .
```

For development dependencies:

```bash
python -m pip install .[development]
```

Optional provider extras:

```bash
python -m pip install .[google]
```

## Quick Start

```python
from minimal_agents.agent import MinimalAgent
from minimal_agents.llm.openai import OpenAIProvider
from minimal_agents.tools.code.python_repl import PythonREPL

llm = OpenAIProvider(model="gpt-4o", temperature=0.4)
tools = [PythonREPL()]

agent = MinimalAgent(llm=llm, tools=tools, verbose=True)
response = agent.run("Calculate the factorial of 5 using Python")
print(response)
```

## Available LLM providers

- `minimal_agents.llm.openai.OpenAIProvider`
- `minimal_agents.llm.gemini.GeminiProvider`
- `minimal_agents.llm.groq.GroqProvider`
- `minimal_agents.llm.ollama.OllamaProvider`

### Notes

- `OpenAIProvider` uses `OPENAI_API_KEY` if `api_key` is not passed.
- `GeminiProvider` uses `GEMINI_API_KEY` or `GOOGLE_API_KEY`.
- `GroqProvider` requires the `groq` package.
- `OllamaProvider` can target a local Ollama server.

## Built-in tools

Some of the provided tools include:

- `PythonREPL` for executing Python code
- calculator and translation utilities
- email sending, web search, and image generation helpers
- file readers and PDF extraction tools

You can also implement your own tool by subclassing `minimal_agents.tools.base.Tool`.

## Creating a custom tool

```python
from minimal_agents.tools.base import Tool

class WeatherTool(Tool):
    name = "Weather Tool"
    description = "Get current weather for a location. Input should be a city name."

    def run(self, input_text: str) -> str:
        location = input_text.strip()
        return f"Weather for {location}: 72°F, Partly Cloudy"
```

## Examples

See `minimal_agents/examples/simple_agent.py` and `minimal_agents/examples/simple_groq_agent.py` for runnable agent examples.

## Project structure

- `minimal_agents/agent.py` — agent orchestration and tool loop
- `minimal_agents/llm/` — LLM provider adapters
- `minimal_agents/tools/` — tool interface and utility tools
- `minimal_agents/utils/` — prompt templates and parsing logic

## License

This project is licensed under the MIT License.
