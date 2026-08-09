# Module 04 — Chunking + Embeddings

**Topics:** section vs fixed-size chunking · chunk overlap · embeddings (the 384 numbers) · cosine similarity by hand · embedding fallbacks.

**Build first:** chunk a document by sections in plain Python; make a 384-number embedding by hand and rank vectors by cosine similarity with no ML libraries — closeness shows up even with random vectors; then chunk the same text at 3 sizes and watch the trade.

**Exercises** (3, gate the lessons)
1. Write a section-based chunker (headings + overlap) in plain Python.
2. Cosine similarity by hand on 384-number vectors — rank them by closeness.
3. Chunk the same text at 3 sizes; write down what each size does to a query.

**Quiz (human-in-the-loop)** — `quizzes/quiz.md`: answered from memory, reviewed by a human. No auto-pass.

**Project — Semantic index of your notes**
A plain-Python index that cuts your notes into sections, turns each section into a 384-number embedding, and answers "what is closest?" by cosine similarity — with a fallback when the embedder is down. Module 03 searched by words; this searches by meaning.
