# Module 09 — Evaluation + Capstone

**Topics:** eval question set (labeled, known-good answers) · scoring (groundedness, recall, pass rate) · the grade gate (pass / retry / fallback) · publishing (repo, README, video plan).

**Build first:** build an eval set by hand as JSON with known-good answers — then score a RAG-style flow with a fake LLM and watch the numbers, then put a grade gate in front of it that refuses to ship bad answers. No eval framework, no judge model — the ruler and the gate are yours before anything imported.

**Exercises** (3, gate the lessons)
1. Build an eval set: write `build_eval_set(corpus)` — questions with known-good answers and sources, validated.
2. Score an answer: write `groundedness()` and `recall()` — numbers, not vibes.
3. Route a score: write `decide()` — pass, retry, or fallback, with a threshold.

**Quiz (human-in-the-loop)** — `quizzes/quiz.md`: answered from memory, reviewed by a human. No auto-pass.

**Project — Measure, ship, publish your assistant (the capstone)**
The full agentic RAG assistant over YOUR notes — tools, the loop, an eval set, scoring, and a grade gate — assembled from every module before it, measured with a committed eval report, and walked through a publish checklist (repo, README, video plan). This is the module that completes the knowledge assistant: from empty machine to something you can point other people at.
