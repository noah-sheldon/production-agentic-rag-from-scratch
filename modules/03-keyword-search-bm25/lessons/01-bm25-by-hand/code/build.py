"""Build it: BM25 in plain Python (stdlib only).

Run:  python3 build.py
"""
import math
import re

DOCS = [
    "the nightly deploy runs at 3am and builds the image",
    "our CI pipeline runs tests on every pull request",
    "the database backup job runs at midnight",
    "PHQ-9 scores are stored in the patient table",
    "deploy failures usually come from missing environment variables",
]


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def idf(term: str, docs: list[list[str]]) -> float:
    n = sum(1 for d in docs if term in d)
    return math.log(1 + (len(docs) - n + 0.5) / (n + 0.5))


def bm25(query: str, docs: list[str], k1: float = 1.2, b: float = 0.75) -> list[tuple[float, str]]:
    tokens = [tokenize(d) for d in docs]
    avgdl = sum(len(d) for d in tokens) / len(tokens)
    scores = []
    for i, doc in enumerate(tokens):
        score = 0.0
        for term in set(tokenize(query)):
            tf = doc.count(term)
            if tf == 0:
                continue
            dl = len(doc)
            score += idf(term, tokens) * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avgdl))
        scores.append((round(score, 3), docs[i]))
    return sorted(scores, reverse=True)


if __name__ == "__main__":
    query = "why does the deploy run at 3am"
    print(f"query: {query!r}\n")
    for score, doc in bm25(query, DOCS):
        print(f"  {score:6.3f}  {doc}")
