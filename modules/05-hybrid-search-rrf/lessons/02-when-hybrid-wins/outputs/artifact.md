# Artifact — the query-mining checklist

Find where hybrid wins in YOUR notes:

- [ ] Build both engines (keyword = Module 03, semantic = Module 04/06)
- [ ] Label 10+ real queries: mark the RELEVANT notes for each
- [ ] Run every query through all three modes; record recall@1 and recall@2
- [ ] Count the camps: how many queries did keyword win, semantic win,
      hybrid win? (A mode "wins" when its recall beats the others)
- [ ] Look for the split camp — the queries where hybrid's top-2 contains
      BOTH answers and neither single engine's top-2 does. Those are the
      ones hybrid exists for.
- [ ] Watch for the traps:
  - a one-word tag/title note that semantically scores ~1.0 (its vector
    IS the query vector) — RRF demotes it if keyword ranks it low
  - the kitchen-sink note that mentions everything — keyword loves it,
    and fusion inherits the mistake at lower ranks
- [ ] Write the three camps down with example queries. That list is your
      "when hybrid wins" cheat sheet.
