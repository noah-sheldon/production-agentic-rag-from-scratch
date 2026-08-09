"""Build it: extract title + body from HTML and markdown, plain Python.

Run:  python3 build.py
"""
import re
from dataclasses import dataclass


@dataclass
class Document:
    title: str
    body: str


def parse_html(raw: str) -> Document:
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", " ", body)          # strip tags
    body = re.sub(r"\s+", " ", body).strip()      # collapse whitespace
    return Document(title.group(1).strip() if title else "(no title)", body)


def parse_markdown(raw: str) -> Document:
    title = ""
    body = raw
    fm = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if fm:
        for line in fm.group(1).splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip().strip("\"'")
        body = raw[fm.end():]
    first = re.search(r"^#\s+(.+)$", body, re.M)
    if not title and first:
        title = first.group(1).strip()
    return Document(title, body.strip())


if __name__ == "__main__":
    html = "<html><head><title>RAG Notes</title></head><body><nav>menu</nav><p>Hello world.</p><script>bad()</script></body></html>"
    md = "---\ntitle: Agents Notes\n---\n# Agents\nNotes about loops."
    print("HTML :", parse_html(html))
    print("MD   :", parse_markdown(md))
