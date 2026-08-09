# Module 04 Project — Semantic Index of Your Notes

**Goal:** a plain-Python index that cuts your notes into sections, turns each
section into a 384-number embedding, and answers "what is closest?" by cosine
similarity — with a fallback that keeps the index alive when the embedder is
down. Module 03 searched by words; this searches by meaning. The chunking,
the 384 numbers, and the size choice are all yours, built by hand.

## What ships

`project/skeleton/`:

| File | What it is |
|---|---|
| `semantic_index.py` | the index: section chunker, 384-dim embedder with a fallback chain, cosine search, JSON persistence |
| `index_cli.py` | terminal: `python3 index_cli.py build` / `search "query"` |
| `notes/` | your documents — drop markdown/text files in here (3 samples ship) |
| `RESULTS.md` | your measurement log: chunk size decision, labeled queries, best/worst cases |

## How to run it

```bash
cd modules/04-chunking-embeddings/project/skeleton
python3 index_cli.py build                 # chunk + embed every note in notes/
python3 index_cli.py search "giant rodent" # what is closest?
```

The skeleton runs out of the box on the sample notes — with the embedder
simulated as DOWN, so you watch the fallback chain fire on the first build.

## Acceptance criteria — done means all of these pass

1. **Index builds.** `build` turns every note in `notes/` into section chunks,
   each with a 384-number embedding, written to `index.json`.
2. **Searches by meaning.** `search` ranks chunks by cosine similarity —
   the closest chunk is first, and you can see why.
3. **Fallback works.** With the real embedder missing, the index still builds
   and searches (hash stand-in), and the degraded tier is visible in the log,
   not silent.
4. **Chunk size chosen, not guessed.** The 3-size experiment (lesson 03) is
   recorded in `RESULTS.md` — the size you picked and the numbers behind it.
5. **Measured.** 10 of your own queries are labeled in `RESULTS.md`
   (answer chunk in top-3? yes/no), with the best and worst query written down
   and explained.
6. **Honest about limits.** One documented query where the hash stand-in fails
   (the exact case a real embedder should fix).

## TODOs (each ties to a lesson)

1. Replace the skeleton's chunker with your own `chunk_by_sections`
   (headings + overlap) from Lesson 01.
2. Wire a real embedder into `embed()` — Ollama local (nomic-embed-text) or
   an API (Jina/OpenAI) — and keep the fallback chain from Lesson 02.
3. Run the 3-size experiment from Lesson 03 on your notes; record the winner
   and its numbers in `RESULTS.md`.
4. Scoreboard vs Module 03: run the same 10 queries through BM25 and through
   this index; write who wins each query and why in `RESULTS.md`.
