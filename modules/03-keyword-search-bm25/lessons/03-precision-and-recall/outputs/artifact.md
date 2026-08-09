# Artifact — precision/recall harness

Label 5 queries with known-good docs, then score any ranker at any k:

```python
def precision_recall(predicted, relevant):
    if not predicted:
        return 0.0, 0.0
    hits = sum(1 for i in predicted if i in relevant)
    return hits / len(predicted), hits / len(relevant) if relevant else 1.0
```

Rules of thumb:
- Search box (users skim top results) → optimize precision at k=5.
- RAG retriever (answer must be in the chunks) → optimize recall at k=5-10;
  a higher k that guarantees the answer beats a lower k that looks precise.
- You can't fix what you don't label — 5 queries is enough to start.
