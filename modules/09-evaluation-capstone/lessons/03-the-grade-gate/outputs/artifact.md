# Artifact — the grade gate

Keep bad answers away from users. A gate is three decisions, not a feature.

- [ ] A score for every answer (lesson 02) — no score, no gate
- [ ] A threshold: groundedness at or above this ships (start at 0.5, tune on your eval set)
- [ ] Retry once on shaky scores: search harder (k + 2), re-answer, re-score
- [ ] Fallback for the rest: "I don't know" + the closest notes as citations
- [ ] The fallback is honest, never a guess — a wrong refusal beats a wrong answer
- [ ] Before/after numbers: how many hallucinated answers were shipped before vs after
- [ ] When retries never help, that is a signal: fix the model or the notes, not the gate
