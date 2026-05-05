import ast
from typing import Any, Dict

import requests

from minimal_agents.tools.base import Tool


class TranslationTool(Tool):
    """Translate user text between languages."""

    name: str = "Translation Tool"
    description: str = (
        "Translate text into a target language. "
        "Input can be a dict-like object: {'text':'Hello','target_lang':'hi','source_lang':'auto'} "
        "or simple format: text || target_lang."
    )

    def run(self, input_text: str) -> str:
        try:
            payload = self._parse_input(input_text)
            text = payload["text"].strip()
            target_lang = payload["target_lang"].strip().lower()
            source_lang = payload.get("source_lang", "auto").strip().lower()

            if not text:
                return "Translation error: text is required."
            if not target_lang:
                return "Translation error: target_lang is required."

            translated = self._translate(text, target_lang, source_lang)
            return (
                f"Translated ({source_lang} -> {target_lang}): {translated}"
            )
        except requests.RequestException as e:
            return f"Translation error: request failed: {str(e)}"
        except Exception as e:
            return f"Translation error: {str(e)}"

    def _parse_input(self, input_text: str) -> Dict[str, str]:
        text = input_text.strip()
        if not text:
            raise ValueError("input is empty")

        # Dict-like form
        if text.startswith("{") and text.endswith("}"):
            parsed: Dict[str, Any] = ast.literal_eval(text)
            if not isinstance(parsed, dict):
                raise ValueError("dictionary input expected")
            return {
                "text": str(parsed.get("text", "")),
                "target_lang": str(parsed.get("target_lang", "")),
                "source_lang": str(parsed.get("source_lang", "auto")),
            }

        # Compact form: "text || target_lang"
        if "||" in text:
            parts = text.split("||", 1)
            return {
                "text": parts[0].strip(),
                "target_lang": parts[1].strip(),
                "source_lang": "auto",
            }

        raise ValueError("Use {'text':'...','target_lang':'..'} or 'text || target_lang'")

    def _translate(self, text: str, target_lang: str, source_lang: str) -> str:
        response = requests.get(
            "https://translate.googleapis.com/translate_a/single",
            params={
                "client": "gtx",
                "sl": source_lang or "auto",
                "tl": target_lang,
                "dt": "t",
                "q": text,
            },
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()

        # First element is sentence chunks. Each chunk[0] contains translated text.
        chunks = data[0] if data and isinstance(data, list) else []
        translated = "".join(chunk[0] for chunk in chunks if chunk and chunk[0])
        if not translated:
            raise ValueError("could not parse translation response")
        return translated
 