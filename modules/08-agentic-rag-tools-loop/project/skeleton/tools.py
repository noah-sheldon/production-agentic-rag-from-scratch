"""Tools: the tool registry for the notes assistant (module 08 skeleton).

Plain Python, stdlib only. The registry holds every tool with its schema —
the schema is what a model sees, the fn is what runs.

Run from the skeleton dir; tools operate on the notes/ folder next to them.
"""
import json
import re
from pathlib import Path


class ToolRegistry:
    def __init__(self, notes_dir: Path) -> None:
        self.notes = Path(notes_dir)
        self._tools: dict[str, dict] = {}
        self._register_all()

    # -- registration -----------------------------------------------------

    def _register_all(self) -> None:
        self.register(
            "list_notes",
            "List every note file available.",
            {"type": "object", "properties": {}},
            self.list_notes,
        )
        self.register(
            "search_notes",
            "Find notes that match a question. Returns files and scores.",
            {"type": "object", "properties": {
                "query": {"type": "string"},
                "k": {"type": "integer", "description": "how many results, default 3"},
            }, "required": ["query"]},
            self.search_notes,
        )
        self.register(
            "read_note",
            "Read one full note by file name.",
            {"type": "object", "properties": {
                "name": {"type": "string"},
            }, "required": ["name"]},
            self.read_note,
        )

    def register(self, name: str, description: str, parameters: dict, fn) -> None:
        self._tools[name] = {
            "schema": {"type": "function", "function": {
                "name": name, "description": description, "parameters": parameters}},
            "fn": fn,
        }

    # -- registry interface ------------------------------------------------

    def schemas(self) -> list[dict]:
        """The schemas to send to a model — lesson 01's describe()."""
        return [t["schema"] for t in self._tools.values()]

    def names(self) -> list[str]:
        return sorted(self._tools)

    def call(self, tool_name: str, **kwargs):
        if tool_name not in self._tools:
            raise KeyError(f"unknown tool {tool_name!r}; known: {self.names()}")
        return self._tools[tool_name]["fn"](**kwargs)

    # -- the tools ---------------------------------------------------------

    def list_notes(self) -> list[str]:
        return sorted(p.name for p in self.notes.glob("*.md"))

    def search_notes(self, query: str, k: int = 3) -> list[dict]:
        """Word-overlap search (TODO 1, lesson 01: swap for Module 05's
        hybrid search so the agent searches like Module 05 does)."""
        words = set(re.findall(r"[a-z]+", query.lower()))
        scored = []
        for path in self.notes.glob("*.md"):
            haystack = f"{path.name} {path.read_text().lower()}"
            hits = len(words & set(re.findall(r"[a-z]+", haystack)))
            scored.append({"file": path.name, "score": hits})
        scored.sort(key=lambda d: d["score"], reverse=True)
        return scored[:k]

    def read_note(self, name: str) -> str:
        path = self.notes / name
        if not path.exists():
            raise FileNotFoundError(f"no note named {name!r}; try list_notes()")
        return path.read_text()


def build_registry(notes_dir: str) -> dict:
    """Exercise-1-compatible wrapper: {name: {"schema": ..., "fn": ...}}."""
    reg = ToolRegistry(Path(notes_dir))
    return {name: {"schema": reg._tools[name]["schema"]["function"],
                   "fn": reg._tools[name]["fn"]} for name in reg._tools}


if __name__ == "__main__":
    reg = ToolRegistry(Path(__file__).parent / "notes")
    print(json.dumps(reg.schemas(), indent=2))
    print(reg.list_notes())
