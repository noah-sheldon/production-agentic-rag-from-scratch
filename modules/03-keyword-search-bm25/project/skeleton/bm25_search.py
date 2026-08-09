#!/usr/bin/env python3
"""BM25 engine over your notes (stdlib only). Index + search + filter.

Run:  python3 search_cli.py "query" [--tag TAG] [--k N]
"""
import math
import re
import sys
from pathlib import Path

NOTES = Path(__file__).resolve().parent / "notes"


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25Index:
    def __init__(self, k1: float = 1.2, b: float = 0.75):
        self.k1, self.b = k1, b
        self.docs: list[tuple[str, str]] = []      # (title, text)
        self.tokens: list[list[str]] = []
        self.tags: list[set[str]] = []

    def add(self, title: str, text: str, tags: set[str] | None = None) -> None:
        self.docs.append((title, text))
        self.tokens.append(tokenize(text))
        self.tags.append(tags or set())

    def _idf(self, term: str) -> float:
        n = sum(1 for t in self.tokens if term in t)
        return math.log(1 + (len(self.tokens) - n + 0.5) / (n + 0.5))

    def search(self, query: str, tag: str | None = None, k: int = 5):
        avgdl = sum(len(t) for t in self.tokens) / max(len(self.tokens), 1)
        scored = []
        for i, toks in enumerate(self.tokens):
            if tag and tag not in self.tags[i]:
                continue
            score = sum(
                self._idf(t) * (toks.count(t) * (self.k1 + 1)) /
                (toks.count(t) + self.k1 * (1 - self.b + self.b * len(toks) / avgdl))
                for t in set(tokenize(query)) if t in toks)
            scored.append((score, self.docs[i][0]))
        return sorted(scored, reverse=True)[:k]


def load_notes() -> BM25Index:
    idx = BM25Index()
    for p in sorted(NOTES.glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        idx.add(p.stem, text, {"python"} if "python" in text.lower() else set())
    return idx


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("usage: python3 search_cli.py \"query\" [--tag TAG] [--k N]")
        return
    query = args[0]
    tag = args[args.index("--tag") + 1] if "--tag" in args else None
    k = int(args[args.index("--k") + 1]) if "--k" in args else 5
    idx = load_notes()
    for score, title in idx.search(query, tag=tag, k=k):
        print(f"  {score:6.3f}  {title}")


if __name__ == "__main__":
    main()
