# Artifact — the resumable-pipeline checklist

Make any fetch job resumable:

- [ ] Track per-item state (done/failed/pending) — a `done` set or a DB column
- [ ] Skip completed items on re-run (idempotency)
- [ ] Retry failures with backoff (see lesson 02)
- [ ] Never re-fetch what's stored (state lives in the store, not your head)
- [ ] One item = one transaction (partial success never corrupts the rest)
