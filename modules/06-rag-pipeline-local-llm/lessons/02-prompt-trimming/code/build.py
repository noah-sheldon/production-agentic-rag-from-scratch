"""Build it: a fat prompt vs a trimmed prompt (stdlib only).

Run:  python3 build.py

Builds the SAME answer prompt two ways, then measures both:
  FAT      — every note stuffed into the prompt, relevant or not.
  TRIMMED  — only the top-k matching notes, only the matching sentences,
             capped at a token budget.

Then it shows WHY size matters: a small local model reads every token, so a
bigger prompt is slower AND buries the answer in noise — the model guesses
(and guesses wrong). The guess is a hallucination.

The note folder is simulated (50 notes, 45 of them filler) on purpose: with a
real folder of 100+ notes the fat prompt would be 10x bigger still.
"""
from __future__ import annotations

import math
import random
import re
import time

# --- the corpus: 45 filler notes + 5 real ones (the real ones last) ---

REAL_NOTES = [
    ("embeddings.md", "Every chunk is embedded with a local model. Each chunk becomes a vector, and the vectors live in a vector store for semantic search."),
    ("rag.md", "RAG means retrieval augmented generation. Step one: retrieve the matching notes. Step two: put them in the prompt as context. Step three: the model answers from the context only."),
    ("streaming.md", "Streaming sends the answer one piece at a time. The user sees the first words fast, instead of staring at a loading spinner."),
    ("ollama.md", "Ollama runs large language models on your own machine, fully local. No API keys, no cloud. Your notes never leave your laptop."),
    ("deploy.md", "The nightly deploy runs at 3am. It builds the Docker image and runs the database migrations. Nightly deploys fail when environment variables are missing."),
]

FILLER_WORDS = (
    "the api returns a list of items when the request succeeds each row maps "
    "to one record validation runs before the store step the job reads input "
    "files and writes output files backoff waits grow after every retry the "
    "index maps words to documents the query hits the inverted index results "
    "are sorted by score the top hits win we log every request with a trace "
    "id health checks ping each service every minute the cache key is the "
    "question the schema stores title and body tables lock during big writes "
    "timeouts are set on every connection the worker retries failed tasks "
    "the queue drains in order small batches keep memory low errors bubble "
    "up to the caller tests run on every pull request the linter checks "
    "style the formatter rewrites indentation the build caches layers the "
    "image is tagged with the commit hash env vars configure the service "
    "secrets come from the vault backups run nightly at midnight"
).split()


def filler_note(i: int) -> tuple[str, str]:
    """A fake note about generic infrastructure stuff — never about deploy."""
    words = [random.Random(i).choice(FILLER_WORDS) for _ in range(14)]
    return (f"filler-{i:02d}.md", " ".join(words).capitalize())


FILLER = [filler_note(i) for i in range(45)]
NOTES = FILLER + REAL_NOTES  # deploy.md sits at the very end — buried

# --- shared helpers (same as lesson 01) ---


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w[:-1] if w.endswith("s") and len(w) > 3 else w for w in words]


def idf(term: str, docs: list[list[str]]) -> float:
    n = sum(1 for d in docs if term in d)
    return math.log(1 + (len(docs) - n + 0.5) / (n + 0.5))


def count_tokens(text: str) -> int:
    """Rough token count: ~4 characters per token. Good enough to compare
    prompts; Ollama reports the real count (see USE IT)."""
    return max(1, math.ceil(len(text) / 4))


STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "at", "to", "for", "and", "or",
    "is", "are", "was", "were", "do", "does", "did", "what", "how", "why",
    "where", "your", "i", "it", "you",
}


def retrieve(question: str, notes: list[tuple[str, str]], k: int = 3) -> list[tuple[str, str]]:
    """Top-k notes by word overlap with the question (module 03's idea)."""
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


def build_prompt(context: str, question: str) -> str:
    return (
        "You answer questions from the notes below. Use ONLY the notes.\n"
        "If the notes do not answer the question, say: I don't know.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {question}\n\n"
        "ANSWER:"
    )


# --- the two ways to build context ---


def fat_context(notes: list[tuple[str, str]]) -> str:
    """Naive: every note, whole, in order."""
    return "\n".join(f"[{title}] {text}" for title, text in notes)


def trim_context(ranked: list[tuple[str, str]], question: str, budget_tokens: int = 120) -> str:
    """Trimmed: top-k notes, but keep only the sentences that contain a
    question word, and stop once the budget runs out."""
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


# --- the weak local model and its measured speed ---


def weak_model(prompt: str, max_context_chars: int = 300) -> str:
    """A small local model with a short attention span: it really only reads
    the first 300 characters of the context. When the answer sits beyond
    that, it guesses — and guesses wrong. That wrong guess is a hallucination."""
    context = prompt.split("CONTEXT:")[1].split("QUESTION:")[0]
    question = prompt.split("QUESTION:")[1].split("ANSWER:")[0]
    visible = context[:max_context_chars]
    content = {w for w in tokenize(question) if w not in STOPWORDS}
    best, best_hits = None, -1
    for line in visible.splitlines():
        hits = len(content & set(tokenize(line)))
        if hits > best_hits:
            best, best_hits = line, hits
    if best_hits > 0:
        return "From your notes: " + best.strip()
    return "I'm not sure. I'd guess the deploy schedule changed last week."


def timed_reply(prompt: str) -> tuple[str, float]:
    """A model reads every token before it answers. Simulate that: 1 ms of
    "thinking" per token, then produce the reply."""
    t0 = time.perf_counter()
    tokens = count_tokens(prompt)
    time.sleep(tokens * 0.001)
    reply = weak_model(prompt)
    return reply, time.perf_counter() - t0


def measure(name: str, prompt: str) -> None:
    reply, seconds = timed_reply(prompt)
    print(f"{name}")
    print(f"  prompt: {len(prompt):5d} chars = {count_tokens(prompt):4d} tokens")
    print(f"  time:   {seconds * 1000:6.1f} ms  (reads every token)")
    print(f"  answer: {reply}")
    print()


if __name__ == "__main__":
    question = "why does the deploy fail?"
    print("question:", question)
    print(f"note folder: {len(NOTES)} notes (45 filler + 5 real); deploy.md is buried at the end\n")

    fat = build_prompt(fat_context(NOTES), question)
    top = retrieve(question, NOTES, k=3)
    trimmed_context = trim_context(top, question, budget_tokens=120)
    trimmed = build_prompt(trimmed_context, question)

    print("=" * 64)
    print("FAT prompt  — every note in the folder, relevant or not")
    print("=" * 64)
    measure("  fat", fat)

    print("=" * 64)
    print("TRIMMED prompt — top-k notes, matching sentences only, budget 120 tokens")
    print("=" * 64)
    measure("  trimmed", trimmed)

    ratio = count_tokens(fat) / max(count_tokens(trimmed), 1)
    speed = len(fat) / max(len(trimmed), 1)
    print(f"trimmed is {speed:.0f}x smaller and answers ~{speed:.0f}x faster — and it got the right answer.")
    print("the fat prompt made the weak model hallucinate: it could not see deploy.md past the noise.")
