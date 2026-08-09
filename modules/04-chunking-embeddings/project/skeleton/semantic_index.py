#!/usr/bin/env python3
"""Semantic index of your notes — plain Python, stdlib only.

The chain (each piece built by hand in this module):
  notes -> section chunks (lesson 01) -> 384-number embeddings with a
  fallback chain (lesson 02) -> cosine search (lesson 02) -> index.json

TODOs point at the lesson that replaces each stand-in with your own build.
"""
import hashlib
import json
import math
from pathlib import Path

DIM = 384                 # the magic number: one number per dimension
INDEX_FILE = Path("index.json")
NOTES = Path(__file__).resolve().parent / "notes"

# Simulate the real embedder being DOWN so the fallback chain is visible on
# the first build. Flip to True once a real embedder is wired into embed().
EMBEDDER_AVAILABLE = False


class EmbedderUnavailable(Exception):
    pass


# --------------------------------------------------------------------------
# Lesson 01 — chunk by sections (headings + overlap)
# --------------------------------------------------------------------------

def chunk_by_sections(text: str, max_words: int = 150, overlap_words: int = 20):
    """Cut text at headings; re-split too-long sections with overlap.

    TODO (lesson 01): replace with YOUR chunk_by_sections from the lesson.
    The skeleton ships a working copy so the index runs end to end.
    Returns a list of (heading, text) tuples.
    """
    sections = []
    heading, body = "(no heading)", []
    for line in text.splitlines():
        if line.startswith("#"):
            if body or sections:
                sections.append((heading, "\n".join(body).strip()))
            heading = line.lstrip("#").strip()
            body = []
        elif line.strip():
            body.append(line)
    if body or not sections:
        sections.append((heading, "\n".join(body).strip()))

    chunks = []
    for h, b in sections:
        words = b.split()
        if len(words) <= max_words:
            chunks.append((h, b))
            continue
        start = 0
        while start < len(words):
            end = start + max_words
            chunks.append((h, " ".join(words[start:end])))
            if end >= len(words):
                break
            start = end - overlap_words
    return chunks


# --------------------------------------------------------------------------
# Lesson 02 — embeddings with a fallback chain
# --------------------------------------------------------------------------

def _real_embed(text: str) -> list[float]:
    """Tier 1 — the real embedder. TODO (lesson 02): call Ollama / Jina /
    OpenAI here and return 384 numbers. The stub always fails so the chain
    below is what keeps the index alive until then."""
    raise EmbedderUnavailable("no real embedder wired yet (lesson 02 TODO)")


def _hash_embed(text: str) -> list[float]:
    """Tier 3 — hash word-count stand-in: 384 buckets, stdlib only.
    Similar text shares buckets, so cosine still ranks sensibly on keywords —
    but it is keyword-flavored, not truly semantic."""
    vec = [0.0] * DIM
    for word in text.lower().split():
        digest = hashlib.blake2b(word.encode(), digest_size=8).digest()
        vec[int.from_bytes(digest, "big") % DIM] += 1.0
    return vec


def embed(text: str) -> tuple[list[float], str]:
    """384-number embedding. Returns (vector, tier_used).

    Fallback chain (lesson 02):
      tier 1: real embedder (trained model)
      tier 2: cache (a future build reads vectors from index.json first)
      tier 3: hash stand-in — always works, marked degraded, never silent.
    """
    if EMBEDDER_AVAILABLE:
        try:
            return _real_embed(text), "tier 1: real embedder"
        except EmbedderUnavailable as exc:
            print(f"  tier 1 down ({exc}) — falling back")
    print("  tier 3: hash stand-in embedding (degraded — no trained model)")
    return _hash_embed(text), "tier 3: hash stand-in (degraded)"


# --------------------------------------------------------------------------
# Lesson 02 — cosine similarity by hand
# --------------------------------------------------------------------------

def cosine_similarity(a: list[float], b: list[float]) -> float:
    denom = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    if denom == 0.0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / denom


# --------------------------------------------------------------------------
# Build + search
# --------------------------------------------------------------------------

def build_index() -> None:
    entries = []
    for path in sorted(NOTES.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for heading, chunk in chunk_by_sections(text):
            vector, tier = embed(chunk)
            entries.append({
                "note": path.name,
                "heading": heading,
                "text": chunk,
                "vector": vector,
                "tier": tier,
            })
            print(f"  [{path.name} :: {heading}] {len(chunk.split())} words")
    INDEX_FILE.write_text(json.dumps(entries))
    print(f"\n{len(entries)} chunks -> {INDEX_FILE.name} "
          f"(384 numbers each)")


def load_index() -> list[dict]:
    if not INDEX_FILE.exists():
        build_index()
    return json.loads(INDEX_FILE.read_text())


def search(query: str, k: int = 3) -> list[dict]:
    entries = load_index()
    qvec, tier = embed(query)
    ranked = sorted(
        entries,
        key=lambda e: cosine_similarity(qvec, e["vector"]),
        reverse=True,
    )
    return [{"score": cosine_similarity(qvec, e["vector"]), **e} for e in ranked[:k]]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build_index()
    else:
        q = " ".join(sys.argv[1:]) or "giant rodent"
        print(f"query: {q!r} (embedded with the fallback chain)\n")
        for hit in search(q):
            print(f"  {hit['score']:.3f}  {hit['note']} :: {hit['heading']}")
            print(f"        {hit['text'][:80]}...")
