#!/usr/bin/env python3
"""Terminal search over your notes.

Run:  python3 search_cli.py "query" [--tag TAG] [--k N]
"""
from bm25_search import main

if __name__ == "__main__":
    main()
