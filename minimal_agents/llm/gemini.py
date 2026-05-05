import os
from typing import List, Optional

from google import genai
from google.genai import types


class GeminiProvider:
    def __init__(self, model: str = "gemini-2.0-flash", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "AIzaSyCEawJqfXfQM3KDe19G2Ttu5UPgOtrm57M"
        if not self.api_key:
            raise ValueError(
                "Gemini API key is required. Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable or pass api_key."
            )
        self._client = genai.Client(api_key=self.api_key)

    def generate(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Generate a response using Google Gemini.

        Args:
            prompt: Full prompt text
            stop: Stop sequences (e.g. for ReAct-style parsing)
        """
        config = None
        if stop:
            config = types.GenerateContentConfig(stop_sequences=stop)

        response = self._client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config,
        )
        text = (response.text or "").strip()
        return text
