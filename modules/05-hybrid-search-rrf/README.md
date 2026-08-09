# Module 05 — Hybrid Search (RRF)

**Topics:** Reciprocal Rank Fusion (RRF) · keyword + semantic search together · when hybrid wins (and when it doesn't) · one unified search API.
**Math you'll meet:** RRF fusion — rank arithmetic only (1/(k+rank)).

**Build first:** fuse two ranked lists — one from keyword search, one from semantic search — with RRF in plain Python. See why merging by *position* beats merging by *score*.

**Exercises** (3, gate the lessons)
1. Implement RRF on two ranked lists; reproduce the merged order by hand.
2. Mine queries where keyword wins alone, semantic wins alone, and fusion finds both.
3. Build the unified API: one function with `mode=keyword|semantic|hybrid`, same inputs, same output shape.

**Quiz (human-in-the-loop)** — `quizzes/quiz.md`: answered from memory, reviewed by a human. No auto-pass.

**Project — Hybrid search over your notes**
One engine over your own notes with three modes — keyword, semantic, hybrid — and RRF to fuse them. You measure which mode wins per query, and you document the honest limits.
