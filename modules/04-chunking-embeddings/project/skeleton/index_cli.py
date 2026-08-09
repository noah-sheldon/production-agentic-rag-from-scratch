#!/usr/bin/env python3
"""Terminal interface to your semantic index.

Run:
  python3 index_cli.py build                     # chunk + embed notes/ -> index.json
  python3 index_cli.py search "giant rodent"     # what is closest? (top 3)
  python3 index_cli.py search "giant rodent" --k 5
"""
import sys

from semantic_index import build_index, search


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    if args[0] == "build":
        build_index()
        return
    if args[0] == "search":
        k = 3
        if "--k" in args:
            k = int(args[args.index("--k") + 1])
            args = args[: args.index("--k")]
        query = " ".join(args[1:]) or "giant rodent"
        print(f"query: {query!r}\n")
        for hit in search(query, k=k):
            print(f"  {hit['score']:.3f}  {hit['note']} :: {hit['heading']}")
            print(f"        {hit['text'][:80]}...")
        return
    print(__doc__)


if __name__ == "__main__":
    main()
