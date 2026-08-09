# Module 04 Quiz — human-in-the-loop

Answer from memory. A human reviews. No auto-pass.

## Questions

1. **Why chunk at all?** What goes wrong if a retriever returns a whole
   5,000-word note instead of one section? Where does the cut belong — and why
   does a naive fixed-size cut fail?

2. **Section vs fixed-size.** When is a section chunker the right choice, and
   when do you have no choice but fixed-size? What is chunk overlap, and what
   problem does it patch?

3. **The 384 numbers.** What is an embedding, and what does "384" mean? How
   does a machine know that "puppy" is closer to "dog" than to "printer"?

4. **Cosine similarity.** How is it computed (in words, not math symbols)?
   What does a score of 1.0 mean, and what does a score near 0 mean? Why does
   the idea work even with random vectors as stand-ins?

5. **Fallbacks.** The embedding provider is down at 3am and the cache is cold.
   Walk the fallback chain. Why must the degraded path be visible instead of
   silent?

## Review (for the human)

- 1: the answer drowns in noise; the model's context window is finite; a cut
  should follow meaning (headings/sentences) — a naive fixed cut splits
  sentences mid-thought.
- 2: sections when the text has honest headings (notes, docs); fixed-size when
  it doesn't (feeds, logs). Overlap repeats the tail into the next chunk so a
  straddling sentence is still whole somewhere.
- 3: a fixed list of numbers (384 dimensions) learned to place similar meanings
  nearby; closeness in numbers = closeness in meaning; trained model, not word
  spelling.
- 4: dot product of the two vectors divided by the product of their lengths —
  the angle between them. 1.0 = same direction (identical), ~0 = unrelated.
  Random vectors prove the MATH (self = 1.0, unrelated ~ 0); word-count
  stand-ins prove that closeness tracks similarity.
- 5: cached embeddings → keyword search (module 03) → smaller local model
  (Ollama), marked degraded. Silent degradation hides broken answers; the log
  must show which tier answered.

Verdict: all five pass → module 04 done, project next. Any fail → re-teach.
