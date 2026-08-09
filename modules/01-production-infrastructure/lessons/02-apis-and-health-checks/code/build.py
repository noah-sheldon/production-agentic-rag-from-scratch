# requires: (none) — server build, run with --selftest
#!/usr/bin/env python3
"""Lesson 02 build — a health-checked HTTP service from the standard library.

Plain Python, standard library only. No frameworks. Runs on macOS.

Run (server mode):
    python3 build.py --port 8000
    # in another terminal:
    curl -s localhost:8000/health
    curl -s localhost:8000/docs

Run (self-test mode, measures real numbers then exits):
    python3 build.py --selftest
"""

import argparse
import json
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# --- the "dependency" the service depends on ---------------------------
# A real service is only healthy if its dependencies are reachable. Here the
# dependency is simulated with a flag; flip it to see /health go 503 -> 200.
DEPENDENCY_OK = True


def dependency_ok() -> bool:
    """True when the fake upstream dependency is reachable."""
    return DEPENDENCY_OK


def toggle_dependency(value: bool) -> None:
    """Flip the dependency flag (used by the demo's /__fail switch)."""
    global DEPENDENCY_OK
    DEPENDENCY_OK = value


# --- the handlers --------------------------------------------------------
class HealthHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 (http.server API name)
        path = self.path.split("?")[0]

        if path == "/health":
            # The honest answer: 200 only when everything we need works.
            if dependency_ok():
                self._send_json(200, {"status": "ok", "checks": {"dependency": "up"}})
            else:
                self._send_json(
                    503,
                    {"status": "degraded", "checks": {"dependency": "down"}},
                )

        elif path == "/docs":
            # A stub: list the endpoints this service exposes. FastAPI will
            # generate a real, clickable version of this (USE IT beat).
            html = """<!doctype html>
<html><head><title>Service docs (stub)</title></head>
<body><h1>Service docs (stub)</h1>
<ul><li>GET /health — is this service ready?</li>
<li>GET /docs — this page</li></ul>
</body></html>"""
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif path == "/__fail":
            # Demo switch: pretend the dependency just died. This is how a
            # health check earns its keep — it must detect a broken service.
            toggle_dependency(False)
            self._send_json(200, {"note": "dependency marked DOWN"})

        elif path == "/__fix":
            toggle_dependency(True)
            self._send_json(200, {"note": "dependency marked UP"})

        else:
            self._send_json(404, {"error": "not found"})

    def log_message(self, fmt: str, *args) -> None:  # quieter logs
        print(f"[server] {self.address_string()} {fmt % args}")


# --- server lifecycle ------------------------------------------------------
def run_server(port: int = 8000) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer(("127.0.0.1", port), HealthHandler)
    print(f"health service on http://127.0.0.1:{port}/health  (Ctrl+C to stop)")
    return server


def probe(url: str) -> tuple[int, object]:
    """GET a URL; return (status_code, parsed JSON or raw text).

    urllib raises HTTPError for non-2xx statuses — which is exactly the
    case we must probe (a degraded service answers 503).
    """
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8") or "{}")
    try:
        return resp.status, json.loads(raw)
    except json.JSONDecodeError:
        return resp.status, raw[:40]  # /docs returns HTML, not JSON


def selftest() -> None:
    """Start the server in a thread, probe it, measure, then stop."""
    server = run_server(port=0)  # port 0 -> OS picks a free port
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"

    print(f"selftest server on ephemeral port {port}\n")

    started = time.perf_counter()
    status, body = probe(f"{base}/health")
    healthy_ms = (time.perf_counter() - started) * 1000
    print(f"GET /health            -> {status} {body}  ({healthy_ms:.2f} ms)")

    status, body = probe(f"{base}/docs")
    print(f"GET /docs              -> {status} (stub page)")

    # Break the dependency, then ask again: the health check must tell the truth.
    probe(f"{base}/__fail")
    status, body = probe(f"{base}/health")
    print(f"after dependency dies: -> {status} {body}")

    probe(f"{base}/__fix")
    status, body = probe(f"{base}/health")
    print(f"after dependency back: -> {status} {body}")

    print(f"\nMeasured: /health answered in {healthy_ms:.2f} ms with zero")
    print("framework code. A process that is ALIVE is not the same as a")
    print("service that is READY — that is why health checks exist.")
    server.shutdown()


def main() -> None:
    parser = argparse.ArgumentParser(description="stdlib health-check service")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
    else:
        run_server(args.port).serve_forever()


if __name__ == "__main__":
    main()
