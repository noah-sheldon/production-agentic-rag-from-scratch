# Artifact — the 3-size chunk experiment

Run this on YOUR notes before trusting any chunk size. The build from lesson
03 is the template: one note, a [fixed-size chunker](../../../../glossary.md#fixed-size-chunker), three sizes, and three measures for the chunk that holds the answer.

Checklist:

- [ ] Pick a real question that one sentence in your notes answers
- [ ] Chunk the same text at 3 sizes (try 30 / 100 / 300 words)
- [ ] For each size, record: chunk count, the answer chunk's word count,
      and whether the answer sentence is whole in one chunk
- [ ] Too small? The answer sentence is cut — add [overlap](../../../../glossary.md#chunk-overlap)
      or grow the size
- [ ] Too big? The answer chunk tops the noise budget — shrink the size
- [ ] Winner = the size where the answer is whole AND the chunk stays small
- [ ] Record the winner and the three numbers in `RESULTS.md` (project)
- [ ] Re-run the same experiment on your real queries (top-k hits, the
      precision/recall idea from module 03) — one note is a hint, ten queries
      is a decision
