# Production Agentic RAG from Scratch

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

Nine modules, build YOUR personal knowledge assistant — from an empty machine
to a tool-wielding agent over your own notes. No week/day framing; move at
your own pace, projects gate modules.

| Module | Title | Project |
|---|---|---|
| 0 | Setup + How to Learn | Environment ready, tutor installed |
| 1 | Production Infrastructure | Your dev lab: one-command local stack |
| 2 | Data Ingestion | Read-it-later: save, parse, store your notes |
| 3 | Keyword Search First (BM25) | BM25 search over your notes |
| 4 | Chunking + Embeddings | Semantic index of your notes |
| 5 | Hybrid Search (RRF) | Hybrid search over your notes |
| 6 | RAG Pipeline + Local LLM | Ask your notes — private, local |
| 7 | Observability + Caching | Cost + cache dashboard |
| 8 | Agentic RAG: Tools + the Loop | Notes assistant with tools |
| 9 | Evaluation + Capstone | Measure, ship, publish your assistant |

Every module ships **2-3 exercises** (gate lessons), a **weekly quiz reviewed
by a human** (no auto-pass), and a **project** (gate the module). Build first,
frameworks second, artifacts always.

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
cat modules/01-production-infrastructure/README.md   # start module 01
```

## License

MIT — free, open source, learn it, build it, ship it.
