# Module 07 — Agentic RAG + Bot

**Topics:** LangGraph state-based orchestration · guardrails (query validation, domain boundaries) · document grading · query rewriting · adaptive retrieval · Telegram bot · reasoning transparency.

**Build first:** the agent loop in plain Python — tools, guardrails, grading, rewriting — before LangGraph. Own the loop, then import the graph.

**Exercises**
1. Write the agent loop in plain Python (raw API calls): decide → tool → result → repeat.
2. Implement a guardrail: reject questions outside the domain — plain Python.
3. Grade retrieved documents as relevant/irrelevant; feed the grade back into retrieval.
4. Rewrite a bad query and show retrieval improving.
5. Expose the agent's decisions (what it called, why) — reasoning transparency.

**Project — The arXiv curator, complete**
The full agentic RAG system: guarded queries, graded retrieval, adaptive search, citations, Telegram bot with async error handling — decisions visible, end to end.
