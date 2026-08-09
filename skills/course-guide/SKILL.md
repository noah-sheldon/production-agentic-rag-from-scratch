---
name: course-guide
version: 1.0.0
description: >
  Topic router for the Production Agentic RAG from Scratch course — answers
  "where do I learn X?" with the exact module + lesson. Trigger phrases:
  "where do I learn", "which module covers", "course guide"
tags: [router, curriculum, agentic-rag]
---

# Course Guide

Answer "where do I learn X?" with the exact module + lesson. Content source:
`https://raw.githubusercontent.com/noah-sheldon/production-agentic-rag-from-scratch/master/` (or local `modules/` if present).

## Topic map

- containers / docker / compose / infra → Module 1
- API / health checks / FastAPI → Module 1
- databases / postgres / opensearch / search engine → Module 1 (db vs search)
- ingestion / pipelines / retries / backoff / parsing / airflow → Module 2
- BM25 / keyword search / ranking / k1 / b → Module 3
- chunking / embeddings / semantic → Module 4
- hybrid search / RRF / fusion → Module 5
- RAG pipeline / Ollama / local LLM / streaming → Module 6
- observability / tracing / caching / Redis / cost → Module 7
- tools / agent loop / guardrails / grading / query rewriting → Module 8
- evaluation / scoring / capstone → Module 9

If the topic isn't mapped, read the module titles from ROADMAP.md and pick the
closest. Reply: module number, lesson (if obvious), and one line why.
