from minimal_agents.tools.base import Tool
import ast
import operator

class CalculatorTool(Tool):
    """Tool for performing basic arithmetic calculations."""

    name: str = "Calculator Tool"
    description: str = (
        "Evaluate a mathematical expression. "
        "Supports +, -, *, /, **, and parentheses."
    )

    def run(self, input_text: str) -> str:
        """Evaluate the given mathematical expression safely."""
        expression = input_text.strip()

        try:
            result = self._safe_eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"

    # ---- Internal Safe Evaluator ---- #

    def _safe_eval(self, expr: str):
        """Safely evaluate arithmetic expressions using AST."""

        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.Mod: operator.mod,
        }

        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)

            elif isinstance(node, ast.Constant):  # Python 3.8+
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Only numbers are allowed.")

            elif isinstance(node, ast.BinOp):
                op_type = type(node.op)
                if op_type in allowed_operators:
                    return allowed_operators[op_type](
                        _eval(node.left), _eval(node.right)
                    )
                raise ValueError("Operator not allowed.")

            elif isinstance(node, ast.UnaryOp):
                op_type = type(node.op)
                if op_type in allowed_operators:
                    return allowed_operators[op_type](_eval(node.operand))
                raise ValueError("Unary operator not allowed.")

            else:
                raise ValueError("Invalid expression.")

        parsed = ast.parse(expr, mode="eval")
        return _eval(parsed)
