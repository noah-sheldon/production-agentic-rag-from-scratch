"""Build it: run a RAG-style flow over the eval set and score it with numbers.

Run:  python3 build.py

Imports the corpus + eval set from lesson 01. A fake LLM answers every
question; we score groundedness, recall, and overlap, and print the table.
Run with `--flaky` to see a model that invents facts for two questions —
the numbers will catch it before a user does.
"""
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "01-build-an-eval-set" / "code"))
from build import CORPUS, EVAL_SET  # noqa: E402

STOP = {
    "the", "a", "an", "is", "are", "was", "were", "at", "on", "in",
    "for", "to", "of", "and", "or", "it", "its", "we", "you", "they",
    "does", "do", "what", "when", "where", "how", "why", "with", "from",
}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9']+", text.lower())
    return [w for w in words if w not in STOP and len(w) > 1]


# --- retrieval: a tiny BM25 over the corpus --------------------------------

def build_index(corpus: dict) -> dict:
    doc_tokens = {note_id: tokenize(text) for note_id, text in corpus.items()}
    df = Counter()
    for toks in doc_tokens.values():
        df.update(set(toks))
    n = len(corpus)
    idf = {term: math.log((n + 1) / (df[term] + 1)) + 1 for term in df}
    return {"doc_tokens": doc_tokens, "idf": idf}


def retrieve(query: str, index: dict, k: int = 3) -> list[str]:
    qt = set(tokenize(query))
    scores = {}
    for note_id, toks in index["doc_tokens"].items():
        tf = Counter(toks)
        score = 0.0
        for term in qt:
            if term in tf:
                score += index["idf"][term] * (1 + math.log(tf[term]))
        if score > 0:
            scores[note_id] = score
    return sorted(scores, key=scores.get, reverse=True)[:k]


def context_for(note_ids: list[str]) -> str:
    return " ".join(CORPUS[i] for i in note_ids)


# --- the fake LLM -----------------------------------------------------------
# Two personalities: grounded answers ONLY from the retrieved context;
# flaky "remembers" two wrong facts and answers from memory for those
# questions — the classic hallucination failure.
TRAP_ANSWERS = {
    "backup-q": "Backups are stored on the laptop and never leave the office.",
    "gate-q": "The grade gate deletes bad answers and bans the user.",
}


class FakeLLM:
    def __init__(self, mode: str = "grounded"):
        self.mode = mode

    def generate(self, question: str, context: str, qid: str) -> str:
        if self.mode == "flaky" and qid in TRAP_ANSWERS:
            return TRAP_ANSWERS[qid]
        qt = set(tokenize(question))
        sentences = re.split(r"(?<=[.!?]) ", context)
        hits = [(sum(t in set(tokenize(s)) for t in qt), s) for s in sentences]
        hits.sort(key=lambda pair: pair[0], reverse=True)
        top = [s for n, s in hits if n > 0][:2]
        return " ".join(top) if top else "I don't know."


# --- scoring ----------------------------------------------------------------

def groundedness(answer: str, context: str) -> float:
    """Share of the answer's words that appear in the retrieved context."""
    at = tokenize(answer)
    if not at:
        return 1.0
    ct = set(tokenize(context))
    return sum(1 for t in at if t in ct) / len(at)


def recall(retrieved: list[str], relevant: list[str]) -> float:
    """Share of the notes that SHOULD be found that WERE found."""
    if not relevant:
        return 1.0
    return len(set(retrieved) & set(relevant)) / len(relevant)


def overlap(answer: str, known: str) -> float:
    """How much the answer and the known-good answer share (Jaccard)."""
    a, b = set(tokenize(answer)), set(tokenize(known))
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# --- run the eval -----------------------------------------------------------

def run_eval(mode: str) -> tuple[list[dict], dict]:
    index = build_index(CORPUS)
    llm = FakeLLM(mode)
    rows = []
    for entry in EVAL_SET:
        retrieved = retrieve(entry["question"], index, k=3)
        ctx = context_for(retrieved)
        ans = llm.generate(entry["question"], ctx, entry["id"])
        g = groundedness(ans, ctx)
        r = recall(retrieved, entry["source"])
        o = overlap(ans, entry["answer"])
        rows.append({
            "id": entry["id"], "question": entry["question"],
            "groundedness": round(g, 2), "recall": round(r, 2),
            "overlap": round(o, 2),
        })
    n = len(rows)
    avg = {
        "groundedness": round(sum(x["groundedness"] for x in rows) / n, 2),
        "recall": round(sum(x["recall"] for x in rows) / n, 2),
    }
    return rows, avg


def main() -> None:
    mode = "flaky" if "--flaky" in sys.argv else "grounded"
    rows, avg = run_eval(mode)
    print(f"mode: {mode}  ({len(rows)} eval questions)")
    print(f"{'question':14s} {'grounded':>8s} {'recall':>6s} {'overlap':>7s}")
    for x in rows:
        print(f"{x['id']:14s} {x['groundedness']:8.2f} {x['recall']:6.2f} {x['overlap']:7.2f}")
    print("-" * 40)
    print(f"{'AVERAGE':14s} {avg['groundedness']:8.2f} {avg['recall']:6.2f}")
    if mode == "flaky":
        low = [x["id"] for x in rows if x["groundedness"] < 0.5]
        print(f"answers below 0.5 groundedness (suspicious): {', '.join(low) or 'none'}")


if __name__ == "__main__":
    main()
