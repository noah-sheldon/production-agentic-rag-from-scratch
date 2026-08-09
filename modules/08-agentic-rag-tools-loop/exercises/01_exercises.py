#!/usr/bin/env python3
"""Module 08 exercises — gate the four lessons (three exercises).

Run:  python3 01_exercises.py

The three exercises:
  1. Tool registry — write tools.py: build_registry(notes_dir) with
     list_notes / search_notes / read_note, each with a schema.
  2. Agent loop — write loop.py: run_agent(question, chat, registry,
     max_turns) = decide -> call -> result -> repeat (lesson 02).
  3. Guardrail + rewrite — write guardrails.py: guard(question) rejects
     out-of-domain questions, rewrite(query, last_topic) fixes bad queries.
"""

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
from pathlib import Path

# --------------------------------------------------------------------------
# EXERCISE 1 — the tool registry
# --------------------------------------------------------------------------

EX1_SPEC = """\
Write `tools.py` next to this file with:

    build_registry(notes_dir) -> dict

Returning a dict {tool_name: {"schema": {...}, "fn": callable}} with three
tools over the notes_dir folder:

  - list_notes()          -> sorted list of *.md file names
  - search_notes(query, k=3) -> list of {"file": name, "score": n} sorted
                                by score descending (word overlap is fine)
  - read_note(name)       -> full text of the file, raising FileNotFoundError
                             if the file is missing

Every schema must have name, description, and parameters keys. The check
creates a temp notes folder and calls all three tools.
"""


def check_ex1() -> bool:
    if not os.path.exists("tools.py"):
        print("  missing tools.py — create it (spec below).")
        print(EX1_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("tools", "tools.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    build = getattr(module, "build_registry", None)
    if build is None:
        print("  tools.py must define build_registry().")
        return False

    with tempfile.TemporaryDirectory() as tmp:
        notes = Path(tmp)
        (notes / "agents.md").write_text("Agents are a loop plus tools. The agent decides, calls, checks, repeats.")
        (notes / "evals.md").write_text("Measure answers before you ship them. Grade every retrieved document.")
        registry = build(str(notes))

        ok = True
        for name in ("list_notes", "search_notes", "read_note"):
            good = name in registry and "schema" in registry[name] and "fn" in registry[name]
            schema = registry[name]["schema"]
            good = good and all(k in schema for k in ("name", "description", "parameters"))
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


# --------------------------------------------------------------------------
# EXERCISE 2 — the agent loop
# --------------------------------------------------------------------------

EX2_SPEC = """\
Write `loop.py` next to this file with:

    run_agent(question, chat, registry, max_turns=4) -> (final_text, turns_used)

chat(messages, tools) returns a chat-completions-shaped dict:

    {"choices": [{"message": {"role": "assistant", "content": ...,
      "tool_calls": [{"id": ..., "type": "function",
        "function": {"name": ..., "arguments": "<json string>"}}]}}]}

registry is a dict like exercise 1's: {name: {"fn": callable}}. Loop rules
(lesson 02): append the assistant message; for each tool_call run
json.loads(arguments) and call the registry fn; append a {"role": "tool",
"tool_call_id": ..., "content": json.dumps(result)} message; repeat until the
model returns no tool_calls — or max_turns is spent, whichever first.
Returns (final_text, turns_used).
"""


def _tool_call(call_id: str, name: str, arguments: dict) -> dict:
    return {"id": call_id, "type": "function",
            "function": {"name": name, "arguments": json.dumps(arguments)}}


def _reply(content=None, tool_calls=None) -> dict:
    return {"choices": [{"message": {"role": "assistant", "content": content,
                                     "tool_calls": tool_calls}}]}


def check_ex2() -> bool:
    if not os.path.exists("loop.py"):
        print("  missing loop.py — create it (spec below).")
        print(EX2_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("loop", "loop.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    run_agent = getattr(module, "run_agent", None)
    if run_agent is None:
        print("  loop.py must define run_agent().")
        return False

    with tempfile.TemporaryDirectory() as tmp:
        notes = Path(tmp)
        (notes / "agents.md").write_text("Agents are a loop plus tools. The agent decides, calls, checks, repeats.")
        registry = {
            "read_note": {"fn": lambda name: (notes / name).read_text()},
        }

        seen = []

        def scripted(messages, tools):
            seen.append(messages)
            if any(m["role"] == "tool" for m in messages):
                return _reply(content="agents are a loop")
            return _reply(tool_calls=[_tool_call("c1", "read_note", {"name": "agents.md"})])

        final, turns = run_agent("what is an agent", scripted, registry, max_turns=4)
        ok = final == "agents are a loop"
        good = turns == 2
        saw_tool_msg = any(
            m["role"] == "tool" and "loop" in m["content"] for messages in seen for m in messages
        )
        print(f"  final answer: {final!r}  {'PASS' if ok else 'FAIL'}")
        print(f"  turns used: {turns} (expected 2)  {'PASS' if good else 'FAIL'}")
        print(f"  model saw the tool result:  {'PASS' if saw_tool_msg else 'FAIL'}")
        ok = ok and good and saw_tool_msg

        def runaway(messages, tools):
            return _reply(tool_calls=[_tool_call("c1", "read_note", {"name": "agents.md"})])

        final, turns = run_agent("loop forever", runaway, registry, max_turns=4)
        good = turns == 4
        print(f"  runaway model stopped at max_turns: {turns} (expected 4)  {'PASS' if good else 'FAIL'}")
        ok = ok and good
    return ok


# --------------------------------------------------------------------------
# EXERCISE 3 — guardrail + rewrite
# --------------------------------------------------------------------------

EX3_SPEC = """\
Write `guardrails.py` next to this file with:

    guard(question) -> {"accepted": bool, "reason": str}
    rewrite(query, last_topic="") -> str

guard rejects questions that name no known topic (pick your own topic list —
agents / rag / evals / python / data is fine) with a non-empty reason.
rewrite fixes bad queries (lesson 04): "the one about evals" -> "evals",
"it" with last_topic="rag" -> "rag", stopwords stripped.
"""


def check_ex3() -> bool:
    if not os.path.exists("guardrails.py"):
        print("  missing guardrails.py — create it (spec below).")
        print(EX3_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("guardrails", "guardrails.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    guard = getattr(module, "guard", None)
    rewrite = getattr(module, "rewrite", None)
    if guard is None or rewrite is None:
        print("  guardrails.py must define guard() and rewrite().")
        return False

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


# --------------------------------------------------------------------------

def main() -> None:
    results = {}
    print("=" * 60)
    print("EXERCISE 1 — the tool registry")
    print("=" * 60)
    results["ex1"] = check_ex1()
    print()
    print("=" * 60)
    print("EXERCISE 2 — the agent loop")
    print("=" * 60)
    results["ex2"] = check_ex2()
    print()
    print("=" * 60)
    print("EXERCISE 3 — guardrail + rewrite")
    print("=" * 60)
    results["ex3"] = check_ex3()
    print()
    passed = sum(1 for v in results.values() if v)
    print(f"{passed}/3 exercises passed")
    if passed < 3:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
