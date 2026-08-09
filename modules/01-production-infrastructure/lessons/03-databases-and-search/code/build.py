#!/usr/bin/env python3
"""Lesson 03 build — a persistent store and a keyword lookup.

Plain Python, standard library only (sqlite3 is part of stdlib).
Runs on macOS. No Docker needed.

Run:  python3 build.py

You will see:
  1. Rows written to a real on-disk database, the connection closed, the
     database reopened — the data is still there (persistence).
  2. A naive keyword lookup that scores every row by how many times the query
     words appear — and its measured cost.
  3. An indexed lookup on a column — and its measured cost. Same data, two
     speeds, because the index exists.
"""

import sqlite3
import tempfile
import time

PAPERS = [
    ("attention-is-all-you-need", 2017, "Attention Is All You Need", "Transformer model with self-attention for sequence tasks"),
    ("bert-pre-training", 2018, "BERT: Pre-training of Deep Bidirectional Transformers", "Pre-training deep bidirectional transformers for language understanding"),
    ("rag-fusion", 2023, "RAG Fusion: a New Take on Retrieval-Augmented Generation", "RAG fusion combines multiple retrieval results for better answers"),
    ("retrieval-augmented-generation", 2020, "Retrieval-Augmented Generation for Knowledge-Intensive Tasks", "Retrieval-augmented generation grounds language models in documents"),
    ("long-context-transformers", 2024, "Long-Context Transformers beyond 1M Tokens", "Long-context transformers extend attention to very long inputs"),
    ("vector-databases-review", 2023, "A Survey of Vector Databases", "A review of vector databases for similarity search at scale"),
    ("bm25-revisited", 2022, "BM25 Revisited: Keyword Search without Neural Models", "BM25 revisited: modern keyword search ranking without neural models"),
    ("semantic-search-applications", 2024, "Semantic Search in Production", "Semantic search applications in production information retrieval"),
    ("tiny-llms-on-laptops", 2025, "Tiny LLMs on Laptops", "Tiny language models that run on laptops with modest hardware"),
    ("prompt-engineering-benchmarks", 2024, "Benchmarking Prompt Engineering", "Benchmarks for prompt engineering techniques on RAG pipelines"),
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    id INTEGER PRIMARY KEY,
    slug TEXT NOT NULL,
    year INTEGER NOT NULL,
    title TEXT NOT NULL,
    abstract TEXT NOT NULL
)
"""


def open_db(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def seed(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM papers")
    conn.executemany(
        "INSERT INTO papers (slug, year, title, abstract) VALUES (?, ?, ?, ?)",
        PAPERS,
    )
    conn.commit()


def keyword_lookup(conn: sqlite3.Connection, query: str, top_k: int = 3) -> list[tuple]:
    """Naive keyword search: scan every row, count query-word hits.

    This is the honest baseline — no index, no ranking model, just counting.
    """
    words = [w.lower() for w in query.split()]
    results: list[tuple] = []
    for row in conn.execute("SELECT slug, year, title, abstract FROM papers"):
        slug, year, title, abstract = row
        haystack = f"{title} {abstract}".lower()
        score = sum(1 for w in words if w in haystack)
        if score:
            results.append((score, slug, year, title))
    results.sort(key=lambda item: item[0], reverse=True)
    return results[:top_k]


def indexed_lookup(conn: sqlite3.Connection, slug: str) -> list[tuple]:
    """Exact lookup on the slug column — WITH and WITHOUT an index."""
    return list(conn.execute("SELECT slug, year, title FROM papers WHERE slug = ?", (slug,)))


def timed(label: str, fn) -> None:
    started = time.perf_counter()
    result = fn()
    elapsed_ms = (time.perf_counter() - started) * 1000
    print(f"{label}: {elapsed_ms:.3f} ms")
    return result


def main() -> None:
    path = tempfile.mktemp(prefix="papers-", suffix=".db")
    print(f"database file: {path}\n")

    # --- persistence: write, close, reopen ---
    conn = open_db(path)
    seed(conn)
    count = conn.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
    print(f"inserted {count} papers, closing the connection...")
    conn.close()

    conn = open_db(path)  # same file, brand-new connection
    count = conn.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
    print(f"reopened the file: {count} papers still there (persistence works)\n")

    # --- keyword lookup: the naive scan ---
    print("naive keyword lookup (scans every row, counts word hits):")
    hits = timed(
        "  'rag retrieval' on 10 rows",
        lambda: keyword_lookup(conn, "rag retrieval"),
    )
    for score, slug, year, title in hits:
        print(f"    score={score}  {year}  {title[:50]}")
    print()

    # --- the same scan at real scale: cost grows with rows ---
    conn.execute(
        "INSERT INTO papers (slug, year, title, abstract) "
        "SELECT 'filler-' || id, 2024, 'filler row', 'lorem ipsum keyword padding' "
        "FROM (WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c LIMIT 10000) SELECT x AS id FROM c)"
    )
    conn.commit()
    timed("  same query on ~10,010 rows (full scan)", lambda: keyword_lookup(conn, "rag retrieval"))
    print()

    # --- indexed lookup: build the index once, query fast ---
    print("exact lookup on the slug column:")
    timed("  without index", lambda: indexed_lookup(conn, "bm25-revisited"))
    conn.execute("CREATE INDEX idx_papers_slug ON papers (slug)")
    conn.commit()
    timed("  with index", lambda: indexed_lookup(conn, "bm25-revisited"))
    print()
    print("The index is the reason databases and search engines scale:")
    print("build the structure once, answer queries without scanning everything.")
    conn.close()


if __name__ == "__main__":
    main()
