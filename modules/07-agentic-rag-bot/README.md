# Module 07 — Agentic RAG: Tools + the Loop

**Topics:** tool design · the tool registry · tool calling · the agent loop (decide, call, check, repeat) · guardrails (query validation, domain boundaries) · document grading · query rewriting · adaptive retrieval · reasoning transparency.

**Build first:** the agent loop and tools in plain Python — tool registry, guardrails, grading, rewriting — before LangGraph. Own the loop, then import the graph.

**Exercises** (3, gate the lessons)
1. Write the agent loop in plain Python (raw API calls): decide → tool → result → repeat.
2. Implement a guardrail: reject questions outside your knowledge domain — plain Python.
3. Rewrite a bad query and show retrieval improving; expose the agent's decisions (what it called, why).

**Quiz (human-in-the-loop)** — `quizzes/quiz.md`: answered from memory, reviewed by a human. No auto-pass.

**Project — Your knowledge assistant, complete**
The full agentic RAG system over YOUR notes: tools (search, read, list), guarded queries, graded retrieval, adaptive search, citations, decisions visible, end to end.
