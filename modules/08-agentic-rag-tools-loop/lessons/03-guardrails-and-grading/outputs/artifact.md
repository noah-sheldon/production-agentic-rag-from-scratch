# Artifact — the guardrail + grading checklist

Both checks before any prompt is built:

- [ ] **Domain defined up front** — a short list of topics you actually have
      notes on. "Everything" is not a domain; it's a hallucination license.
- [ ] **Reject with a reason** — an out-of-domain question gets a clear
      "out of domain — question names none of [topics]", never silence.
- [ ] **Guardrail runs BEFORE any tool call** — stop the cost before it starts.
- [ ] **Every retrieved document is graded** before it reaches the prompt —
      relevant goes in, irrelevant is dropped, always by a number.
- [ ] **Scores logged, not just verdicts** — `score=0.24 -> irrelevant` tells
      you when the threshold is wrong; a bare "no" tells you nothing.
- [ ] **Threshold is a dial you tune** — decoy docs in the context = too loose;
      missing evidence = too strict. Both are visible in the log.
- [ ] **Measured** — a decoy vs real-note score gap printed in every run.

Grading the evidence (this lesson) and grading the answer (module 06) are
different checks; an agentic RAG system runs both.
