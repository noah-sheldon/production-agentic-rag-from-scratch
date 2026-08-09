#!/usr/bin/env python3
"""Module 01 project skeleton — plain-Python health endpoint.

Standard library only, so it runs on macOS AND inside the compose container
without any pip installs.

Run standalone on macOS:
    python3 app.py --port 8000
    curl -s localhost:8000/health

Run the full stack (see compose.yml):
    docker compose up -d
    docker compose ps          # health of every service, one command
    curl -s localhost:8000/health

One-shot mode (for scripts):
    python3 app.py --once

TODOs — the point of this skeleton. Each maps to a lesson in module 01:
  [ ] Swap the stdlib server for FastAPI (lesson 02 USE IT). Keep /health,
      get real automatic docs at /docs for free.
  [ ] Make the db probe honest: open a real SQL connection and run
      `SELECT 1`, not just a TCP connect (lesson 03).
  [ ] Probe Ollama for a loaded model by name, not just "server answers".
  [ ] Move probes into their own module and add tests (lesson 04).
  [ ] Add type hints and run mypy + pre-commit on this file (lesson 04).
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB_HOST = os.environ.get("SERVICE_DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("SERVICE_DB_PORT", "5432"))
SEARCH_URL = os.environ.get("SERVICE_SEARCH_URL", "http://127.0.0.1:9200")
LLM_URL = os.environ.get("SERVICE_LLM_URL", "http://127.0.0.1:11434")

TODO_COUNT = 5  # keep in sync with the TODO list at the top of this file


def probe_tcp(host: str, port: int) -> tuple[str, float]:
    """Probe a service by opening a TCP connection (fast, but shallow)."""
    started = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=2.0):
            return "up", (time.perf_counter() - started) * 1000
    except OSError:
        return "down", (time.perf_counter() - started) * 1000


def probe_http(url: str, path: str) -> tuple[str, float]:
    """Probe an HTTP service; 'up' only when it answers 200 with JSON."""
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(f"{url}{path}", timeout=3.0) as resp:
            if resp.status == 200:
                return "up", (time.perf_counter() - started) * 1000
            return "degraded", (time.perf_counter() - started) * 1000
    except OSError:
        return "down", (time.perf_counter() - started) * 1000


def collect_health() -> dict:
    """Ask every dependency, measure each, and aggregate the verdict."""
    checks = {}
    checks["db"], latency = probe_tcp(DB_HOST, DB_PORT)
    checks["db_latency_ms"] = round(latency, 1)
    checks["search"], latency = probe_http(SEARCH_URL, "/_cluster/health")
    checks["search_latency_ms"] = round(latency, 1)
    checks["llm"], latency = probe_http(LLM_URL, "/api/tags")
    checks["llm_latency_ms"] = round(latency, 1)

    required = [checks[name] for name in ("db", "search", "llm")]
    status = "ok" if all(state == "up" for state in required) else "degraded"
    return {
        "status": status,
        "service": "knowledge-assistant-skeleton",
        "checks": checks,
        "todos_remaining": TODO_COUNT,
    }


class HealthHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 (http.server API name)
        path = self.path.split("?")[0]
        if path == "/health":
            health = collect_health()
            status = 200 if health["status"] == "ok" else 503
            self._send_json(status, health)
        elif path == "/docs":
            html = """<!doctype html>
<html><head><title>Knowledge assistant skeleton — docs stub</title></head>
<body><h1>Docs (stdlib stub — FastAPI will generate this)</h1>
<ul><li>GET /health — every service's state in one answer</li>
<li>GET /docs — this page</li></ul>
<p>TODO: replace this whole server with FastAPI to get real docs.</p>
</body></html>"""
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self._send_json(404, {"error": "not found"})

    def log_message(self, fmt: str, *args) -> None:
        print(f"[app] {fmt % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description="knowledge assistant skeleton")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--once", action="store_true", help="print health and exit")
    args = parser.parse_args()

    if args.once:
        print(json.dumps(collect_health(), indent=2))
        return

    server = ThreadingHTTPServer(("0.0.0.0", args.port), HealthHandler)
    print(f"knowledge-assistant skeleton on http://0.0.0.0:{args.port}/health")
    print(f"probes -> db {DB_HOST}:{DB_PORT} | search {SEARCH_URL} | llm {LLM_URL}")
    print(f"TODOs remaining: {TODO_COUNT} (see the header of app.py)")
    server.serve_forever()


if __name__ == "__main__":
    main()
