# Artifact — the unified search API contract

```python
class SearchEngine:
    def __init__(self, notes): ...        # index once
    def search(self, query, mode="hybrid", k=3):
        """mode: 'keyword' | 'semantic' | 'hybrid'
        Returns [(score, text)] sorted best first. Always."""
        ...
```

The contract:

- **Same inputs for every mode** — `query`, `mode`, `k`. No mode-specific
  arguments, no mode-specific callers.
- **Same output shape for every mode** — a sorted list of `(score, text)`
  pairs. Callers read it the same way no matter the mode.
- **Mode is a parameter, not a fork** — no `if` chains in app code.
- **Unknown modes fail loudly** (`ValueError`), never silently.
- **Measure the modes** — latency and precision on labeled queries (lesson
  02 mining + this lesson's measurement) are the only honest way to choose
  a default mode.
- **Swap internals freely** — the contract is why you can replace the
  stand-in semantic engine with real embeddings (Module 06) without
  touching a single caller.
