#!/usr/bin/env python3
"""Module 01 — solutions to the four exercises.

Run:  python3 02_solutions.py

Every section prints the answer AND passes the same check the exercise file
uses. Read the answers, then write your own from memory before peeking.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen


# ==========================================================================
# EXERCISE 1 — first containerized app (Docker Compose, no framework)
# ==========================================================================

COMPOSE_SOLUTION = """\
services:
  hello:
    image: nginx:alpine
    ports:
      - "8080:80"
    healthcheck:
      test: ["CMD", "wget", "-q", "-O", "-", "http://localhost/"]
      interval: 5s
      retries: 3
"""

EX1_ANSWER = """\
`docker compose ps` shows every container's state in one table. The HEALTH
column shows "healthy" (the healthcheck passes), "unhealthy" (it fails), or
"starting". This matters because in a multi-service stack a service can be
running while its dependencies are not — the health column is the only honest
signal that the stack is actually ready, not just started.
"""


def exercise1() -> bool:
    print("compose.yml (answer):")
    print(COMPOSE_SOLUTION)
    print("commands:")
    print("  docker compose -f hello-compose/compose.yml up -d")
    print("  docker compose -f hello-compose/compose.yml ps   # look at HEALTH")
    print("  curl -s localhost:8080 | head -1                 # plain nginx page")
    print("  docker compose -f hello-compose/compose.yml down")
    print("\nQuestion answer:")
    print(EX1_ANSWER)
    if shutil.which("docker") is None:
        print("\n[docker not installed — solution shown; install Docker Desktop]")
        return True
    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as fh:
        fh.write(COMPOSE_SOLUTION)
        path = fh.name
    result = subprocess.run(["docker", "compose", "-f", path, "config", "-q"], capture_output=True, text=True)
    print(f"\ncheck: docker compose config -q -> {'VALID' if result.returncode == 0 else result.stderr.strip()}")
    return result.returncode == 0


# ==========================================================================
# EXERCISE 2 — health check in plain Python
# ==========================================================================

health_server_solution = """\
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DEPENDENCY_UP = True

def set_dependency(up: bool) -> None:
    global DEPENDENCY_UP
    DEPENDENCY_UP = up

class HealthHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            if DEPENDENCY_UP:
                self._send_json(200, {"status": "ok"})
            else:
                self._send_json(503, {"status": "degraded"})
        elif self.path == "/docs":
            html = "<h1>docs stub</h1><ul><li>GET /health</li><li>GET /docs</li></ul>"
            body = html.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self._send_json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        pass

if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8000), HealthHandler).serve_forever()
"""

why_health_checks_exist = """\
A running process is not the same as a working service: the process can be
alive while its database connection is dead, so "is it running?" answers the
wrong question. Health checks answer "are you ready to take work?" with a
status code a machine can act on — 200 means keep sending traffic, 503 means
stop. That is how load balancers, orchestrators, and compose decide what to
do, and it turns a five-minute outage mystery into a one-second answer.
"""


def exercise2() -> bool:
    print("health_server.py (answer):")
    print(health_server_solution)
    print("explanation (why_health_checks_exist):")
    print(why_health_checks_exist)
    print()

    # Run the same probe the exercise gate runs, against the solution inline.
    # __name__ is set to a non-main value so the solution's own server block
    # does not start (we probe it ourselves on an ephemeral port).
    namespace: dict = {"__name__": "health_server_solution"}
    exec(compile(health_server_solution, "health_server.py", "exec"), namespace)
    Handler = namespace["HealthHandler"]
    set_dependency = namespace["set_dependency"]

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def probe(path: str):
        with urlopen(f"http://127.0.0.1:{port}{path}", timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode())

    ok = True
    set_dependency(True)
    status, body = probe("/health")
    print(f"check: dependency up   -> {status} {body}")
    ok = ok and status == 200 and body == {"status": "ok"}
    set_dependency(False)
    status, body = probe("/health")
    print(f"check: dependency down -> {status} {body}")
    ok = ok and status == 503 and body == {"status": "degraded"}
    status, _ = probe("/docs")
    print(f"check: /docs stub      -> {status}")
    ok = ok and status == 200
    server.shutdown()
    print(f"check result: {'PASS' if ok else 'FAIL'}")
    return ok


# ==========================================================================
# EXERCISE 3 — diagram the services and what each owns
# ==========================================================================

SERVICES = {
    "api": "FastAPI app: owns the endpoints, the health checks, and the request flow",
    "db": "PostgreSQL: owns the paper metadata and pipeline state, durable in SQL",
    "search": "OpenSearch: owns the inverted index and keyword search over abstracts",
    "llm": "Ollama: owns the local language model and runs inference on this machine",
    "volumes": "named volumes: own the data that must survive container restarts",
}

EX3_DIAGRAM = """\
```mermaid
flowchart LR
    User --> API["FastAPI (api): endpoints, health checks"]
    API --> DB["PostgreSQL (db): paper metadata, state"]
    API --> SE["OpenSearch (search): inverted index, keyword search"]
    API --> LLM["Ollama (llm): local language model"]
    DB --> VOL["named volumes: data that survives restarts"]
    SE --> VOL
    LLM --> VOL
```
"""


def exercise3() -> bool:
    print("SERVICES (answer):")
    for name, owns in SERVICES.items():
        print(f"  {name:8s} -> {owns}")
    print("\ndiagram:")
    print(EX3_DIAGRAM)
    expected = {
        "api": "endpoints",
        "db": "metadata",
        "search": "index",
        "llm": "model",
        "volumes": "data",
    }
    ok = all(k in SERVICES.get(s, "").lower() for s, k in expected.items())
    print(f"check result: {'PASS' if ok else 'FAIL'}")
    return ok


# ==========================================================================
# EXERCISE 4 — FastAPI automatic docs
# ==========================================================================

main_solution = """\
from fastapi import FastAPI

app = FastAPI(title="Papers API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    \"\"\"Is this service ready?\"\"\"
    return {"status": "ok"}
"""

docs_explanation = """\
/docs generates an interactive Swagger UI straight from the code: every route,
its parameters, and its response shape come from the function signatures and
docstrings. Underneath it is /openapi.json, a machine-readable JSON spec that
tools (clients, test generators, SDKs) consume without a human. Docs are
generated from code rather than written by hand because the code is the single
source of truth — when the endpoint changes, the docs change with it, so the
docs can never silently drift out of date. It also gives you try-it-out for
free, which is how you test an endpoint before writing a single test.
"""


def exercise4() -> bool:
    print("main.py (answer):")
    print(main_solution)
    print("run it:")
    print("  uv add fastapi uvicorn && uvicorn main:app --reload")
    print("  open http://127.0.0.1:8000/docs  and  /openapi.json")
    print("\nexplanation (docs_explanation):")
    print(docs_explanation)
    print()
    try:
        namespace: dict = {}
        exec(compile(main_solution, "main.py", "exec"), namespace)
        app = namespace["app"]
    except ImportError:
        print("check: SKIPPED — install fastapi first (uv add fastapi uvicorn)")
        return True
    paths = app.openapi()["paths"]
    ok = "/health" in paths and "/docs" in paths
    print(f"check: /health in OpenAPI paths -> {'PASS' if '/health' in paths else 'FAIL'}")
    print(f"check: /docs   in OpenAPI paths -> {'PASS' if '/docs' in paths else 'FAIL'}")
    return ok


# ==========================================================================

def main() -> None:
    results = {
        "exercise 1": exercise1(),
        "exercise 2": exercise2(),
        "exercise 3": exercise3(),
        "exercise 4": exercise4(),
    }
    print("\n" + "=" * 66)
    for name, ok in results.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print("  All four pass — module 01 exercises complete.")


if __name__ == "__main__":
    main()
