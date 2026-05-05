import os
import requests
from typing import Optional

from minimal_agents.tools.base import Tool


class WolframTool(Tool):
    """Universal utility tool powered by Wolfram|Alpha."""

    name: str = "Wolfram Tool"
    description: str = (
        "Answer factual, mathematical, scientific, unit conversion, and "
        "data-driven questions using Wolfram|Alpha. Input should be a clear "
        "natural-language query."
    )
    app_id: Optional[str] = None
    timeout_seconds: int = 20

    def __init__(self, app_id: Optional[str] = None, timeout_seconds: int = 20, **data):
        super().__init__(**data)
        self.app_id = app_id or os.environ.get("WOLFRAM_APP_ID")
        self.timeout_seconds = timeout_seconds

    def run(self, input_text: str) -> str:
        query = input_text.strip()
        if not query:
            return "Error: Please provide a query."

        if not self.app_id:
            return "Error: Missing WOLFRAM_APP_ID. Add it to your environment or pass app_id."

        try:
            result = self._query_short_answer_api(query)
            if result:
                return f"Wolfram result: {result}"

            # Fallback to full results API for more detail if short answer is empty.
            detailed = self._query_full_results_api(query)
            if detailed:
                return f"Wolfram result: {detailed}"

            return "No Wolfram result found for that query."
        except requests.RequestException as e:
            return f"Wolfram request failed: {str(e)}"
        except Exception as e:
            return f"Wolfram tool error: {str(e)}"

    def _query_short_answer_api(self, query: str) -> str:
        url = "https://api.wolframalpha.com/v1/result"
        response = requests.get(
            url,
            params={"appid": self.app_id, "i": query},
            timeout=self.timeout_seconds,
        )

        if response.status_code == 501:
            # Wolfram may return 501 for no short answer; not fatal.
            return ""

        response.raise_for_status()
        return response.text.strip()

    def _query_full_results_api(self, query: str) -> str:
        url = "https://api.wolframalpha.com/v2/query"
        response = requests.get(
            url,
            params={
                "appid": self.app_id,
                "input": query,
                "output": "json",
                "format": "plaintext",
            },
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()

        pods = (
            data.get("queryresult", {})
            .get("pods", [])
        )
        lines = []
        for pod in pods[:4]:
            title = pod.get("title", "").strip()
            subpods = pod.get("subpods", [])
            for subpod in subpods[:2]:
                text = (subpod.get("plaintext") or "").strip()
                if text:
                    lines.append(f"{title}: {text}" if title else text)

        return "\n".join(lines).strip()
 