# Module 09 Quiz — human-in-the-loop

Answer from memory. A human reviews. No auto-pass.

## Questions

1. **Eval set vs vibes** — why must an eval question carry a known-good
   answer written by a human? What goes wrong when you "just feel" whether
   the assistant is good?

2. **The two numbers** — what does groundedness measure, and what does
   recall measure? Give one example where recall is 1.0 but groundedness is
   low.

3. **The grade gate** — a score comes in at 0.3, threshold 0.5. What does
   the gate do, and what happens if the retry still fails? When is a
   fallback the right answer instead of a retry?

4. **Too good to be true** — your eval says pass rate 100% on 5 questions.
   Is the assistant ready to ship? What is the danger of a tiny eval set?

5. **The capstone** — name the pieces from modules 0-8 that your capstone
   assistant assembles (at least four), and the three parts of the publish
   checklist.

## Review (for the human)

- 1: labels are ground truth written before the model runs; vibes miss the
  quiet failures and cannot be re-run, shared, or compared.
- 2: groundedness = answer sticks to the retrieved notes (anti-hallucination);
  recall = the right note was found. Example: the right note is retrieved
  (recall 1.0) but the model answers from memory and invents facts
  (groundedness low).
- 3: 0.3 vs 0.5 → retry once (more context, re-score); still failing →
  fallback: "I don't know" + citations. Fallback is right when the problem is
  the generator (hallucination), retry is right when the problem is retrieval.
- 4: not ready — 5 questions are not a measure; a tiny eval set can pass by
  luck and misses the questions users actually ask. Expand to 10+, cover edges.
- 5: ingest + chunk (0, 2, 4), search (3, 5), agent loop + tools (8),
  eval set + scoring + gate (9), measured eval report (7), documented and
  published (repo, README, video plan).

Verdict: all five pass → module 09 done, course complete, publish the capstone.
Any fail → re-teach that lesson.
