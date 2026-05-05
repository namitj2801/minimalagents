import requests
from minimal_agents.llm.base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(self, model="llama3", host="http://localhost:11434"):
        self._model = model
        self.host = host

    @property
    def provider_name(self) -> str:
        return "ollama"

    @property
    def model_name(self) -> str:
        return self._model

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self._model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()["response"]
