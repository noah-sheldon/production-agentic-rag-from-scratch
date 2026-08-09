# 01 — What Is an Ingestion Pipeline

## MOTTO
> A pipeline is a script that can survive a failure — a script is a pipeline that can't.

## PROBLEM
A naive script pulls articles, hits a rate limit, crashes — and you re-fetch everything from zero. Half-saved data, duplicate rows, no memory of what it already did. "Run it again" is not a plan.

## CONCEPT
An [ingestion pipeline](../../../../../glossary.md#ingestion) moves data from sources into your store in small, resumable steps. The difference from a script: each item is tracked (done / failed / pending), failures are retried, and re-running never duplicates. The state lives in the database, not in your head.

```mermaid
flowchart LR
    S[Sources: articles, notes, feeds] --> F[Fetch, with retries]
    F --> P[Parse to clean text]
    P --> M[Extract metadata]
    M --> DB[(Your store)]
    DB --> Q[Re-run: skips what's done]
```

## BUILD IT

```bash
python3 lessons/01-what-is-an-ingestion-pipeline/code/build.py
```

A plain-Python pipeline: a `done` set persisted to disk, per-item fetch/parse/store steps, and a re-run that skips completed items. Run it twice — the second run does nothing new.

## USE IT
[Airflow](../../../../../glossary.md#airflow) is the same idea with scheduling, retries, and a UI.

| Airflow gives you | Airflow hides from you |
|---|---|
| DAGs, schedules, retry policies, a web UI | the scheduler, the worker pool, the metadata DB |
| per-task state and logs | how tasks are executed under the hood |

Honest trade-off: Airflow earns its keep when you have many pipelines and need visibility. For one pipeline, a script with a `done` set is honest.

## SHIP IT
The resumable pipeline pattern — `outputs/artifact.md`: checklist for making any fetch job idempotent.
