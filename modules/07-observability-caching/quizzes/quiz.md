# Module 07 Quiz — human-in-the-loop

Answer from memory. A human reviews. No auto-pass.

## Questions

1. **Trace** — what does a trace record, and why is "the answer feels slow"
   not a plan? Where did the time go in your build?

2. **TTL** — what is a TTL, what happens when an entry expires, and why have
   one at all? What breaks if entries never expire?

3. **Hit rate** — what is hit rate, and what does a 90% hit rate mean for your
   cost and latency? What makes a good cache key?

4. **Cost per question** — how do you count tokens and price one question?
   Which is more expensive, retrieval or the model call — and by how much (the
   150-400x math)?

5. **Dashboard** — what must a cost + cache dashboard show, and who reads it?
   How does it help a decision instead of just looking pretty?

## Review (for the human)

- 1: name + start + end + duration per step (retrieve, prompt, answer); "slow"
  without numbers is a guess. The model call usually dominates.
- 2: time-to-live = expiry; expired entries are deleted and re-answered; with
  no TTL, answers go stale and memory grows forever.
- 3: hits ÷ total questions; 90% = 9 in 10 questions skip the pipeline. Keys =
  normalized questions (trim, lowercase), stable, one key per question.
- 4: 4 chars ≈ 1 token; (in_tokens × in_price + out_tokens × out_price) ÷ 1M;
  the model call is 150-400x retrieval; caching turns repeats into ~$0.
- 5: per-question latency + cost, hit rate, with/without-cache totals — so a
  human can decide: buy the cache, change the model, fix the slow step.

Verdict: all five pass → module 07 done, project next. Any fail → re-teach.
