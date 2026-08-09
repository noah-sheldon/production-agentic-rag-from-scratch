# Artifact — the TTL cache checklist

Cache any expensive step:

- [ ] Cache key = the question, normalized (trim, lowercase)
- [ ] Store (value, expires-at) with `time.monotonic()`
- [ ] On get: expired entries are deleted and count as misses
- [ ] Track hits and misses; print the hit rate
- [ ] Set a TTL that matches how fast your data changes
- [ ] Measure cost before and after — caching must show up in the numbers
- [ ] Every entry needs a TTL; "forever" means stale answers forever
