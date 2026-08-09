# Artifact — the transparency checklist

A run is explainable when every line below is true:

- [ ] **Every decision logged with a why** — guardrail verdict, rewrite,
      search, grade, answer: each line says what and why, not just what.
- [ ] **Rewrite rules documented** — pointer extraction ("the one about X"),
      pronoun resolution ("it" → last topic), stopword stripping. A human can
      predict the rewrite before it happens.
- [ ] **Bad queries fixed before they search** — rewriting happens before
      retrieval, and its effect is measured (chars saved, better top hit).
- [ ] **Scores and verdicts in the log** — `grade: relevant (score=1.00)`,
      never a bare "yes".
- [ ] **The trace reads top to bottom** — a run is a story: question →
      verdict → rewrite → search → grade → grounded answer with citation.
- [ ] **The log is a file, not a print** — JSON lines you can grep, diff, and
      count across runs (this is the trace from module 07, built by hand).
- [ ] **Out-of-domain and budget-stops are logged too** — failures are
      decisions; silence is not transparency.

The loop from lesson 02 + this log = an agent you can debug by reading.
