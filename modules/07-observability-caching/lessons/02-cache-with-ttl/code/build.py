"""Build it: a plain-Python dict cache with TTL expiry (stdlib only).

Run:  python3 build.py
Asks a list of questions with repeats; prints hit/miss per question, the hit
rate, and the cost with vs without the cache. Then proves an entry expires.
"""
import time
from typing import Optional

MODEL_CALL_COST = 0.0055  # one LLM call, from the lesson 03 pricing table


class TTLCache:
    """A dict cache where every entry dies after its TTL."""

    def __init__(self, default_ttl: float = 10.0) -> None:
        self.default_ttl = default_ttl
        self._data: dict[str, tuple[str, float]] = {}  # key -> (value, expires_at)
        self.hits = 0
        self.misses = 0

    def set(self, key: str, value: str, ttl: Optional[float] = None) -> None:
        ttl = self.default_ttl if ttl is None else ttl
        self._data[key] = (value, time.monotonic() + ttl)

    def get(self, key: str) -> Optional[str]:
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


def run_pipeline(question: str) -> str:
    """The expensive part a cache lets us skip (the module 06 flow)."""
    time.sleep(0.05)
    return f"answer to: {question}"


def main() -> None:
    questions = [
        "what is rag?",
        "how do chunks work?",
        "what is rag?",
        "what is a ttl cache?",
        "how do chunks work?",
        "what is rag?",
    ]
    cache = TTLCache(default_ttl=24 * 60 * 60)  # one day

    print(f"{'question':<26}{'result':<8}{'cost':>10}")
    cost_with = 0.0
    for q in questions:
        key = q.strip().lower()  # normalized cache key
        cached = cache.get(key)
        if cached is not None:
            print(f"{q:<26}{'hit':<8}{'$0.0000':>10}")
            continue
        out = run_pipeline(q)
        cache.set(key, out)
        cost_with += MODEL_CALL_COST
        print(f"{q:<26}{'miss':<8}{'$0.0055':>10}")

    cost_without = len(questions) * MODEL_CALL_COST
    print(f"\nhit rate:            {cache.hit_rate():.0%}")
    print(f"cost with cache:     ${cost_with:.4f}")
    print(f"cost without cache:  ${cost_without:.4f}")

    # prove the TTL: an entry dies after its TTL
    short = TTLCache(default_ttl=0.1)
    short.set("q", "stale answer")
    print(f"\nTTL check: immediate get -> {short.get('q')!r}")
    time.sleep(0.15)
    print(f"TTL check: after 0.15s   -> {short.get('q')!r} (expired, miss)")


if __name__ == "__main__":
    main()
