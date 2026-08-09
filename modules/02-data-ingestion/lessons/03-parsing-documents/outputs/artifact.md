# Artifact — tiny HTML/markdown extractor

```python
import re

def parse_html(raw: str):
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    return (title.group(1).strip() if title else ""), re.sub(r"\s+", " ", body).strip()

def parse_markdown(raw: str):
    title, body = "", raw
    fm = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if fm:
        for line in fm.group(1).splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip().strip("\"'")
        body = raw[fm.end():]
    return title, body.strip()
```

PDFs: use a real library (docling) — that's the honest trade-off.
