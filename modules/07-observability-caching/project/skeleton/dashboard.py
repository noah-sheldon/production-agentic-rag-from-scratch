#!/usr/bin/env python3
"""Cost + cache dashboard skeleton — stdlib only, runs on macOS.

Run:  python3 dashboard.py
Reads questions.txt, answers each through a simulated RAG flow with a TTL
cache, and prints a per-question dashboard plus a summary: hit rate, average
latency, and cost with vs without the cache. Writes trace.jsonl.
"""
import json
import time
from pathlib import Path

QUESTIONS_FILE = Path("questions.txt")
TRACE_FILE = Path("trace.jsonl")

# ---------------------------------------------------------------------------
# Pricing table (lesson 03) — USD per 1 million tokens. Edit to your prices.
# ---------------------------------------------------------------------------
PRICES = {"embed_per_1m": 0.02, "input_per_1m": 2.50, "output_per_1m": 10.00}
TTL_SECONDS = 24 * 60 * 60  # cache lives one day (lesson 02)
EMBED_TOKENS = 1000         # retrieval tokens per question
INPUT_TOKENS = 1000         # prompt tokens per question
OUTPUT_TOKENS = 300         # answer tokens per question


def count_tokens(text: str) -> int:
    """Naive token count: 4 characters ≈ 1 token (lesson 03)."""
    return len(text) // 4


def call_cost(in_tokens: int, out_tokens: int) -> float:
    """Dollars for one model call."""
    return (in_tokens * PRICES["input_per_1m"]
            + out_tokens * PRICES["output_per_1m"]) / 1_000_000


def retrieval_cost() -> float:
    return EMBED_TOKENS * PRICES["embed_per_1m"] / 1_000_000


# ---------------------------------------------------------------------------
# Tracer (lesson 01)
# ---------------------------------------------------------------------------
class Tracer:
    """Records a per-step breakdown: name -> milliseconds."""

    def __init__(self) -> None:
        self.steps = []

    def step(self, name, fn):
        # TODO(lesson 01): swap the wall-clock timer for a Langfuse span when
        # this moves to a server.
        t0 = time.perf_counter()
        result = fn()
        self.steps.append((name, (time.perf_counter() - t0) * 1000.0))
        return result

    def report(self):
        return self.steps


# ---------------------------------------------------------------------------
# TTL cache (lesson 02)
# ---------------------------------------------------------------------------
class TTLCache:
    """A dict cache where every entry dies after its TTL."""

    def __init__(self, default_ttl: float) -> None:
        self.default_ttl = default_ttl
        self._data = {}  # key -> (value, expires_at)
        self.hits = 0
        self.misses = 0

    def set(self, key, value, ttl=None) -> None:
        # TODO(lesson 02): swap the dict for Redis when servers share the cache.
        ttl = self.default_ttl if ttl is None else ttl
        self._data[key] = (value, time.monotonic() + ttl)

    def get(self, key):
        entry = self._data.get(key)
        if entry is None:
            self.misses += 1
            return None
        value, expires_at = entry
        if time.monotonic() > expires_at:
            del self._data[key]  # expired: gone
            self.misses += 1
            return None
        self.hits += 1
        return value

    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


# ---------------------------------------------------------------------------
# Simulated RAG flow (the module 06 pipeline, simplified)
# ---------------------------------------------------------------------------
def retrieve(question: str):
    time.sleep(0.015)
    return [f"chunk from: {question[:24]}"]


def build_prompt(question: str, chunks):
    time.sleep(0.002)
    return "Q: " + question + "\nContext:\n" + "\n".join(chunks)


def answer(prompt: str) -> str:
    time.sleep(0.010)
    return "Answer: " + prompt.splitlines()[0][3:]


def ask(question, cache, tracer):
    key = question.strip().lower()  # normalized cache key
    cached = cache.get(key)
    if cached is not None:
        return {"hit": True, "answer": cached, "cost": 0.0, "latency_ms": 0.0}

    chunks = tracer.step("retrieve", lambda: retrieve(question))
    prompt = tracer.step("prompt", lambda: build_prompt(question, chunks))
    out = tracer.step("answer", lambda: answer(prompt))
    cache.set(key, out)
    cost = call_cost(INPUT_TOKENS, OUTPUT_TOKENS)
    latency = sum(ms for _, ms in tracer.report())
    return {"hit": False, "answer": out, "cost": cost, "latency_ms": latency}


# ---------------------------------------------------------------------------
def main() -> None:
    questions = [
        line.strip() for line in QUESTIONS_FILE.read_text().splitlines() if line.strip()
    ]
    cache = TTLCache(default_ttl=TTL_SECONDS)
    rows = []

    print(f"{'question':<28}{'hit':<6}{'latency ms':<12}{'cost $':<10}")
    print("-" * 56)
    for q in questions:
        tracer = Tracer()
        row = ask(q, cache, tracer)
        rows.append({"question": q, **row})
        print(f"{q[:27]:<28}{'yes' if row['hit'] else 'no':<6}"
              f"{row['latency_ms']:>9.1f}   {row['cost']:.6f}")
        if not row["hit"]:
            for name, ms in tracer.report():
                print(f"    |_ {name}: {ms:.1f} ms")

    TRACE_FILE.write_text("\n".join(json.dumps(r) for r in rows) + "\n")

    hits = sum(1 for r in rows if r["hit"])
    total = len(rows)
    hit_rate = hits / total if total else 0.0
    cost_with = sum(r["cost"] for r in rows)
    cost_without = total * (call_cost(INPUT_TOKENS, OUTPUT_TOKENS) + retrieval_cost())
    latencies = [r["latency_ms"] for r in rows]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0

    print("\n== SUMMARY ==")
    print(f"questions          : {total}")
    print(f"cache hits         : {hits} ({hit_rate:.0%})")
    print(f"avg latency/quest  : {avg_latency:.1f} ms")
    print(f"cost with cache    : ${cost_with:.4f}")
    print(f"cost without cache : ${cost_without:.4f}")
    if cost_with:
        print(f"savings factor     : {cost_without / cost_with:.1f}x")
    print(f"\ntrace written to {TRACE_FILE}")


if __name__ == "__main__":
    main()
