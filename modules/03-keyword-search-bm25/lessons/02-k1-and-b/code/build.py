"""Build it: how k1 and b change BM25 rankings.

Run:  python3 build.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "01-bm25-by-hand" / "code"))
from build import DOCS, bm25

QUERY = "deploy runs at 3am"

if __name__ == "__main__":
    for label, k1, b in [("k1=0,  b=0   (presence only)", 0.0, 0.0),
                         ("k1=1.2,b=0.75 (defaults)", 1.2, 0.75),
                         ("k1=5,  b=1   (max saturation, heavy length penalty)", 5.0, 1.0)]:
        print(f"== {label} ==")
        for score, doc in bm25(QUERY, DOCS, k1=k1, b=b)[:3]:
            print(f"   {score:6.3f}  {doc}")
        print()
