#!/usr/bin/env python3
"""Module 06 exercises — gate the three lessons (three exercises).

Run:  python3 01_exercises.py

The three exercises:
  1. The RAG flow — write `rag_flow.py`: retrieve(), build_prompt(), answer().
  2. Prompt trimming — write `trim.py`: count_tokens(), trim_context().
  3. Streaming (SSE) — write `stream.py`: sse_event(), token_stream().

Each check imports your file, runs it against a fixed sample, and prints
PASS/FAIL. All three must pass.
"""

from __future__ import annotations

import importlib.util
import os

# --------------------------------------------------------------------------
# EXERCISE 1 — the RAG flow
# --------------------------------------------------------------------------

EX1_SPEC = """\
Write `rag_flow.py` next to this file with:

  def retrieve(question, docs, k=2) -> list[(title, text)]
      Rank docs (list of (title, text)) by how many question words each
      contains. Return the top k as (title, text) pairs.
  def build_prompt(context, question) -> str
      Instructions that put the context first and the question last.
  def answer(question, docs, model, k=2) -> str
      retrieve -> build_prompt -> model(prompt); return the model's reply.

The check expects retrieve() to rank the matching note first, build_prompt()
to contain both the context and the question, and answer() to feed a prompt
to the model that contains the matching note.
"""

CHECK_DOCS = [
    ("deploy", "the deploy runs at 3am and builds the image"),
    ("vectors", "chunks become vectors in a vector store"),
    ("ollama", "ollama runs models on your own machine"),
]
CHECK_QUESTION = "where does the deploy run?"


def load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_ex1() -> bool:
    if not os.path.exists("rag_flow.py"):
        print("  missing rag_flow.py — create it (spec below).")
        print(EX1_SPEC)
        return False
    module = load_module("rag_flow", "rag_flow.py")
    ok = True

    top = module.retrieve(CHECK_QUESTION, CHECK_DOCS, k=1)
    good = top and top[0][0] == "deploy"
    print(f"  retrieve ranks the matching note first:      {'PASS' if good else 'FAIL'}")
    ok = ok and good

    prompt = module.build_prompt("some context", CHECK_QUESTION)
    good = "some context" in prompt and CHECK_QUESTION in prompt
    print(f"  build_prompt packs context and question:     {'PASS' if good else 'FAIL'}")
    ok = ok and good

    seen = {}

    def model(p: str) -> str:
        seen["prompt"] = p
        return "ok"

    reply = module.answer(CHECK_QUESTION, CHECK_DOCS, model)
    good = reply == "ok" and "deploy" in seen.get("prompt", "")
    print(f"  answer runs retrieve -> prompt -> model:     {'PASS' if good else 'FAIL'}")
    ok = ok and good
    return ok


# --------------------------------------------------------------------------
# EXERCISE 2 — prompt trimming
# --------------------------------------------------------------------------

EX2_SPEC = """\
Write `trim.py` next to this file with:

  def count_tokens(text) -> int
      Rough token count (~4 characters per token), at least 1.
  def trim_context(ranked, question, budget_tokens=30) -> str
      ranked is a list of (title, text). Keep ONLY the sentences that
      contain a question word, prefixed with [title], and stop once the
      budget is used up.

The check feeds two notes (one matches the question, one does not) and
expects the matching sentence back, the unrelated one dropped, and the
result within the budget.
"""

RANKED = [
    ("deploy", "The deploy runs at 3am. Chunks become vectors in a store."),
    ("ollama", "Ollama runs models on your own machine."),
]


def check_ex2() -> bool:
    if not os.path.exists("trim.py"):
        print("  missing trim.py — create it (spec below).")
        print(EX2_SPEC)
        return False
    module = load_module("trim", "trim.py")
    ok = True

    n = module.count_tokens("hello world")
    good = 1 <= n <= 4
    print(f"  count_tokens('hello world') = {n} (1-4 expected):  {'PASS' if good else 'FAIL'}")
    ok = ok and good

    out = module.trim_context(RANKED, "deploy", budget_tokens=30)
    good = "deploy" in out and "vectors" not in out and "Ollama" not in out
    print(f"  matching sentence kept, unrelated dropped:   {'PASS' if good else 'FAIL'}")
    ok = ok and good
    good = module.count_tokens(out) <= 30
    print(f"  trimmed prompt within budget ({module.count_tokens(out)} <= 30 tokens):  {'PASS' if good else 'FAIL'}")
    ok = ok and good
    return ok


# --------------------------------------------------------------------------
# EXERCISE 3 — streaming (SSE)
# --------------------------------------------------------------------------

EX3_SPEC = """\
Write `stream.py` next to this file with:

  def sse_event(data) -> str
      Return the Server-Sent Events frame: exactly "data: {data}\\n\\n".
  def token_stream(text, delay=0.0) -> generator
      Yield the words of text one at a time (a generator, no list).

The check verifies the exact frame format and that the generator yields the
tokens in order.
"""


def check_ex3() -> bool:
    if not os.path.exists("stream.py"):
        print("  missing stream.py — create it (spec below).")
        print(EX3_SPEC)
        return False
    module = load_module("stream", "stream.py")
    ok = True

    frame = module.sse_event("hello")
    good = frame == "data: hello\n\n"
    print(f"  sse_event format: {frame!r:24} {'PASS' if good else 'FAIL'}")
    ok = ok and good

    tokens = list(module.token_stream("a b c", delay=0.0))
    good = tokens == ["a", "b", "c"]
    print(f"  token_stream yields tokens in order:         {'PASS' if good else 'FAIL'}")
    ok = ok and good
    return ok


# --------------------------------------------------------------------------

def main() -> None:
    results = {}
    print("=" * 60)
    print("EXERCISE 1 — the RAG flow (rag_flow.py)")
    print("=" * 60)
    results["ex1"] = check_ex1()
    print()
    print("=" * 60)
    print("EXERCISE 2 — prompt trimming (trim.py)")
    print("=" * 60)
    results["ex2"] = check_ex2()
    print()
    print("=" * 60)
    print("EXERCISE 3 — streaming / SSE (stream.py)")
    print("=" * 60)
    results["ex3"] = check_ex3()
    print()
    passed = sum(1 for v in results.values() if v)
    print(f"{passed}/3 exercises passed")
    if passed < 3:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
