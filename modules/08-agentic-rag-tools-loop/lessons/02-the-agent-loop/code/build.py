"""Build it: the agent loop in plain Python — raw HTTP + FAKE mode (stdlib only).

Run:  python3 build.py                    # FAKE mode, runs keyless
      OPENAI_API_KEY=... python3 build.py # real OpenAI-compatible endpoint

The loop: decide -> call -> result -> repeat, until the model answers or the
max_turns budget is spent. Tool arguments arrive as JSON strings and are
parsed with json.loads.
"""
import json
import os
import re
import time
import urllib.request
from pathlib import Path

NOTES = Path("sample_notes")
MAX_TURNS = 6

SAMPLE_NOTES = {
    "agents.md": "# Agents\nAn agent is a loop plus tools. It decides, calls, checks, repeats.",
    "evals.md": "# Evals\nMeasure answers before you ship them. Grade every retrieved document.",
    "rag.md": "# RAG\nRetrieve relevant chunks, then ask the model with the chunks in the prompt.",
    "python.md": "# Python\nUse stdlib first. A tool is a function with a good docstring.",
}


def ensure_notes() -> None:
    NOTES.mkdir(exist_ok=True)
    for name, text in SAMPLE_NOTES.items():
        (NOTES / name).write_text(text)


# --------------------------------------------------------------------------
# Tools + registry (lesson 01's build, kept small)
# --------------------------------------------------------------------------

def list_notes() -> list[str]:
    return sorted(p.name for p in NOTES.glob("*.md"))


def search_notes(query: str, k: int = 3) -> list[dict]:
    words = set(re.findall(r"[a-z]+", query.lower()))
    scored = []
    for path in NOTES.glob("*.md"):
        hits = len(words & set(re.findall(r"[a-z]+", path.read_text().lower())))
        scored.append({"file": path.name, "score": hits})
    scored.sort(key=lambda d: d["score"], reverse=True)
    return scored[:k]


def read_note(name: str) -> str:
    path = NOTES / name
    if not path.exists():
        raise FileNotFoundError(f"no note named {name!r}")
    return path.read_text()


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, dict] = {}

    def register(self, name, description, parameters, fn) -> None:
        self._tools[name] = {"schema": {
            "type": "function",
            "function": {"name": name, "description": description, "parameters": parameters},
        }, "fn": fn}

    def schemas(self) -> list[dict]:
        return [t["schema"] for t in self._tools.values()]

    def call(self, tool_name: str, **kwargs):
        if tool_name not in self._tools:
            raise KeyError(f"unknown tool {tool_name!r}")
        return self._tools[tool_name]["fn"](**kwargs)


# --------------------------------------------------------------------------
# The model — real endpoint or FAKE mode
# --------------------------------------------------------------------------

def real_chat(messages: list[dict], tools: list[dict]) -> dict:
    """One raw HTTP call to an OpenAI-compatible /chat/completions endpoint."""
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    key = os.environ.get("OPENAI_API_KEY", "")
    body = json.dumps({"model": model, "messages": messages, "tools": tools}).encode()
    req = urllib.request.Request(
        f"{base}/chat/completions", data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def make_fake_chat(notes: Path):
    """A scripted model: search -> read the top hit -> answer. No network."""
    def fake_chat(messages: list[dict], tools: list[dict]) -> dict:
        tool_results = [m for m in messages if m["role"] == "tool"]
        if not tool_results:  # first decision: search
            return _reply(tool_calls=[_call("call_search", "search_notes", {"query": "agents"})])
        if len(tool_results) == 1:  # saw search results: read the top hit
            top = json.loads(tool_results[-1]["content"])[0]["file"]
            return _reply(tool_calls=[_call("call_read", "read_note", {"name": top})])
        return _reply(content="Agents are a loop plus tools: the model decides, calls a tool, checks the result, and repeats. Your agents.md note says exactly that.")
    return fake_chat


def make_runaway_chat():
    """A model that never answers — the max-turns budget must stop it."""
    def runaway(messages: list[dict], tools: list[dict]) -> dict:
        return _reply(tool_calls=[_call("call_loop", "search_notes", {"query": "loop"})])
    return runaway


def _call(call_id: str, name: str, arguments: dict) -> dict:
    return {"id": call_id, "type": "function",
            "function": {"name": name, "arguments": json.dumps(arguments)}}


def _reply(content: str | None = None, tool_calls: list | None = None) -> dict:
    return {"choices": [{"message": {"role": "assistant", "content": content,
                                     "tool_calls": tool_calls}}]}


# --------------------------------------------------------------------------
# The loop — decide -> call -> result -> repeat
# --------------------------------------------------------------------------

def run_agent(question: str, chat, registry: ToolRegistry,
              max_turns: int = MAX_TURNS) -> tuple[str, int]:
    messages = [{"role": "user", "content": question}]
    for turn in range(1, max_turns + 1):
        reply = chat(messages, registry.schemas())
        msg = reply["choices"][0]["message"]
        calls = msg.get("tool_calls") or []
        if not calls:
            return msg.get("content") or "", turn
        messages.append({"role": "assistant", "content": msg.get("content"),
                         "tool_calls": calls})
        for call in calls:
            fn = call["function"]
            try:
                args = json.loads(fn["arguments"] or "{}")
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"model returned bad JSON arguments: {exc}")
            print(f"  [turn {turn}] call {fn['name']}({args})")
            try:
                result = registry.call(fn["name"], **args)
            except Exception as exc:
                result = {"error": str(exc)}
            print(f"  [turn {turn}] {fn['name']} -> {str(result)[:70]}")
            messages.append({"role": "tool", "tool_call_id": call.get("id", f"call_{turn}"),
                             "content": json.dumps(result)})
    return "MAX_TURNS_REACHED — budget spent, stopped.", max_turns


def main() -> None:
    ensure_notes()
    registry = ToolRegistry()
    registry.register("list_notes", "List every note file available.",
                      {"type": "object", "properties": {}}, list_notes)
    registry.register("search_notes", "Find notes that match a question.",
                      {"type": "object", "properties": {
                          "query": {"type": "string"},
                          "k": {"type": "integer"}},
                       "required": ["query"]}, search_notes)
    registry.register("read_note", "Read one full note by file name.",
                      {"type": "object", "properties": {
                          "name": {"type": "string"}},
                       "required": ["name"]}, read_note)

    use_real = bool(os.environ.get("OPENAI_API_KEY"))
    chat = real_chat if use_real else make_fake_chat(NOTES)
    mode = "REAL (OpenAI-compatible)" if use_real else "FAKE (keyless)"

    print(f"== agent loop, {mode} mode, max_turns={MAX_TURNS} ==")
    question = "What did I write about agents?"
    started = time.perf_counter()
    answer, turns = run_agent(question, chat, registry)
    elapsed = time.perf_counter() - started
    print(f"\n== answer after {turns} turn(s) ({elapsed:.2f}s) ==")
    print(answer)

    print("\n== runaway model — the max-turns budget must stop it ==")
    answer, turns = run_agent("loop forever", make_runaway_chat(), registry)
    print(f"  turns used: {turns} (budget {MAX_TURNS}) — stopped, no infinite loop.")


if __name__ == "__main__":
    main()
