#!/usr/bin/env python3
"""Module 05 exercises — gate the three lessons (three exercises).

Run:  python3 01_exercises.py

The three exercises:
  1. Implement RRF — write rrf.py, fuse two ranked lists, match the order.
  2. Mine the queries — write hybrid.py: find where keyword wins alone,
     semantic wins alone, and fusion finds both.
  3. Build the unified API — write search_api.py: one function,
     mode=keyword|semantic|hybrid, same inputs, same output shape.
"""

from __future__ import annotations

import importlib.util
import os

# --------------------------------------------------------------------------
# EXERCISE 1 — RRF by hand
# --------------------------------------------------------------------------

EX1_SPEC = """\
Write `rrf.py` next to this file with an
`rrf(ranked_lists, k=60)` function: each ranked list is a list of doc
strings (best first); a doc earns 1/(k+rank) points per list; return a
sorted list of (doc, points) pairs, highest points first. Use the lesson 01
code. The check feeds two cases and expects the exact merged order.
"""


def _check_case(fn, lists: list[list[str]], expected: list[str], k: int = 60) -> bool:
    try:
        fused = fn(lists, k=k)
    except TypeError:
        fused = fn(lists)  # tolerate missing k parameter
    names = [d for d, _p in fused] if fused and isinstance(fused[0], tuple) else list(fused)
    scores_ok = all(
        isinstance(p, (int, float)) for _d, p in fused
    ) if fused and isinstance(fused[0], tuple) else True
    good = names == expected and scores_ok
    print(f"  rrf({lists}, k={k}) -> {names}  {'PASS' if good else 'FAIL (expected ' + str(expected) + ')'}")
    return good


def check_ex1() -> bool:
    if not os.path.exists("rrf.py"):
        print("  missing rrf.py — create it (spec below).")
        print(EX1_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("rrf", "rrf.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fn = getattr(module, "rrf", None)
    if fn is None:
        print("  rrf.py must define rrf().")
        return False
    case1 = [["a", "b", "c", "d"], ["c", "a", "b", "d"]]
    case2 = [["x", "y"], ["y", "z"]]
    ok1 = _check_case(fn, case1, ["a", "c", "b", "d"])
    ok2 = _check_case(fn, case2, ["y", "x", "z"])
    return ok1 and ok2


# --------------------------------------------------------------------------
# EXERCISE 2 — mine the queries
# --------------------------------------------------------------------------

EX2_SPEC = """\
Write `hybrid.py` with the lesson 02 corpus and rankers:
  keyword_rank(notes, query) -> list of (name, score), best first
  semantic_rank(notes, query) -> list of (name, score), best first
  find_queries() -> (kw_query, sem_query, both_query)
Use the EXACT lesson 02 code: same corpus (A..Z), DIM=64, and the
sha256-seeded token vectors. find_queries must return three queries with
these properties (the check verifies them):
  kw_query:    keyword top-1 is a real note (A or B), semantic top-1 is
               the one-word tag note H
  sem_query:   semantic top-1 is B or Z, keyword top-1 is NOT B or Z
  both_query:  keyword top-1 and semantic top-1 are different notes,
               both from {A, B}, and RRF fusion puts both A and B in its
               top 2
"""

# The lesson 02 corpus — same texts, same order.
NOTES = {
    "A": "postgres timeout happens when the connection pool is full",
    "B": "postgres timeout config",
    "C": "python requests library timeout config",
    "D": "the api client hangs when the server is slow to answer",
    "E": "kubernetes pod restart loop after memory pressure",
    "W": "notes on config: postgres config, connection pool, timeout issues",
    "H": "timeout",
    "Z": "postgres config",
}


def _local_rrf(keyword: list, semantic: list, k: int = 60) -> list[str]:
    points: dict[str, float] = {}
    for ranked in (keyword, semantic):
        for rank, (name, _s) in enumerate(ranked, start=1):
            points[name] = points.get(name, 0.0) + 1.0 / (k + rank)
    order = list(points)
    return [d for d, _p in sorted(points.items(), key=lambda kv: (-kv[1], order.index(kv[0])))]


def check_ex2() -> bool:
    if not os.path.exists("hybrid.py"):
        print("  missing hybrid.py — create it (spec below).")
        print(EX2_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("hybrid", "hybrid.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for fn_name in ("keyword_rank", "semantic_rank", "find_queries"):
        if not hasattr(module, fn_name):
            print(f"  hybrid.py must define {fn_name}().")
            return False

    kw_query, sem_query, both_query = module.find_queries()
    if not all(isinstance(q, str) and q.strip() for q in (kw_query, sem_query, both_query)):
        print("  find_queries() must return three non-empty query strings.")
        return False

    ok = True

    kw1 = module.keyword_rank(NOTES, kw_query)[0][0]
    sem1 = module.semantic_rank(NOTES, kw_query)[0][0]
    good = kw1 in {"A", "B"} and sem1 == "H" and kw1 != sem1
    print(f"  kw_query {kw_query!r}: keyword top-1={kw1}, semantic top-1={sem1}  "
          f"{'PASS' if good else 'FAIL'}")
    ok = ok and good

    sem1 = module.semantic_rank(NOTES, sem_query)[0][0]
    kw1 = module.keyword_rank(NOTES, sem_query)[0][0]
    good = sem1 in {"B", "Z"} and kw1 not in {"B", "Z"}
    print(f"  sem_query {sem_query!r}: semantic top-1={sem1}, keyword top-1={kw1}  "
          f"{'PASS' if good else 'FAIL'}")
    ok = ok and good

    kw_top = module.keyword_rank(NOTES, both_query)[0][0]
    sem_top = module.semantic_rank(NOTES, both_query)[0][0]
    fused = _local_rrf(module.keyword_rank(NOTES, both_query),
                       module.semantic_rank(NOTES, both_query))
    good = kw_top != sem_top and {kw_top, sem_top} <= {"A", "B"} and set(fused[:2]) == {"A", "B"}
    print(f"  both_query {both_query!r}: kw top-1={kw_top}, sem top-1={sem_top}, "
          f"fused top-2={fused[:2]}  {'PASS' if good else 'FAIL'}")
    ok = ok and good
    return ok


# --------------------------------------------------------------------------
# EXERCISE 3 — the unified search API
# --------------------------------------------------------------------------

EX3_SPEC = """\
Write `search_api.py` with a single function
  search(corpus, query, mode="hybrid", k=3) -> [(score, text), ...]
corpus is a list of note strings; mode is 'keyword', 'semantic', or
'hybrid'; every mode takes the SAME inputs and returns the SAME shape:
a sorted (score, text) list, best first, at most k results. Reuse the
lesson 03 SearchEngine. The check verifies shape, determinism, and that
hybrid's top result comes from one of the two engines.
"""

CORPUS = [
    "postgres timeout happens when the connection pool is full",
    "postgres timeout config",
    "the api client hangs when the server is slow to answer",
    "kubernetes pod restart loop after memory pressure",
]
QUERY = "postgres timeout"


def check_ex3() -> bool:
    if not os.path.exists("search_api.py"):
        print("  missing search_api.py — create it (spec below).")
        print(EX3_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("search_api", "search_api.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fn = getattr(module, "search", None)
    if fn is None:
        print("  search_api.py must define search().")
        return False

    ok = True
    results = {}
    try:
        for mode in ("keyword", "semantic", "hybrid"):
            results[mode] = fn(CORPUS, QUERY, mode=mode, k=2)
    except TypeError:
        for mode in ("keyword", "semantic", "hybrid"):
            results[mode] = fn(CORPUS, QUERY, mode=mode)

    for mode, out in results.items():
        shape = (isinstance(out, list) and len(out) <= 2
                 and all(isinstance(s, (int, float)) and isinstance(t, str) for s, t in out))
        scores = all(out[i][0] >= out[i + 1][0] for i in range(len(out) - 1))
        print(f"  {mode}: {[(round(s, 3), t[:24]) for s, t in out]}  "
              f"{'PASS' if shape and scores else 'FAIL'}")
        ok = ok and shape and scores

    again = fn(CORPUS, QUERY, mode="semantic", k=2)
    det = again == results["semantic"]
    print(f"  semantic is deterministic (same call, same answer): {'PASS' if det else 'FAIL'}")
    ok = ok and det

    kw_top = results["keyword"][0][1] if results["keyword"] else None
    sem_top = results["semantic"][0][1] if results["semantic"] else None
    hy_top = results["hybrid"][0][1] if results["hybrid"] else None
    union = {kw_top, sem_top}
    good = hy_top in union
    print(f"  hybrid top-1 {hy_top[:24]!r} comes from an engine's top-1: {'PASS' if good else 'FAIL'}")
    ok = ok and good
    return ok


# --------------------------------------------------------------------------

def main() -> None:
    results = {}
    print("=" * 60)
    print("EXERCISE 1 — RRF by hand")
    print("=" * 60)
    results["ex1"] = check_ex1()
    print()
    print("=" * 60)
    print("EXERCISE 2 — mine the queries")
    print("=" * 60)
    results["ex2"] = check_ex2()
    print()
    print("=" * 60)
    print("EXERCISE 3 — the unified search API")
    print("=" * 60)
    results["ex3"] = check_ex3()
    print()
    passed = sum(1 for v in results.values() if v)
    print(f"{passed}/3 exercises passed")
    if passed < 3:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
