# Module 07 Project — Cost + Cache Dashboard

**Goal:** a dashboard that shows every question's latency and cost, before and
after a TTL cache — hit rate, where the time goes, and the money saved. All
plain Python, no frameworks, runnable on macOS.

## What ships

`project/skeleton/`:

| File | What it is |
|---|---|
| `dashboard.py` | the dashboard: simulated RAG flow + tracer + TTL cache + pricing, prints per-question rows and a summary |
| `questions.txt` | the questions to answer (repeats on purpose — that's what caching loves) |
| `trace.jsonl` | the trace store: one JSON line per question (written by `dashboard.py`) |

## How to run it

```bash
cd modules/07-observability-caching/project/skeleton
python3 dashboard.py
```

## Acceptance criteria — done means all of these pass

1. **Runs stdlib-only** on macOS: `python3 dashboard.py` prints a dashboard.
2. **Per-question row**: question, hit/miss, latency, cost.
3. **Hit rate**: printed, and greater than zero (the repeated questions hit).
4. **Cost math**: with-cache total < without-cache total; both shown, plus the
   savings factor.
5. **Per-step breakdown**: for a cache miss, retrieve/prompt/answer times are
   shown (the trace, lesson 01).
6. **TTL proven**: change `TTL_SECONDS` to 0 and re-run — previously cached
   questions go through the pipeline again (lesson 02).
7. **Trace written**: `trace.jsonl` has one JSON line per question.

## TODOs (each ties to a lesson)

1. Replace the fake `time.sleep` steps with your real RAG pipeline from module
   06 (retrieve → prompt → answer).
2. Swap the `TTLCache` dict for Redis (lesson 02 USE IT) — keep the same
   `get`/`set`/`hit_rate` API.
3. Send the tracer steps to Langfuse (lesson 01 USE IT) instead of printing
   them.
4. Use real token counts and your real model prices in the pricing table
   (lesson 03).
