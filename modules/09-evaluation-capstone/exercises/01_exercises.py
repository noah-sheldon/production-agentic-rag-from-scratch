#!/usr/bin/env python3
"""Module 09 exercises — gate the three lessons (three exercises).

Run:  python3 01_exercises.py

The three exercises:
  1. Build an eval set — write build_eval_set(corpus), pass the validation.
  2. Score an answer — write groundedness() and recall(), pass the cases.
  3. Route a score — write decide(), pass pass/retry/fallback.
"""

from __future__ import annotations

import importlib.util
import os

# --------------------------------------------------------------------------
# EXERCISE 1 — build an eval set
# --------------------------------------------------------------------------

EX1_SPEC = """\
Write `evalset.py` next to this file with a `build_eval_set(corpus)`
function. corpus is a dict {note_id: text}. Return a list of at least 3
entries, each a dict with "question", "answer", and "source" (a list of
note_ids that hold the answer's facts). Every source must exist in corpus.
The check feeds a tiny corpus and validates the shape.
"""

TINY_CORPUS = {
    "deploy": "The nightly deploy runs at 3am.",
    "ci": "CI takes about 3 minutes.",
    "backup": "Backups are stored in S3.",
}


def check_ex1() -> bool:
    if not os.path.exists("evalset.py"):
        print("  missing evalset.py — create it (spec below).")
        print(EX1_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("evalset", "evalset.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fn = getattr(module, "build_eval_set", None)
    if fn is None:
        print("  evalset.py must define build_eval_set(corpus).")
        return False
    entries = fn(TINY_CORPUS)
    if not isinstance(entries, list) or len(entries) < 3:
        print(f"  build_eval_set must return a list of >=3 entries, got {len(entries) if isinstance(entries, list) else type(entries).__name__}  FAIL")
        return False
    ok = True
    for e in entries:
        if not isinstance(e, dict):
            print(f"  entry {e!r} is not a dict  FAIL")
            ok = False
            continue
        q, a, s = e.get("question", ""), e.get("answer", ""), e.get("source", [])
        if not str(q).strip():
            print(f"  entry {e!r}: empty question  FAIL")
            ok = False
        if not str(a).strip():
            print(f"  entry {e!r}: empty answer  FAIL")
            ok = False
        if not isinstance(s, list) or not s:
            print(f"  entry {e!r}: source must be a non-empty list of note ids  FAIL")
            ok = False
        for note_id in s:
            if note_id not in TINY_CORPUS:
                print(f"  entry {e!r}: unknown source {note_id!r}  FAIL")
                ok = False
    print(f"  build_eval_set -> {len(entries)} entries, shape valid:  {'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------
# EXERCISE 2 — score an answer
# --------------------------------------------------------------------------

EX2_SPEC = """\
Write `scoring.py` next to this file with:
  groundedness(answer, context) -> float  # share of answer words in context
  recall(retrieved, relevant) -> float    # share of relevant notes retrieved
Both return 0.0-1.0. The check feeds a perfect answer, a hallucinated one,
and a missed-recall case.
"""

CONTEXT = "The nightly deploy runs at 3am. Backups are stored in S3."


def check_ex2() -> bool:
    if not os.path.exists("scoring.py"):
        print("  missing scoring.py — create it (spec below).")
        print(EX2_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("scoring", "scoring.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ok = True

    g = getattr(module, "groundedness", None)
    if g is None:
        print("  scoring.py must define groundedness(answer, context).")
        return False
    perfect = g("The nightly deploy runs at 3am.", CONTEXT)
    good = perfect >= 0.8
    print(f"  groundedness(grounded answer) = {perfect:.2f}  {'PASS' if good else 'FAIL'}")
    ok = ok and good
    bad = g("The deploy runs at noon on Mars.", CONTEXT)
    good = bad <= 0.6
    print(f"  groundedness(noontime answer)  = {bad:.2f}  {'PASS' if good else 'FAIL'}")
    ok = ok and good

    r = getattr(module, "recall", None)
    if r is None:
        print("  scoring.py must define recall(retrieved, relevant).")
        return False
    hit = r(["deploy", "backup"], ["deploy"])
    good = hit == 1.0
    print(f"  recall(source retrieved)       = {hit:.2f}  {'PASS' if good else 'FAIL'}")
    ok = ok and good
    miss = r(["deploy"], ["backup"])
    good = miss == 0.0
    print(f"  recall(source missed)          = {miss:.2f}  {'PASS' if good else 'FAIL'}")
    ok = ok and good
    return ok


# --------------------------------------------------------------------------
# EXERCISE 3 — route a score
# --------------------------------------------------------------------------

EX3_SPEC = """\
Write `gate.py` next to this file with `decide(score, threshold=0.5)`:
  score >= threshold      -> "pass"
  score >= threshold / 2  -> "retry"
  otherwise               -> "fallback"
The check feeds three scores against threshold 0.7.
"""


def check_ex3() -> bool:
    if not os.path.exists("gate.py"):
        print("  missing gate.py — create it (spec below).")
        print(EX3_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("gate", "gate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fn = getattr(module, "decide", None)
    if fn is None:
        print("  gate.py must define decide(score, threshold=0.5).")
        return False
    cases = [(0.9, "pass"), (0.4, "retry"), (0.1, "fallback")]
    ok = True
    for score, want in cases:
        got = fn(score, threshold=0.7)
        good = got == want
        print(f"  decide({score}, threshold=0.7) = {got!r} (want {want!r})  {'PASS' if good else 'FAIL'}")
        ok = ok and good
    return ok


# --------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("EXERCISE 1 — build an eval set")
    print("=" * 60)
    ex1 = check_ex1()
    print()
    print("=" * 60)
    print("EXERCISE 2 — score an answer")
    print("=" * 60)
    ex2 = check_ex2()
    print()
    print("=" * 60)
    print("EXERCISE 3 — route a score")
    print("=" * 60)
    ex3 = check_ex3()
    print()
    passed = sum(1 for v in (ex1, ex2, ex3) if v)
    print(f"{passed}/3 exercises passed")
    if passed < 3:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
