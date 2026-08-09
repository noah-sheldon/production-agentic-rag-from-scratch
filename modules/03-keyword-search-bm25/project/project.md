# Module 03 Project — BM25 Search Over Your Notes

**Goal:** a keyword search engine over your own documents (notes, articles,
code) — ranked results, filters, and a relevance measurement. No vector search
allowed yet — this is the foundation Module 05 builds on.

## What ships

`project/skeleton/`:

| File | What it is |
|---|---|
| `bm25_search.py` | your BM25 engine: index (tokenize + IDF), search (score + rank), top-k |
| `notes/` | your documents — drop markdown/text files in here |
| `search_cli.py` | a terminal search: `python3 search_cli.py "deploy at 3am"` |

## How to run it

```bash
cd modules/03-keyword-search-bm25/project/skeleton
python3 search_cli.py "why does the deploy run at 3am"
```

## Acceptance criteria — done means all of these pass

1. **Ranks sensibly.** Queries return relevant docs first (you can tell).
2. **Filters.** Search supports a tag filter (`--tag=python`) — narrowing works.
3. **Measured.** You labeled 10 of your own queries; precision@5 and recall@5
   are written in `RESULTS.md` with the settings (k1, b) you chose and why.
4. **Tuned, not vibed.** k1/b chosen by measurement, not gut feel.
5. **Honest about limits.** One documented query where keyword search fails
   (the exact case Module 05's vectors should fix).

## TODOs (each ties to a lesson)

1. Implement BM25 indexing + ranking (Lesson 01).
2. Tune k1/b on your labeled queries (Lesson 02).
3. Build the precision/recall measurement + RESULTS.md (Lesson 03).
4. Add a tag filter to the index (Lesson 01 USE IT — filters in OpenSearch).
