# Module 03 — Keyword Search First (BM25)

**Topics:** why keyword search is the foundation · OpenSearch index/mappings · BM25 math · Query DSL (filters, boosting) · search analytics (precision, recall, relevance).
**Math you'll meet:** One formula, by hand in lesson 01: IDF (arithmetic + log). k1 and b are two knobs, not theorems.

**Build first:** BM25 by hand in plain Python on a few documents — understand the formula, then import the engine.

**Exercises**
1. Implement BM25 scoring on 5 documents with plain Python; rank a query.
2. Explain the two BM25 knobs (k1, b) in simple words; show what each changes.
3. Write three queries: exact term, filtered, boosted — compare results.
4. Measure precision/recall on a small set; say which is worse for your use case and why.

**Project — Your own search engine**
A keyword search over your own documents (docs, notes, code) using BM25 — ranked results, filters, and a relevance measurement. No vector search allowed yet.
