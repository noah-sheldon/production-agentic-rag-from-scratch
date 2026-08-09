"""Build it: the grade gate — reject low-scoring answers, retry, or fall back.

Run:  python3 build.py

Scores every answer like lesson 02, then runs a gate: pass good answers,
retry shaky ones with more context, and fall back to an honest 'I don't
know' with citations when a retry still fails. Prints before/after numbers.
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]


def _load(code_dir: str, name: str):
    """Load a sibling lesson's build.py under a unique module name, so two
    files named build.py never collide in sys.modules."""
    path = HERE / code_dir / "code" / "build.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lesson01 = _load("01-build-an-eval-set", "lesson01_build")
lesson02 = _load("02-score-your-assistant", "lesson02_build")

CORPUS = lesson01.CORPUS
EVAL_SET = lesson01.EVAL_SET
FakeLLM = lesson02.FakeLLM
build_index = lesson02.build_index
context_for = lesson02.context_for
groundedness = lesson02.groundedness
overlap = lesson02.overlap
recall = lesson02.recall
retrieve = lesson02.retrieve
tokenize = lesson02.tokenize

THRESHOLD = 0.5  # groundedness at or above this ships


def decide(score: float, threshold: float = THRESHOLD) -> str:
    """pass: good enough to ship. retry: shaky, try once more.
    fallback: not trustworthy — refuse with citations."""
    if score >= threshold:
        return "pass"
    if score >= threshold / 2:
        return "retry"
    return "fallback"


def expand_query(question: str, note_id: str) -> str:
    """Retry searches harder: the question plus words from the best hit."""
    return question + " " + note_id.replace("-", " ")


def fallback_answer(question: str, note_ids: list[str]) -> str:
    cites = ", ".join(f"`{n}`" for n in note_ids)
    return f"I don't know — that is not in my notes. Closest notes: {cites}."


def run_with_gate(mode: str) -> tuple[list[dict], dict]:
    index = build_index(CORPUS)
    llm = FakeLLM(mode)
    rows = []
    for entry in EVAL_SET:
        qid = entry["id"]
        # --- first try ----------------------------------------------
        retrieved = retrieve(entry["question"], index, k=3)
        ctx = context_for(retrieved)
        ans = llm.generate(entry["question"], ctx, qid)
        g1 = groundedness(ans, ctx)
        decision = decide(g1)
        final = ans
        retried = False
        if decision == "retry":
            retried = True
            q2 = expand_query(entry["question"], retrieved[0] if retrieved else entry["source"][0])
            retrieved2 = retrieve(q2, index, k=5)
            ctx2 = context_for(retrieved2)
            ans2 = llm.generate(entry["question"], ctx2, qid)
            g2 = groundedness(ans2, ctx2)
            if decide(g2) == "pass":
                final, decision = ans2, "pass"
            else:
                final = fallback_answer(entry["question"], retrieved2)
                decision = "fallback"
        elif decision == "fallback":
            final = fallback_answer(entry["question"], retrieved)
        rows.append({
            "id": qid,
            "score1": round(g1, 2),
            "decision": decision,
            "retried": retried,
            "recall": round(recall(retrieved, entry["source"]), 2),
            "overlap": round(overlap(final, entry["answer"]), 2),
            "answer": final,
        })
    n = len(rows)
    passed = sum(1 for x in rows if x["decision"] == "pass")
    refused = sum(1 for x in rows if x["decision"] == "fallback")
    avg_g = sum(x["score1"] for x in rows) / n
    avg_pass_g = sum(x["score1"] for x in rows if x["decision"] == "pass")
    n_pass = max(1, passed)
    summary = {
        "mode": mode,
        "threshold": THRESHOLD,
        "avg_groundedness_before_gate": round(avg_g, 2),
        "avg_groundedness_of_shipped": round(avg_pass_g / n_pass, 2),
        "passed": passed,
        "fell_back": refused,
        "answers_sent_to_user": passed,
        "hallucinated_answers_sent": sum(
            1 for x in rows if x["decision"] == "pass" and x["score1"] < THRESHOLD
        ),
    }
    return rows, summary


def main() -> None:
    mode = "flaky" if "--flaky" in sys.argv else "grounded"
    rows, summary = run_with_gate(mode)
    print(f"mode: {mode}  |  threshold: {THRESHOLD}  |  {len(rows)} eval questions")
    print(f"{'question':13s} {'score':>5s} {'retry':>5s} {'final':>8s}")
    for x in rows:
        r = "yes" if x["retried"] else "-"
        final = x["decision"][:8]
        print(f"{x['id']:13s} {x['score1']:5.2f} {r:>5s} {final:>8s}")
        if x["decision"] != "pass":
            print(f"    -> {x['answer']}")
    print("-" * 42)
    print(f"before the gate: avg groundedness {summary['avg_groundedness_before_gate']:.2f}, "
          f"every answer sent ({len(rows)}/{len(rows)})")
    print(f"after the gate:  {summary['passed']} passed, {summary['fell_back']} honest 'I don't know' "
          f"({summary['hallucinated_answers_sent']} hallucinated answers shipped)")


if __name__ == "__main__":
    main()
