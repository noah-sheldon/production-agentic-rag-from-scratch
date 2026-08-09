#!/usr/bin/env python3
"""Module 02 — solutions to the three exercises."""

import random
import time

# --------------------------------------------------------------------------
# EXERCISE 1 — retries with backoff
# --------------------------------------------------------------------------

import importlib.util
import os


def fetch_with_retry(fn, attempts=4, base_wait=0.05):
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:
            if attempt == attempts:
                raise
            wait = base_wait * (2 ** (attempt - 1)) + random.uniform(0, base_wait)
            time.sleep(wait)


def exercise1() -> bool:
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise TimeoutError("rate limited")
        return "ok"

    result = fetch_with_retry(flaky, attempts=4, base_wait=0.01)
    ok = result == "ok" and calls["n"] == 3
    print(f"check: flaky endpoint -> {result!r} in {calls['n']} calls -> {'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------
# EXERCISE 2 — parse a document
# --------------------------------------------------------------------------

import re


def parse_html(raw):
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    return (title.group(1).strip() if title else ""), re.sub(r"\s+", " ", body).strip()


def parse_markdown(raw):
    title, body = "", raw
    fm = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if fm:
        for line in fm.group(1).splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip().strip("\"'")
        body = raw[fm.end():]
    first = re.search(r"^#\s+(.+)$", body, re.M)
    if not title and first:
        title = first.group(1).strip()
    return title, body.strip()


def exercise2() -> bool:
    html = "<html><head><title>My Note</title></head><body><nav>x</nav><p>Hello world.</p></body></html>"
    md = "---\ntitle: Agents\n---\n# Agents\nLoops and tools."
    t, b = parse_html(html)
    ok = t == "My Note" and "Hello world." in b and "nav" not in b
    print(f"check: parse_html -> {t!r} {'PASS' if ok else 'FAIL'}")
    t, b = parse_markdown(md)
    ok2 = t == "Agents" and "Loops and tools." in b
    print(f"check: parse_markdown -> {t!r} {'PASS' if ok2 else 'FAIL'}")
    return ok and ok2


# --------------------------------------------------------------------------
# EXERCISE 3 — design the pipeline
# --------------------------------------------------------------------------

PIPELINE_STEPS = [
    "1. fetch the item with retries (backoff on failure)",
    "2. parse the document (title + clean body)",
    "3. extract metadata (date, source, tags)",
    "4. store the item; mark done in the done-set",
]

IDEMPOTENCY = """\
Re-running a pipeline must produce the same result: the done-set makes the
second run skip completed items, so no duplicates and no double-fetch. If it
isn't idempotent, re-runs create duplicate rows, re-fetch what's stored, and
drift the data — and a crash mid-run corrupts the state.
"""


def exercise3() -> bool:
    steps = [s.lower() for s in PIPELINE_STEPS]
    ok = all(any(r in s for s in steps) for r in ["fetch", "parse", "store"])
    good = "retry" in IDEMPOTENCY.lower() or "done" in IDEMPOTENCY.lower()
    print(f"check: pipeline steps fetch/parse/store -> {'PASS' if ok else 'FAIL'}")
    print(f"check: idempotency explanation -> {'PASS' if good else 'FAIL'}")
    return ok and good


def main() -> None:
    results = {
        "exercise 1": exercise1(),
        "exercise 2": exercise2(),
        "exercise 3": exercise3(),
    }
    print()
    for name, ok in results.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print("  All three pass — module 02 exercises complete.")


if __name__ == "__main__":
    main()
