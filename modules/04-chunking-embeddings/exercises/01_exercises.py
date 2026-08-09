#!/usr/bin/env python3
"""Module 04 exercises — gate the three lessons (three exercises).

Run:  python3 01_exercises.py

The three exercises:
  1. Section chunker — write chunker.py, pass the split + overlap checks.
  2. Cosine by hand — write cosine.py, rank 384-number vectors by closeness.
  3. Chunk-size comparison — chunk the same text at 3 sizes, fill in SIZE_NOTES.
"""

from __future__ import annotations

import importlib.util
import os
import random

# --------------------------------------------------------------------------
# EXERCISE 1 — the section chunker
# --------------------------------------------------------------------------

EX1_SPEC = """\
Write `chunker.py` next to this file with
`chunk_by_sections(text, max_words=120, overlap_words=20)` returning a list
of (heading, text) tuples. Split the text at lines starting with '#', then
re-split any section longer than max_words into pieces of max_words words,
carrying the last overlap_words words into the next piece (see lesson 01's
build). The check feeds the sample below with max_words=12, overlap_words=4
and expects: every heading appears, no words lost, and overlap between
neighboring pieces.
"""

SAMPLE = """# Setup
Install Python and make a venv.

## Notes Folder
Put markdown notes in this folder, one idea per file, and keep the headings honest.

# Daily Log
First entry: planned the semantic index. Second entry: built the chunker. Third entry: tested the embedder. Fourth entry: searched by meaning. Fifth entry: measured the results. Sixth entry: wrote it down. Seventh entry: cleaned the index. Eighth entry: ran it again."""


def check_ex1() -> bool:
    if not os.path.exists("chunker.py"):
        print("  missing chunker.py — create it (spec below).")
        print(EX1_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("chunker", "chunker.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fn = getattr(module, "chunk_by_sections", None)
    if fn is None:
        print("  chunker.py must define chunk_by_sections().")
        return False
    chunks = fn(SAMPLE, max_words=12, overlap_words=4)
    if not chunks or not all(isinstance(c, tuple) and len(c) == 2 for c in chunks):
        print(f"  expected (heading, text) tuples, got {chunks!r}")
        return False
    headings = [h.lower() for h, _ in chunks]
    ok_head = all(any(h in hh for hh in headings) for h in ("setup", "notes folder", "daily log"))
    print(f"  all three headings present:  {'PASS' if ok_head else 'FAIL'}")
    # heading words live in the tuple's heading part; body words must survive
    body_lines = [l for l in SAMPLE.splitlines()
                  if l.strip() and not l.lstrip().startswith("#")]
    doc_words = " ".join(body_lines).lower().split()
    joined = " ".join(t for _, t in chunks).lower().split()
    ok_loss = all(w in joined for w in doc_words)
    print(f"  no words lost:                {'PASS' if ok_loss else 'FAIL'}")
    shared = max(
        (len(set(chunks[i - 1][1].split()) & set(chunks[i][1].split()))
         for i in range(1, len(chunks))),
        default=0,
    )
    ok_overlap = shared >= 1
    print(f"  overlap between neighbors:    {shared} shared word(s)  "
          f"{'PASS' if ok_overlap else 'FAIL'}")
    return ok_head and ok_loss and ok_overlap


# --------------------------------------------------------------------------
# EXERCISE 2 — cosine similarity by hand
# --------------------------------------------------------------------------

EX2_SPEC = """\
Write `cosine.py` next to this file with:
  cosine_similarity(a, b) -> float       (dot / (len(a) * len(b)))
  rank_by_cosine(query, candidates) -> list[int]
rank_by_cosine returns candidate indices sorted best-first (closest first).
No ML libraries — plain math (lesson 02's build). The check feeds seeded
random 384-number vectors: a vector vs itself must score ~1.0, a vector vs
an unrelated one must score < 0.2, and a slightly perturbed copy must rank
first among 5 candidates.
"""

DIM = 384


def make_vector(seed: int) -> list[float]:
    rng = random.Random(seed)
    return [rng.uniform(-1.0, 1.0) for _ in range(DIM)]


def check_ex2() -> bool:
    if not os.path.exists("cosine.py"):
        print("  missing cosine.py — create it (spec below).")
        print(EX2_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("cosine", "cosine.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cosine = getattr(module, "cosine_similarity", None)
    rank = getattr(module, "rank_by_cosine", None)
    if cosine is None or rank is None:
        print("  cosine.py must define cosine_similarity() and rank_by_cosine().")
        return False
    v = make_vector(1)
    w = make_vector(2)
    self_score = cosine(v, v)
    ok_self = abs(self_score - 1.0) < 0.01
    print(f"  cosine(v, v) = {self_score:.4f}        {'PASS' if ok_self else 'FAIL'}")
    other = cosine(v, w)
    ok_other = other < 0.2
    print(f"  cosine(v, unrelated) = {other:.4f}  {'PASS' if ok_other else 'FAIL'}")
    candidates = [v] + [make_vector(s) for s in (10, 11, 12, 13)]
    order = rank(v, candidates)
    ok_rank = isinstance(order, list) and order[0] == 0
    print(f"  closest candidate ranks first:  {order[:3]}  {'PASS' if ok_rank else 'FAIL'}")
    return ok_self and ok_other and ok_rank


# --------------------------------------------------------------------------
# EXERCISE 3 — chunk size matters
# --------------------------------------------------------------------------

EX3_QUESTION = """\
Chunk the lesson 03 note (or any text with one clear answer sentence) at 3
sizes with a fixed-size splitter (text.split() into N-word pieces). Then fill
SIZE_NOTES (2-3 sentences): what does each size do to the answer — which size
cuts the answer, which buries it, which keeps it whole and small?
"""

SIZE_NOTES = ""


def check_ex3() -> bool:
    ok = "noise" in SIZE_NOTES.lower() and "context" in SIZE_NOTES.lower()
    print(f"  SIZE_NOTES explains too-big (noise) + too-small (context): "
          f"{'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------

def main() -> None:
    results = {}
    print("=" * 60)
    print("EXERCISE 1 — the section chunker")
    print("=" * 60)
    results["ex1"] = check_ex1()
    print()
    print("=" * 60)
    print("EXERCISE 2 — cosine similarity by hand")
    print("=" * 60)
    results["ex2"] = check_ex2()
    print()
    print("=" * 60)
    print("EXERCISE 3 — chunk size matters")
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
