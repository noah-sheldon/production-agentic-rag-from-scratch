#!/usr/bin/env python3
"""Read-it-later pipeline skeleton — resumable, retried, parsed.

Run:  python3 pipeline.py        (twice — the second run skips what's done)
"""
import json
import random
import re
import time
from pathlib import Path

DONE_FILE = Path("done.json")
STORE_FILE = Path("store.jsonl")
SOURCES = Path("sources.txt")


def fetch_with_retry(url: str, attempts: int = 3, base_wait: float = 0.2) -> str:
    # TODO (lesson 02): real HTTP fetch with retry/backoff. Returns raw text.
    # For the skeleton, we simulate: urls ending in .md parse as markdown.
    for attempt in range(1, attempts + 1):
        try:
            return _simulate_fetch(url)
        except Exception:
            if attempt == attempts:
                raise
            time.sleep(base_wait * (2 ** (attempt - 1)) + random.uniform(0, base_wait))


def _simulate_fetch(url: str) -> str:
    if "fail" in url:
        raise TimeoutError("simulated failure")
    if url.endswith(".md"):
        return f"---\ntitle: {url.split('/')[-1]}\n---\n# Note\nContent from {url}."
    return f"<html><head><title>{url}</title></head><body><p>Article body.</p></body></html>"


def parse(raw: str) -> tuple[str, str]:
    # TODO (lesson 03): real HTML/markdown parser. Skeleton: naive split.
    title = re.search(r"title:\s*(.+)", raw)
    return (title.group(1).strip() if title else "untitled"), raw


def load_done() -> set:
    if DONE_FILE.exists():
        return set(json.loads(DONE_FILE.read_text()))
    return set()


def main() -> None:
    done = load_done()
    urls = SOURCES.read_text().splitlines() if SOURCES.exists() else []
    for url in urls:
        url = url.strip()
        if not url or url in done:
            print(f"skip {url}")
            continue
        try:
            raw = fetch_with_retry(url)
            title, body = parse(raw)
            with STORE_FILE.open("a") as fh:
                fh.write(json.dumps({"url": url, "title": title, "body": body}) + "\n")
            done.add(url)
            print(f"stored {title}")
        except Exception as exc:
            print(f"FAILED {url}: {exc}")
    DONE_FILE.write_text(json.dumps(sorted(done)))
    print(f"\n{len(done)} items ingested. Re-run to see it skip.")


if __name__ == "__main__":
    main()
