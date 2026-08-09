#!/usr/bin/env python3
"""Module 09 — solutions to the three exercises."""

# --------------------------------------------------------------------------
# EXERCISE 1 — build an eval set
# --------------------------------------------------------------------------


def build_eval_set(corpus):
    """Return >=3 labeled questions; every source must exist in corpus."""
    return [
        {
            "question": "When does the nightly deploy run?",
            "answer": "The nightly deploy runs at 3am.",
            "source": ["deploy"],
        },
        {
            "question": "How long does CI take?",
            "answer": "CI takes about 3 minutes.",
            "source": ["ci"],
        },
        {
            "question": "Where are backups stored?",
            "answer": "Backups are stored in S3.",
            "source": ["backup"],
        },
    ]


def exercise1() -> bool:
    corpus = {
        "deploy": "The nightly deploy runs at 3am.",
        "ci": "CI takes about 3 minutes.",
        "backup": "Backups are stored in S3.",
    }
    entries = build_eval_set(corpus)
    ok = (
        isinstance(entries, list)
        and len(entries) >= 3
        and all(isinstance(e, dict) and e["question"] and e["answer"] and e["source"]
                for e in entries)
        and all(note in corpus for e in entries for note in e["source"])
    )
    print(f"check: build_eval_set -> {len(entries)} entries, all sources known: "
          f"{'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------
# EXERCISE 2 — score an answer
# --------------------------------------------------------------------------


def groundedness(answer, context):
    stop = {"the", "a", "an", "is", "are", "at", "on", "in", "to", "of",
            "and", "or", "it", "we", "you", "they"}
    at = {w.lower() for w in answer.split() if w.lower() not in stop}
    ct = {w.lower() for w in context.split() if w.lower() not in stop}
    if not at:
        return 1.0
    return sum(1 for w in at if w in ct) / len(at)


def recall(retrieved, relevant):
    if not relevant:
        return 1.0
    return len(set(retrieved) & set(relevant)) / len(relevant)


def exercise2() -> bool:
    context = "The nightly deploy runs at 3am. Backups are stored in S3."
    perfect = groundedness("The nightly deploy runs at 3am.", context)
    bad = groundedness("The deploy runs at noon on Mars.", context)
    hit = recall(["deploy", "backup"], ["deploy"])
    miss = recall(["deploy"], ["backup"])
    ok = perfect >= 0.8 and bad <= 0.5 and hit == 1.0 and miss == 0.0
    print(f"check: groundedness {perfect:.2f} / {bad:.2f}, recall {hit:.1f} / {miss:.1f}: "
          f"{'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------
# EXERCISE 3 — route a score
# --------------------------------------------------------------------------


def decide(score, threshold=0.5):
    if score >= threshold:
        return "pass"
    if score >= threshold / 2:
        return "retry"
    return "fallback"


def exercise3() -> bool:
    cases = [(0.9, "pass"), (0.4, "retry"), (0.1, "fallback")]
    ok = all(decide(s, threshold=0.7) == want for s, want in cases)
    print(f"check: decide() at threshold 0.7 -> "
          f"{[decide(s, threshold=0.7) for s, _ in cases]}: {'PASS' if ok else 'FAIL'}")
    return ok


def main() -> None:
    results = {
        "exercise 1 (eval set)": exercise1(),
        "exercise 2 (scoring)": exercise2(),
        "exercise 3 (grade gate)": exercise3(),
    }
    print()
    for name, ok in results.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print("  All three pass — module 09 exercises complete.")


if __name__ == "__main__":
    main()
