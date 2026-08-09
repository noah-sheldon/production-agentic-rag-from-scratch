# Artifact — the chunk-by-sections pattern

Paste this into any pipeline that turns documents into searchable pieces:

```python
from dataclasses import dataclass

@dataclass
class Chunk:
    heading: str
    text: str

def split_sections(text: str) -> list[tuple[str, str]]:
    sections, heading, body = [], "(no heading)", []
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

def split_long_section(heading: str, body: str, max_words: int, overlap_words: int):
    words = body.split()
    if len(words) <= max_words:
        return [Chunk(heading, body)]
    out, start = [], 0
    while start < len(words):
        end = start + max_words
        out.append(Chunk(heading, " ".join(words[start:end])))
        if end >= len(words):
            break
        start = end - overlap_words
    return out

def chunk_by_sections(text: str, max_words: int = 200, overlap_words: int = 30):
    return [c for h, b in split_sections(text) for c in split_long_section(h, b, max_words, overlap_words)]
```

Checklist:

- [ ] Cut at headings first — one idea per chunk
- [ ] Cap every chunk at a max size (your window / a sensible budget)
- [ ] Carry overlap so a straddling sentence is whole somewhere
- [ ] Measure: print chunk word counts — outliers mean a bad cut
- [ ] No headings in your text? Fall back to fixed-size + overlap (lesson 03)
