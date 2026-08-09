# Artifact — Postgres + OpenSearch: one-command start & ownership cheat sheet

Use this the next time you need storage + search locally. It is the same
service pair this course's project ships.

## Part 1 — one-command start (Docker Compose)

`compose.yml`:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: papers
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d papers"]
      interval: 5s
      retries: 5

  search:
    image: opensearchproject/opensearch:2
    environment:
      discovery.type: single-node
      DISABLE_SECURITY_PLUGIN: "true"
    ports: ["9200:9200"]
    volumes: [osdata:/usr/share/opensearch/data]

volumes:
  pgdata:
  osdata:
```

```bash
docker compose up -d
docker compose ps                  # both services, one command
```

Probe the services:

```bash
# Postgres answers SQL
docker compose exec db psql -U app -d papers -c "SELECT version();"

# OpenSearch answers JSON
curl -s localhost:9200/_cluster/health
```

## Part 2 — what each owns (the cheat sheet)

| Question | Answered by | Why |
|---|---|---|
| "Store the paper metadata" | PostgreSQL | facts with schema, durable, queryable in SQL |
| "Store pipeline state / retry counters" | PostgreSQL | one source of truth, transactional |
| "Find the 20 best matches for 'rag retrieval'" | OpenSearch | inverted index + relevance ranking |
| "Count papers by year" | PostgreSQL | SQL aggregation, exact |
| "Rank by keyword relevance" | OpenSearch | BM25 scoring built in |

**Rule of thumb:** if the question is "give me the row", it is the database's
job. If the question is "rank the best matches", it is the search engine's job.
One of each, never one tool doing both badly.
