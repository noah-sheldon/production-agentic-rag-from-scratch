# Module 05 Quiz — human-in-the-loop

Answer from memory. A human reviews. No auto-pass.

## Questions

1. **RRF in one line** — how does a document earn points in Reciprocal Rank
   Fusion? Why position and not score?

2. **The scale trap** — two engines score the same doc `9.9` and `0.02`.
   What does score averaging do, and what does RRF do differently? Which
   document wins each way?

3. **The three camps** — describe a query where keyword wins alone, one
   where semantic wins alone, and one where hybrid wins. What is a "tag
   note" and why does it fool a semantic engine?

4. **The constant k** — what does `k` (usually 60) do in `1/(k + rank)`?
   What happens if you set it very low (1) or very high (1000)?

5. **The unified API** — what stays the same across `mode=keyword`,
   `mode=semantic`, and `mode=hybrid`? Why does that contract matter for
   the rest of your app?

## Review (for the human)

- 1: `1/(k + rank)` per list, summed; positions are comparable across
  engines, raw scores are not (different scales).
- 2: averaging crowns the doc (`9.9` dwarfs `0.02` — one engine's scale
  decides). RRF asks what each engine THINKS: a doc both engines
  half-agree on beats a doc only one engine loves.
- 3: exact-token query → keyword; paraphrase/meaning query → semantic;
  split query (two answers, one by word one by meaning) → hybrid. Tag
  note = one-word note whose vector IS the query vector (cosine 1.0).
- 4: k softens the top-rank bonus; low k makes rank differences loud
  (top picks dominate), high k flattens everything toward a tie.
- 5: same inputs (query, mode, k), same output shape ((score, text)
  list), mode is a parameter not a fork; callers never change when
  engines change.

Verdict: all five pass → module 05 done, project next. Any fail → re-teach.
