# Applied AI from Scratch

> Learn it. Build it. Ship it for others.

A curriculum for engineers who want to build applied AI systems the way a
practitioner actually does: **every system built in plain Python before a
single framework gets imported.**

Maintained by Noah Sheldon — 6 years building ML and AI systems in production
(financial services), MSc Data Science. Not a tutorial re-teller: every lesson
is a build, measured, and explained from first principles.

## Why this exists

Tutorials teach you to call frameworks. Frameworks hide the system. This
curriculum teaches you the system — the loop, the retrieval, the evaluation,
the cost — by hand. Then, and only then, we import the framework and see what
it was doing for us.

## Curriculum v1.0 (2026) — open source · MIT

| Module | Title | Project |
|---|---|---|
| 01 | Production Infrastructure | Service skeleton |
| 02 | Data Ingestion | Paper ingest pipeline |
| 03 | Keyword Search First (BM25) | Your own BM25 search |
| 04 | Chunking & Hybrid Search | Hybrid search endpoint |
| 05 | RAG Pipeline + Local LLM | Private ask-your-papers |
| 06 | Observability & Caching | Cache + cost dashboard |
| 07 | Agentic RAG + Bot | The arXiv curator, complete |

Every module ships **exercises** (gate lessons) and a **project** (gate the
module). Build first, frameworks second, artifacts always.

## Lesson format (Six Beats)

1. **MOTTO** — one-line core idea
2. **PROBLEM** — the concrete pain
3. **CONCEPT** — intuition + diagrams (mermaid / excalidraw)
4. **BUILD IT** — raw math/code, no frameworks
5. **USE IT** — the same thing with the framework, honest trade-offs
6. **SHIP IT** — the reusable artifact

## Learn it — from your terminal

Your agent becomes your tutor: placement quiz, personalized path, lessons
taught interactively, progress tracked.

```bash
npx skills add noah-sheldon/production-agentic-rag-from-scratch
/start-learning
```

Works with Qwen Code, Claude Code, Cursor, Codex — any agent reading a
SKILL.md. Or clone and run locally:

```bash
git clone https://github.com/noah-sheldon/production-agentic-rag-from-scratch
cd production-agentic-rag-from-scratch
python modules/03-keyword-search-bm25/exercises/bm25_by_hand.py   # build it yourself
```

## License

MIT — free, open source, learn it, build it, ship it.
