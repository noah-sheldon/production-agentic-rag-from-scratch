# Module 06 — Observability & Caching

**Topics:** Langfuse tracing · Redis caching (cache keys, TTL) · monitoring dashboards (latency, cost) · LLM cost optimization.

**Build first:** measure a RAG answer's latency and token cost with plain timers and token counting before adding any tracing tool.

**Exercises**
1. Measure end-to-end latency and token cost of one answer — plain Python, no tools.
2. Implement a simple cache with TTL in plain Python; show the hit-rate effect.
3. Trace one request through every service; list where time goes.
4. Calculate the cost of 1,000 questions with and without caching — show the 150-400x math.

**Project — Measure and cache**
A Redis cache in front of the RAG pipeline with intelligent cache keys + a dashboard showing latency and cost per query, before/after caching, with real numbers.
