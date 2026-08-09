"""Prompt building + trimming — stdlib only.

TODO (lesson 02): tune the budget and the sentence trim for YOUR notes.
Bigger budgets keep more context but cost more tokens per question.
"""
from __future__ import annotations

import math
import re

from retrieve import tokenize

STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "at", "to", "for", "and", "or",
    "is", "are", "was", "were", "do", "does", "did", "what", "how", "why",
    "where", "your", "i", "it", "you",
}


def count_tokens(text: str) -> int:
    """Rough token count (~4 chars per token). Ollama reports the real one."""
    return max(1, math.ceil(len(text) / 4))


def build_prompt(context: str, question: str) -> str:
    """Fill-in-the-blank instructions: context first, question last."""
    return (
        "You answer questions from the notes below. Use ONLY the notes.\n"
        "If the notes do not answer the question, say: I don't know.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {question}\n\n"
        "ANSWER:"
    )


def trim_context(ranked: list[tuple[str, str]], question: str, budget_tokens: int = 200) -> str:
    """Trim the retrieved notes: keep only the sentences that contain a
    question word, and stop once the budget is used up. Returns "" when no
    note answers the question — the model should then say "I don't know"."""
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
