# MinimalAgents - Module Description

## Project Overview

**MinimalAgents** is a lightweight, extensible Python framework for building LLM-powered autonomous agents with tool integration capabilities. The framework provides a clean, minimal interface for creating AI agents that can reason, plan, and execute actions using various tools to solve complex problems.

---

## Core Architecture

The framework is organized into four main modules, each serving a distinct purpose in the agent ecosystem:

### 1. **Agent Module** (`agent.py`)
**Purpose**: Core orchestration engine that manages agent behavior and decision-making.

**Key Responsibilities**:
- Manages conversation flow and context tracking
- Coordinates interactions between LLM and tools
- Implements the ReAct (Reasoning + Acting) pattern
- Handles multi-step reasoning and iterative problem-solving
- Parses LLM responses to extract tool calls and final answers
- Manages iteration limits and error handling

**Key Features**:
- Configurable system prompts and templates
- Support for both tool-using and direct chat responses
- Verbose mode for debugging and transparency
- Dynamic tool management (add/remove tools at runtime)
- Context-aware prompt formatting with conversation history

---

### 2. **LLM Module** (`llm/`)
**Purpose**: Abstract interface and implementations for various Large Language Model providers.

**Structure**:
- **`base.py`**: Abstract base class defining the LLM provider interface
- **`openai.py`**: Integration with OpenAI's API (GPT-3.5, GPT-4, GPT-4o)
- **`gemini.py`**: Integration with Google's Gemini models
- **`ollama.py`**: Integration with local Ollama models

**Key Features**:
- Unified interface across different LLM providers
- Easy switching between providers without code changes
- Support for streaming and non-streaming responses
- Configurable model parameters (temperature, max tokens, etc.)
- Extensible architecture for adding new providers

**Design Pattern**: Strategy pattern - allows runtime selection of LLM providers

---

### 3. **Tools Module** (`tools/`)
**Purpose**: Extensible tool ecosystem providing capabilities for agents to interact with the world.

**Architecture**:
- **`base.py`**: Abstract base class defining the tool interface
  - All tools inherit from `Tool` class
  - Standardized `name`, `description`, and `run()` method

**Tool Categories**:

#### **Code Tools** (`tools/code/`)
- **`python_repl.py`**: Execute Python code dynamically
  - Enables agents to perform calculations, data processing, and algorithmic tasks
  - Sandboxed execution environment

#### **Data Tools** (`tools/data/`)
- **`file_reader.py`**: Read and process text files
- **`pdf_extraction.py`**: Extract text content from PDF documents
  - Enables document analysis and information extraction

#### **Web Tools** (`tools/web/`)
- **`search.py`**: Web search capabilities
  - Access to real-time information from the internet
- **`scraper.py`**: Web scraping functionality
  - Extract structured data from web pages

#### **Utility Tools** (`tools/utilities/`)
- **`calculator.py`**: Mathematical calculations
- **`translation.py`**: Language translation services
- **`wolfram.py`**: Integration with Wolfram Alpha for advanced computations
- **`email_tool.py`**: Email sending and management
- **`image_gen.py`**: Image generation capabilities
- **`weather_tool.py`**: Weather information retrieval

**Key Features**:
- Plugin-based architecture - easy to add custom tools
- Consistent interface across all tools
- Self-documenting (tools describe themselves to the LLM)
- Error handling and validation

---

### 4. **Utils Module** (`utils/`)
**Purpose**: Supporting utilities for agent operation and response processing.

**Components**:
- **`parsing.py`**: Response parsing utilities
  - Extracts tool calls from LLM responses
  - Identifies final answers vs. intermediate steps
  - Handles various response formats and edge cases

- **`prompts.py`**: Prompt template management
  - Default system prompts for agent behavior
  - Configurable prompt templates
  - Dynamic prompt formatting with context injection

**Key Features**:
- Robust parsing with fallback mechanisms
- Flexible prompt customization
- Context-aware prompt generation

---

## Module Interactions

```
┌─────────────┐
│   Agent     │  ← Orchestrates everything
│  (Core)     │
└──────┬──────┘
       │
       ├──────────────┬──────────────┐
       │              │              │
       ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│   LLM    │   │  Tools   │   │  Utils   │
│ Provider │   │          │   │          │
└──────────┘   └──────────┘   └──────────┘
```

**Workflow**:
1. Agent receives user query
2. Agent formats prompt using Utils (prompts.py)
3. Agent sends prompt to LLM Provider
4. LLM generates response
5. Agent parses response using Utils (parsing.py)
6. Agent executes appropriate Tool if needed
7. Agent incorporates tool results and iterates
8. Agent returns final answer to user

---

## Design Principles

1. **Minimalism**: Clean interfaces with minimal abstractions
2. **Flexibility**: Easy to extend with new LLMs and tools
3. **Pragmatism**: Built for practical, real-world use cases
4. **Separation of Concerns**: Each module has a single, well-defined responsibility
5. **Extensibility**: Plugin-based architecture allows easy customization

---

## Use Cases

- **Research Assistants**: Combine web search, PDF reading, and data analysis
- **Code Assistants**: Use Python REPL for dynamic code execution
- **Data Analysis**: Process files, perform calculations, and generate insights
- **Task Automation**: Chain multiple tools to complete complex workflows
- **Custom Applications**: Build domain-specific agents with specialized tools

---

## Technical Specifications

- **Language**: Python 3.9+
- **Dependencies**: 
  - Pydantic (data validation)
  - Requests (HTTP operations)
  - OpenAI SDK (for OpenAI provider)
  - Google Generative AI (for Gemini provider)
- **Architecture**: Modular, object-oriented design
- **Patterns**: Strategy pattern (LLM providers), Template method (tools), ReAct pattern (agent)

---

## Extension Points

Developers can extend the framework by:
1. **Adding New LLM Providers**: Implement the `LLMProvider` interface
2. **Creating Custom Tools**: Inherit from `Tool` base class
3. **Customizing Prompts**: Override default prompts in agent configuration
4. **Adding Utilities**: Extend parsing or prompt utilities as needed

---

## Summary

MinimalAgents provides a complete, production-ready framework for building intelligent agents. Its modular architecture ensures that each component can be developed, tested, and maintained independently while working seamlessly together to create powerful AI applications.
