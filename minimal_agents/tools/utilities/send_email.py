import ast
import os
import smtplib
import json
from email.message import EmailMessage
from typing import Any, Dict

from minimal_agents.tools.base import Tool


class SendEmailTool(Tool):
    """Tool that sends emails via SMTP."""

    name: str = "Send Email"
    description: str = (
        "Send an email using SMTP. Input must be a dict-like object with keys: "
        "to, subject, body. Optional keys: from_email, is_html (true/false). "
        "Example: {'from_email':'me@domain.com','to':'you@domain.com','subject':'Hi','body':'Hello'}"
    )

    def run(self, input_text: str) -> str:
        try:
            payload = self._parse_input(input_text)
            self._validate_payload(payload)
            self._send(payload)
            return f"Email sent successfully to {payload['to']}"
        except Exception as e:
            return f"Email send failed: {str(e)}"

    def _parse_input(self, input_text: str) -> Dict[str, Any]:
        text = input_text.strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.lower().startswith("json"):
                text = text[4:].strip()

        # Try direct Python dict parsing first.
        parsed = self._try_parse_dict(text)
        if isinstance(parsed, dict):
            return parsed

        # If the model added extra text, extract the first {...} block and parse it.
        dict_block = self._extract_first_braced_block(text)
        if dict_block:
            parsed = self._try_parse_dict(dict_block)
            if isinstance(parsed, dict):
                return parsed

        raise ValueError(
            "Input must contain a valid dictionary payload, e.g. "
            "{'to':'a@b.com','subject':'Hi','body':'Hello','from_email':'me@b.com'}"
        )

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

    def _extract_first_braced_block(self, text: str) -> str:
        start = text.find("{")
        if start == -1:
            return ""

        depth = 0
        for idx in range(start, len(text)):
            if text[idx] == "{":
                depth += 1
            elif text[idx] == "}":
                depth -= 1
                if depth == 0:
                    return text[start : idx + 1]
        return ""

    def _validate_payload(self, payload: Dict[str, Any]) -> None:
        required = ["to", "subject", "body"]
        missing = [k for k in required if not payload.get(k)]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        if "@" not in str(payload["to"]):
            raise ValueError("Recipient email appears invalid.")
        if payload.get("from_email") and "@" not in str(payload["from_email"]):
            raise ValueError("Sender email appears invalid.")

    def _send(self, payload: Dict[str, Any]) -> None:
        smtp_host = payload.get("SMTP_HOST") or os.environ.get("SMTP_HOST")
        smtp_port = int(payload.get("SMTP_PORT") or os.environ.get("SMTP_PORT", "587"))
        smtp_user = payload.get("SMTP_USER") or os.environ.get("SMTP_USER")
        smtp_password = payload.get("SMTP_PASSWORD") or os.environ.get("SMTP_PASSWORD")
        smtp_use_tls_raw = payload.get("SMTP_USE_TLS", os.environ.get("SMTP_USE_TLS", "true"))
        smtp_use_tls = str(smtp_use_tls_raw).lower() == "true"
        default_from = os.environ.get("SMTP_FROM_EMAIL") or smtp_user

        if not smtp_host or not smtp_user or not smtp_password:
            raise ValueError(
                "SMTP credentials missing. Set SMTP_HOST, SMTP_USER, SMTP_PASSWORD."
            )

        from_email = payload.get("from_email") or default_from
        if not from_email:
            raise ValueError("No sender email found. Set SMTP_FROM_EMAIL or provide from_email.")

        is_html = bool(payload.get("is_html", False))

        msg = EmailMessage()
        msg["Subject"] = str(payload["subject"])
        msg["From"] = str(from_email)
        msg["To"] = str(payload["to"])

        body = str(payload["body"])
        if is_html:
            msg.add_alternative(body, subtype="html")
        else:
            msg.set_content(body)

        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            if smtp_use_tls:
                server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
