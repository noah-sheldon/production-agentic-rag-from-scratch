#!/usr/bin/env python3
"""Module 01 exercises — gate the four lessons (three exercises).

Run:  python3 01_exercises.py

Each exercise has a small automatic check plus manual steps. Where a tool
(Docker, FastAPI) must be present, the check tells you what to install
instead of pretending.

The three exercises:
  1. Run your first containerized app with Docker Compose (no framework).
  2. Add a health check endpoint in plain Python; explain why health checks exist.
  3. Diagram the services + explain what each owns and what /docs generates.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen

# --------------------------------------------------------------------------
# EXERCISE 1 — run your first containerized app with Docker Compose
# --------------------------------------------------------------------------

HELLO_COMPOSE = """\
# Your first compose file: one plain web server, no framework in sight.
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


def write_compose_file(path: str = "hello-compose/compose.yml") -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(HELLO_COMPOSE)
    print(f"wrote {path}")
    return path


def validate_compose(path: str) -> bool:
    if shutil.which("docker") is None:
        print("  docker not found — install Docker Desktop, then re-run.")
        print("  Text check instead:")
        text = open(path, encoding="utf-8").read()
        required = ("services:", "image:", "ports:", "healthcheck:")
        missing = [tok for tok in required if tok not in text]
        print("  missing tokens:", missing or "none — structure looks right")
        return not missing
    result = subprocess.run(
        ["docker", "compose", "-f", path, "config", "-q"],
        capture_output=True, text=True)
    if result.returncode == 0:
        print("  docker compose config: VALID")
        return True
    print("  docker compose config FAILED:")
    print("  " + result.stderr.strip())
    return False


def check_ex1(path: str = "hello-compose/compose.yml") -> bool:
    """Exercise 1 gate: the compose file must validate.

    Then, manually:
        docker compose -f hello-compose/compose.yml up -d
        docker compose -f hello-compose/compose.yml ps
        curl -s localhost:8080 | head -1
        docker compose -f hello-compose/compose.yml down
    Question: what does the STATUS/HEALTH column in `docker compose ps`
    show, and why does that matter for a multi-service stack?
    """
    return validate_compose(path)


# --------------------------------------------------------------------------
# EXERCISE 2 — health check endpoint in plain Python
# --------------------------------------------------------------------------

HEALTH_SPEC = """\
Write `health_server.py` next to this file. Contract (read carefully):

    class HealthHandler(http.server.BaseHTTPRequestHandler):
        # do_GET must answer:
        #   GET /health  -> 200 {"status": "ok"}       when dependency is up
        #   GET /health  -> 503 {"status": "degraded"} when dependency is down
        #   GET /docs    -> 200 (a small HTML stub listing endpoints)
        #   anything else -> 404 {"error": "not found"}

    def set_dependency(up: bool) -> None:
        # Flip the dependency flag the handler reads. The check below calls
        # this to simulate a database dying mid-request.

Starter (copy into health_server.py, then fill the TODOs):

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

        def do_GET(self):  # TODO: implement /health, /docs, 404 per the spec
            self._send_json(501, {"error": "not implemented"})

    if __name__ == "__main__":
        ThreadingHTTPServer(("127.0.0.1", 8000), HealthHandler).serve_forever()

Then explain in a variable `why_health_checks_exist` (string, 3-5 sentences):
why a running process is not the same as a working service, and what a
machine can do with the 200/503 answer.
"""


def check_ex2(module_path: str = "health_server.py") -> bool:
    if not os.path.exists(module_path):
        print("  missing " + module_path + " — create it (spec below).")
        print(HEALTH_SPEC)
        return False
    spec = importlib.util.spec_from_file_location("health_server", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "set_dependency") or not hasattr(module, "HealthHandler"):
        print("  health_server.py must define set_dependency() and HealthHandler.")
        return False

    server = ThreadingHTTPServer(("127.0.0.1", 0), module.HealthHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def probe(path: str):
        with urlopen(f"http://127.0.0.1:{port}{path}", timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode())

    ok = True
    module.set_dependency(True)
    status, body = probe("/health")
    good = status == 200 and body.get("status") == "ok"
    print(f"  dependency up   -> /health {status} {body}  {'PASS' if good else 'FAIL'}")
    ok = ok and good

    module.set_dependency(False)
    status, body = probe("/health")
    good = status == 503 and body.get("status") == "degraded"
    print(f"  dependency down -> /health {status} {body}  {'PASS' if good else 'FAIL'}")
    ok = ok and good

    try:
        status, _ = probe("/docs")
        good = status == 200
        print(f"  /docs stub      -> {status}  {'PASS' if good else 'FAIL'}")
        ok = ok and good
    except Exception as exc:
        print(f"  /docs probe error: {exc}")
        ok = False

    server.shutdown()

    explanation = getattr(module, "why_health_checks_exist", "")
    good = ("alive" in explanation.lower() or "running" in explanation.lower()) and "503" in explanation
    print(f"  explanation mentions alive-vs-ready and 503:  {'PASS' if good else 'FAIL'}")
    ok = ok and good
    return ok


# --------------------------------------------------------------------------
# EXERCISE 3 — diagram the services, what each owns, and FastAPI docs
# --------------------------------------------------------------------------

EX3_QUESTION = """\
Part A — Fill the SERVICES dict: each of the five services in this module's
project maps to a one-line description of WHAT IT OWNS. Then draw the same
picture as a mermaid flowchart in a comment (services as nodes, arrows showing
what calls what).

Part B — Answer in `docs_explanation` (3-5 sentences):
  - What does FastAPI /docs generate, and where does it come from?
  - What is /openapi.json, and who consumes it?
  - Why is generating docs from code better than writing docs by hand?
"""

SERVICES = {
    # "api":    "",  # FastAPI app — what does it own?
    # "db":     "",  # PostgreSQL — what does it own?
    # "search": "",  # OpenSearch — what does it own?
    # "llm":    "",  # Ollama — what does it own?
    # "volumes": "",  # named volumes — what do they own?
}

docs_explanation = ""


def check_ex3(services: dict[str, str]) -> bool:
    expected = {
        "api": "endpoints",
        "db": "metadata",
        "search": "index",
        "llm": "model",
        "volumes": "data",
    }
    ok = True
    for service, keyword in expected.items():
        description = services.get(service, "").lower()
        if not description:
            print(f"  {service}: MISSING — fill SERVICES")
            ok = False
        elif keyword not in description:
            print(f"  {service}: ownership missing '{keyword}': '{description}'")
            ok = False
        else:
            print(f"  {service}: ok — '{description}'")
    lower = docs_explanation.lower()
    good = ("openapi" in lower or "/openapi.json" in lower) and ("type hint" in lower or "signature" in lower)
    print(f"  docs explanation mentions openapi + code-as-source: {'PASS' if good else 'FAIL'}")
    return ok and good


# --------------------------------------------------------------------------
# runner
# --------------------------------------------------------------------------

def main() -> None:
    results = {}
    print("=" * 66)
    print("EXERCISE 1 — first containerized app (Docker Compose, no framework)")
    print("=" * 66)
    path = write_compose_file()
    results["ex1"] = check_ex1(path)
    print()

    print("=" * 66)
    print("EXERCISE 2 — plain-Python health check + why it exists")
    print("=" * 66)
    results["ex2"] = check_ex2()
    print()

    print("=" * 66)
    print("EXERCISE 3 — diagram the services + FastAPI docs")
    print("=" * 66)
    print(EX3_QUESTION)
    results["ex3"] = check_ex3(SERVICES)
    print()

    print("-" * 66)
    passed = sum(1 for v in results.values() if v)
    print(f"{passed}/3 exercises passed")
    for name, ok in results.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL — do it again, then check the solutions'}")
    if passed < 3:
        print("\nStuck? Read the lesson builds again, then check 02_solutions.py.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
