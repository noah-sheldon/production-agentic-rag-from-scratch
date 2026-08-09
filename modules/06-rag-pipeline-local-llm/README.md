# Module 06 — RAG Pipeline + Local LLM

**Topics:** Ollama local LLM · prompt trimming · streaming (SSE) · local vs cloud.

**Build first:** the RAG answer flow in plain Python — retrieve, prompt, answer — with a stand-in model, no API keys. See the flow work before any server exists.

**Exercises** (3, gate the lessons)
1. Write the retrieve → prompt → answer flow in plain Python; rank a small doc set and answer from context (`rag_flow.py`).
2. Build the prompt two ways — fat vs trimmed — count tokens, and explain why smaller prompts answer faster and cheaper (`trim.py`).
3. Write an SSE-style stream in plain Python (a generator that yields tokens); explain why streaming matters (`stream.py`).

**Quiz (human-in-the-loop)** — `quizzes/quiz.md`: answered from memory, reviewed by a human. No auto-pass.

**Project — Ask your notes (private, local)**
A CLI that answers questions from your own notes: retrieve → trim → prompt → model → answer, with sources, streaming, and measurements. No cloud API — your notes never leave your machine.
