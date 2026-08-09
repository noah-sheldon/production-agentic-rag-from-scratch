"""Build it: your first eval set — labeled questions with known-good answers.

Run:  python3 build.py

Writes eval_set.json next to where you run it. The eval set is the ruler you
will measure the assistant with in lessons 02 and 03. Six notes stand in for
YOUR notes; your own set will hold real questions about your own data.
"""
import json
from pathlib import Path

# The notes corpus — six notes about a small team project. In your own
# assistant these are YOUR notes; here they stand in for them.
CORPUS = {
    "deploy": (
        "The nightly deploy runs at 3am. It builds the image, runs "
        "migrations, then restarts the server. Deploy failures usually "
        "come from missing environment variables."
    ),
    "ci": (
        "The CI pipeline runs tests on every pull request. Tests take "
        "about 3 minutes. A failing test blocks the pull request from "
        "merging."
    ),
    "backup": (
        "The database backup runs at midnight. Backups are kept for 30 "
        "days and stored in S3. Restoring from backup takes about an hour."
    ),
    "evals": (
        "The eval set has 20 questions. Every question has a known-good "
        "answer and a source note id. We score groundedness and recall."
    ),
    "agent-loop": (
        "The agent loop repeats three steps: decide which tool to call, "
        "call it, and check the result. The loop stops when the question "
        "is answered."
    ),
    "grade-gate": (
        "The grade gate scores every answer. A low score triggers a retry "
        "with more context. If the retry fails, the assistant says 'I "
        "don't know' and shows citations."
    ),
}

# The eval set. Each question carries:
#   question  — what a user would ask
#   answer    — the known-good answer (the ground truth)
#   source    — the note id(s) the facts live in
#   facts     — the atomic facts the answer must contain
EVAL_SET = [
    {
        "id": "deploy-q",
        "question": "When does the nightly deploy run?",
        "answer": "The nightly deploy runs at 3am.",
        "source": ["deploy"],
        "facts": ["runs at 3am"],
    },
    {
        "id": "ci-q",
        "question": "How long does CI take?",
        "answer": "CI takes about 3 minutes.",
        "source": ["ci"],
        "facts": ["3 minutes"],
    },
    {
        "id": "backup-q",
        "question": "Where are backups stored?",
        "answer": "Backups are stored in S3.",
        "source": ["backup"],
        "facts": ["S3"],
    },
    {
        "id": "evals-q",
        "question": "What is in the eval set?",
        "answer": "The eval set has 20 questions, each with a known-good "
                  "answer and a source note id.",
        "source": ["evals"],
        "facts": ["20 questions", "known-good answer", "source note id"],
    },
    {
        "id": "agent-loop-q",
        "question": "What are the steps of the agent loop?",
        "answer": "Decide which tool to call, call it, and check the result.",
        "source": ["agent-loop"],
        "facts": ["decide", "call", "check"],
    },
    {
        "id": "gate-q",
        "question": "What happens when the grade gate sees a low score?",
        "answer": "A low score triggers a retry. If the retry fails, the "
                  "assistant says 'I don't know' and shows citations.",
        "source": ["grade-gate"],
        "facts": ["retry", "I don't know", "citations"],
    },
]


def validate(eval_set: list[dict]) -> list[str]:
    """Check the eval set is well-formed. Returns a list of problems."""
    problems: list[str] = []
    ids = [e["id"] for e in eval_set]
    if len(set(ids)) != len(ids):
        problems.append("duplicate question ids")
    for entry in eval_set:
        if not entry["question"].strip():
            problems.append(f"{entry['id']}: empty question")
        if not entry["answer"].strip():
            problems.append(f"{entry['id']}: empty answer")
        if not entry["source"]:
            problems.append(f"{entry['id']}: no source note")
        for src in entry["source"]:
            if src not in CORPUS:
                problems.append(f"{entry['id']}: unknown source {src!r}")
    return problems


def main() -> None:
    problems = validate(EVAL_SET)
    if problems:
        print("eval set has problems:")
        for p in problems:
            print(f"  - {p}")
        raise SystemExit(1)
    out = Path("eval_set.json")
    out.write_text(json.dumps(EVAL_SET, indent=2) + "\n")
    print(f"wrote {out} — {len(EVAL_SET)} questions, each with a known-good answer and a source.")
    for entry in EVAL_SET:
        src = ",".join(entry["source"])
        print(f"  {entry['id']:13s} [{src}]  {entry['question']}")
    print("validation: no problems found — the ruler is ready.")


if __name__ == "__main__":
    main()
