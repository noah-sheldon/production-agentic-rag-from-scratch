#!/usr/bin/env python3
"""Module 06 — solutions to the three exercises.

Run:  python3 02_solutions.py

Implements the same specs as exercises/01_exercises.py so you can compare
your rag_flow.py / trim.py / stream.py against a reference, and verifies the
solutions pass all three checks.
"""

from __future__ import annotations

import re

# --------------------------------------------------------------------------
# EXERCISE 1 — the RAG flow (rag_flow.py)
# --------------------------------------------------------------------------


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w[:-1] if w.endswith("s") and len(w) > 3 else w for w in words]


def retrieve(question: str, docs: list[tuple[str, str]], k: int = 2) -> list[tuple[str, str]]:
    """Rank docs by how many question words each contains. Top k."""
    q_words = set(tokenize(question))
    scored = []
    for title, text in docs:
        hits = len(q_words & set(tokenize(text)))
        scored.append((hits, title, text))
    scored.sort(reverse=True)
    return [(title, text) for _, title, text in scored[:k]]


def build_prompt(context: str, question: str) -> str:
    return (
        "You answer from the notes below. Use ONLY the notes.\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {question}\n\n"
        "ANSWER:"
    )


def answer(question: str, docs: list[tuple[str, str]], model, k: int = 2) -> str:
    top = retrieve(question, docs, k=k)
    context = "\n".join(f"[{title}] {text}" for title, text in top)
    prompt = build_prompt(context, question)
    return model(prompt)


def exercise1() -> bool:
    docs = [
        ("deploy", "the deploy runs at 3am and builds the image"),
        ("vectors", "chunks become vectors in a vector store"),
        ("ollama", "ollama runs models on your own machine"),
    ]
    question = "where does the deploy run?"

    top = retrieve(question, docs, k=1)
    ok = top and top[0][0] == "deploy"
    print(f"check: retrieve ranks the matching note first -> {'PASS' if ok else 'FAIL'}")

    prompt = build_prompt("some context", question)
    ok = ok and "some context" in prompt and question in prompt
    print(f"check: build_prompt packs context and question -> {'PASS' if ok else 'FAIL'}")

    seen = {}

    def model(p: str) -> str:
        seen["prompt"] = p
        return "ok"

    reply = answer(question, docs, model)
    ok = ok and reply == "ok" and "deploy" in seen.get("prompt", "")
    print(f"check: answer runs retrieve -> prompt -> model -> {'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------
# EXERCISE 2 — prompt trimming (trim.py)
# --------------------------------------------------------------------------

import math

STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "at", "to", "for", "and", "or",
    "is", "are", "was", "were", "do", "does", "did", "what", "how", "why",
    "where", "your", "i", "it", "you",
}


def count_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def trim_context(ranked: list[tuple[str, str]], question: str, budget_tokens: int = 30) -> str:
    content = {w for w in tokenize(question) if w not in STOPWORDS}
    kept: list[str] = []
    used = 0
    for title, text in ranked:
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            if content & set(tokenize(sentence)):
                piece = f"[{title}] {sentence.strip()}"
                if used + count_tokens(piece) > budget_tokens:
                    continue
                kept.append(piece)
                used += count_tokens(piece)
    return "\n".join(kept)


def exercise2() -> bool:
    ranked = [
        ("deploy", "The deploy runs at 3am. Chunks become vectors in a store."),
        ("ollama", "Ollama runs models on your own machine."),
    ]
    ok = 1 <= count_tokens("hello world") <= 4
    print(f"check: count_tokens('hello world') in 1-4     -> {'PASS' if ok else 'FAIL'}")

    out = trim_context(ranked, "deploy", budget_tokens=30)
    ok = ok and "deploy" in out and "vectors" not in out and "Ollama" not in out
    print(f"check: matching sentence kept, unrelated dropped -> {'PASS' if ok else 'FAIL'}")
    ok = ok and count_tokens(out) <= 30
    print(f"check: trimmed prompt within budget            -> {'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------
# EXERCISE 3 — streaming / SSE (stream.py)
# --------------------------------------------------------------------------


def sse_event(data: str) -> str:
    return f"data: {data}\n\n"


def token_stream(text: str, delay: float = 0.0):
    for word in text.split():
        yield word
        time.sleep(delay)


def exercise3() -> bool:
    ok = sse_event("hello") == "data: hello\n\n"
    print(f"check: sse_event format is exact              -> {'PASS' if ok else 'FAIL'}")
    tokens = list(token_stream("a b c", delay=0.0))
    ok = ok and tokens == ["a", "b", "c"]
    print(f"check: token_stream yields tokens in order     -> {'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------

import time


def main() -> None:
    print("=" * 60)
    print("SOLUTIONS — module 06")
    print("=" * 60)
    results = {
        "exercise 1 (the RAG flow)": exercise1(),
        "exercise 2 (prompt trimming)": exercise2(),
        "exercise 3 (streaming / SSE)": exercise3(),
    }
    print()
    for name, ok in results.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    if not all(results.values()):
        raise SystemExit(1)
    print("  All three pass — module 06 exercises complete.")


if __name__ == "__main__":
    main()
