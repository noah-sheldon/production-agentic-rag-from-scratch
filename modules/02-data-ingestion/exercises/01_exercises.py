#!/usr/bin/env python3
"""Module 02 exercises — gate the three lessons (three exercises).

Run:  python3 01_exercises.py

The three exercises:
  1. Fetch with retry/backoff — write fetch_with_retry, pass the flaky test.
  2. Parse a document — extract title + body from HTML and markdown.
  3. Design the pipeline — fill in the step list and the idempotency answer.
"""

from __future__ import annotations

import importlib.util
import os
import random
import time

# --------------------------------------------------------------------------
# EXERCISE 1 — retries with backoff
# --------------------------------------------------------------------------

EX1_SPEC = """\
Write `retry.py` next to this file with a `fetch_with_retry(fn, attempts=4,
base_wait=0.05)` function: exponential backoff (wait = base * 2**(attempt-1)
+ a little jitter), raise on the last attempt. The check feeds it a flaky
function and expects it to succeed by attempt 3.
"""


def check_ex1() -> bool:
    if not os.path.exists("retry.py"):
        print("  missing retry.py — create it (spec below).")
        print(EX1_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("retry", "retry.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fn = getattr(module, "fetch_with_retry", None)
    if fn is None:
        print("  retry.py must define fetch_with_retry().")
        return False
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise TimeoutError("rate limited")
        return "ok"

    result = fn(flaky, attempts=4, base_wait=0.01)
    good = result == "ok" and calls["n"] == 3
    print(f"  flaky endpoint -> {result!r} in {calls['n']} calls  {'PASS' if good else 'FAIL'}")
    return good


# --------------------------------------------------------------------------
# EXERCISE 2 — parse a document
# --------------------------------------------------------------------------

EX2_SPEC = """\
Write `parser.py` with `parse_html(raw)` and `parse_markdown(raw)` returning
(title, body). Title from <title> (HTML) or frontmatter/`# ` (markdown). Body
with tags stripped and whitespace collapsed. The check feeds samples.
"""

HTML_SAMPLE = "<html><head><title>My Note</title></head><body><nav>x</nav><p>Hello world.</p></body></html>"
MD_SAMPLE = "---\ntitle: Agents\n---\n# Agents\nLoops and tools."


def check_ex2() -> bool:
    if not os.path.exists("parser.py"):
        print("  missing parser.py — create it (spec below).")
        print(EX2_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("parser", "parser.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ok = True
    if hasattr(module, "parse_html"):
        title, body = module.parse_html(HTML_SAMPLE)
        good = title == "My Note" and "Hello world." in body and "nav" not in body
        print(f"  parse_html -> title={title!r}, body={body!r}  {'PASS' if good else 'FAIL'}")
        ok = ok and good
    if hasattr(module, "parse_markdown"):
        title, body = module.parse_markdown(MD_SAMPLE)
        good = title == "Agents" and "Loops and tools." in body
        print(f"  parse_markdown -> title={title!r}, body={body!r}  {'PASS' if good else 'FAIL'}")
        ok = ok and good
    return ok


# --------------------------------------------------------------------------
# EXERCISE 3 — design the pipeline
# --------------------------------------------------------------------------

EX3_QUESTION = """\
Fill PIPELINE_STEPS: the ordered steps for a read-it-later pipeline (from
source to store). Include where retries and the done-set go. Then answer in
IDEMPOTENCY (2-3 sentences): why must re-running a pipeline produce the same
result, and what breaks if it doesn't?
"""

PIPELINE_STEPS = []
IDEMPOTENCY = ""


def check_ex3() -> bool:
    steps = [s.lower() for s in PIPELINE_STEPS]
    required = ["fetch", "parse", "store"]
    ok = all(any(r in s for s in steps) for r in required)
    print(f"  pipeline steps include fetch/parse/store: {'PASS' if ok else 'FAIL'}")
    good = "retry" in IDEMPOTENCY.lower() or "done" in IDEMPOTENCY.lower()
    print(f"  idempotency mentions retry/done-set:      {'PASS' if good else 'FAIL'}")
    return ok and good


# --------------------------------------------------------------------------

def main() -> None:
    results = {}
    print("=" * 60)
    print("EXERCISE 1 — retries with backoff")
    print("=" * 60)
    results["ex1"] = check_ex1()
    print()
    print("=" * 60)
    print("EXERCISE 2 — parse a document")
    print("=" * 60)
    results["ex2"] = check_ex2()
    print()
    print("=" * 60)
    print("EXERCISE 3 — design the pipeline")
    print("=" * 60)
    print(EX3_QUESTION)
    results["ex3"] = check_ex3()
    print()
    passed = sum(1 for v in results.values() if v)
    print(f"{passed}/3 exercises passed")
    if passed < 3:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
