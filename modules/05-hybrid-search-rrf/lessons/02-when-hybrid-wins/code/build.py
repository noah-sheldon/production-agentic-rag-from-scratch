"""Build it: when does hybrid win? keyword + semantic + RRF in plain Python.

Run:  python3 build.py

Three engines, one corpus of notes:
  - keyword:   tf x idf scoring (Module 03 style)
  - semantic:  cosine over random-vector embeddings (a STAND-IN for a
               real embedding model — it only senses token overlap and
               doc length; it has no real meaning knowledge)
  - hybrid:    RRF fusion of the two ranked lists (lesson 01)

Then the code MINES the corpus: for each query it prints how each mode
scores, and which mode wins at the top. Look at the three experiments —
one query where keyword wins alone, one where semantic wins alone, one
where fusion finds both notes.
"""
import hashlib
import math
import random
import re

DIM = 64  # vector size for the random-vector stand-in

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "when", "why", "my",
    "how", "do", "does", "i", "to", "and", "at", "under", "too", "for",
    "of", "it", "with", "on", "in", "as", "you", "your", "that", "this",
}


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


# --- the corpus ----------------------------------------------------------
# Eight notes. Each has a job in the story:
#   A  the long, rich note (keyword likes it best)
#   B  the short config snippet (semantic likes it best)
#   C  a second config note
#   D, E  unrelated notes
#   W  the kitchen-sink note: mentions many words, answers nothing
#   H  the tag note: one word ("timeout")
#   Z  a note titled with the exact query words
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

# --- keyword engine -------------------------------------------------------

def keyword_rank(notes: dict[str, str], query: str) -> list[tuple[str, float]]:
    """Score each note by tf x idf over the query tokens. Best first."""
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


# --- semantic engine (random-vector stand-in) -----------------------------

def token_vector(token: str) -> list[float]:
    """A fixed random vector per word. Same word -> same vector, always."""
    seed = int.from_bytes(hashlib.sha256(token.encode()).digest()[:8], "big")
    rng = random.Random(seed)
    v = [rng.gauss(0.0, 1.0) for _ in range(DIM)]
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def doc_vector(tokens: list[str]) -> list[float]:
    """Mean of the word vectors, then normalized (a stand-in embedding)."""
    if not tokens:
        return [0.0] * DIM
    vs = [token_vector(t) for t in tokens]
    mean = [sum(v[i] for v in vs) / len(vs) for i in range(DIM)]
    n = math.sqrt(sum(x * x for x in mean)) or 1.0
    return [x / n for x in mean]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def semantic_rank(notes: dict[str, str], query: str) -> list[tuple[str, float]]:
    """Rank by cosine between the query vector and each note vector."""
    qv = doc_vector(tokenize(query))
    names = list(notes)
    scored = []
    for name in names:
        dv = doc_vector(tokenize(notes[name]))
        scored.append((name, round(cosine(qv, dv), 4)))
    return sorted(scored, key=lambda kv: (-kv[1], names.index(kv[0])))


# --- hybrid engine (RRF) ---------------------------------------------------

def rrf_rank(keyword: list[tuple[str, float]], semantic: list[tuple[str, float]],
             k: int = 60) -> list[tuple[str, float]]:
    """Fuse two ranked lists by position, not score (lesson 01)."""
    points: dict[str, float] = {}
    for ranked in (keyword, semantic):
        for rank, (name, _s) in enumerate(ranked, start=1):
            points[name] = points.get(name, 0.0) + 1.0 / (k + rank)
    order = list(points)
    return sorted(points.items(), key=lambda kv: (-kv[1], order.index(kv[0])))


# --- measurement ------------------------------------------------------------

def recall(predicted: list[str], relevant: set[str]) -> float:
    hits = sum(1 for p in predicted if p in relevant)
    return hits / len(relevant) if relevant else 0.0


def report(query: str, relevant: set[str], topk: int = 2) -> dict[str, float]:
    kw = keyword_rank(NOTES, query)
    sem = semantic_rank(NOTES, query)
    hy = rrf_rank(kw, sem)
    kw_names = [n for n, _ in kw]
    sem_names = [n for n, _ in sem]
    hy_names = [n for n, _ in hy]
    return {
        "kw@1": recall(kw_names[:1], relevant),
        "kw@2": recall(kw_names[:topk], relevant),
        "sem@1": recall(sem_names[:1], relevant),
        "sem@2": recall(sem_names[:topk], relevant),
        "hy@1": recall(hy_names[:1], relevant),
        "hy@2": recall(hy_names[:topk], relevant),
    }


def show_ranks(title: str, ranked: list[tuple[str, float]]) -> None:
    print(f"  {title}")
    for i, (name, score) in enumerate(ranked, start=1):
        print(f"    {i:2d}.  {score:8.4f}  {name}  {NOTES[name]}")
    print()


# --- experiments -------------------------------------------------------------

EXPERIMENTS = [
    ("postgres config", {"B", "Z"},
     "semantic wins alone: the kitchen-sink note W (postgres + config, "
     "twice) takes keyword's top spot. Semantic's top two are Z — its "
     "two words ARE the query — and the snippet B."),
    ("postgres timeout", {"A", "B"},
     "fusion finds BOTH notes: semantic's #2 is the one-word tag note H, "
     "not the second answer. RRF rescues A — A is keyword #1 and semantic "
     "#5 (0.0320 points), H is semantic #2 but keyword #6 (0.0313). Two "
     "moderate votes beat one loud vote."),
    ("timeout", {"A", "B"},
     "keyword wins alone: the tag note H scores a PERFECT 1.0 — its vector "
     "IS the query vector — and fools the stand-in semantic. Keyword ranks "
     "the real notes first."),
]


def run_experiment(query: str, relevant: set[str], note: str) -> None:
    print("=" * 70)
    print(f"QUERY: {query!r}     relevant = {sorted(relevant)}")
    print(note)
    print()
    kw = keyword_rank(NOTES, query)
    sem = semantic_rank(NOTES, query)
    hy = rrf_rank(kw, sem)
    show_ranks("keyword (tf x idf):", kw)
    show_ranks("semantic (stand-in):", sem)
    show_ranks("hybrid (RRF):", hy)
    m = report(query, relevant)
    print(f"  recall@1:  keyword {m['kw@1']:.1f} | semantic {m['sem@1']:.1f} | hybrid {m['hy@1']:.1f}")
    print(f"  recall@2:  keyword {m['kw@2']:.1f} | semantic {m['sem@2']:.1f} | hybrid {m['hy@2']:.1f}")
    print()


if __name__ == "__main__":
    print("Corpus of notes (name: text)")
    for name, text in NOTES.items():
        print(f"  {name}: {text}")
    print()
    for query, relevant, note in EXPERIMENTS:
        run_experiment(query, relevant, note)

    print("=" * 70)
    print("MINING TABLE — every query in the demo, all three modes")
    print("=" * 70)
    print(f"{'query':<28} {'relevant':<14} {'kw@1':>5} {'sem@1':>6} {'hy@1':>5} {'winner'}")
    for query, relevant, _note in EXPERIMENTS:
        m = report(query, relevant)
        best2 = max(m["kw@2"], m["sem@2"], m["hy@2"])
        if m["hy@2"] == best2 and best2 > 0:
            winner = "hybrid"
        elif m["sem@2"] == best2:
            winner = "semantic"
        else:
            winner = "keyword"
        print(f"{query:<28} {sorted(relevant)!s:<14} {m['kw@1']:5.1f} {m['sem@1']:6.1f} {m['hy@1']:5.1f} {winner}")
    print()
    print("winner = the mode with the best recall@2 (ties go to hybrid).")
    print()
    print("Lesson: with a stand-in semantic engine, keyword and semantic")
    print("mostly AGREE (both sense token overlap). Real embeddings know")
    print("meaning, so they disagree much more — on paraphrases. The three")
    print("experiments show the machinery of disagreement + fusion, and")
    print("the mining table is how you measure which mode wins per query.")
