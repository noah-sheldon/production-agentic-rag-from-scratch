"""Build it: precision and recall as k changes (stdlib only).

Run:  python3 build.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "01-bm25-by-hand" / "code"))
from build import DOCS, bm25

# Labeled set: for each query, the docs that are RELEVANT.
LABELS = {
    "why does the deploy run at 3am": {0, 4},   # deploy docs
    "what runs in our ci pipeline": {1},
    "when is the database backup": {2},
    "where are phq-9 scores stored": {3},
    "deploy failures env variables": {4},
}


def precision_recall(predicted: list[int], relevant: set[int]) -> tuple[float, float]:
    if not predicted:
        return 0.0, 0.0
    hits = sum(1 for i in predicted if i in relevant)
    p = hits / len(predicted)
    r = hits / len(relevant) if relevant else 1.0
    return round(p, 2), round(r, 2)


if __name__ == "__main__":
    for k in (1, 3, 5):
        total_p = total_r = 0.0
        for query, relevant in LABELS.items():
            ranked = [DOCS.index(doc) for _, doc in bm25(query, DOCS)[:k]]
            p, r = precision_recall(ranked, relevant)
            total_p += p
            total_r += r
        n = len(LABELS)
        print(f"k={k}: precision {total_p/n:.2f}  recall {total_r/n:.2f}")
