# Module 08 — Agentic RAG: Tools + the Loop

**Topics:** tool design · the tool registry (list/search/read) · tool schema (name, description, params) · tool calling · the agent loop (decide → call → result → repeat) · max turns · guardrails (out-of-domain rejection) · document grading (relevant/irrelevant) · query rewriting · reasoning transparency.

**Build first:** tools and the loop in plain Python — a hand-rolled tool registry over your notes, a loop that calls a model and runs its tool calls (raw HTTP, with a FAKE mode that runs keyless), guardrails and grading by hand, then query rewriting with a decision log. Own the loop, then import the graph.

**Exercises** (3, gate the lessons)
1. Build the tool registry — `tools.py`: schema, list/search/read, call by name.
2. Build the agent loop — `loop.py`: decide → call → result → repeat with a fake model, max turns respected.
3. Guardrail + rewrite — `guardrails.py`: reject out-of-domain questions, rewrite a bad query.

**Quiz (human-in-the-loop)** — `quizzes/quiz.md`: 5 questions, answered from memory, reviewed by a human. No auto-pass.

**Project — Notes assistant with tools**
A runnable assistant over YOUR notes folder: guard the question, rewrite it, search, read, cite — with every decision logged and a fake-LLM mode so it runs with no API key. The full loop from module 06's RAG pipeline, now with hands.
