"""Build it: a resumable ingestion pipeline in plain Python (stdlib only).

Run:  python3 build.py
Runs the pipeline twice — the second run skips everything already done.
"""
import json
from pathlib import Path

DONE_FILE = Path("done.json")


def load_done() -> set:
    if DONE_FILE.exists():
        return set(json.loads(DONE_FILE.read_text()))
    return set()


def save_done(done: set) -> None:
    DONE_FILE.write_text(json.dumps(sorted(done)))


def fetch(item: str) -> str:
    """Pretend network fetch — in real life this is requests.get()."""
    return f"<content of {item}>"


def parse(raw: str) -> str:
    return raw.strip()


def store(item: str, text: str) -> None:
    print(f"  stored {item}: {text[:40]}...")


def run(items: list[str]) -> None:
    done = load_done()
    for item in items:
        if item in done:
            print(f"  skip {item} (already done)")
            continue
        raw = fetch(item)
        text = parse(raw)
        store(item, text)
        done.add(item)
    save_done(done)


if __name__ == "__main__":
    articles = ["notes/rag-notes.md", "notes/agents.md", "notes/evals.md"]
    print("== run 1 (fetches everything) ==")
    run(articles)
    print("== run 2 (resumes — nothing new) ==")
    run(articles)
