"""Build it: retries with exponential backoff + jitter (stdlib only).

Run:  python3 build.py
A flaky endpoint recovers on attempt 3 — watch the waits grow.
"""
import random
import time


def fetch_with_retry(fn, attempts: int = 4, base_wait: float = 0.1):
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:
            if attempt == attempts:
                raise
            wait = base_wait * (2 ** (attempt - 1)) + random.uniform(0, base_wait)
            print(f"  attempt {attempt} failed ({exc}); waiting {wait:.2f}s")
            time.sleep(wait)


calls = 0


def flaky():
    global calls
    calls += 1
    if calls < 3:
        raise TimeoutError("rate limited")
    return "ok"


if __name__ == "__main__":
    print("== flaky endpoint, 4 attempts ==")
    result = fetch_with_retry(flaky)
    print(f"result: {result} (calls made: {calls})")
