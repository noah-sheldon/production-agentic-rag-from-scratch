# Artifact — the RRF fuse

```python
def rrf(ranked_lists, k=60):
    """Fuse ranked lists (each = docs best-first) into one order.
    Points = 1/(k + rank), summed per document. Rank by points."""
    points = {}
    for ranked in ranked_lists:
        for rank, doc in enumerate(ranked, start=1):
            points[doc] = points.get(doc, 0.0) + 1.0 / (k + rank)
    return sorted(points.items(), key=lambda kv: kv[1], reverse=True)
```

Recipe:

- Each list is your engine's output, best document first. Nothing else.
- `k = 60` — softens the top-rank bonus. Lower `k` (20) makes rank
  differences louder; higher (100) flattens them.
- A document in only one list still scores — it just gets fewer votes.
- When scores tie, the document seen first wins — the tie means "both
  engines half-agree", which is a good sign, not a bug.
- Never normalize scores and average them instead: different engines live
  on different scales (module lesson 01's scale trap).
