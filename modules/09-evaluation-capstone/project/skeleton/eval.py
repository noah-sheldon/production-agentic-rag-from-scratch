"""Score the assistant over the eval set; write eval_report.json.

Run:  python3 eval.py             # honest model
      python3 eval.py --mode flaky  # the liar gets caught by the gate

Every module-09 lesson comes together here: labeled questions, scoring,
and the grade gate, measured and written to a file you can commit.
"""
import json
import sys
from pathlib import Path

from assistant import Assistant, groundedness, recall
from gate import THRESHOLD


def _mode(argv: list[str]) -> str:
    if "--mode" in argv:
        i = argv.index("--mode")
        if i + 1 < len(argv) and argv[i + 1] == "flaky":
            return "flaky"
    return "grounded"


def main() -> None:
    mode = _mode(list(sys.argv[1:]))
    agent = Assistant(mode=mode)
    entries = json.loads(Path("eval_set.json").read_text())

    rows = []
    for entry in entries:
        result = agent.answer(entry["question"])
        # measured twice: what was retrieved vs what should have been
        rows.append({
            "id": entry["id"],
            "question": entry["question"],
            "groundedness": result["groundedness"],
            "recall": round(recall(result["citations"], entry["source"]), 2),
            "decision": result["decision"],
            "retried": result["retried"],
            "answer": result["answer"],
        })

    n = len(rows)
    passed = sum(1 for r in rows if r["decision"] == "pass")
    refused = sum(1 for r in rows if r["decision"] == "fallback")
    hallucinated_shipped = sum(
        1 for r in rows if r["decision"] == "pass" and r["groundedness"] < THRESHOLD
    )
    report = {
        "mode": mode,
        "threshold": THRESHOLD,
        "questions": n,
        "passed": passed,
        "honest_fallbacks": refused,
        "hallucinated_answers_shipped": hallucinated_shipped,
        "avg_groundedness": round(
            sum(r["groundedness"] for r in rows) / n, 2),
        "avg_recall": round(sum(r["recall"] for r in rows) / n, 2),
        "rows": rows,
    }
    Path("eval_report.json").write_text(
        json.dumps(report, indent=2) + "\n")

    print(f"mode: {mode}  |  threshold: {THRESHOLD}")
    print(f"{'question':13s} {'grounded':>8s} {'recall':>6s} {'decision':>8s}")
    for r in rows:
        print(f"{r['id']:13s} {r['groundedness']:8.2f} {r['recall']:6.2f} "
              f"{r['decision']:>8s}")
    print("-" * 40)
    print(f"passed: {passed}/{n}  honest fallbacks: {refused}  "
          f"hallucinated answers shipped: {hallucinated_shipped}")
    print(f"wrote eval_report.json — commit it with your results.")


if __name__ == "__main__":
    main()
