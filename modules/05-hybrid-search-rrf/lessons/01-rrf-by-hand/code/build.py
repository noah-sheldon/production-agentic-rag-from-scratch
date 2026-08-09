"""Build it: Reciprocal Rank Fusion (RRF) in plain Python (stdlib only).

Run:  python3 build.py

Fuses two ranked lists — one from keyword search, one from semantic
search — into one merged list. Then shows WHY rank-based fusion beats
score averaging when the two engines score on different scales.
"""

# Two engines ranked the same five notes for the query "why does my
# database hang?". These are placeholder lists — swap in your own
# Module 03 BM25 list and Module 04 embedding list later.
# NOTE the scales: keyword scores ~0-10, semantic scores ~0-1.
KEYWORD_RANKED = [
    ("postgres timeout happens when the connection pool is full", 9.8),
    ("python requests library timeout config", 7.4),
    ("the api client hangs when the server is slow to answer", 4.1),
    ("the database stalls when too many sessions ask at once", 1.1),
    ("kubernetes pod restart loop", 0.2),
]

SEMANTIC_RANKED = [
    ("the database stalls when too many sessions ask at once", 0.94),
    ("the api client hangs when the server is slow to answer", 0.91),
    ("postgres timeout happens when the connection pool is full", 0.85),
    ("python requests library timeout config", 0.62),
    ("kubernetes pod restart loop", 0.55),
]


def rrf(ranked_lists: list[list], k: int = 60) -> list[tuple[str, float]]:
    """Reciprocal Rank Fusion.

    A document gets 1/(k + rank) points from each list it appears in.
    Points from all lists are summed. Rank documents by total points.

    rank is 1-based: the top document of a list has rank 1.
    k softens the bonus for the very top — 60 is the usual choice.
    """
    points: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, (doc, _score) in enumerate(ranked, start=1):
            points[doc] = points.get(doc, 0.0) + 1.0 / (k + rank)
    return sorted(points.items(), key=lambda kv: kv[1], reverse=True)


def average_scores(scored_lists: list[list[tuple[str, float]]]) -> list[tuple[float, str]]:
    """Naive fusion: average the raw scores across lists.

    This ignores that the lists are on different scales — the engine
    with the bigger numbers silently wins.
    """
    totals: dict[str, float] = {}
    counts: dict[str, int] = {}
    for scored in scored_lists:
        for doc, score in scored:
            totals[doc] = totals.get(doc, 0.0) + score
            counts[doc] = counts.get(doc, 0) + 1
    return sorted(((totals[d] / counts[d], d) for d in totals), reverse=True)


def show(title: str, rows: list) -> None:
    print(f"{title}")
    for i, row in enumerate(rows, start=1):
        if len(row) == 2 and isinstance(row[1], str):
            doc, val = row[1], row[0]
            print(f"  {i:2d}.  {val:7.4f}  {doc}")
        else:
            doc, val = row
            print(f"  {i:2d}.  {val:7.4f}  {doc}")
    print()


if __name__ == "__main__":
    print("Two engines ranked the same five notes for:")
    print('  query: "why does my database hang?"')
    print()

    show("keyword engine (scores ~0-10):", [(d, s) for d, s in KEYWORD_RANKED])
    show("semantic engine (scores ~0-1):", [(d, s) for d, s in SEMANTIC_RANKED])

    print("=" * 64)
    print("FUSION 1 — score averaging (the naive way)")
    print("=" * 64)
    print("average the raw scores. The keyword numbers are ~10x bigger,")
    print("so they swallow the semantic list. One engine decides for both.")
    print()
    averaged = average_scores([KEYWORD_RANKED, SEMANTIC_RANKED])
    show("averaged order:", averaged)

    print("=" * 64)
    print("FUSION 2 — RRF (rank-based)")
    print("=" * 64)
    print("points = 1/(k + rank) per list. Position, not score.")
    print("Both engines get an equal vote.")
    print()
    fused = rrf([KEYWORD_RANKED, SEMANTIC_RANKED])
    show("RRF merged order:", fused)

    print("=" * 64)
    print("THE SCALE TRAP, in miniature")
    print("=" * 64)
    print("Three notes, query: 'database slow'")
    print("  A: 'postgres timeout config'          keyword 9.9   semantic 0.02")
    print("  B: 'the database stalls at noon'      keyword 1.2   semantic 0.90")
    print("  C: 'the api client waits'             keyword 0.5   semantic 0.80")
    print()
    mini_kw = [
        ("A: postgres timeout config", 9.9),
        ("B: the database stalls at noon", 1.2),
        ("C: the api client waits", 0.5),
    ]
    mini_sem = [
        ("B: the database stalls at noon", 0.90),
        ("C: the api client waits", 0.80),
        ("A: postgres timeout config", 0.02),
    ]
    show("averaging (scale-hijacked):", average_scores([mini_kw, mini_sem]))
    show("RRF (fair vote):", rrf([mini_kw, mini_sem]))

    print("Read the two mini rows: averaging crowns A because keyword's")
    print("9.9 dwarfs semantic's 0.02 — one engine's scale decides for")
    print("both. RRF asks 'what did each ENGINE think?' A is #1 for")
    print("keyword but LAST for semantic. B is #2 for keyword and #1 for")
    print("semantic — both engines half-agree on B, so RRF crowns B.")
