# Module 02 Quiz — human-in-the-loop

Answer from memory. A human reviews. No auto-pass.

## Questions

1. **Pipeline vs script** — what makes a pipeline different from a script? What
   must survive a crash?

2. **Resumability** — how does the pipeline know what's already done? What
   breaks if it doesn't remember?

3. **Retries + backoff** — why wait between retries, and why wait LONGER each
   time? What is the retry budget and what happens when it's hit?

4. **Parsing** — why is a document "a blob until someone tells you where the
   text is"? Which format is the worst and why?

5. **Idempotency** — re-run the pipeline twice. Same result? Why does that
   matter?

## Review (for the human)

- 1: state tracking, per-item steps, failure survival. "Run it again is not a plan".
- 2: done-set / DB column; duplicates + double-fetch without it.
- 3: rate limits + sync storms; exponential backoff + jitter; budget = guard
  (mark failed, move on).
- 4: content vs structure; PDF text layer (sometimes shapes, not text).
- 5: yes — same result, no duplicates; without it the data drifts.

Verdict: all five pass → module 02 done, project next. Any fail → re-teach.
