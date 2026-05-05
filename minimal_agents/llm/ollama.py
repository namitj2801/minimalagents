import requests
from typing import List, Optional


class OllamaProvider:
    def __init__(self, model="llama3", host="http://localhost:11434"):
        self.model = model
        self.host = host

    def generate(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Generate a response using local Ollama.

        Args:
            prompt: Full prompt text
            stop: Stop tokens (accepted for compatibility, ignored by Ollama)
        """
        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        text = response.json()["response"].strip()
        return f"Final Answer: {text}"


