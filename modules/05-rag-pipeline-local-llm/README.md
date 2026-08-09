# Module 05 — RAG Pipeline + Local LLM

**Topics:** Ollama local LLM · prompt optimization (80% reduction) · streaming (SSE) · dual API (standard + streaming) · Gradio UI.

**Build first:** a plain-Python RAG answer flow against a local model — retrieve, prompt, answer — before any framework or server.

**Exercises**
1. Run a local model (Ollama) and answer a question from one chunk, plain Python.
2. Measure prompt size before/after trimming; quantify the speed change.
3. Implement streaming with SSE in plain Python; explain why streaming matters.
4. Write the worst prompt you can, then fix it — document what changed.

**Project — Ask your papers**
A local, private RAG pipeline over the ingested papers: retrieve → generate → stream the answer in a Gradio UI. No cloud APIs, your data stays on your machine.
