# Module 08 Quiz — human-in-the-loop

Answer from memory. A human reviews. No auto-pass.

## Questions

1. **Tool schema** — a tool schema has three parts: name, description,
   parameters. Which one teaches the model WHEN to use the tool — and what
   happens if that part is lazy or missing?

2. **The loop** — why does the agent's `messages` list grow every turn, and
   why must the tool result be appended as a `role: "tool"` message? What
   breaks if you drop it?

3. **Max turns** — why does every agent need a turn budget? What exactly
   happens when the budget is spent — and what would happen without it?

4. **Guardrails vs grading** — the guardrail and the grader both say "no".
   What does each one stop, and when in the flow does each run? Why does a
   guardrail have to run BEFORE any tool call?

5. **Rewriting + transparency** — give one example of a query that searches
   badly and its rewritten form. Then: what does a decision log give you that
   a final answer alone never can?

## Review (for the human)

- 1: the description is the instruction manual — the model never sees the
  code. A lazy description means the model calls the tool at the wrong time
  (or not at all).
- 2: the model sees its own past calls and results; the tool result is the
  only way the model learns what the tool returned. Dropping it = the model
  re-decides on nothing and loops or hallucinates.
- 3: an agent that never answers burns tokens forever; the budget stops it
  and returns a clear "budget spent" answer. Without a budget: runaway cost.
- 4: the guardrail stops bad QUESTIONS (out-of-domain, before cost starts);
  the grader stops bad EVIDENCE (irrelevant documents, before the prompt).
  Guardrail first because a rejected question should cost nothing.
- 5: e.g. "the one about evals" → "evals". A decision log turns a run into
  a story — what was called, why, with scores — so failures are debuggable
  and answers are checkable (reasoning transparency).

Verdict: all five pass → module 08 done, project next. Any fail → re-teach.
