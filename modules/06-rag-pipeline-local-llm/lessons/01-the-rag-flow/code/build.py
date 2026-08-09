"""Build it: the RAG flow in plain Python (stdlib only, no API keys).

Run:  python3 build.py

Three steps, in order:
  1. RETRIEVE  — find the notes that match the question (keyword scoring).
  2. PROMPT    — pack the found notes + the question into one instruction.
  3. ANSWER    — the model reads the prompt and answers from the notes only.

The "model" here is FAKE: a stand-in that reads the prompt and answers from
the context. It shows the shape of the flow without any API key. Swap it for
a real local model (Ollama) in the USE IT beat of docs/en.md.
"""
from __future__ import annotations

import math
import re
import time

# --- the notes (the same little corpus the project will grow) ---
NOTES = [
    ("embeddings.md", "Every chunk is embedded with a local model. Each chunk becomes a vector, and the vectors live in a vector store for semantic search."),
    ("rag.md", "RAG means retrieval augmented generation. Step one: retrieve the matching notes. Step two: put them in the prompt as context. Step three: the model answers from the context only."),
    ("streaming.md", "Streaming sends the answer one piece at a time. The user sees the first words fast, instead of staring at a loading spinner."),
    ("ollama.md", "Ollama runs large language models on your own machine, fully local. No API keys, no cloud. Your notes never leave your laptop."),
    ("deploy.md", "The nightly deploy runs at 3am. It builds the Docker image and runs the database migrations. Nightly deploys fail when environment variables are missing."),
]

# --- helpers shared by every step ---


def tokenize(text: str) -> list[str]:
    """Split text into lowercase word pieces. A tiny stemmer turns "runs"
    into "run" and "models" into "model" so the search matches better."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w[:-1] if w.endswith("s") and len(w) > 3 else w for w in words]


def idf(term: str, docs: list[list[str]]) -> float:
    """How rare is this word across the notes? Rare words matter more."""
    n = sum(1 for d in docs if term in d)
    return math.log(1 + (len(docs) - n + 0.5) / (n + 0.5))


# --- step 1: RETRIEVE ---


def retrieve(question: str, notes: list[tuple[str, str]], k: int = 2) -> list[tuple[str, str]]:
    """Rank the notes by word overlap with the question, return the top k.
    This is the same idea as the BM25 you built in module 03."""
    tokens = [tokenize(text) for _, text in notes]
    avgdl = sum(len(t) for t in tokens) / max(len(tokens), 1)
    scored = []
    for i, (title, text) in enumerate(notes):
        score = 0.0
        for term in set(tokenize(question)):
            tf = tokens[i].count(term)
            if tf:
                dl = len(tokens[i])
                score += idf(term, tokens) * (tf * 2.2) / (tf + 1.2 * (0.25 + 0.75 * dl / avgdl))
        scored.append((score, title, text))
    scored.sort(reverse=True)
    return [(title, text) for _, title, text in scored[:k]]


# --- step 2: PROMPT ---


def build_prompt(context: str, question: str) -> str:
    """Fill-in-the-blank instructions: context first, question last."""
    return (
        "You answer questions from the notes below. Use ONLY the notes.\n"
        "If the notes do not answer the question, say: I don't know.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {question}\n\n"
        "ANSWER:"
    )


# --- step 3: ANSWER with a FAKE model ---

STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "at", "to", "for", "and", "or",
    "is", "are", "was", "were", "do", "does", "did", "what", "how", "why",
    "where", "your", "i", "it", "you",
}


def fake_model(prompt: str) -> str:
    """Stand-in for a local LLM. Reads the prompt, answers from the context.

    Honest rules it follows (a real model should follow too):
      - no context  ->  "I don't know"
      - no matching line -> "I won't guess" (no hallucination)
    Swap me for a real Ollama call — see the USE IT beat in docs/en.md.
    """
    if "CONTEXT:" not in prompt or "QUESTION:" not in prompt:
        return "I don't know."
    context = prompt.split("CONTEXT:")[1].split("QUESTION:")[0]
    question = prompt.split("QUESTION:")[1].split("ANSWER:")[0]
    if not context.strip():
        return "I don't know — no notes matched."
    content = {w for w in tokenize(question) if w not in STOPWORDS}
    best, best_hits = None, -1
    for line in context.splitlines():
        hits = len(content & set(tokenize(line)))
        if hits > best_hits:
            best, best_hits = line, hits
    if best_hits > 0:
        return "From your notes: " + best.strip()
    return "I can see notes, but none of them answer this. I won't guess."


# --- the whole flow, measured ---


def answer(question: str, k: int = 2) -> None:
    t0 = time.perf_counter()
    top = retrieve(question, NOTES, k=k)
    t1 = time.perf_counter()
    context = "\n".join(f"[{title}] {text}" for title, text in top)
    prompt = build_prompt(context, question)
    t2 = time.perf_counter()
    reply = fake_model(prompt)
    t3 = time.perf_counter()

    print(f"question: {question}")
    print(f"  retrieved {len(top)} of {len(NOTES)} notes: {', '.join(t for t, _ in top)}")
    print(f"  prompt size: {len(prompt)} chars, ~{len(prompt) // 4} tokens")
    print(f"  retrieve {(t1 - t0) * 1000:5.1f} ms | prompt {(t2 - t1) * 1000:5.1f} ms | answer {(t3 - t2) * 1000:5.1f} ms")
    print(f"  answer: {reply}\n")


if __name__ == "__main__":
    print("== the RAG flow: retrieve -> prompt -> answer ==")
    print("   (the model is a FAKE stand-in — no API keys, no network)\n")
    answer("how do I run a local model?")
    answer("what does the deploy do at 3am?")
    answer("what is the capital of mars?")  # in no note -> grounded refusal
