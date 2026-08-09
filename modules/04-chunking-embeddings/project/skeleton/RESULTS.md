# Semantic index — RESULTS

Your measurement log. Numbers, not vibes. Update as you work the project TODOs.

## Chunk size decision (TODO 3 — lesson 03)

| size (words) | chunk count (your notes) | answer sentence whole? | verdict |
|---|---|---|---|
| 30 | | | |
| 100 | | | |
| 300 | | | |

**Winner:** 100 words — the answer stays whole and the chunk stays small.
(Replace with your own three numbers.)

## Labeled queries (TODO 4 — 10 of your own)

| # | query | answer chunk in top-3? | who wins: semantic / BM25 / tie | why |
|---|---|---|---|---|
| 1 | | yes/no | | |
| 2 | | yes/no | | |
| 3 | | yes/no | | |
| 4 | | yes/no | | |
| 5 | | yes/no | | |
| 6 | | yes/no | | |
| 7 | | yes/no | | |
| 8 | | yes/no | | |
| 9 | | yes/no | | |
| 10 | | yes/no | | |

## Best and worst

**Best query:** — what it was and why the index nailed it.

**Worst query:** — what it was and why it failed (acceptance criterion 6:
the honest limit the real embedder should fix).

## Fallback test (acceptance criterion 3)

Run the build twice — once with the embedder "down" (as shipped), once with a
real embedder wired in (TODO 2). Record what each build printed for the
degraded tier, and confirm the search still answers.
