"""Build it: chunk a document by sections in plain Python (stdlib only).

Run:  python3 build.py
Splits a note at its headings, re-splits too-long sections with overlap,
and proves the overlap by showing shared words between neighbors.
"""
from dataclasses import dataclass


@dataclass
class Chunk:
    heading: str
    text: str

    @property
    def words(self) -> int:
        return len(self.text.split())


NOTE = """# What Is a Vector Store

A vector store is a database that searches by meaning instead of by exact words.
It stores each piece of text next to a list of numbers that captures the meaning.

## How Embeddings Get In

Every section of a document is cut into chunks first, and each chunk is turned
into a list of numbers called an embedding. The vector store keeps the chunk
and the embedding side by side. A search question becomes an embedding too, and
the store returns the chunks whose embeddings point closest to the question.
That is how a search can find "how do I pay an invoice" even when the note only
says "settle a bill" — the numbers know the words mean the same thing.

## When It Fails

A chunk that mixes five topics makes the embedding an average of five meanings,
so the chunk matches nothing well. Chunking badly quietly destroys the search.
"""


def split_sections(text: str) -> list[tuple[str, str]]:
    """Cut text into (heading, body) sections at lines that start with '#'.

    A section keeps its heading; body lines before any heading belong to
    a section with the heading "(no heading)".
    """
    sections: list[tuple[str, str]] = []
    heading = "(no heading)"
    body: list[str] = []
    for line in text.splitlines():
        if line.startswith("#"):
            if body or sections:
                sections.append((heading, "\n".join(body).strip()))
            heading = line.lstrip("#").strip()
            body = []
        elif line.strip():
            body.append(line)
    if body or not sections:
        sections.append((heading, "\n".join(body).strip()))
    return sections


def split_long_section(
    heading: str, body: str, max_words: int, overlap_words: int
) -> list[Chunk]:
    """Re-split a section longer than max_words, carrying the tail forward."""
    words = body.split()
    if len(words) <= max_words:
        return [Chunk(heading, body)]
    chunks: list[Chunk] = []
    start = 0
    while start < len(words):
        end = start + max_words
        chunks.append(Chunk(heading, " ".join(words[start:end])))
        if end >= len(words):
            break
        start = end - overlap_words
    return chunks


def chunk_by_sections(text: str, max_words: int = 200, overlap_words: int = 30) -> list[Chunk]:
    """The pipeline: sections first, then size caps with overlap."""
    chunks: list[Chunk] = []
    for heading, body in split_sections(text):
        chunks.extend(split_long_section(heading, body, max_words, overlap_words))
    return chunks


def shared_words(a: Chunk, b: Chunk) -> set[str]:
    return set(a.text.lower().split()) & set(b.text.lower().split())


if __name__ == "__main__":
    chunks = chunk_by_sections(NOTE, max_words=25, overlap_words=5)
    print(f"== {len(chunks)} chunks ==")
    for i, chunk in enumerate(chunks):
        print(f"  [{i}] ({chunk.heading}, {chunk.words:>2} words) {chunk.text[:45]}...")
    print("\n== overlap proof (words shared with the previous chunk) ==")
    for i in range(1, len(chunks)):
        shared = shared_words(chunks[i - 1], chunks[i])
        print(f"  chunk {i - 1} <-> chunk {i}: {len(shared)} shared words "
              f"-> {sorted(shared)[:4]}")
    print("\n== measurement ==")
    print(f"  max chunk size: {max(c.words for c in chunks)} words "
          f"(cap {25}, overlap {5})")
