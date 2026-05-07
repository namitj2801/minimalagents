import ast
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple

from minimal_agents.tools.base import Tool


class GitHubDocumentationTool(Tool):
    """Generate markdown documentation for a local GitHub codebase."""

    name: str = "GitHub Documentation Generator"
    description: str = (
        "Automatically generate Markdown documentation for a codebase. "
        "Input can be a dict-like payload with keys: repo_path, output_file, repository_url, focus_paths, max_files. "
        "You can also pass a plain repo path string."
    )
    default_repo_path: str = "."
    default_output_file: str = "CODEBASE_DOCUMENTATION.md"

    def run(self, input_text: str) -> str:
        try:
            payload = self._parse_input(input_text)
            repo_path = os.path.abspath(payload.get("repo_path") or self.default_repo_path)
            output_file = payload.get("output_file") or self.default_output_file
            repository_url = str(payload.get("repository_url", "")).strip()
            focus_paths = payload.get("focus_paths") or []
            max_files = int(payload.get("max_files", 120))

            if not os.path.isdir(repo_path):
                return f"Documentation error: repo_path does not exist: {repo_path}"

            output_path = output_file
            if not os.path.isabs(output_path):
                output_path = os.path.join(repo_path, output_path)

            markdown = self._build_documentation(
                repo_path=repo_path,
                repository_url=repository_url,
                focus_paths=focus_paths,
                max_files=max_files,
            )

            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown)

            return f"Documentation generated successfully: {output_path}"
        except Exception as e:
            return f"Documentation error: {str(e)}"

    def _parse_input(self, input_text: str) -> Dict[str, Any]:
        text = (input_text or "").strip()
        if not text:
            return {}

        # Plain path input.
        if not text.startswith("{"):
            return {"repo_path": text}

        parsed = self._try_parse_dict(text)
        if isinstance(parsed, dict):
            return parsed

        raise ValueError(
            "Invalid input. Use a repo path string or dict-like input such as "
            "{'repo_path':'.','output_file':'docs/CODEBASE.md'}"
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

    def _build_documentation(
        self,
        repo_path: str,
        repository_url: str,
        focus_paths: List[str],
        max_files: int,
    ) -> str:
        all_files = self._collect_files(repo_path)
        python_files = [p for p in all_files if p.endswith(".py")]
        markdown_files = [p for p in all_files if p.endswith(".md")]

        lines: List[str] = []
        repo_name = os.path.basename(repo_path.rstrip("\\/")) or "repository"
        lines.append(f"# {repo_name} - Automated Documentation")
        lines.append("")
        lines.append(f"- Generated: {datetime.now().isoformat(timespec='seconds')}")
        if repository_url:
            lines.append(f"- Repository URL: {repository_url}")
        lines.append(f"- Total tracked files: {len(all_files)}")
        lines.append(f"- Python files: {len(python_files)}")
        lines.append(f"- Markdown files: {len(markdown_files)}")
        lines.append("")

        lines.append("## Project Tree (Top-Level)")
        lines.append("")
        lines.extend(self._top_level_tree(repo_path))
        lines.append("")

        lines.append("## Python Module Index")
        lines.append("")

        for rel_path in python_files[:max_files]:
            module_summary = self._summarize_python_file(os.path.join(repo_path, rel_path))
            lines.append(f"### `{rel_path}`")
            lines.append("")
            if module_summary["docstring"]:
                lines.append(f"- Purpose: {module_summary['docstring']}")
            if module_summary["classes"]:
                lines.append(f"- Classes: {', '.join(module_summary['classes'][:8])}")
            if module_summary["functions"]:
                lines.append(f"- Functions: {', '.join(module_summary['functions'][:10])}")
            if (
                not module_summary["docstring"]
                and not module_summary["classes"]
                and not module_summary["functions"]
            ):
                lines.append("- Purpose: (No module-level docstring found)")
            lines.append("")

        if len(python_files) > max_files:
            lines.append(
                f"_Truncated module index at {max_files} files. "
                "Increase `max_files` in tool input for more coverage._"
            )
            lines.append("")

        if focus_paths:
            lines.append("## Focus Files")
            lines.append("")
            for item in focus_paths:
                normalized = item.replace("\\", "/").strip("./")
                absolute_path = os.path.join(repo_path, normalized)
                if os.path.isfile(absolute_path):
                    lines.append(f"### `{normalized}`")
                    lines.append("")
                    lines.extend(self._focus_file_snapshot(absolute_path))
                    lines.append("")
                else:
                    lines.append(f"- `{normalized}` (not found)")
            lines.append("")

        lines.append("## Suggested Next Steps")
        lines.append("")
        lines.append(
            "- Keep this file updated via the GitHub Documentation Generator tool "
            "after major architecture or API changes."
        )
        lines.append("- Add deeper docs for high-complexity modules and tool workflows.")
        lines.append("")
        return "\n".join(lines)

    def _collect_files(self, repo_path: str) -> List[str]:
        excluded_dirs = {".git", "venv", ".venv", "__pycache__", ".mypy_cache", ".pytest_cache"}
        collected: List[str] = []
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file_name in files:
                if file_name.endswith((".py", ".md")):
                    full_path = os.path.join(root, file_name)
                    rel_path = os.path.relpath(full_path, repo_path).replace("\\", "/")
                    collected.append(rel_path)
        return sorted(collected)

    def _top_level_tree(self, repo_path: str) -> List[str]:
        entries = []
        for name in sorted(os.listdir(repo_path)):
            if name in {".git", "venv", ".venv", "__pycache__"}:
                continue
            full = os.path.join(repo_path, name)
            suffix = "/" if os.path.isdir(full) else ""
            entries.append(f"- `{name}{suffix}`")
        if not entries:
            entries.append("- _(empty)_")
        return entries

    def _summarize_python_file(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source)
            docstring = ast.get_docstring(tree) or ""
            classes, functions = self._extract_symbols(tree)
            return {"docstring": docstring, "classes": classes, "functions": functions}
        except Exception:
            return {"docstring": "", "classes": [], "functions": []}

    def _extract_symbols(self, tree: ast.AST) -> Tuple[List[str], List[str]]:
        classes: List[str] = []
        functions: List[str] = []
        for node in tree.body if isinstance(tree, ast.Module) else []:
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)
        return classes, functions

    def _focus_file_snapshot(self, file_path: str) -> List[str]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source)
            docstring = ast.get_docstring(tree) or "(No module-level docstring)"
            classes, functions = self._extract_symbols(tree)
            lines = [f"- Purpose: {docstring}"]
            if classes:
                lines.append(f"- Classes: {', '.join(classes[:10])}")
            if functions:
                lines.append(f"- Functions: {', '.join(functions[:12])}")
            return lines
        except Exception as e:
            return [f"- Could not parse file: {str(e)}"]
