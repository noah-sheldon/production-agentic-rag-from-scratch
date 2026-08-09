# Module 06 Quiz — human-in-the-loop

Answer from memory. A human reviews. No auto-pass.

## Questions

1. **The RAG flow** — why retrieve BEFORE asking the model? What does
   "grounded" mean, and what does grounding stop the model from doing?

2. **Prompt trimming** — a smaller prompt answers faster and cheaper. Why?
   Name the three knobs you turn to shrink a prompt.

3. **Tokens** — what is a token, roughly? Why does prompt size in tokens
   matter for cost and latency, and who reports the real count (your
   `chars / 4` is only an estimate)?

4. **Streaming / SSE** — what does SSE send to the client, and one line at a
   time? Why does first-token latency matter more than total latency for how
   the user feels? When is streaming NOT worth the trouble?

5. **Local vs cloud** — what does a local model (Ollama) give you, and what
   does it cost you, compared to a cloud model? For a private-notes assistant,
   which is the right call and why?

## Review (for the human)

- 1: retrieve first so the model sees the relevant notes, not everything;
  grounded = the answer comes from the notes; grounding stops hallucination
  ("I don't know" beats inventing).
- 2: the model reads every token before answering — more tokens = more time
  and more cost per request; the three knobs are k (how many chunks),
  chunk/sentence trim (only the matching parts), and the token budget cap.
- 3: a token is a small piece of a word (~4 characters); every token in the
  prompt is paid for and read; Ollama's response includes the real counts
  (prompt_eval_count / eval_count).
- 4: SSE sends "data: <payload>\n\n" frames over one open HTTP connection;
  first-token latency is what the user feels (they start reading at ~24 ms
  vs ~1.2 s for the whole answer); for very short answers or offline
  non-interactive use, streaming overhead may not pay off.
- 5: local gives privacy (data never leaves the machine), no per-token cost,
  offline use; costs you model strength and speed (your laptop does the
  math). For private notes, local is the right call.

Verdict: all five pass → module 06 done, project next. Any fail → re-teach.
