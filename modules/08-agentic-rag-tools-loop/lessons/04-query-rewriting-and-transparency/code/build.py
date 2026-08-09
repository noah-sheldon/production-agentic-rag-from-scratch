"""Build it: query rewriting (heuristics) + a decision log for
reasoning transparency — plain Python, keyless (stdlib only).

Run:  python3 build.py
Rewrites bad queries, then runs a mini agent (fake model) where every step
logs to decision_log.jsonl — the trace prints top to bottom.
"""
import json
import re
from pathlib import Path

STOPWORDS = {
    "a", "an", "the", "about", "stuff", "things", "thing", "some", "any",
    "what", "is", "are", "was", "my", "me", "i", "it", "this", "that",
    "there", "of", "for", "on", "in", "to", "with", "and", "or", "please",
    "can", "you", "do", "does", "did", "have", "has", "one", "get",
    "how", "use", "using", "used", "write", "wrote", "written", "say",
    "says", "mention", "mentions", "talk", "talks",
}

# --------------------------------------------------------------------------
# Query rewriting — three cheap heuristics
# --------------------------------------------------------------------------

def _extract_pointer(query: str) -> str | None:
    """'the one about evals' / 'that thing about rag' -> 'evals'."""
    m = re.search(r"\b(?:one|thing|note|post)\s+about\s+([a-z0-9 ]+)", query.lower())
    return m.group(1).strip() if m else None


def rewrite(query: str, last_topic: str = "") -> str:
    """Rewrite a bad query so it searches well. Rules, in order."""
    q = re.sub(r"[^a-z0-9 ]+", " ", query.lower()).strip()

    # 1. pointer extraction: "the one about X" means X
    pointer = _extract_pointer(q)
    if pointer:
        return pointer

    # 2. pronoun resolution: "it / this / that" means the last topic
    if q in {"it", "this", "that", "these", "those"}:
        if last_topic:
            return last_topic

    # 3. stopword stripping: keep the words that carry meaning
    words = [w for w in q.split() if w not in STOPWORDS]
    if words:
        return " ".join(words)

    # fallback: the original was all filler — keep it as-is
    return query.strip().lower()


def rewrite_report(query: str, last_topic: str = "") -> dict:
    original_chars = len(query)
    new = rewrite(query, last_topic)
    return {"original": query, "rewritten": new,
            "chars": original_chars, "chars_after": len(new),
            "saved": original_chars - len(new)}


# --------------------------------------------------------------------------
# The decision log — reasoning transparency
# --------------------------------------------------------------------------

class DecisionLog:
    def __init__(self, path: str = "decision_log.jsonl") -> None:
        self.path = Path(path)
        if self.path.exists():
            self.path.unlink()

    def log(self, **event) -> None:
        line = json.dumps(event)
        self.path.open("a").write(line + "\n")
        print(f"  LOG {line}")


# --------------------------------------------------------------------------
# Mini agent run — every step logs its reason
# --------------------------------------------------------------------------

DOMAIN = ["agents", "rag", "evals", "python", "data"]

NOTES = {
    "agents.md": "An agent is a loop plus tools. It decides, calls, checks, repeats.",
    "evals.md": "Measure answers before you ship them. Grade every retrieved document.",
    "rag.md": "Retrieve relevant chunks, then ask with the chunks in the prompt.",
    "python.md": "Use the standard library first.",
}


def mini_agent(question: str, last_topic: str, log: DecisionLog) -> str:
    # 1. guardrail
    hits = [t for t in DOMAIN if t in question.lower()]
    if not hits:
        log.log(step="guardrail", decision="reject",
                reason=f"out of domain — none of {DOMAIN} in question")
        return "Sorry, that is out of my domain."

    # 2. rewrite
    report = rewrite_report(question, last_topic)
    log.log(step="rewrite", decision=report["rewritten"],
            reason=f"heuristics applied; saved {report['saved']} chars")

    # 3. search (word overlap over file name + content)
    words = set(re.findall(r"[a-z]+", report["rewritten"]))
    ranked = sorted(
        NOTES.items(),
        key=lambda kv: len(words & set(re.findall(r"[a-z]+", f"{kv[0]} {kv[1]}"))),
        reverse=True,
    )
    log.log(step="search", decision=[f for f, _ in ranked[:2]],
            reason=f"word overlap with rewritten query {report['rewritten']!r}")

    # 4. grade the top hit (threshold 0.3, like lesson 03)
    top_file, top_text = ranked[0]
    query_words = words
    doc_words = set(re.findall(r"[a-z]+", f"{top_file} {top_text}"))
    score = len(query_words & doc_words) / max(1, len(query_words))
    verdict = "relevant" if score >= 0.3 else "irrelevant"
    log.log(step="grade", decision=verdict, reason=f"{top_file} score={score:.2f}")

    if verdict == "irrelevant":
        return "I found no relevant note for that."

    # 5. answer with a citation
    log.log(step="answer", decision=f"grounded in {top_file}", reason="grade passed")
    return f"From {top_file}: {top_text}"


# --------------------------------------------------------------------------

def main() -> None:
    print("== query rewriting ==")
    for query, topic in [
        ("agents stuff", ""),
        ("the one about evals", ""),
        ("it", "rag"),
        ("what is rag and how do i use it for evals", ""),
    ]:
        r = rewrite_report(query, topic)
        print(f"  {r['original']!r:45} -> {r['rewritten']!r:20} "
              f"({r['saved']:+d} chars)")

    print("\n== the trace: one decision log line per step ==")
    log = DecisionLog()
    answer = mini_agent("the one about evals", "rag", log)
    print(f"\n  answer: {answer}")

    print("\n== out-of-domain question — rejected, still logged ==")
    log2 = DecisionLog("decision_log_ood.jsonl")
    answer = mini_agent("best pizza in London", "", log2)
    print(f"  answer: {answer}")

    print("\n== the log file (decision_log.jsonl) ==")
    print(Path("decision_log.jsonl").read_text())


if __name__ == "__main__":
    main()
