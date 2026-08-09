# Artifact — reusable retry wrapper

```python
import random
import time


def fetch_with_retry(fn, attempts: int = 4, base_wait: float = 0.5):
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:
            if attempt == attempts:
                raise
            wait = base_wait * (2 ** (attempt - 1)) + random.uniform(0, base_wait)
            time.sleep(wait)


# usage
# data = fetch_with_retry(lambda: requests.get(url, timeout=10))
```

Budget = your guard. Raise it for slow APIs, lower it when the job must be fast.
