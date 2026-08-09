# Module 01 — Production Infrastructure

**Topics:** Docker Compose · FastAPI (async, docs, health checks) · PostgreSQL · OpenSearch · Ollama · service orchestration · code quality (UV, Ruff, MyPy, pre-commit).

**Build first:** a plain-Python service with a health endpoint before FastAPI touches it. Understand what each infra piece does before you wire it.

**Exercises** (3, gate the lessons — runnable in `exercises/01_exercises.py`)
1. Run your first containerized app with Docker Compose (no framework).
2. Add a health check endpoint in plain Python; explain why health checks exist.
3. Diagram the services + what each owns + explain what FastAPI `/docs` generates.

**Quiz (human-in-the-loop)** — `quizzes/quiz.md`: 5 questions, answered from
memory, reviewed by a human. No auto-pass.

**Diagrams** — every lesson's CONCEPT has mermaid + an excalidraw whiteboard
file in `lessons/<NN>/diagrams/` (open in excalidraw.com). Diagram-first.

**Project — Service skeleton**
Stand up the service skeleton for YOUR personal knowledge assistant: compose file, FastAPI app with health + docs, PostgreSQL, OpenSearch, Ollama, all running locally, health of every service visible in one command.
