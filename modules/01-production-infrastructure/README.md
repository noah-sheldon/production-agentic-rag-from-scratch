# Module 01 — Production Infrastructure

**Topics:** Docker Compose · FastAPI (async, docs, health checks) · PostgreSQL · OpenSearch · Ollama · service orchestration · code quality (UV, Ruff, MyPy, pre-commit).

**Build first:** a plain-Python service with a health endpoint before FastAPI touches it. Understand what each infra piece does before you wire it.

**Exercises**
1. Run your first containerized app with Docker Compose (no framework).
2. Add a health check endpoint in plain Python; explain why health checks exist.
3. Diagram the services in this system and what each one owns.
4. Run FastAPI's automatic docs and explain what it generates and why.

**Project — Service skeleton**
Stand up the full service skeleton for the arXiv paper curator: compose file, FastAPI app with health + docs, PostgreSQL, OpenSearch, Ollama, all running locally, health of every service visible in one command.
