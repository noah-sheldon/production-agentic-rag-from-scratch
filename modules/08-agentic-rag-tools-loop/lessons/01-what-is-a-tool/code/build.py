"""Build it: tool design + a plain-Python tool registry (stdlib only).

Run:  python3 build.py
Creates sample_notes/, registers list/search/read tools with schemas,
prints the schemas exactly as a model would see them, then calls each tool.
"""
import json
import re
from pathlib import Path

NOTES = Path("sample_notes")

SAMPLE_NOTES = {
    "agents.md": (
        "# Agents\n"
        "An agent is a loop plus tools. It decides what to do, calls a tool,"
        " checks the result, and repeats until it can answer."
    ),
    "evals.md": (
        "# Evals\n"
        "Measure answers before you ship them. Grade relevance: is the"
        " retrieved document actually about the question?"
    ),
    "rag.md": (
        "# RAG\n"
        "Retrieve relevant chunks, then ask the model with the chunks in the"
        " prompt. Retrieved docs must pass a relevance grade."
    ),
    "python.md": (
        "# Python\n"
        "Use the standard library first. A tool is a function with a good"
        " docstring — the docstring teaches the model how to call it."
    ),
}


def ensure_notes() -> None:
    NOTES.mkdir(exist_ok=True)
    for name, text in SAMPLE_NOTES.items():
        (NOTES / name).write_text(text)


# --------------------------------------------------------------------------
# The tools (each is a plain function — the schema is written by hand)
# --------------------------------------------------------------------------

def list_notes() -> list[str]:
    """List every note file in the notes folder."""
    return sorted(p.name for p in NOTES.glob("*.md"))


def search_notes(query: str, k: int = 3) -> list[dict]:
    """Find the k notes whose text best matches the query (word overlap)."""
    words = set(re.findall(r"[a-z]+", query.lower()))
    scored = []
    for path in NOTES.glob("*.md"):
        text_words = set(re.findall(r"[a-z]+", path.read_text().lower()))
        hits = len(words & text_words)
        scored.append({"file": path.name, "score": hits})
    scored.sort(key=lambda d: d["score"], reverse=True)
    return scored[:k]


def read_note(name: str) -> str:
    """Return the full text of one note file by name."""
    path = NOTES / name
    if not path.exists():
        raise FileNotFoundError(f"no note named {name!r}; try list_notes() first")
    return path.read_text()


# --------------------------------------------------------------------------
# The registry — one dict from tool name to {schema, callable}
# --------------------------------------------------------------------------

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, dict] = {}

    def register(self, name: str, description: str, parameters: dict, fn) -> None:
        self._tools[name] = {
            "schema": {
                "name": name,
                "description": description,
                "parameters": parameters,
            },
            "fn": fn,
        }

    def describe(self) -> str:
        """The schemas, serialized exactly as a model would receive them."""
        return json.dumps([t["schema"] for t in self._tools.values()], indent=2)

    def call(self, tool_name: str, **kwargs):
        if tool_name not in self._tools:
            raise KeyError(f"unknown tool {tool_name!r}; known: {sorted(self._tools)}")
        return self._tools[tool_name]["fn"](**kwargs)


def main() -> None:
    ensure_notes()
    registry = ToolRegistry()
    registry.register(
        "list_notes",
        "Use when you need to see every note file available.",
        {"type": "object", "properties": {}},
        list_notes,
    )
    registry.register(
        "search_notes",
        "Use to find notes that match a question. Returns files and scores.",
        {"type": "object", "properties": {
            "query": {"type": "string", "description": "words to match"},
            "k": {"type": "integer", "description": "how many results, default 3"},
        }, "required": ["query"]},
        search_notes,
    )
    registry.register(
        "read_note",
        "Use AFTER search_notes to read one full note by file name.",
        {"type": "object", "properties": {
            "name": {"type": "string", "description": "file name from list_notes"},
        }, "required": ["name"]},
        read_note,
    )

    print("== the schemas the model sees ==")
    print(registry.describe())

    print("\n== calling the tools ==")
    notes = registry.call("list_notes")
    print(f"list_notes -> {notes}  ({len(notes)} notes)")
    hits = registry.call("search_notes", query="agents")
    print(f"search_notes('agents') -> {hits}")
    top = hits[0]["file"]
    print(f"read_note({top!r}) -> {registry.call('read_note', name=top).splitlines()[0]}")

    print("\n== failure modes (designed to fail loudly) ==")
    for tool_name, kwargs in (("read_note", {}), ("no_such_tool", {})):
        try:
            registry.call(tool_name, **kwargs)
        except Exception as exc:
            print(f"{tool_name} {kwargs} -> {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
