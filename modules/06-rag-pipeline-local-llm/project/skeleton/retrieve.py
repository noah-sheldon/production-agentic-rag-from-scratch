"""Keyword retrieval over a notes folder — stdlib only.

TODO (lesson 01): the scoring here is a word-overlap rank. Swap it for the
full BM25 you built in module 03 — same shape, better ranking on longer
notes.
"""
from __future__ import annotations

import math
import re
from pathlib import Path


def tokenize(text: str) -> list[str]:
    """Split into lowercase word pieces; a tiny stemmer makes "runs" match
    "run" and "models" match "model"."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w[:-1] if w.endswith("s") and len(w) > 3 else w for w in words]


def load_notes(notes_dir: str = "notes") -> list[tuple[str, str]]:
    """Read every .md file in the folder: title from the filename, body
    from the text. TODO: read real metadata (date, tags) like module 02."""
    notes = []
    for path in sorted(Path(notes_dir).glob("*.md")):
        notes.append((path.stem, path.read_text().strip()))
    return notes


def retrieve(question: str, notes: list[tuple[str, str]], k: int = 3) -> list[tuple[str, str]]:
    """Return the top-k notes ranked by word overlap with the question."""
    tokens = [tokenize(text) for _, text in notes]
    avgdl = sum(len(t) for t in tokens) / max(len(tokens), 1)
    scored = []
    for i, (title, text) in enumerate(notes):
        score = 0.0
        for term in set(tokenize(question)):
            tf = tokens[i].count(term)
            if tf:
                dl = len(tokens[i])
                n = sum(1 for t in tokens if term in t)
                idf = math.log(1 + (len(tokens) - n + 0.5) / (n + 0.5))
                score += idf * (tf * 2.2) / (tf + 1.2 * (0.25 + 0.75 * dl / avgdl))
        scored.append((score, title, text))
    scored.sort(reverse=True)
    return [(title, text) for _, title, text in scored[:k]]
