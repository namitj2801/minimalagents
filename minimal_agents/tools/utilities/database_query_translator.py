import ast
import json
from typing import Any, Dict

from minimal_agents.tools.base import Tool


class DatabaseQueryTranslatorTool(Tool):
    """Translate natural language actions into SQL or MongoDB queries."""

    name: str = "Database Query Translator"
    description: str = (
        "Convert natural language actions to SQL or MongoDB queries. "
        "Input must be dict-like with keys: database ('sql' or 'mongodb') and action. "
        "Optional keys: table, collection, columns, condition, limit, values."
    )

    def run(self, input_text: str) -> str:
        try:
            payload = self._parse_input(input_text)
            database = str(payload.get("database", "")).strip().lower()
            action = str(payload.get("action", "")).strip()

            if not database:
                return "Database query error: 'database' is required ('sql' or 'mongodb')."
            if not action:
                return "Database query error: 'action' is required."

            if database == "sql":
                return self._translate_sql(payload, action)
            if database in {"mongodb", "mongo"}:
                return self._translate_mongodb(payload, action)

            return "Database query error: database must be 'sql' or 'mongodb'."
        except Exception as e:
            return f"Database query error: {str(e)}"

    def _parse_input(self, input_text: str) -> Dict[str, Any]:
        text = (input_text or "").strip()
        if not text:
            raise ValueError("input is empty")

        parsed = self._try_parse_dict(text)
        if isinstance(parsed, dict):
            return parsed

        # Fallback compact format: "database || action"
        if "||" in text:
            db, action = text.split("||", 1)
            return {"database": db.strip(), "action": action.strip()}

        raise ValueError(
            "Use {'database':'sql|mongodb','action':'...'} or 'database || action'"
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

    def _translate_sql(self, payload: Dict[str, Any], action: str) -> str:
        action_l = action.lower()
        table = str(payload.get("table", "your_table")).strip()
        columns = str(payload.get("columns", "*")).strip() or "*"
        condition = str(payload.get("condition", "1=1")).strip() or "1=1"
        limit = payload.get("limit", 10)
        values = payload.get("values", {"column": "value"})

        if "insert" in action_l or "add" in action_l or "create record" in action_l:
            if not isinstance(values, dict) or not values:
                values = {"column": "value"}
            cols = ", ".join(values.keys())
            vals = ", ".join([self._sql_literal(v) for v in values.values()])
            query = f"INSERT INTO {table} ({cols}) VALUES ({vals});"
        elif "update" in action_l or "modify" in action_l:
            if not isinstance(values, dict) or not values:
                values = {"column": "new_value"}
            set_clause = ", ".join([f"{k} = {self._sql_literal(v)}" for k, v in values.items()])
            query = f"UPDATE {table} SET {set_clause} WHERE {condition};"
        elif "delete" in action_l or "remove" in action_l:
            query = f"DELETE FROM {table} WHERE {condition};"
        else:
            query = f"SELECT {columns} FROM {table} WHERE {condition} LIMIT {int(limit)};"

        return (
            "Generated SQL query:\n"
            f"{query}\n\n"
            "Note: Review table/column names and conditions before executing."
        )

    def _translate_mongodb(self, payload: Dict[str, Any], action: str) -> str:
        action_l = action.lower()
        collection = str(payload.get("collection", "your_collection")).strip()
        condition = payload.get("condition", {})
        values = payload.get("values", {"field": "value"})
        limit = int(payload.get("limit", 10))

        if not isinstance(condition, dict):
            condition = {}
        if not isinstance(values, dict):
            values = {"field": "value"}

        if "insert" in action_l or "add" in action_l or "create record" in action_l:
            query = f"db.{collection}.insertOne({json.dumps(values, ensure_ascii=True)});"
        elif "update" in action_l or "modify" in action_l:
            query = (
                f"db.{collection}.updateMany("
                f"{json.dumps(condition, ensure_ascii=True)}, "
                f"{{\"$set\": {json.dumps(values, ensure_ascii=True)}}}"
                ");"
            )
        elif "delete" in action_l or "remove" in action_l:
            query = f"db.{collection}.deleteMany({json.dumps(condition, ensure_ascii=True)});"
        else:
            query = f"db.{collection}.find({json.dumps(condition, ensure_ascii=True)}).limit({limit});"

        return (
            "Generated MongoDB query:\n"
            f"{query}\n\n"
            "Note: Review collection names and filters before executing."
        )

    def _sql_literal(self, value: Any) -> str:
        if value is None:
            return "NULL"
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        if isinstance(value, (int, float)):
            return str(value)
        escaped = str(value).replace("'", "''")
        return f"'{escaped}'"
