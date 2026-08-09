# Artifact — BM25 scorer

```python
import math, re

def tokenize(text): return re.findall(r"[a-z0-9]+", text.lower())

def bm25(query, docs, k1=1.2, b=0.75):
    tokens = [tokenize(d) for d in docs]
    avgdl = sum(len(d) for d in tokens) / len(tokens)
    def idf(term):
        n = sum(1 for d in tokens if term in d)
        return math.log(1 + (len(tokens) - n + 0.5) / (n + 0.5))
    out = []
    for doc in tokens:
        score = sum(
            idf(t) * (doc.count(t) * (k1 + 1)) /
            (doc.count(t) + k1 * (1 - b + b * len(doc) / avgdl))
            for t in set(tokenize(query)) if t in doc)
        out.append((score, docs[tokens.index(doc)]))
    return sorted(out, reverse=True)
```

Defaults k1=1.2, b=0.75 — see lesson 02 for what they do.
