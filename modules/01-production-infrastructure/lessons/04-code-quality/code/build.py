#!/usr/bin/env python3
"""Lesson 04 build — a small, lint-clean module with three tests.

Plain Python, standard library only. Runs on macOS. No pytest needed to run
it — but the same test functions run under pytest untouched (USE IT beat).

This file is written to pass Ruff's default rules (ruff check build.py):
docstrings on public functions, no unused imports, no undefined names.
Run it:

    python3 build.py            # runs the three tests, prints PASS/FAIL
    ruff check build.py         # the USE IT beat: must say "All checks passed"
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Paper:
    """One paper in the curator's library."""

    slug: str
    year: int
    title: str


def normalize_slug(title: str) -> str:
    """Turn a title into a url-safe slug: lowercase, dashes for spaces."""
    words = title.strip().lower().split()
    return "-".join(words)


def is_recent(paper: Paper, cutoff_year: int = 2022) -> bool:
    """True when the paper is newer than or equal to the cutoff year."""
    return paper.year >= cutoff_year


def keyword_hits(paper: Paper, words: list[str]) -> int:
    """Count how many of the given words appear in the paper's title."""
    haystack = paper.title.lower()
    return sum(1 for word in words if word in haystack)


# --- the three tests -------------------------------------------------------
# Plain functions with assertions. pytest discovers them by name; this file
# also runs them directly so the build works with zero dependencies.


def test_normalize_slug() -> None:
    assert normalize_slug("Retrieval Augmented Generation") == "retrieval-augmented-generation"
    assert normalize_slug("  BM25   Revisited  ") == "bm25-revisited"


def test_is_recent() -> None:
    old = Paper(slug="bert", year=2018, title="BERT Pre-training")
    new = Paper(slug="rag-fusion", year=2023, title="RAG Fusion")
    assert is_recent(old) is False
    assert is_recent(new) is True
    assert is_recent(Paper(slug="edge", year=2022, title="Edge Case")) is True


def test_keyword_hits() -> None:
    paper = Paper(slug="rag-fusion", year=2023, title="RAG Fusion for Retrieval")
    assert keyword_hits(paper, ["rag", "retrieval"]) == 2
    assert keyword_hits(paper, ["vector"]) == 0
    assert keyword_hits(paper, []) == 0


def _run_tests() -> None:
    """Run the test functions and report pass/fail, no framework needed."""
    tests = [test_normalize_slug, test_is_recent, test_keyword_hits]
    failures = 0
    for test in tests:
        try:
            test()
            print(f"PASS  {test.__name__}")
        except AssertionError as exc:
            failures += 1
            print(f"FAIL  {test.__name__}: {exc}")
    total = len(tests)
    print(f"\n{total - failures}/{total} tests passed")
    if failures:
        raise SystemExit(1)
    print("green — this module is safe to build on.")


if __name__ == "__main__":
    _run_tests()
