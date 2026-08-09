# Module 02 — Data Ingestion

**Topics:** arXiv API (rate limiting, retries) · scientific PDF parsing (Docling) · Airflow pipelines · metadata extraction · API → database flow.

**Build first:** fetch a paper from arXiv in plain Python with retry logic — no client library. See what rate limits and backoff actually do.

**Exercises**
1. Fetch a paper's metadata with plain `requests` + retry/backoff.
2. Parse one PDF and extract the abstract — what breaks, and why.
3. Explain why ingestion is a pipeline, not a script (failures, resumability).
4. Trace one paper from API to database row; list every step.

**Project — Paper ingest pipeline**
An Airflow DAG that pulls new arXiv papers on schedule, parses them, stores metadata, and survives failures (retries, idempotency, re-run).
