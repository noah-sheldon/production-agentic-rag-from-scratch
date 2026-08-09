"""Retrieval for the capstone assistant: ingest notes, chunk them, search them.

Run:  python3 retrieval.py    (prints a demo search over notes/)

This is the seam for YOUR modules 4-5 pieces: keep load_notes, build_index,
and search signatures; replace the bodies with your own chunker + index.
"""
import math
import re
from collections import Counter
from pathlib import Path

STOP = {
    "the", "a", "an", "is", "are", "was", "were", "at", "on", "in",
    "for", "to", "of", "and", "or", "it", "its", "we", "you", "they",
    "does", "do", "what", "when", "where", "how", "why", "with", "from",
    "i", "about", "that", "this",
}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9']+", text.lower())
    return [w for w in words if w not in STOP and len(w) > 1]


def chunk(text: str, size: int = 180) -> list[str]:
    """Cut text into fixed-size chunks with a little overlap."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        pieces = words[start:start + size]
        chunks.append(" ".join(pieces))
        start += size - 20  # overlap keeps sentences from being cut in half
    return chunks or [text]


def load_notes(notes_dir: str = "notes") -> dict[str, dict]:
    """Read every .md file: {note_id: {"title": str, "text": str}}."""
    notes = {}
    for path in sorted(Path(notes_dir).glob("*.md")):
        raw = path.read_text()
        title = ""
        first = re.search(r"^#\s+(.+)$", raw, re.M)
        if first:
            title = first.group(1).strip()
        text = re.sub(r"^#\s+.+\n", "", raw, count=1).strip()
        notes[path.stem] = {"title": title or path.stem, "text": text}
    return notes


def build_index(notes: dict[str, dict]) -> dict:
    """Precompute tokens, chunks, and idf per note."""
    doc_tokens = {nid: tokenize(info["text"]) for nid, info in notes.items()}
    df = Counter()
    for toks in doc_tokens.values():
        df.update(set(toks))
    n = len(notes)
    idf = {term: math.log((n + 1) / (df[term] + 1)) + 1 for term in df}
    index = {}
    for nid, info in notes.items():
        index[nid] = {
            "title": info["title"],
            "tokens": doc_tokens[nid],
            "chunks": chunk(info["text"]),
            "idf": idf,
        }
    return index


def search(index: dict, query: str, k: int = 3) -> list[str]:
    """Rank note ids by BM25-lite score, best first."""
    qt = set(tokenize(query))
    scores = {}
    for nid, note in index.items():
        tf = Counter(note["tokens"])
        score = 0.0
        for term in qt:
            if term in tf:
                score += note["idf"][term] * (1 + math.log(tf[term]))
        if score > 0:
            scores[nid] = score
    return sorted(scores, key=scores.get, reverse=True)[:k]


def read_note(index: dict, note_id: str) -> str:
    note = index.get(note_id)
    if note is None:
        return f"(no note named {note_id})"
    return f"# {note['title']}\n{note['text']}"


def main() -> None:
    notes = load_notes()
    print(f"indexed {len(notes)} notes: {', '.join(sorted(notes))}")
    index = build_index(notes)
    for query in ["when does the nightly deploy run", "where are backups stored"]:
        print(f"\nquery: {query!r}")
        for nid in search(index, query):
            print(f"  {nid}: {notes[nid]['title']}")


if __name__ == "__main__":
    main()
