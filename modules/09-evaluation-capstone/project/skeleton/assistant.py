"""The capstone assistant: tool registry + agent loop + fake LLM + grade gate.

Run:  python3 assistant.py "when does the nightly deploy run"
Or:   python3 assistant.py --mode flaky "where are backups stored"
"""
import re
import sys

import retrieval
from gate import decide, fallback_answer, THRESHOLD

# --------------------------------------------------------------------------
# The fake LLM — swap this class for your real model (Ollama, Module 6).
# --------------------------------------------------------------------------


def trapped_answer(question: str) -> str | None:
    """In flaky mode, two questions get a confident WRONG answer from
    'memory'. The grade gate is what stops these from reaching users."""
    q = question.lower()
    if "backup" in q and "stored" in q:
        return "Backups are stored on the laptop and never leave the office."
    if "grade gate" in q and ("low score" in q or "happens" in q):
        return "The grade gate deletes bad answers and bans the user."
    return None


class FakeLLM:
    """A stand-in for a real model.

    grounded: answers ONLY from the retrieved context.
    flaky: for two trap questions, 'remembers' a wrong fact and answers
    from memory — the classic hallucination failure the gate must catch.
    """

    def __init__(self, mode: str = "grounded"):
        self.mode = mode

    def generate(self, question: str, context: str) -> str:
        if self.mode == "flaky":
            trapped = trapped_answer(question)
            if trapped is not None:
                return trapped
        qt = set(retrieval.tokenize(question))
        sentences = re.split(r"(?<=[.!?]) ", context)
        hits = [(sum(t in set(retrieval.tokenize(s)) for t in qt), s)
                for s in sentences]
        hits.sort(key=lambda pair: pair[0], reverse=True)
        top = [s for n, s in hits if n > 0][:2]
        return " ".join(top) if top else "I don't know."


# --------------------------------------------------------------------------
# Scoring (from lesson 02) — numbers, not vibes.
# --------------------------------------------------------------------------

def groundedness(answer: str, context: str) -> float:
    at = retrieval.tokenize(answer)
    if not at:
        return 1.0
    ct = set(retrieval.tokenize(context))
    return sum(1 for t in at if t in ct) / len(at)


def recall(retrieved: list[str], relevant: list[str]) -> float:
    if not relevant:
        return 1.0
    return len(set(retrieved) & set(relevant)) / len(relevant)


# --------------------------------------------------------------------------
# The agent: tool registry + the loop (decide, call, check, repeat).
# --------------------------------------------------------------------------

class Assistant:
    def __init__(self, notes_dir: str = "notes", mode: str = "grounded"):
        self.notes = retrieval.load_notes(notes_dir)
        self.index = retrieval.build_index(self.notes)
        self.llm = FakeLLM(mode)
        self.mode = mode
        # The tool registry — one place holding every tool the agent can call.
        self.tools = {
            "list_notes": {
                "fn": self._list_notes,
                "doc": "list the titles of all notes",
            },
            "search_notes": {
                "fn": self._search_notes,
                "doc": "search the notes for a question, return ranked note ids",
            },
            "read_note": {
                "fn": self._read_note,
                "doc": "read one note by id, return its text",
            },
        }

    # --- tools ----------------------------------------------------------
    def _list_notes(self) -> str:
        return "\n".join(f"- {nid}: {info['title']}"
                         for nid, info in sorted(self.notes.items()))

    def _search_notes(self, query: str, k: int = 3) -> list[str]:
        return retrieval.search(self.index, query, k)

    def _read_note(self, note_id: str) -> str:
        return retrieval.read_note(self.index, note_id)

    # --- the loop -------------------------------------------------------
    def _evidence(self, note_ids: list[str], n: int = 2) -> str:
        texts = [self.notes[nid]["text"] for nid in note_ids[:n]]
        return " ".join(texts)

    def answer(self, question: str) -> dict:
        """The agent loop with the grade gate built in."""
        # 1. decide: which tool? 2. call it.
        if "list" in question.lower():
            note_ids = []
            used_tool = "list_notes"
        else:
            note_ids = self.tools["search_notes"]["fn"](question, k=3)
            used_tool = "search_notes"
        # 3. check: gather evidence from the best hits.
        evidence = self._evidence(note_ids)
        # 4. generate.
        answer = self.llm.generate(question, evidence)
        # 5. grade.
        g1 = groundedness(answer, evidence)
        decision = decide(g1)
        retried = False
        if decision == "retry":
            retried = True
            expanded = question + " " + (note_ids[0] if note_ids else "").replace("-", " ")
            note_ids = self.tools["search_notes"]["fn"](expanded, k=5)
            evidence = self._evidence(note_ids)
            answer = self.llm.generate(question, evidence)
            g2 = groundedness(answer, evidence)
            if decide(g2) == "pass":
                decision = "pass"
            else:
                decision = "fallback"
                answer = fallback_answer(question, note_ids, self.index)
        elif decision == "fallback":
            answer = fallback_answer(question, note_ids, self.index)
        return {
            "question": question,
            "answer": answer,
            "decision": decision,
            "groundedness": round(g1, 2),
            "retried": retried,
            "used_tool": used_tool,
            "citations": note_ids,
        }


def main() -> None:
    args = list(sys.argv[1:])
    mode = "grounded"
    questions = []
    i = 0
    while i < len(args):
        if args[i] == "--mode" and i + 1 < len(args):
            mode = args[i + 1]
            i += 2
        elif args[i].startswith("--"):
            i += 1  # ignore unknown flags
        else:
            questions.append(args[i])
            i += 1
    if not questions:
        print(__doc__)
        raise SystemExit(1)
    agent = Assistant(mode=mode)
    for question in questions:
        result = agent.answer(question)
        print(f"Q: {result['question']}")
        print(f"tool: {result['used_tool']}  citations: {result['citations']}")
        print(f"decision: {result['decision']}  groundedness: {result['groundedness']}"
              f"  retried: {'yes' if result['retried'] else 'no'}")
        print(f"A: {result['answer']}")
        print()


if __name__ == "__main__":
    main()
