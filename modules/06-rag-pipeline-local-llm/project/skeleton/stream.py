"""SSE-style token streaming — stdlib only.

TODO (lesson 03): stream from the real Ollama model (set "stream": true in
the API call) so the tokens arrive while the model is still generating, not
only while the CLI prints a finished reply.
"""
from __future__ import annotations

import time


def sse_event(data: str) -> str:
    """One Server-Sent Events frame: data line + blank line."""
    return f"data: {data}\n\n"


def token_stream(text: str, delay: float = 0.03):
    """Yield the words of the reply one at a time, like a model streaming."""
    for word in text.split():
        yield word
        time.sleep(delay)
