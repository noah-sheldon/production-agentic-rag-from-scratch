# Module 04 — Chunking & Hybrid Search

**Topics:** section-based chunking with overlap · embeddings (Jina AI + fallbacks) · hybrid search with RRF fusion · unified API · trade-offs.

**Build first:** chunk a document by sections in plain Python; embed with a local model; fuse two ranked lists with RRF by hand — see why hybrid beats either alone.

**Exercises**
1. Write a section-based chunker (headings, overlap) in plain Python.
2. Implement RRF fusion on two ranked lists; show when fusion wins.
3. Find one query where keyword wins and one where semantic wins — same documents.
4. Design the fallback chain: embedding provider down → what happens?

**Project — Hybrid search endpoint**
One API endpoint supporting keyword, semantic, and hybrid modes over the same corpus; benchmark all three on your test questions; document the trade-offs.
