#!/usr/bin/env python3
"""Hybrid search over your notes — keyword + semantic + RRF (stdlib only).

The engine indexes every .md in notes/, then answers queries in three
modes through ONE unified API:

    search(query, mode="hybrid", k=5) -> [(score, title), ...]

  - keyword:  tf x idf scoring (Module 03 style)
  - semantic: cosine over random-vector embeddings — a STAND-IN for a
              real embedding model, seeded so results are deterministic
  - hybrid:   RRF fusion of the two ranked lists (lesson 01)

TODO (see project.md):
  1. Drop YOUR notes into notes/
  2. Write RESULTS.md with your labeled queries (see search_cli --measure)
  3. Swap the stand-in embeddings for real ones in Module 06 — the
     search() contract does not change.
"""
import hashlib
import math
import random
import re
from pathlib import Path

NOTES_DIR = Path(__file__).resolve().parent / "notes"
DIM = 64  # stand-in embedding size

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "when", "why", "my",
    "how", "do", "does", "i", "to", "and", "at", "under", "too", "for",
    "of", "it", "with", "on", "in", "as", "you", "your", "that", "this",
}


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


def _token_vector(token: str) -> list[float]:
    """A fixed random vector per word: same word, same vector, always."""
    seed = int.from_bytes(hashlib.sha256(token.encode()).digest()[:8], "big")
    rng = random.Random(seed)
    v = [rng.gauss(0.0, 1.0) for _ in range(DIM)]
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def _doc_vector(tokens: list[str]) -> list[float]:
    """Mean of the word vectors, normalized (the stand-in embedding)."""
    if not tokens:
        return [0.0] * DIM
    vs = [_token_vector(t) for t in tokens]
    mean = [sum(v[i] for v in vs) / len(vs) for i in range(DIM)]
    n = math.sqrt(sum(x * x for x in mean)) or 1.0
    return [x / n for x in mean]


class HybridSearch:
    """One engine, three modes, one output shape."""

    def __init__(self, notes_dir: Path = NOTES_DIR):
        self.titles: list[str] = []
        self.texts: list[str] = []
        self.tokens: list[list[str]] = []
        self._doc_vecs: list[list[float]] = []
        self._idf: dict[str, float] = {}
        for path in sorted(notes_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            toks = tokenize(text)
            self.titles.append(path.stem)
            self.texts.append(text)
            self.tokens.append(toks)
            self._doc_vecs.append(_doc_vector(toks))

    # --- internals -------------------------------------------------------

    def _idf_value(self, term: str) -> float:
        if term not in self._idf:
            n = sum(1 for t in self.tokens if term in t)
            self._idf[term] = math.log(1 + (len(self.tokens) - n + 0.5) / (n + 0.5))
        return self._idf[term]

    def _keyword_scores(self, query: str) -> list[float]:
        return [
            sum(tok.count(t) * self._idf_value(t) for t in set(tokenize(query)) if t in tok)
            for tok in self.tokens
        ]

    def _semantic_scores(self, query: str) -> list[float]:
        qv = _doc_vector(tokenize(query))
        return [sum(a * b for a, b in zip(qv, dv)) for dv in self._doc_vecs]

    def _rrf(self, kw: list[float], sem: list[float], k: int = 60) -> list[float]:
        kw_rank = {i: r for r, i in enumerate(sorted(range(len(kw)), key=lambda i: (-kw[i], i)), 1)}
        sem_rank = {i: r for r, i in enumerate(sorted(range(len(sem)), key=lambda i: (-sem[i], i)), 1)}
        return [
            1.0 / (k + kw_rank[i]) + 1.0 / (k + sem_rank[i])
            for i in range(len(kw))
        ]

    # --- the unified API ---------------------------------------------------

    def search(self, query: str, mode: str = "hybrid", k: int = 5) -> list[tuple[float, str]]:
        """Same inputs for every mode. Returns [(score, title)] best first."""
        if mode == "keyword":
            scores = self._keyword_scores(query)
        elif mode == "semantic":
            scores = self._semantic_scores(query)
        elif mode == "hybrid":
            scores = self._rrf(self._keyword_scores(query), self._semantic_scores(query))
        else:
            raise ValueError(f"unknown mode {mode!r}")
        order = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
        return [(round(scores[i], 4), self.titles[i]) for i in order[:k]]


if __name__ == "__main__":
    engine = HybridSearch()
    print(f"indexed {len(engine.titles)} notes: {', '.join(engine.titles)}")
    for mode in ("keyword", "semantic", "hybrid"):
        print(f"\nsearch('postgres timeout', mode={mode!r}):")
        for score, title in engine.search("postgres timeout", mode=mode, k=3):
            print(f"  {score:8.4f}  {title}")
