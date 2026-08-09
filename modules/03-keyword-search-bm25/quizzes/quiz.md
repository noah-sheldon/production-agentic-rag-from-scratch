# Module 03 Quiz — human-in-the-loop

Answer from memory. A human reviews. No auto-pass.

## Questions

1. **BM25 in one line** — what does BM25 actually score? Why do rare words
   matter more than common ones?

2. **k1 and b** — what does each knob control, and what happens at k1=0 / b=0?

3. **Precision vs recall** — define both. Your RAG retriever: which one do you
   optimize and why?

4. **Why keyword first** — before embeddings, why start with keyword search?

5. **Measure** — you changed the ranking and it "feels" better. What's the
   problem with that, and what do you do instead?

## Review (for the human)

- 1: term frequency × IDF (rarity); rare terms discriminate, common ones don't.
- 2: k1 = term-frequency saturation (presence at 0); b = length penalty (none at 0).
- 3: precision = returned that are relevant; recall = relevant that got
  returned. Retriever → recall (answer must be in the top-k).
- 4: transparent, free, exact-term wins (code, names, ids) — the foundation
  hybrid builds on (grep vs vectors).
- 5: vibes aren't measurement — label queries, compute precision/recall.

Verdict: all five pass → module 03 done, project next. Any fail → re-teach.
