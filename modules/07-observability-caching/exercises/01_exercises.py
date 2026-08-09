#!/usr/bin/env python3
"""Module 07 exercises — gate the three lessons (three exercises).

Run:  python3 01_exercises.py

The three exercises:
  1. Trace the flow — write trace.py with a Tracer class (per-step times).
  2. TTL cache — write ttl_cache.py with a TTLCache class (expiry + hit rate).
  3. Cost per question — write cost.py (count_tokens + call_cost); the
     1,000-question math must land in the 150-400x band.
"""

from __future__ import annotations

import importlib.util
import os
import time


def _load(name: str):
    """Import <name>.py from this directory; None if missing."""
    path = f"{name}.py"
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------
# EXERCISE 1 — trace the flow
# --------------------------------------------------------------------------

EX1_SPEC = """\
Write `trace.py` next to this file with a `Tracer` class:
  step(name, fn)  — runs fn, records (name, seconds) in self.steps,
                    returns fn's result
  report()        — returns (self.steps, total_seconds)
"""


def check_ex1() -> bool:
    module = _load("trace")
    if module is None:
        print("  missing trace.py — create it (spec below).")
        print(EX1_SPEC)
        return False
    Tracer = getattr(module, "Tracer", None)
    if Tracer is None:
        print("  trace.py must define class Tracer.")
        return False
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
    print(f"  steps recorded: {[(n, round(s, 3)) for n, s in steps]}  {'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------
# EXERCISE 2 — TTL cache
# --------------------------------------------------------------------------

EX2_SPEC = """\
Write `ttl_cache.py` with a `TTLCache` class:
  __init__(self, default_ttl)   — TTL in seconds
  set(key, value, ttl=None)     — ttl overrides default_ttl
  get(key)                      — value, or None if missing/expired
  hit_rate()                    — hits / (hits + misses), 0.0 if empty
Expired entries count as misses.
"""


def check_ex2() -> bool:
    module = _load("ttl_cache")
    if module is None:
        print("  missing ttl_cache.py — create it (spec below).")
        print(EX2_SPEC)
        return False
    TTLCache = getattr(module, "TTLCache", None)
    if TTLCache is None:
        print("  ttl_cache.py must define class TTLCache.")
        return False
    cache = TTLCache(default_ttl=0.1)
    cache.set("q1", "answer 1")
    got = cache.get("q1")
    ok_hit = got == "answer 1"
    time.sleep(0.15)  # let q1 expire
    gone = cache.get("q1")
    ok_expire = gone is None
    cache.set("q2", "answer 2", ttl=10)  # long TTL survives
    got2 = cache.get("q2")
    ok_long = got2 == "answer 2"
    hr = cache.hit_rate()
    ok_rate = abs(hr - 2 / 3) < 0.01  # 2 hits (q1, q2), 1 miss (expired q1)
    ok = ok_hit and ok_expire and ok_long and ok_rate
    print(f"  hit {got!r}, expired->{gone!r}, long-ttl hit {got2!r}, "
          f"hit_rate {hr:.3f}  {'PASS' if ok else 'FAIL'}")
    return ok


# --------------------------------------------------------------------------
# EXERCISE 3 — cost per question (the 150-400x math)
# --------------------------------------------------------------------------

EX3_SPEC = """\
Write `cost.py` with:
  count_tokens(text)  — naive: 4 characters ≈ 1 token (len(text) // 4)
  call_cost(in_tokens, out_tokens, in_per_1m, out_per_1m)
                      — dollars for one model call:
                        (in_tokens*in_per_1m + out_tokens*out_per_1m) / 1_000_000

Then check 3 feeds the lesson's pricing table through your functions: the
model-vs-retrieval ratio and the 1,000-question savings factor must both land
in the 150-400x band.
"""

# Lesson 03 pricing table (USD per 1M tokens)
EMBED_PER_1M = 0.02
IN_PER_1M = 2.50
OUT_PER_1M = 10.00
RETRIEVAL_COST = 0.00002           # 1,000 embedding tokens at $0.02/1M
INPUT_TOKENS, OUTPUT_TOKENS = 1000, 300
TOTAL_QUESTIONS = 1000
UNIQUE_QUESTIONS = 4               # the rest are repeats -> cache hits


def check_ex3() -> bool:
    module = _load("cost")
    if module is None:
        print("  missing cost.py — create it (spec below).")
        print(EX3_SPEC)
        return False
    count_tokens = getattr(module, "count_tokens", None)
    call_cost = getattr(module, "call_cost", None)
    if count_tokens is None or call_cost is None:
        print("  cost.py must define count_tokens() and call_cost().")
        return False

    ok_tokens = count_tokens("hello world") == 2 and count_tokens("a" * 40) == 10
    model_call = call_cost(INPUT_TOKENS, OUTPUT_TOKENS, IN_PER_1M, OUT_PER_1M)
    ok_call = abs(model_call - 0.0055) < 1e-9  # (2500 + 3000) / 1e6

    ratio = model_call / RETRIEVAL_COST
    ok_ratio = 150 <= ratio <= 400

    cost_no_cache = TOTAL_QUESTIONS * model_call
    cost_with_cache = UNIQUE_QUESTIONS * model_call  # repeats hit at ~0 cost
    factor = cost_no_cache / cost_with_cache
    ok_factor = 150 <= factor <= 400

    print(f"  count_tokens: {count_tokens('hello world')}/{count_tokens('a'*40)}  "
          f"{'PASS' if ok_tokens else 'FAIL'}")
    print(f"  call_cost(1000, 300, 2.5, 10): ${model_call:.6f}  "
          f"{'PASS' if ok_call else 'FAIL'}")
    print(f"  model/retrieval ratio: {ratio:.0f}x  {'PASS' if ok_ratio else 'FAIL'}")
    print(f"  1,000-question savings factor: {factor:.0f}x  {'PASS' if ok_factor else 'FAIL'}")
    return ok_tokens and ok_call and ok_ratio and ok_factor


# --------------------------------------------------------------------------

def main() -> None:
    results = {}
    print("=" * 60)
    print("EXERCISE 1 — trace the flow")
    print("=" * 60)
    results["ex1"] = check_ex1()
    print()
    print("=" * 60)
    print("EXERCISE 2 — TTL cache")
    print("=" * 60)
    results["ex2"] = check_ex2()
    print()
    print("=" * 60)
    print("EXERCISE 3 — cost per question")
    print("=" * 60)
    results["ex3"] = check_ex3()
    print()
    passed = sum(1 for v in results.values() if v)
    print(f"{passed}/3 exercises passed")
    if passed < 3:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
