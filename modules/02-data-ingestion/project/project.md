# Module 02 Project — Read-it-Later Pipeline

**Goal:** a pipeline that saves your articles and notes on a schedule, parses
them, stores metadata, and survives failures — retries, idempotency, re-run.
Your knowledge base starts here.

## What ships

`project/skeleton/`:

| File | What it is |
|---|---|
| `pipeline.py` | plain-Python pipeline: fetch (retry+backoff) → parse → store, with a done-set (no Airflow yet) |
| `dag.py` | Airflow DAG stub (scheduled, retries) — the USE IT of lesson 01 |
| `sources.txt` | your list of article/note URLs to ingest |

## How to run it

```bash
cd modules/02-data-ingestion/project/skeleton
python3 pipeline.py          # ingest sources.txt, resumable
python3 pipeline.py          # re-run — skips what's done
```

## Acceptance criteria — done means all of these pass

1. **Resumable.** Run twice; the second run does no duplicate work (done-set).
2. **Retries work.** A failing source is retried with backoff, marked failed
   after the budget, and the rest of the list still completes.
3. **Parsed properly.** Title + clean body extracted from HTML and markdown
   sources (no nav/script junk).
4. **Metadata stored.** Each item stored with title, source, date — visible in
   the store (a JSONL file is fine for module 02).
5. **Failure survived.** Kill the process mid-run, re-run: no duplicates, no
   lost items.
6. **Airflow stub present** (USE IT) — `dag.py` schedules the same pipeline.

## TODOs (each ties to a lesson)

1. Wire `fetch_with_retry` into `pipeline.py` (Lesson 02).
2. Wire the HTML/markdown parser into the parse step (Lesson 03).
3. Expand `sources.txt` with real URLs (your read-it-later list).
4. Replace the JSONL store with PostgreSQL (Module 01 project + Module 03+).
