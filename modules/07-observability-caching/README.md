# Module 07 — Observability & Caching

**Topics:** tracing · cache + TTL · cost per question · dashboards.

**Build first:** time and log every step of a RAG answer in plain Python — a
per-step breakdown — before any tracing tool. Build a dict cache with TTL and
count tokens against a pricing table before touching Redis or a dashboard.

**Exercises** (3, gate the lessons)
1. Trace a RAG-style flow — per-step breakdown in plain Python, no tools.
2. Build a TTL cache — hit rate and cost per question, before and after.
3. Cost per question — token counting + a pricing table; the 150-400x caching
   math on 1,000 questions.

**Quiz (human-in-the-loop)** — `quizzes/quiz.md`: answered from memory,
reviewed by a human. No auto-pass.

**Project — Cost + cache dashboard**
A dashboard that shows every question's latency and cost, before and after a
TTL cache — hit rate, where the time goes, and the money saved — all plain
Python, runnable on macOS.
