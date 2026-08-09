# 04 — Query Rewriting and Transparency

## MOTTO
> A bad question gets a bad search — fix the question, then show your work.

## PROBLEM
"agents stuff" is how humans actually talk to a search box, and it searches terribly. And the worst kind of query is the *pointer*: "the one about evals" — nothing to search at all unless you remember the previous topic. Meanwhile the agent acts like a black box: it called search twice and nobody knows why. Two fixes: rewrite the query before it searches, and log every decision so the run is explainable.

## CONCEPT
[Query rewriting](../../../../glossary.md#query-rewriting) (the course's [query translation](../../../../glossary.md#query-translation)) fixes the question before retrieval: cut filler words, turn "the one about X" into X, and resolve pronouns ("it", "this") from the conversation's last topic. Cheap heuristics beat nothing — a rewritten query is measurable: it retrieves the right note.

[Reasoning transparency](../../../../glossary.md#reasoning-transparency) is the opposite of the black box: every decision the agent makes is written to a [decision log](../../../../glossary.md#decision-log) — what was called, why, with what score. A run becomes a story you can read top to bottom. This is the same idea as the [trace](../../../../glossary.md#trace) from module 07, built by hand.

```mermaid
flowchart LR
    Q[bad query: "the one about evals"] --> R[rewrite]
    R -->|"evals"| S[search the notes]
    S --> G[graded documents]
    G --> A[answer with citations]
    Q -.->|every step| L[(decision log)]
    R -.-> L
    S -.-> L
    G -.-> L
    A -.-> L
```

**Diagram (whiteboard):** open `diagrams/rewrite-transparency.excalidraw` in excalidraw.com — same picture, traceable by hand.

## BUILD IT
Rewriting heuristics and a decision log in plain Python, wired into a tiny agent run:

```bash
python3 lessons/04-query-rewriting-and-transparency/code/build.py
```

The build rewrites queries with three heuristics — pronoun resolution ("it" → the last topic), pointer extraction ("the one about X" → X), and stopword stripping — then runs a mini agent (fake model, keyless) where *every* step logs to a JSON-lines decision log: guardrail verdict, before/after rewrite, search scores, graded docs, final answer. The trace prints top to bottom; the rewritten query's size is measured against the original.

## USE IT
LangGraph and LangSmith automate the recording — but not the thinking.

| LangGraph gives you | LangGraph hides from you |
|---|---|
| tracing: every node and edge recorded by default | deciding what "why" means — you choose what to log |
| retriever wrappers that expand one query into many | the rewriting heuristics and their tuning |
| streaming + replay of a whole run | the decision log is only as good as what you wire into it |

Honest trade-off: the trace comes free, but a free trace of a thoughtless loop is still noise. The transparency you built by hand — one log line per decision with a reason — is what makes a trace readable.

## SHIP IT
The transparency checklist — `outputs/artifact.md`: every decision logged with why, rewrite rules documented, trace readable top to bottom, scores and verdicts included, bad queries fixed before they search.
