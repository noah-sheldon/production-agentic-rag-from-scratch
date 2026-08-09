# Artifact — the prompt-trimming recipe

Shrink every prompt before it reaches the model. Measure before and after.

- [ ] **k** — retrieve only the top-k notes (2-5 is usually plenty)
- [ ] **Sentence trim** — inside each note, keep only sentences containing a question word
- [ ] **Budget cap** — hard stop at N tokens; stop adding past it
- [ ] **Prefix sources** — `[title]` on each kept piece, so the answer can show where it came from
- [ ] **Measure** — print chars + tokens + latency for fat vs trimmed on the SAME question
- [ ] **Estimate honestly** — `chars / 4` is rough; Ollama reports `prompt_eval_count`
- [ ] **Tune per question** — too aggressive a trim cuts the answer out; test your own questions

Rule of thumb from the lesson build: trimming a 50-note folder took the prompt
from 1253 → 74 tokens and the answer from hallucinated → grounded.
