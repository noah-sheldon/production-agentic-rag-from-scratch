"""Build it: SSE-style streaming in plain Python (stdlib only).

Run:  python3 build.py

Part 1 — the FORMAT: a generator yields the answer one token at a time, and
each token is wrapped in a Server-Sent Events frame (data: ...\\n\\n).

Part 2 — the DELIVERY: a tiny HTTP server streams those events over the
network; a client reads them one by one and prints each token the moment it
arrives. You will see the answer appear word by word, and the numbers will
show why: first-token latency is tiny, total latency is not.

In a terminal you can also watch it live: curl -N http://127.0.0.1:<port>/stream
(the build prints the port before it starts).
"""
from __future__ import annotations

import json
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# the "answer" a model would generate (token by token, with a real delay)
ANSWER = (
    "Ollama runs large language models on your own machine, fully local. "
    "No API keys, no cloud. Your notes never leave your laptop."
)
TOKEN_DELAY = 0.05  # seconds per token — how fast a small local model talks


# --- part 1: the generator and the SSE frame ---


def token_stream(text: str, delay: float = TOKEN_DELAY):
    """Yield the answer one token at a time, like a real LLM does.

    A generator is lazy: nothing is produced until someone asks. Each
    `next()` call does a tiny bit of work and yields one token.
    """
    for word in text.split():
        yield word
        time.sleep(delay)


def sse_event(data: str) -> str:
    """Wrap one payload in the Server-Sent Events frame: data line, blank line."""
    return f"data: {data}\n\n"


def make_stream_events(text: str):
    """Turn the token generator into SSE frames."""
    for token in token_stream(text):
        yield sse_event(json.dumps({"token": token}))


# --- part 2: the delivery (a tiny SSE server) ---


class SSEHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        # text/event-stream tells the client: keep this connection open,
        # more data is coming.
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        for event in make_stream_events(ANSWER):
            self.wfile.write(event.encode())
            self.wfile.flush()  # push it NOW — never wait for a buffer

    def log_message(self, *args) -> None:
        pass  # keep the console quiet


def run_client(url: str) -> None:
    """Read the stream the way a browser would, and time what the user feels."""
    t0 = time.perf_counter()
    first_seen: float | None = None
    tokens: list[str] = []
    with urllib.request.urlopen(url) as resp:
        for raw in resp:  # one line as soon as the server sends it
            line = raw.decode().strip()
            if not line.startswith("data:"):
                continue
            if first_seen is None:
                first_seen = time.perf_counter() - t0
            tokens.append(json.loads(line[5:].strip())["token"])
    total = time.perf_counter() - t0
    print(f"\n  client got {len(tokens)} tokens")
    print(f"  first token after   {first_seen * 1000:6.1f} ms")
    print(f"  whole answer after  {total * 1000:6.1f} ms")
    print(f"  -> the user starts reading {(total / max(first_seen, 1e-9)):.0f}x sooner than with a non-streaming answer")


def main() -> None:
    print("== part 1: the raw SSE format ==")
    print("   (this is exactly what goes over the wire)\n")
    for event in make_stream_events(ANSWER):
        print(event, end="")
    print("== end of stream (a real stream ends with data: [DONE])\n")

    server = ThreadingHTTPServer(("127.0.0.1", 0), SSEHandler)  # port 0 = OS picks one
    port = server.server_address[1]
    print(f"== part 2: streaming over HTTP ==")
    print(f"   server on http://127.0.0.1:{port}/stream")
    print(f"   watch it live in another terminal: curl -N http://127.0.0.1:{port}/stream")
    print("   client connecting...\n")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        run_client(f"http://127.0.0.1:{port}/stream")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
