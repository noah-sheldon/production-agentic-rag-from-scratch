#!/usr/bin/env python3
"""Module 03 exercises — gate the three lessons (three exercises).

Run:  python3 01_exercises.py

The three exercises:
  1. Rank with BM25 — implement bm25(), pass the ordering check.
  2. The knobs — explain k1 and b, and pick settings for YOUR data.
  3. Measure — label 5 queries and report precision/recall at k=3.
"""

from __future__ import annotations

import importlib.util
import math
import os
import re

DOCS = [
    "the nightly deploy runs at 3am and builds the image",
    "our ci pipeline runs tests on every pull request",
    "the database backup job runs at midnight",
    "phq-9 scores are stored in the patient table",
    "deploy failures usually come from missing environment variables",
]


# --------------------------------------------------------------------------
# EXERCISE 1 — BM25 ranking
# --------------------------------------------------------------------------

EX1_SPEC = """\
Write `bm25_search.py` with a `bm25(query, docs, k1=1.2, b=0.75)` function
returning sorted (score, doc) pairs (highest first). Use the lesson 01 code.
The check runs the query "deploy runs at 3am" and expects the doc containing
"nightly deploy runs at 3am" to rank FIRST.
"""


def check_ex1() -> bool:
    if not os.path.exists("bm25_search.py"):
        print("  missing bm25_search.py — create it (spec below).")
        print(EX1_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("bm25_search", "bm25_search.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fn = getattr(module, "bm25", None)
    if fn is None:
        print("  bm25_search.py must define bm25().")
        return False
    ranked = fn("deploy runs at 3am", DOCS)
    top_doc = ranked[0][1]
    good = "nightly deploy" in top_doc
    print(f"  top result: {top_doc!r}  {'PASS' if good else 'FAIL'}")
    return good


# --------------------------------------------------------------------------
# EXERCISE 2 — the knobs
# --------------------------------------------------------------------------

EX2_QUESTION = """\
Answer in the strings K1_EXPLANATION and B_EXPLANATION (2-3 sentences each):
- What does k1 control, and what happens at k1=0 vs high k1?
- What does b control, and when would you raise it?
Then set YOUR_K1, YOUR_B for short, precise notes (1-2 lines each) and justify.
"""

K1_EXPLANATION = ""
B_EXPLANATION = ""
YOUR_K1 = 1.2
YOUR_B = 0.75


def check_ex2() -> bool:
    ok = True
    k1 = K1_EXPLANATION.lower()
    good = "saturat" in k1 and ("presence" in k1 or "repetition" in k1 or "frequency" in k1)
    print(f"  k1 explanation (saturation + frequency): {'PASS' if good else 'FAIL'}")
    ok = ok and good
    b = B_EXPLANATION.lower()
    good = "length" in b and "long" in b
    print(f"  b explanation (length penalty):          {'PASS' if good else 'FAIL'}")
    ok = ok and good
    return ok


# --------------------------------------------------------------------------
# EXERCISE 3 — measure
# --------------------------------------------------------------------------

LABELS = {
    "why does the deploy run at 3am": {0, 4},
    "what runs in our ci pipeline": {1},
    "when is the database backup": {2},
    "where are phq-9 scores stored": {3},
    "deploy failures env variables": {4},
}


def precision_recall(predicted: list[int], relevant: set[int]) -> tuple[float, float]:
    if not predicted:
        return 0.0, 0.0
    hits = sum(1 for i in predicted if i in relevant)
    return hits / len(predicted), hits / len(relevant) if relevant else 1.0


def check_ex3() -> bool:
    if not os.path.exists("bm25_search.py"):
        print("  missing bm25_search.py (do exercise 1 first).")
        return False
    spec = importlib.util.spec_from_file_location("bm25_search", "bm25_search.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fn = module.bm25
    p_total = r_total = 0.0
    for query, relevant in LABELS.items():
        ranked = [DOCS.index(doc) for _, doc in fn(query, DOCS)[:3]]
        p, r = precision_recall(ranked, relevant)
        p_total += p
        r_total += r
    n = len(LABELS)
    print(f"  precision@3 = {p_total/n:.2f}, recall@3 = {r_total/n:.2f}")
    print(f"  report: {'PASS' if r_total/n >= 0.5 else 'FAIL (recall too low — is ranking correct?)'}")
    return r_total / n >= 0.5


# --------------------------------------------------------------------------

def main() -> None:
    results = {}
    print("=" * 60)
    print("EXERCISE 1 — BM25 ranking")
    print("=" * 60)
    results["ex1"] = check_ex1()
    print()
    print("=" * 60)
    print("EXERCISE 2 — the knobs")
    print("=" * 60)
    print(EX2_QUESTION)
    results["ex2"] = check_ex2()
    print()
    print("=" * 60)
    print("EXERCISE 3 — measure precision/recall")
    print("=" * 60)
    results["ex3"] = check_ex3()
    print()
    passed = sum(1 for v in results.values() if v)
    print(f"{passed}/3 exercises passed")
    if passed < 3:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
