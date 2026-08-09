#!/usr/bin/env python3
"""Module 08 — solutions to the three exercises.

Run:  python3 02_solutions.py
Same checks as 01_exercises.py, with the learner solutions implemented here.
"""

from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

# --------------------------------------------------------------------------
# EXERCISE 1 — the tool registry (solution)
# --------------------------------------------------------------------------

def build_registry(notes_dir: str) -> dict:
    notes = Path(notes_dir)

    def list_notes() -> list[str]:
        return sorted(p.name for p in notes.glob("*.md"))

    def search_notes(query: str, k: int = 3) -> list[dict]:
        words = set(re.findall(r"[a-z]+", query.lower()))
        scored = []
        for path in notes.glob("*.md"):
            hits = len(words & set(re.findall(r"[a-z]+", path.read_text().lower())))
            scored.append({"file": path.name, "score": hits})
        scored.sort(key=lambda d: d["score"], reverse=True)
        return scored[:k]

    def read_note(name: str) -> str:
        path = notes / name
        if not path.exists():
            raise FileNotFoundError(f"no note named {name!r}")
        return path.read_text()

    return {
        "list_notes": {
            "schema": {"name": "list_notes",
                       "description": "List every note file available.",
                       "parameters": {"type": "object", "properties": {}}},
            "fn": list_notes,
        },
        "search_notes": {
            "schema": {"name": "search_notes",
                       "description": "Find notes that match a question.",
                       "parameters": {"type": "object", "properties": {
                           "query": {"type": "string"},
                           "k": {"type": "integer"}},
                        "required": ["query"]}},
            "fn": search_notes,
        },
        "read_note": {
            "schema": {"name": "read_note",
                       "description": "Read one full note by file name.",
                       "parameters": {"type": "object", "properties": {
                           "name": {"type": "string"}},
                        "required": ["name"]}},
            "fn": read_note,
        },
    }


# --------------------------------------------------------------------------
# EXERCISE 2 — the agent loop (solution)
# --------------------------------------------------------------------------

def run_agent(question: str, chat, registry: dict, max_turns: int = 4):
    messages = [{"role": "user", "content": question}]
    for turn in range(1, max_turns + 1):
        reply = chat(messages, [])
        msg = reply["choices"][0]["message"]
        calls = msg.get("tool_calls") or []
        if not calls:
            return msg.get("content") or "", turn
        messages.append({"role": "assistant", "content": msg.get("content"),
                         "tool_calls": calls})
        for call in calls:
            fn = call["function"]
            args = json.loads(fn["arguments"] or "{}")
            result = registry[fn["name"]]["fn"](**args)
            messages.append({"role": "tool", "tool_call_id": call.get("id", "call"),
                             "content": json.dumps(result)})
    return "MAX_TURNS_REACHED", max_turns


# --------------------------------------------------------------------------
# EXERCISE 3 — guardrail + rewrite (solution)
# --------------------------------------------------------------------------

DOMAIN = ["agents", "rag", "evals", "python", "data"]

STOPWORDS = {
    "a", "an", "the", "about", "stuff", "things", "thing", "some", "any",
    "what", "is", "are", "was", "my", "me", "i", "it", "this", "that",
    "there", "of", "for", "on", "in", "to", "with", "and", "or", "please",
    "can", "you", "do", "does", "did", "have", "has", "one", "get",
    "how", "use", "using", "used", "write", "wrote", "say", "says",
    "mention", "mentions", "talk", "talks",
}


def guard(question: str) -> dict:
    hits = [t for t in DOMAIN if t in question.lower()]
    if not hits:
        return {"accepted": False,
                "reason": f"out of domain — question names none of {DOMAIN}"}
    return {"accepted": True, "reason": "in domain"}


def rewrite(query: str, last_topic: str = "") -> str:
    q = re.sub(r"[^a-z0-9 ]+", " ", query.lower()).strip()
    m = re.search(r"\b(?:one|thing|note|post)\s+about\s+([a-z0-9 ]+)", q)
    if m:
        return m.group(1).strip()
    if q in {"it", "this", "that", "these", "those"} and last_topic:
        return last_topic
    words = [w for w in q.split() if w not in STOPWORDS]
    return " ".join(words) if words else q


# --------------------------------------------------------------------------
# The checks (identical to 01_exercises.py)
# --------------------------------------------------------------------------

def _tool_call(call_id: str, name: str, arguments: dict) -> dict:
    return {"id": call_id, "type": "function",
            "function": {"name": name, "arguments": json.dumps(arguments)}}


def _reply(content=None, tool_calls=None) -> dict:
    return {"choices": [{"message": {"role": "assistant", "content": content,
                                     "tool_calls": tool_calls}}]}


def check_ex1() -> bool:
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        notes = Path(tmp)
        (notes / "agents.md").write_text("Agents are a loop plus tools. The agent decides, calls, checks, repeats.")
        (notes / "evals.md").write_text("Measure answers before you ship them. Grade every retrieved document.")
        registry = build_registry(str(notes))
        for name in ("list_notes", "search_notes", "read_note"):
            schema = registry[name]["schema"]
            good = all(k in schema for k in ("name", "description", "parameters"))
            print(f"  tool {name!r} registered with full schema: {'PASS' if good else 'FAIL'}")
            ok = ok and good
        listed = registry["list_notes"]["fn"]()
        good = listed == ["agents.md", "evals.md"]
        print(f"  list_notes -> {listed}  {'PASS' if good else 'FAIL'}")
        ok = ok and good
        hits = registry["search_notes"]["fn"]("agents")
        good = hits and hits[0]["file"] == "agents.md" and hits[0]["score"] > 0
        print(f"  search_notes('agents') top hit -> {hits[0] if hits else None}  {'PASS' if good else 'FAIL'}")
        ok = ok and good
        text = registry["read_note"]["fn"]("agents.md")
        good = "loop" in text
        print(f"  read_note('agents.md') mentions the loop: {'PASS' if good else 'FAIL'}")
        ok = ok and good
        try:
            registry["read_note"]["fn"]("missing.md")
            print("  read_note('missing.md') raised nothing: FAIL")
            ok = False
        except FileNotFoundError:
            print("  read_note('missing.md') raises FileNotFoundError: PASS")
    return ok


def check_ex2() -> bool:
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        notes = Path(tmp)
        (notes / "agents.md").write_text("Agents are a loop plus tools. The agent decides, calls, checks, repeats.")
        registry = {"read_note": {"fn": lambda name: (notes / name).read_text()}}
        seen = []

        def scripted(messages, tools):
            seen.append(messages)
            if any(m["role"] == "tool" for m in messages):
                return _reply(content="agents are a loop")
            return _reply(tool_calls=[_tool_call("c1", "read_note", {"name": "agents.md"})])

        final, turns = run_agent("what is an agent", scripted, registry, max_turns=4)
        good = final == "agents are a loop"
        print(f"  final answer: {final!r}  {'PASS' if good else 'FAIL'}")
        ok = ok and good
        good = turns == 2
        print(f"  turns used: {turns} (expected 2)  {'PASS' if good else 'FAIL'}")
        ok = ok and good
        saw_tool_msg = any(
            m["role"] == "tool" and "loop" in m["content"] for messages in seen for m in messages
        )
        print(f"  model saw the tool result:  {'PASS' if saw_tool_msg else 'FAIL'}")
        ok = ok and saw_tool_msg

        def runaway(messages, tools):
            return _reply(tool_calls=[_tool_call("c1", "read_note", {"name": "agents.md"})])

        final, turns = run_agent("loop forever", runaway, registry, max_turns=4)
        good = turns == 4
        print(f"  runaway model stopped at max_turns: {turns} (expected 4)  {'PASS' if good else 'FAIL'}")
        ok = ok and good
    return ok


def check_ex3() -> bool:
    ok = True
    out = guard("what is the best pizza in London?")
    good = out.get("accepted") is False and len(out.get("reason", "")) > 0
    print(f"  guard('best pizza in London') rejected with reason:  {'PASS' if good else 'FAIL'}")
    ok = ok and good
    out = guard("what did I write about agents?")
    good = out.get("accepted") is True
    print(f"  guard('...about agents') accepted:                    {'PASS' if good else 'FAIL'}")
    ok = ok and good
    q = rewrite("the one about evals")
    good = "evals" in q
    print(f"  rewrite('the one about evals') -> {q!r}:               {'PASS' if good else 'FAIL'}")
    ok = ok and good
    q = rewrite("it", "rag")
    good = "rag" in q
    print(f"  rewrite('it', 'rag') -> {q!r}:                        {'PASS' if good else 'FAIL'}")
    ok = ok and good
    return ok


def main() -> None:
    results = {
        "exercise 1 (tool registry)": check_ex1(),
        "exercise 2 (agent loop)": check_ex2(),
        "exercise 3 (guardrail + rewrite)": check_ex3(),
    }
    print()
    for name, ok in results.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    all_ok = all(results.values())
    print("  All three pass — module 08 exercises complete."
          if all_ok else "  Fix the failing checks, then re-run.")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
