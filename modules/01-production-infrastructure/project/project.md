# Module 01 Project — Service Skeleton

**Goal:** stand up the full service skeleton for the arXiv paper curator —
compose file, FastAPI app with health + docs, PostgreSQL, OpenSearch, and
Ollama — all running locally, with the health of every service visible in one
command. This is the foundation every later module plugs into.

## What ships

`project/skeleton/`:

| File | What it is |
|---|---|
| `compose.yml` | one file, five services: `app`, `db`, `search`, `llm` + three named volumes |
| `app.py` | plain-Python health endpoint (stdlib only) with the TODOs that make this a skeleton |

## How to run it

```bash
cd modules/01-production-infrastructure/project/skeleton

docker compose up -d          # start everything (first run pulls images)
docker compose ps             # ← the one command: health of every service
curl -s localhost:8000/health # the app aggregates all three dependencies
```

First run of OpenSearch on Linux may need `sudo sysctl -w vm.max_map_count=262144`
(Docker Desktop on macOS handles this itself). Give Ollama time to boot; the
healthcheck has a 20s start period.

## Acceptance criteria — done means all of these pass

1. **One command shows everything.** `docker compose ps` lists all five
   services and every healthcheck column reads `healthy`.
2. **The app aggregates.** `curl -s localhost:8000/health` returns one JSON
   body with `db`, `search`, `llm` states and their measured latencies —
   `200` only when all three are up, `503` with the details otherwise.
3. **Auto docs exist.** After the FastAPI swap (TODO 1), `curl -s
   localhost:8000/docs` and `/openapi.json` answer 200 and describe the
   `/health` route — generated from the code, not handwritten.
4. **Data survives restarts.** `docker compose down` then `docker compose up -d`
   loses nothing: the three named volumes (`pgdata`, `osdata`, `ollama`) hold
   the state.
5. **Ollama actually works.** `docker compose exec llm ollama run llama3.2:1b
   "say ok"` answers (or `ollama pull llama3.2:1b` first). The LLM is real and
   local — module 05 will use it.

## The TODOs in app.py (the skeleton's reason to exist)

Each TODO is one lesson's payoff. Do them in order:

1. **Swap the stdlib server for FastAPI** (Lesson 02 USE IT) — same `/health`
   contract, and `/docs` + `/openapi.json` appear for free from type hints.
   Add a `requirements.txt` and switch `compose.yml` to build a Dockerfile.
2. **Make the db probe honest** (Lesson 03) — a real SQL connection running
   `SELECT 1` via psycopg, not a TCP connect. Same for OpenSearch: use a
   client, not a raw HTTP call.
3. **Probe Ollama by model name** — report which models are loaded, not just
   "server answered".
4. **Split probes into a module and test them** (Lesson 04) — pytest + mypy +
   pre-commit wired into the repo before the next module touches it.

## Out of scope (later modules)

No real data, no retrieval, no LLM calls — the skeleton only proves the
*machinery* works. Module 02 ingests papers into Postgres, module 03 builds
keyword search on OpenSearch, module 05 talks to Ollama for real.

## Verification checklist (copy into your module log)

- [ ] `docker compose up -d` completes
- [ ] `docker compose ps` → all `healthy`
- [ ] `curl localhost:8000/health` → 200 with all checks `up`
- [ ] `docker compose down && up -d` → data still there (criterion 4)
- [ ] `docker compose exec llm ollama run llama3.2:1b "say ok"` answers
- [ ] FastAPI swap done, `/docs` returns generated docs (criterion 3)
