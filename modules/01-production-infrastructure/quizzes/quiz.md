# Module 01 Quiz — human-in-the-loop

Answer in your own words, from memory (no peeking at the lessons). Then a
**human reviews your answers** — no auto-pass. The tutor asks, the human
approves.

## Questions

1. **What is a container, in one simple sentence?** What does it add that a
   plain process does not have?

2. **"Alive is not ready."** Why is a running process not a working service,
   and what can a machine do with a `200` vs a `503` health answer?

3. **What does each service own?** PostgreSQL vs OpenSearch vs Ollama — one
   line each. Why do two of them exist for "data"?

4. **Where does FastAPI's `/docs` come from?** What is `/openapi.json`, and why
   is generating docs from code better than hand-writing them?

5. **The quality gate.** Lint, types, tests — what does each catch that the
   other two don't? What happens when the gate fails?

## Review (for the human)

- Answer 1 must mention isolation (own files/network) — "like a VM" without
  the kernel cost is also correct.
- Answer 2 must mention a dependency (DB) and the 200/503 machine action.
- Answer 3 must name: facts/metadata (Postgres), search index (OpenSearch),
  the model (Ollama).
- Answer 4 must mention code-as-source (signatures/docstrings) and
  machine-readable JSON.
- Answer 5 must distinguish the three and name the block (pre-commit gate).

Verdict: all five pass → module 01 lessons are done, project next.
Any fail → re-teach that lesson from first principles, re-ask.
