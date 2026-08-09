# Artifact — Containerize anything: the 5-point checklist

Use this checklist the next time you need to run a service in a container.
It applies to every service in this course's stack.

## The checklist

1. **Base image** — start from a small official image (e.g. `python:3.12-slim`),
   never from a huge kitchen-sink image. Smaller image = less to patch, faster pulls.
2. **One service per container** — the box runs one process. No "postgres and
   redis in the same container" shortcuts; you lose isolation the moment you cheat.
3. **Ports are doors** — publish only what the outside world needs (`ports: "8000:8000"`).
   Internal services (db, search) stay inside the compose network, unreachable from your laptop.
4. **Volumes for data that must survive** — a database file inside a container dies
   with the container. Put it in a named [volume](../../../../glossary.md#volume):
   `volumes: - pgdata:/var/lib/postgresql/data`.
5. **Health over hope** — give every long-running service a `healthcheck` so
   `docker compose ps` shows you real state, not a guess (Lesson 02).

## The one command

```bash
docker compose up -d      # start every service from compose.yml
docker compose ps         # one command, every service's state
docker compose logs -f    # follow all logs at once
docker compose down       # stop, keep volumes
docker compose down -v    # stop AND delete volumes (data gone — careful)
```

## Trade-off reminder

Containers share the host kernel. You get filesystem + network isolation, not
full machine isolation. For hostile code, use a VM. For your own stack, a
container is the right amount of box.
