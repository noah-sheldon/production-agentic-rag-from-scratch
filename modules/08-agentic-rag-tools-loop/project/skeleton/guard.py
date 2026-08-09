"""Guardrail, query rewriting, and the decision log (module 08 skeleton).

Plain Python, stdlib only. Lessons 03 (guardrail + grading helpers live in
assistant.py's loop) and 04 (rewrite + transparency).
"""
import json
import re
from pathlib import Path

# --------------------------------------------------------------------------
# Guardrail — the domain is YOUR knowledge. Edit this list for your notes.
# --------------------------------------------------------------------------

DOMAIN_TOPICS = ["agents", "rag", "evals", "python", "data", "notes"]


def guard(question: str) -> dict:
    """Accept only questions that name a topic the assistant knows about."""
    q = question.lower()
    hits = [t for t in DOMAIN_TOPICS if t in q]
    if not hits:
        return {"accepted": False,
                "reason": f"out of domain — question names none of {DOMAIN_TOPICS}"}
    return {"accepted": True, "reason": "in domain"}


# --------------------------------------------------------------------------
# Query rewriting — fix the question before it searches (lesson 04)
# --------------------------------------------------------------------------

STOPWORDS = {
    "a", "an", "the", "about", "stuff", "things", "thing", "some", "any",
    "what", "is", "are", "was", "my", "me", "i", "it", "this", "that",
    "there", "of", "for", "on", "in", "to", "with", "and", "or", "please",
    "can", "you", "do", "does", "did", "have", "has", "one", "get",
    "how", "use", "using", "used", "write", "wrote", "written", "say",
    "says", "mention", "mentions", "talk", "talks",
}


def rewrite(query: str, last_topic: str = "") -> str:
    """Rewrite a bad query so it searches well. Rules, in order."""
    q = re.sub(r"[^a-z0-9 ]+", " ", query.lower()).strip()

    # 1. pointer extraction: "the one about X" means X
    m = re.search(r"\b(?:one|thing|note|post)\s+about\s+([a-z0-9 ]+)", q)
    if m:
        return m.group(1).strip()

    # 2. pronoun resolution: "it / this / that" means the last topic
    if q in {"it", "this", "that", "these", "those"} and last_topic:
        return last_topic

    # 3. stopword stripping: keep the words that carry meaning
    words = [w for w in q.split() if w not in STOPWORDS]
    return " ".join(words) if words else q


# --------------------------------------------------------------------------
# The decision log — reasoning transparency (lesson 04)
# --------------------------------------------------------------------------

class DecisionLog:
    """Every step appends one JSON line: what happened and why."""

    def __init__(self, path: str = "decision_log.jsonl") -> None:
        self.path = Path(path)
        if self.path.exists():
            self.path.unlink()

    def log(self, **event) -> None:
        line = json.dumps(event)
        self.path.open("a").write(line + "\n")
        print(f"  LOG {line}")
