# Artifact — the scoring harness

Read a score table like a mechanic reads a gauge.

- [ ] One row per eval question — never score the set as a single blob
- [ ] Groundedness per answer: share of answer words present in the retrieved context (hallucination shows up here)
- [ ] Recall per question: did the labeled source note get retrieved?
- [ ] Averages for the whole set — but always glance at the worst row first
- [ ] Look for patterns, not just totals: one bad note? one bad question type?
  - low recall everywhere → fix retrieval
  - high recall, low groundedness → fix the model / the prompt
  - one low row → fix that one question's note
- [ ] Re-run after every change — a fix that moves the average is a real fix
