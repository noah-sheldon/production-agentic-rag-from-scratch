# Module 05 Project — Hybrid Search Over Your Notes

**Goal:** one engine over your own notes with three modes — keyword,
semantic, hybrid — fused with RRF. You measure which mode wins per query
and document the honest limits. This is the search layer Module 06 will
ask questions against.

## What ships

`project/skeleton/`:

| File | What it is |
|---|---|
| `hybrid_search.py` | the engine: keyword (tf x idf), semantic (random-vector stand-in), RRF fusion, one unified `search(query, mode, k)` |
| `search_cli.py` | terminal search: `python3 search_cli.py "query" --mode hybrid` |
| `notes/` | 5 sample notes — replace them with YOUR notes |
| `RESULTS.md` | you write this: your labeled queries + measured precision |

## How to run it

```bash
cd modules/05-hybrid-search-rrf/project/skeleton
python3 search_cli.py "postgres timeout"                 # hybrid (default)
python3 search_cli.py "postgres timeout" --mode keyword
python3 search_cli.py "postgres timeout" --mode semantic
python3 search_cli.py --measure                          # precision table
```

## Acceptance criteria — done means all of these pass

1. **One CLI, three modes.** The same command switches modes with
   `--mode keyword|semantic|hybrid`; the output shape never changes.
2. **Keyword finds exact words.** A query with a rare exact token (try
   `"kubernetes pod restart"`) puts the exact note first.
3. **Semantic finds the near note.** A query like `"postgres timeout"`
   puts the SHORT config snippet first — the note closest to the
   question's meaning.
4. **Hybrid finds both.** For `"postgres timeout"`, hybrid's top-2
   contains the long explanation AND the snippet — neither single mode
   returns both at once.
5. **Deterministic.** Same query twice → same order, every time (the
   stand-in embeddings are seeded, not random at runtime).
6. **Measured, not vibed.** You labeled 10 of YOUR queries; `RESULTS.md`
   reports precision@3 per mode with the three modes compared.
7. **Honest limits.** One documented query where hybrid still fails —
   and why (the exact case Module 06's real embeddings should fix).

## TODOs (each ties to a lesson)

1. Replace the sample notes with YOUR notes — drop `.md` files into
   `notes/` and re-run (Lessons 01-03).
2. Add your own labeled queries; write `RESULTS.md` with precision@3 per
   mode (Lesson 02 mining + Lesson 03 measurement).
3. Tune `k` (the RRF constant) and `DIM` on your data; note what changed
   and why (Lesson 01).
4. Swap the random-vector stand-in for real embeddings when Module 06
   lands — the `search()` contract does not change (Lesson 03).
