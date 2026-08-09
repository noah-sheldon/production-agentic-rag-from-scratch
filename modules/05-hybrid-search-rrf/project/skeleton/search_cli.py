#!/usr/bin/env python3
"""Terminal hybrid search over your notes.

Run:
    python3 search_cli.py "postgres timeout"                    (hybrid)
    python3 search_cli.py "postgres timeout" --mode keyword
    python3 search_cli.py "postgres timeout" --mode semantic --k 3
    python3 search_cli.py --measure   # precision table (replace labels)
"""
import argparse

from hybrid_search import HybridSearch

# Your labeled queries: title -> set of relevant note stems.
# Replace with YOUR queries once you drop in your own notes.
LABELED_QUERIES = [
    ("postgres timeout", {"postgres-timeout", "postgres-config"}),
    ("timeout config", {"postgres-config", "python-requests"}),
    ("api client slow", {"api-client-hangs"}),
]


def measure(engine: HybridSearch, k: int = 3) -> None:
    print(f"precision@{k} per mode on {len(LABELED_QUERIES)} labeled queries")
    print(f"{'query':<22} {'keyword':>8} {'semantic':>9} {'hybrid':>8}")
    for query, relevant in LABELED_QUERIES:
        row = []
        for mode in ("keyword", "semantic", "hybrid"):
            results = engine.search(query, mode=mode, k=k)
            hits = sum(1 for _s, title in results if title in relevant)
            row.append(hits / k)
        print(f"{query:<22} {row[0]:8.2f} {row[1]:9.2f} {row[2]:8.2f}")
    print("\nWrite these numbers (with YOUR queries) into RESULTS.md.")


def main() -> None:
    parser = argparse.ArgumentParser(description="hybrid search over your notes")
    parser.add_argument("query", nargs="?", default=None, help="the question")
    parser.add_argument("--mode", default="hybrid",
                        choices=["hybrid", "keyword", "semantic"])
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--measure", action="store_true",
                        help="print the precision table instead of searching")
    args = parser.parse_args()

    engine = HybridSearch()
    if args.measure or args.query is None:
        measure(engine, k=2)
        return
    for score, title in engine.search(args.query, mode=args.mode, k=args.k):
        print(f"  {score:8.4f}  {title}")


if __name__ == "__main__":
    main()
