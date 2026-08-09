# 03 — The Unified Search API

## MOTTO
> One door, three rooms: same question, same answer shape — you pick the search.

## PROBLEM
By now you have two search functions with different names, different inputs, and different output shapes — one returns scores around `1.19`, the other around `0.83`. Your app code forks everywhere: `if query looks exact: keyword; else: semantic`. Adding hybrid means a third branch. This is how search code rots — every caller knows every engine.

## CONCEPT
A [unified API](../../../../glossary.md#api) hides the engines behind ONE function. The caller passes a `mode` parameter — `keyword`, `semantic`, or `hybrid` — and gets the same shape back every time: a list of `(score, text)` pairs, best first. Callers never change when an engine changes inside. The `k` (how many results) is a plain parameter. The mode is a choice, not a fork.

```mermaid
flowchart LR
    CALLER["search(query, mode, k)"] --> R{which mode?}
    R -->|keyword| K[keyword scores]
    R -->|semantic| S[semantic scores]
    R -->|hybrid| F[RRF fusion]
    K --> OUT[(score, text) list]
    S --> OUT
    F --> OUT
    OUT --> APP[app code — never changes]
```

## BUILD IT

```bash
python3 lessons/03-unified-search-api/code/build.py
```

One `SearchEngine` class, one `search(query, mode='hybrid', k=3)` method. The build calls all three modes with IDENTICAL arguments on the same 8 notes, then MEASURES: latency per mode (keyword `0.01 ms`, semantic `0.08 ms`, hybrid `0.09 ms` — fusion pays for both engines) and precision@2 on the three labeled queries. No mode wins everything — the numbers say so.

## USE IT
OpenSearch, Elasticsearch, and pgvector expose similar unified APIs — one request, a mode/parameter, a fixed response shape.

| The framework gives you | The framework hides from you |
|---|---|
| a hybrid endpoint out of the box | that keyword and semantic may run on different clusters |
| query DSL with mode switches | the fusion weights and where scores come from |
| a stable response schema | latency: you still pay for BOTH engines |

Honest trade-off: a framework API saves the wiring, but the interface contract — same inputs, same shape, mode as a parameter — is a design decision you just made yourself.

## SHIP IT
The `SearchEngine` contract — `outputs/artifact.md` — the one-function search API for your notes.
