"""Build it: guardrails (reject out-of-domain questions) + document grading
(relevant / irrelevant) in plain Python (stdlib only).

Run:  python3 build.py
Prints a battery of verdicts with scores — every number shown, nothing vibed.
"""
import re

# --------------------------------------------------------------------------
# Guardrail — the domain is your knowledge. Define it up front.
# --------------------------------------------------------------------------

DOMAIN_TOPICS = ["agents", "rag", "evals", "python", "data", "notes"]


def guard_question(question: str) -> dict:
    """Accept only questions that name a topic the assistant knows about."""
    q = question.lower()
    hits = [t for t in DOMAIN_TOPICS if t in q]
    if not hits:
        return {"accepted": False, "reason": f"out of domain — question names none of {DOMAIN_TOPICS}", "hits": []}
    return {"accepted": True, "reason": "in domain", "hits": hits}


# --------------------------------------------------------------------------
# Grading — does this document actually answer the query?
# --------------------------------------------------------------------------

GRADE_THRESHOLD = 0.3


def grade_doc(query: str, doc_text: str) -> dict:
    """Score relevance as the share of query words present in the doc."""
    query_words = set(re.findall(r"[a-z]+", query.lower()))
    doc_words = set(re.findall(r"[a-z]+", doc_text.lower()))
    if not query_words:
        return {"score": 0.0, "verdict": "irrelevant"}
    score = len(query_words & doc_words) / len(query_words)
    verdict = "relevant" if score >= GRADE_THRESHOLD else "irrelevant"
    return {"score": round(score, 3), "verdict": verdict}


# --------------------------------------------------------------------------

def main() -> None:
    print("== GUARDRAIL — is the question in domain? ==")
    for question in [
        "what did I write about agents?",
        "does the evals note mention grading?",
        "what is the best pizza in London?",
        "recommend a good film",
    ]:
        verdict = guard_question(question)
        print(f"  {question!r:45} -> accepted={verdict['accepted']}  reason={verdict['reason']}")

    print("\n== GRADING — is the retrieved document relevant? ==")
    query = "what did I write about agents and the loop?"
    docs = {
        "agents.md": "An agent is a loop plus tools. It decides what to do, calls a tool, and repeats.",
        "evals.md": "Measure answers before you ship them. Grade every retrieved document.",
        "python.md": "The word 'agents' appears here as a decoy. Real topic: standard library only.",
        "recipes.txt": "Pasta, tomatoes, basil. Nothing to do with agents at all.",
    }
    for name, text in docs.items():
        result = grade_doc(query, text)
        print(f"  {name:14} score={result['score']:<6} -> {result['verdict']}")

    print("\n== THE POINT ==")
    decoy = grade_doc(query, docs["python.md"])
    real = grade_doc(query, docs["agents.md"])
    print(f"  decoy note scores {decoy['score']} ({decoy['verdict']}) — it stays OUT of the prompt.")
    print(f"  real note scores {real['score']} ({real['verdict']}) — it goes IN. "
          f"Threshold is {GRADE_THRESHOLD}; move the dial and the answer changes.")


if __name__ == "__main__":
    main()
