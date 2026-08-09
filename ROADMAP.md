# Roadmap — Production Agentic RAG, from scratch

Seven modules. Every module: lessons (build-first) + **exercises** + a **project**.
No week/day framing — move at your own pace, projects gate progress.

## The modules

| Module | Title | Project (ships) |
|---|---|---|
| 01 | Production Infrastructure | Service skeleton: compose + FastAPI + Postgres + OpenSearch + Ollama |
| 02 | Data Ingestion | arXiv paper ingest pipeline (Airflow DAG, retries, idempotent) |
| 03 | Keyword Search First (BM25) | Your own BM25 search engine (no vectors) |
| 04 | Chunking & Hybrid Search | Hybrid search endpoint (keyword / semantic / fused) |
| 05 | RAG Pipeline + Local LLM | Ask-your-papers: private RAG, streaming, Gradio UI |
| 06 | Observability & Caching | Redis cache + latency/cost dashboard, real numbers |
| 07 | Agentic RAG + Bot | The complete arXiv curator + Telegram bot, decisions visible |

## How it works

- **Build first:** each module's lessons build the concept in plain Python before
  the framework (BM25 by hand before OpenSearch, the agent loop by hand before
  LangGraph).
- **Exercises gate lessons:** a lesson isn't done until its exercises are.
- **Projects gate modules:** a module isn't done until its project ships.
- **Capstone:** Module 07's project is the whole system, end to end.

## Content pipeline

Each module's lessons produce short-form + long-form content (the
content-planner pipeline): one long-form per module topic, shorts per concept.
Videos link from module docs.
