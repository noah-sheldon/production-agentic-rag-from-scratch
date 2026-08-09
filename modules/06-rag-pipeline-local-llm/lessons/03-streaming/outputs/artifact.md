# Artifact — the SSE streaming pattern

Send the answer token by token. Users feel the first token, not the last.

```python
def sse_event(data: str) -> str:
    return f"data: {data}\n\n"          # the frame: data line + blank line

def token_stream(text):                  # the generator: lazy, one token at a time
    for word in text.split():
        yield word
        time.sleep(delay)
```

Checklist:

- [ ] Generator, not a list — the model produces tokens lazily
- [ ] Frame every payload: `data: <json or text>\n\n`
- [ ] `Content-Type: text/event-stream` + `Cache-Control: no-cache`
- [ ] **Flush after every event** — never let the buffer hold the stream
- [ ] Measure first-token latency AND total latency; report both
- [ ] End the stream cleanly (`data: [DONE]` for the OpenAI-style format)
- [ ] Stream when a human waits; skip it for short answers and offline batches
