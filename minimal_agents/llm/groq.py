import os
import time
from typing import List, Optional


class GroqProvider:
    def __init__(
        self,
        model: str = "llama-3.1-8b-instant",
        temperature: float = 0.4,
        max_tokens: Optional[int] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Groq API key is required. Set GROQ_API_KEY environment variable or pass api_key."
            )

        try:
            from groq import Groq
        except Exception as e:
            raise ImportError(
                "Groq provider requires the `groq` package. Install it with `pip install groq`."
            ) from e

        client_kwargs = {"api_key": self.api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        self._client = Groq(**client_kwargs)

    def generate(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Generate a response using Groq.

        Args:
            prompt: Full prompt text
            stop: Stop sequences (for ReAct-style parsing compatibility)
        """
        last_error = None
        for _ in range(3):
            try:
                response = self._client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    stop=stop,
                )
                content = (response.choices[0].message.content or "").strip()
                return content
            except Exception as e:
                last_error = e
                error_text = str(e).lower()
                if "rate limit" in error_text or "429" in error_text:
                    time.sleep(3)
                    continue
                return (
                    "Chat Response: I ran into an API issue while generating a response. "
                    f"Details: {str(e)}"
                )

        return (
            "Chat Response: The model is currently rate-limited. "
            "Please wait a few seconds and try again."
        )

