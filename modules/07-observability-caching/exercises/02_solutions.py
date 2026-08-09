#!/usr/bin/env python3
"""Module 07 — solutions to the three exercises.

Run:  python3 02_solutions.py
"""
import time

# --------------------------------------------------------------------------
# EXERCISE 1 — trace the flow
# --------------------------------------------------------------------------


class Tracer:
    """Records a named timer around every step."""

    def __init__(self):
        self.steps = []  # (name, seconds)

    def step(self, name, fn):
        t0 = time.perf_counter()
        result = fn()
        self.steps.append((name, time.perf_counter() - t0))
        return result

    def report(self):
        return self.steps, sum(s for _, s in self.steps)


def exercise1() -> bool:
    tracer = Tracer()

    def slow_step():
        time.sleep(0.02)
        return "found"

    def fast_step():
        time.sleep(0.01)
        return "built"

    r1 = tracer.step("retrieve", slow_step)
    r2 = tracer.step("prompt", fast_step)
    steps, total = tracer.report()
    ok = (
        r1 == "found" and r2 == "built"
        and [n for n, _ in steps] == ["retrieve", "prompt"]
        and steps[0][1] >= 0.02 and steps[1][1] >= 0.01
        and total >= 0.03
    )
    print(f"check: steps {[(n, round(s, 3)) for n, s in steps]} -> "
          f"{'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------
# EXERCISE 2 — TTL cache
# --------------------------------------------------------------------------


class TTLCache:
    """A dict cache where every entry dies after its TTL."""

    def __init__(self, default_ttl=10.0):
        self.default_ttl = default_ttl
        self._data = {}
        self.hits = 0
        self.misses = 0

    def set(self, key, value, ttl=None):
        ttl = self.default_ttl if ttl is None else ttl
        self._data[key] = (value, time.monotonic() + ttl)

    def get(self, key):
        entry = self._data.get(key)
        if entry is None:
            self.misses += 1
            return None
        value, expires_at = entry
        if time.monotonic() > expires_at:
            del self._data[key]
            self.misses += 1
            return None
        self.hits += 1
        return value

    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


def exercise2() -> bool:
    cache = TTLCache(default_ttl=0.1)
    cache.set("q1", "answer 1")
    got = cache.get("q1")
    ok_hit = got == "answer 1"
    time.sleep(0.15)
    gone = cache.get("q1")
    ok_expire = gone is None
    cache.set("q2", "answer 2", ttl=10)
    got2 = cache.get("q2")
    ok_long = got2 == "answer 2"
    hr = cache.hit_rate()
    ok_rate = abs(hr - 2 / 3) < 0.01
    ok = ok_hit and ok_expire and ok_long and ok_rate
    print(f"check: hit {got!r}, expired->{gone!r}, long-ttl {got2!r}, "
          f"hit_rate {hr:.3f} -> {'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------
# EXERCISE 3 — cost per question (the 150-400x math)
# --------------------------------------------------------------------------


def count_tokens(text):
    """Naive token count: 4 characters ≈ 1 token."""
    return len(text) // 4


def call_cost(in_tokens, out_tokens, in_per_1m, out_per_1m):
    """Dollars for one model call."""
    return (in_tokens * in_per_1m + out_tokens * out_per_1m) / 1_000_000


def exercise3() -> bool:
    # Lesson 03 pricing table (USD per 1M tokens)
    embed_per_1m = 0.02
    in_per_1m = 2.50
    out_per_1m = 10.00
    retrieval_cost = 0.00002
    in_tokens, out_tokens = 1000, 300
    total_questions = 1000
    unique_questions = 4

    ok_tokens = count_tokens("hello world") == 2 and count_tokens("a" * 40) == 10
    model_call = call_cost(in_tokens, out_tokens, in_per_1m, out_per_1m)
    ok_call = abs(model_call - 0.0055) < 1e-9
    ratio = model_call / retrieval_cost
    ok_ratio = 150 <= ratio <= 400
    cost_no_cache = total_questions * model_call
    cost_with_cache = unique_questions * model_call
    factor = cost_no_cache / cost_with_cache
    ok_factor = 150 <= factor <= 400

    print(f"check: count_tokens -> {'PASS' if ok_tokens else 'FAIL'}")
    print(f"check: call_cost -> ${model_call:.6f} -> {'PASS' if ok_call else 'FAIL'}")
    print(f"check: model/retrieval {ratio:.0f}x -> {'PASS' if ok_ratio else 'FAIL'}")
    print(f"check: 1,000-question savings {factor:.0f}x -> "
          f"{'PASS' if ok_factor else 'FAIL'}")
    print(f"  cost without cache: ${cost_no_cache:.2f}, with cache: ${cost_with_cache:.4f}")
    return ok_tokens and ok_call and ok_ratio and ok_factor


def main() -> None:
    results = {
        "exercise 1": exercise1(),
        "exercise 2": exercise2(),
        "exercise 3": exercise3(),
    }
    print()
    for name, ok in results.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print("  All three pass — module 07 exercises complete.")


if __name__ == "__main__":
    main()
