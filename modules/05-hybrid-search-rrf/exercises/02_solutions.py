#!/usr/bin/env python3
"""Module 05 — solutions to the three exercises.

Run:  python3 02_solutions.py
Self-contained: each exercise implementation + the same checks the
exercises file runs. All three must PASS.
"""
import hashlib
import math
import random
import re

DIM = 64

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "when", "why", "my",
    "how", "do", "does", "i", "to", "and", "at", "under", "too", "for",
    "of", "it", "with", "on", "in", "as", "you", "your", "that", "this",
}


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


# --------------------------------------------------------------------------
# EXERCISE 1 — RRF by hand
# --------------------------------------------------------------------------

def rrf(ranked_lists: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    """Fuse ranked lists (each = docs best-first) by position, not score."""
    points: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, doc in enumerate(ranked, start=1):
            points[doc] = points.get(doc, 0.0) + 1.0 / (k + rank)
    order = list(points)
    return [(d, p) for d, p in sorted(points.items(), key=lambda kv: (-kv[1], order.index(kv[0])))]


def exercise1() -> bool:
    ok = True
    case1 = [["a", "b", "c", "d"], ["c", "a", "b", "d"]]
    names = [d for d, _p in rrf(case1)]
    good = names == ["a", "c", "b", "d"]
    print(f"check: rrf(case1) -> {names} {'PASS' if good else 'FAIL'}")
    ok = ok and good
    case2 = [["x", "y"], ["y", "z"]]
    names = [d for d, _p in rrf(case2)]
    good = names == ["y", "x", "z"]
    print(f"check: rrf(case2) -> {names} {'PASS' if good else 'FAIL'}")
    return ok and good


# --------------------------------------------------------------------------
# EXERCISE 2 — mine the queries
# --------------------------------------------------------------------------

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


def keyword_rank(notes: dict[str, str], query: str) -> list[tuple[str, float]]:
    names = list(notes)
    toks = [tokenize(t) for t in notes.values()]

    def idf(term: str) -> float:
        n = sum(1 for t in toks if term in t)
        return math.log(1 + (len(toks) - n + 0.5) / (n + 0.5))

    scored = []
    for name, tok in zip(names, toks):
        score = sum(tok.count(t) * idf(t) for t in set(tokenize(query)) if t in tok)
        scored.append((name, round(score, 3)))
    return sorted(scored, key=lambda kv: (-kv[1], names.index(kv[0])))


def token_vector(token: str) -> list[float]:
    seed = int.from_bytes(hashlib.sha256(token.encode()).digest()[:8], "big")
    rng = random.Random(seed)
    v = [rng.gauss(0.0, 1.0) for _ in range(DIM)]
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def doc_vector(tokens: list[str]) -> list[float]:
    if not tokens:
        return [0.0] * DIM
    vs = [token_vector(t) for t in tokens]
    mean = [sum(v[i] for v in vs) / len(vs) for i in range(DIM)]
    n = math.sqrt(sum(x * x for x in mean)) or 1.0
    return [x / n for x in mean]


def semantic_rank(notes: dict[str, str], query: str) -> list[tuple[str, float]]:
    qv = doc_vector(tokenize(query))
    names = list(notes)
    scored = []
    for name in names:
        dv = doc_vector(tokenize(notes[name]))
        scored.append((name, round(sum(a * b for a, b in zip(qv, dv)), 4)))
    return sorted(scored, key=lambda kv: (-kv[1], names.index(kv[0])))


def find_queries() -> tuple[str, str, str]:
    """The three queries the lesson 02 build mined."""
    return ("timeout", "postgres config", "postgres timeout")


def _fused_top2(query: str) -> list[str]:
    kw = keyword_rank(NOTES, query)
    sem = semantic_rank(NOTES, query)
    points: dict[str, float] = {}
    for ranked in (kw, sem):
        for rank, (name, _s) in enumerate(ranked, start=1):
            points[name] = points.get(name, 0.0) + 1.0 / (60 + rank)
    order = list(points)
    return [d for d, _p in sorted(points.items(), key=lambda kv: (-kv[1], order.index(kv[0])))][:2]


def exercise2() -> bool:
    kw_query, sem_query, both_query = find_queries()
    ok = True

    kw1 = keyword_rank(NOTES, kw_query)[0][0]
    sem1 = semantic_rank(NOTES, kw_query)[0][0]
    good = kw1 in {"A", "B"} and sem1 == "H" and kw1 != sem1
    print(f"check: kw_query {kw_query!r}: kw top-1={kw1}, sem top-1={sem1} -> {'PASS' if good else 'FAIL'}")
    ok = ok and good

    sem1 = semantic_rank(NOTES, sem_query)[0][0]
    kw1 = keyword_rank(NOTES, sem_query)[0][0]
    good = sem1 in {"B", "Z"} and kw1 not in {"B", "Z"}
    print(f"check: sem_query {sem_query!r}: sem top-1={sem1}, kw top-1={kw1} -> {'PASS' if good else 'FAIL'}")
    ok = ok and good

    kw_top = keyword_rank(NOTES, both_query)[0][0]
    sem_top = semantic_rank(NOTES, both_query)[0][0]
    fused = _fused_top2(both_query)
    good = kw_top != sem_top and {kw_top, sem_top} <= {"A", "B"} and set(fused) == {"A", "B"}
    print(f"check: both_query {both_query!r}: kw={kw_top}, sem={sem_top}, fused top-2={fused} -> "
          f"{'PASS' if good else 'FAIL'}")
    return ok and good


# --------------------------------------------------------------------------
# EXERCISE 3 — the unified search API
# --------------------------------------------------------------------------

CORPUS = [
    "postgres timeout happens when the connection pool is full",
    "postgres timeout config",
    "the api client hangs when the server is slow to answer",
    "kubernetes pod restart loop after memory pressure",
]


def search(corpus: list[str], query: str, mode: str = "hybrid", k: int = 3) -> list[tuple[float, str]]:
    """One function, three modes, same inputs, same output shape."""
    notes = {str(i): text for i, text in enumerate(corpus)}
    engine = _Engine(notes)
    if mode == "keyword":
        scores = engine.keyword_scores(query)
    elif mode == "semantic":
        scores = engine.semantic_scores(query)
    elif mode == "hybrid":
        scores = engine.rrf(query)
    else:
        raise ValueError(f"unknown mode {mode!r}")
    order = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
    return [(round(scores[i], 4), notes[str(i)]) for i in order[:k]]


class _Engine:
    def __init__(self, notes: dict[str, str]):
        self.names = list(notes)
        self.texts = [notes[n] for n in self.names]
        self.tokens = [tokenize(t) for t in self.texts]
        self._doc_vecs = [doc_vector(t) for t in self.tokens]
        self._idf: dict[str, float] = {}

    def _idf_value(self, term: str) -> float:
        if term not in self._idf:
            n = sum(1 for t in self.tokens if term in t)
            self._idf[term] = math.log(1 + (len(self.tokens) - n + 0.5) / (n + 0.5))
        return self._idf[term]

    def keyword_scores(self, query: str) -> list[float]:
        return [sum(tok.count(t) * self._idf_value(t) for t in set(tokenize(query)) if t in tok)
                for tok in self.tokens]

    def semantic_scores(self, query: str) -> list[float]:
        qv = doc_vector(tokenize(query))
        return [sum(a * b for a, b in zip(qv, dv)) for dv in self._doc_vecs]

    def rrf(self, query: str) -> list[float]:
        kw = self.keyword_scores(query)
        sem = self.semantic_scores(query)
        kw_rank = {i: r for r, i in enumerate(sorted(range(len(kw)), key=lambda i: (-kw[i], i)), 1)}
        sem_rank = {i: r for r, i in enumerate(sorted(range(len(sem)), key=lambda i: (-sem[i], i)), 1)}
        return [1.0 / (60 + kw_rank[i]) + 1.0 / (60 + sem_rank[i]) for i in range(len(kw))]


def exercise3() -> bool:
    ok = True
    results = {}
    for mode in ("keyword", "semantic", "hybrid"):
        results[mode] = search(CORPUS, "postgres timeout", mode=mode, k=2)
    for mode, out in results.items():
        shape = (isinstance(out, list) and len(out) <= 2
                 and all(isinstance(s, (int, float)) and isinstance(t, str) for s, t in out))
        scores = all(out[i][0] >= out[i + 1][0] for i in range(len(out) - 1))
        print(f"check: {mode} -> {[(round(s, 3), t[:24]) for s, t in out]} "
              f"{'PASS' if shape and scores else 'FAIL'}")
        ok = ok and shape and scores
    det = search(CORPUS, "postgres timeout", mode="semantic", k=2) == results["semantic"]
    print(f"check: semantic deterministic -> {'PASS' if det else 'FAIL'}")
    ok = ok and det
    union = {results["keyword"][0][1], results["semantic"][0][1]}
    good = results["hybrid"][0][1] in union
    print(f"check: hybrid top-1 from an engine's top-1 -> {'PASS' if good else 'FAIL'}")
    return ok and good


def main() -> None:
    print("=" * 60)
    print("EXERCISE 1 — RRF by hand")
    print("=" * 60)
    ok1 = exercise1()
    print()
    print("=" * 60)
    print("EXERCISE 2 — mine the queries")
    print("=" * 60)
    ok2 = exercise2()
    print()
    print("=" * 60)
    print("EXERCISE 3 — the unified search API")
    print("=" * 60)
    ok3 = exercise3()
    print()
    passed = sum((ok1, ok2, ok3))
    print(f"{passed}/3 exercises passed")
    if passed < 3:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
