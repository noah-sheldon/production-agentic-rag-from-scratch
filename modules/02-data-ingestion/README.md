# Module 02 — Data Ingestion

**Topics:** API ingestion (rate limiting, retries) · article/PDF parsing · Airflow pipelines · metadata extraction · API → database flow.

**Build first:** fetch an article or note from any source in plain Python with retry logic — no client library. See what rate limits and backoff actually do.

**Exercises** (3, gate the lessons)
1. Fetch an article's content with plain `requests` + retry/backoff.
2. Parse one document (HTML/markdown/PDF) and extract the title + body — what breaks, and why.
3. Trace one item from source to database row; list every step.

**Quiz (human-in-the-loop)** — `quizzes/quiz.md`: answered from memory, reviewed by a human. No auto-pass.

**Project — Read-it-later pipeline**
An Airflow DAG that pulls your saved articles and notes on schedule, parses them, stores metadata, and survives failures (retries, idempotency, re-run). Your knowledge base starts here.
