import ast
import json
from typing import Any, Dict

from minimal_agents.tools.base import Tool


class EmailResponseTool(Tool):
    """Create a professional email reply draft from an incoming email."""

    name: str = "Email Response Tool"
    description: str = (
        "Draft an appropriate email reply from the provided email content. "
        "Input supports dict-like payload with keys: email (required), intent (optional), tone (optional), "
        "sender_name (optional), recipient_name (optional), signature_name (optional). "
        "Also supports compact format: intent || email."
    )

    def run(self, input_text: str) -> str:
        try:
            payload = self._parse_input(input_text)
            email_body = str(payload.get("email", "")).strip()
            if not email_body:
                return "Email response error: 'email' content is required."

            intent = str(payload.get("intent", "reply to this email")).strip()
            tone = str(payload.get("tone", "professional")).strip()
            sender_name = str(payload.get("sender_name", "Sender")).strip()
            recipient_name = str(payload.get("recipient_name", "there")).strip()
            signature_name = str(payload.get("signature_name", "Your Name")).strip()

            summary = self._summarize_email(email_body)
            draft = self._compose_reply(
                intent=intent,
                tone=tone,
                sender_name=sender_name,
                recipient_name=recipient_name,
                signature_name=signature_name,
                summary=summary,
            )

            return (
                "Suggested email reply:\n"
                f"{draft}\n\n"
                "Note: Review names, dates, and commitments before sending."
            )
        except Exception as e:
            return f"Email response error: {str(e)}"

    def _parse_input(self, input_text: str) -> Dict[str, Any]:
        text = (input_text or "").strip()
        if not text:
            raise ValueError("input is empty")

        parsed = self._try_parse_dict(text)
        if isinstance(parsed, dict):
            return parsed

        if "||" in text:
            intent, email = text.split("||", 1)
            return {"intent": intent.strip(), "email": email.strip()}

        return {"email": text}

    def _try_parse_dict(self, text: str) -> Dict[str, Any] | None:
        try:
            value = ast.literal_eval(text)
            if isinstance(value, dict):
                return value
        except Exception:
            pass
        try:
            value = json.loads(text)
            if isinstance(value, dict):
                return value
        except Exception:
            pass
        return None

    def _summarize_email(self, email_body: str) -> str:
        # Lightweight heuristic summary to avoid external dependencies.
        lines = [line.strip() for line in email_body.splitlines() if line.strip()]
        if not lines:
            return "No clear details were provided in the email."

        if len(lines) == 1:
            return lines[0]

        first = lines[0]
        middle = lines[min(1, len(lines) - 1)]
        last = lines[-1]
        if first == last:
            return f"{first} {middle}".strip()
        return f"{first} {middle} {last}".strip()

    def _compose_reply(
        self,
        intent: str,
        tone: str,
        sender_name: str,
        recipient_name: str,
        signature_name: str,
        summary: str,
    ) -> str:
        greeting_name = sender_name if sender_name and sender_name != "Sender" else recipient_name
        greeting = f"Hi {greeting_name},"
        opening = (
            f"Thank you for your email. I understand that you are asking to {intent.lower()}."
        )
        context = f"From your message, the key details are: {summary}"

        if tone.lower() in {"friendly", "warm"}:
            action = "I appreciate the context and I am happy to help with this."
        elif tone.lower() in {"formal", "executive"}:
            action = "I acknowledge your request and will proceed accordingly."
        else:
            action = "I can help with this and will take the required next steps."

        close = (
            f"Please let me know if you would like me to adjust anything before we finalize.\n\n"
            f"Best regards,\n{signature_name}"
        )

        return (
            f"{greeting}\n\n"
            f"{opening}\n\n"
            f"{context}\n\n"
            f"{action}\n\n"
            f"{close}"
        )
