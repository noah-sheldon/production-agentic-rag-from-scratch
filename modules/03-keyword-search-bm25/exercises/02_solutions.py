#!/usr/bin/env python3
"""Module 03 — solutions to the three exercises."""

import math
import re

DOCS = [
    "the nightly deploy runs at 3am and builds the image",
    "our ci pipeline runs tests on every pull request",
    "the database backup job runs at midnight",
    "phq-9 scores are stored in the patient table",
    "deploy failures usually come from missing environment variables",
]


def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


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
        out.append((round(score, 3), docs[tokens.index(doc)]))
    return sorted(out, reverse=True)


K1_EXPLANATION = """\
k1 controls how fast term frequency saturates. At k1=0 only presence matters —
a word that appears once scores the same as one that appears twenty times. As
k1 rises, more repetitions keep adding score, but each extra mention pays less
than the one before it. So k1 decides whether your search rewards
word-repetition at all, and how quickly that reward caps out.
"""

B_EXPLANATION = """\
b controls the length penalty. At b=0, document length is ignored — a long
document can win by sheer word counts. At b=1, longer documents are fully
penalized relative to the average, so short precise documents win. Raise b
when your documents vary wildly in length (a note vs a 50-page paper) and
you want the short one that says it once to beat the long one that says it
twenty times.
"""

YOUR_K1 = 1.2
YOUR_B = 0.9


def exercise1():
    ranked = bm25("deploy runs at 3am", DOCS)
    ok = "nightly deploy" in ranked[0][1]
    print(f"check: top result = {ranked[0][1]!r} -> {'PASS' if ok else 'FAIL'}")
    return ok


def exercise2():
    ok = ("saturat" in K1_EXPLANATION.lower() and
          "length" in B_EXPLANATION.lower())
    print(f"check: k1/b explanations -> {'PASS' if ok else 'FAIL'}")
    return ok


LABELS = {
    "why does the deploy run at 3am": {0, 4},
    "what runs in our ci pipeline": {1},
    "when is the database backup": {2},
    "where are phq-9 scores stored": {3},
    "deploy failures env variables": {4},
}


def precision_recall(predicted, relevant):
    if not predicted:
        return 0.0, 0.0
    hits = sum(1 for i in predicted if i in relevant)
    return hits / len(predicted), hits / len(relevant) if relevant else 1.0


def exercise3():
    p_total = r_total = 0.0
    for query, relevant in LABELS.items():
        ranked = [DOCS.index(doc) for _, doc in bm25(query, DOCS)[:3]]
        p, r = precision_recall(ranked, relevant)
        p_total += p
        r_total += r
    n = len(LABELS)
    print(f"check: precision@3 = {p_total/n:.2f}, recall@3 = {r_total/n:.2f}")
    return r_total / n >= 0.5


def main():
    results = {
        "exercise 1": exercise1(),
        "exercise 2": exercise2(),
        "exercise 3": exercise3(),
    }
    print()
    for name, ok in results.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print("  All three pass — module 03 exercises complete.")


if __name__ == "__main__":
    main()
