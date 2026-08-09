#!/usr/bin/env python3
"""Module 04 — solutions to the three exercises.

Each solution stands alone (python3 02_solutions.py) and mirrors the API the
exercises load: chunker.py's chunk_by_sections and cosine.py's
cosine_similarity / rank_by_cosine.
"""
import math
import random

# --------------------------------------------------------------------------
# EXERCISE 1 — the section chunker
# --------------------------------------------------------------------------


def chunk_by_sections(text: str, max_words: int = 120, overlap_words: int = 20):
    """Split at headings, re-split long sections with overlap -> (h, text)."""
    chunks = []
    heading, body = "(no heading)", []
    for line in text.splitlines():
        if line.startswith("#"):
            if body or chunks:
                chunks.append((heading, "\n".join(body).strip()))
            heading = line.lstrip("#").strip()
            body = []
        elif line.strip():
            body.append(line)
    if body or not chunks:
        chunks.append((heading, "\n".join(body).strip()))
    # re-split any section longer than max_words, carrying the tail over
    out = []
    for h, b in chunks:
        words = b.split()
        if len(words) <= max_words:
            out.append((h, b))
            continue
        start = 0
        while start < len(words):
            end = start + max_words
            out.append((h, " ".join(words[start:end])))
            if end >= len(words):
                break
            start = end - overlap_words
    return out


def exercise1() -> bool:
    sample = """# Setup
Install Python and make a venv.

## Notes Folder
Put markdown notes in this folder, one idea per file, and keep the headings honest.

# Daily Log
First entry: planned the semantic index. Second entry: built the chunker. Third entry: tested the embedder. Fourth entry: searched by meaning. Fifth entry: measured the results. Sixth entry: wrote it down. Seventh entry: cleaned the index. Eighth entry: ran it again."""
    chunks = chunk_by_sections(sample, max_words=12, overlap_words=4)
    headings = [h.lower() for h, _ in chunks]
    ok_head = all(any(h in hh for hh in headings) for h in ("setup", "notes folder", "daily log"))
    # heading words live in the tuple's heading part; body words must survive
    body_lines = [l for l in sample.splitlines()
                  if l.strip() and not l.lstrip().startswith("#")]
    doc_words = " ".join(body_lines).lower().split()
    joined = " ".join(t for _, t in chunks).lower().split()
    ok_loss = all(w in joined for w in doc_words)
    shared = max((len(set(chunks[i - 1][1].split()) & set(chunks[i][1].split()))
                  for i in range(1, len(chunks))), default=0)
    ok_overlap = shared >= 1
    print(f"check: chunker -> {len(chunks)} chunks, headings "
          f"{'PASS' if ok_head else 'FAIL'}, no loss "
          f"{'PASS' if ok_loss else 'FAIL'}, overlap {shared} "
          f"{'PASS' if ok_overlap else 'FAIL'}")
    return ok_head and ok_loss and ok_overlap


# --------------------------------------------------------------------------
# EXERCISE 2 — cosine similarity by hand
# --------------------------------------------------------------------------

DIM = 384


def cosine_similarity(a: list[float], b: list[float]) -> float:
    denom = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    if denom == 0.0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / denom


def rank_by_cosine(query: list[float], candidates: list[list[float]]) -> list[int]:
    return sorted(range(len(candidates)),
                  key=lambda i: cosine_similarity(query, candidates[i]),
                  reverse=True)


def exercise2() -> bool:
    def make_vector(seed: int) -> list[float]:
        rng = random.Random(seed)
        return [rng.uniform(-1.0, 1.0) for _ in range(DIM)]

    v = make_vector(1)
    w = make_vector(2)
    self_score = cosine_similarity(v, v)
    ok_self = abs(self_score - 1.0) < 0.01
    other = cosine_similarity(v, w)
    ok_other = other < 0.2
    candidates = [v] + [make_vector(s) for s in (10, 11, 12, 13)]
    order = rank_by_cosine(v, candidates)
    ok_rank = order[0] == 0
    print(f"check: cosine self {self_score:.3f} {'PASS' if ok_self else 'FAIL'}, "
          f"unrelated {other:.3f} {'PASS' if ok_other else 'FAIL'}, "
          f"rank-first {order[0]} {'PASS' if ok_rank else 'FAIL'}")
    return ok_self and ok_other and ok_rank


# --------------------------------------------------------------------------
# EXERCISE 3 — chunk size matters
# --------------------------------------------------------------------------


def fixed_chunks(text: str, size_words: int) -> list[str]:
    words = text.split()
    return [" ".join(words[i:i + size_words]) for i in range(0, len(words), size_words)]


SIZE_NOTES = """\
At 30 words the answer sentence is cut in half by a chunk boundary, so the
context is lost and neither piece answers the question. At 300 words the same
answer sits whole inside a wall of 300 words, buried in noise, so the
embedding matches everything a little and nothing well. At 100 words the
answer is whole and the chunk stays small enough to stay precise — that is
the balanced size, and the right one is chosen by measuring, not guessing.
"""


def exercise3() -> bool:
    ok = "noise" in SIZE_NOTES.lower() and "context" in SIZE_NOTES.lower()
    print(f"check: SIZE_NOTES covers too-big (noise) + too-small (context) -> "
          f"{'PASS' if ok else 'FAIL'}")
    return ok


def main() -> None:
    results = {
        "exercise 1": exercise1(),
        "exercise 2": exercise2(),
        "exercise 3": exercise3(),
    }
    print()
    for name, ok in results.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    if all(results.values()):
        print("  All three pass — module 04 exercises complete.")
    else:
        print("  Fix the failures above — then re-run.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
