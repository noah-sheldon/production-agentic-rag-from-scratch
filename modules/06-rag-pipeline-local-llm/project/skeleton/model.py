"""The answer step — stdlib only.

fake_model   reads the prompt and answers from the context only (grounded:
             no context -> "I don't know", no matching line -> won't guess).
ollama_model calls a real local model over HTTP when Ollama is running.

TODO (lesson USE IT): once Ollama is running on this machine, make
ollama_model the default. It keeps everything else the same — the flow does
not care which model answers.
"""
from __future__ import annotations

import json
import urllib.request

from prompt import STOPWORDS
from retrieve import tokenize

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"


def fake_model(prompt: str) -> str:
    """Stand-in for a local LLM: answers from the context, refuses to guess."""
    if "CONTEXT:" not in prompt or "QUESTION:" not in prompt:
        return "I don't know."
    context = prompt.split("CONTEXT:")[1].split("QUESTION:")[0]
    question = prompt.split("QUESTION:")[1].split("ANSWER:")[0]
    if not context.strip():
        return "I don't know — no notes matched."
    content = {w for w in tokenize(question) if w not in STOPWORDS}
    best, best_hits = None, -1
    for line in context.splitlines():
        hits = len(content & set(tokenize(line)))
        if hits > best_hits:
            best, best_hits = line, hits
    if best_hits > 0:
        return "From your notes: " + best.strip()
    return "I can see notes, but none of them answer this. I won't guess."


def ollama_model(prompt: str) -> str:
    """Call the local Ollama model. Raises OSError when Ollama is not
    running or has not pulled the model. TODO: add a timeout + retry like
    module 02's fetch_with_retry."""
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    return data["response"].strip()
