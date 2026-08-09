# Artifact — cosine by hand + the fallback chain

Paste the math into any index (stdlib only):

```python
import math

def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))

def length(v: list[float]) -> float:
    return math.sqrt(sum(x * x for x in v))

def cosine_similarity(a: list[float], b: list[float]) -> float:
    denom = length(a) * length(b)
    if denom == 0.0:
        return 0.0
    return dot(a, b) / denom

def rank_by_cosine(query: list[float], candidates: list[list[float]]) -> list[int]:
    return sorted(range(len(candidates)),
                  key=lambda i: cosine_similarity(query, candidates[i]),
                  reverse=True)
```

Fallback chain checklist — survive a dead embedder:

- [ ] Cache every embedding next to its chunk (never re-embed what you have)
- [ ] Embedder down / rate-limited → serve from cache first
- [ ] Cache empty → fall back to keyword search (module 03's BM25)
- [ ] Last resort → a smaller local model (Ollama), marked as degraded
- [ ] Log which tier answered, so the degraded path is visible, not silent
- [ ] Test the chain: kill the embedder, the index must still answer
