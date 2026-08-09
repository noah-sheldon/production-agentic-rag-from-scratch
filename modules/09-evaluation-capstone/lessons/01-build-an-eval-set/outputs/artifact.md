# Artifact — the labeled eval set

A ruler for your assistant. Build it before you judge anything.

- [ ] 10+ questions a real user would actually ask (not the questions you wish they'd ask)
- [ ] Every question has a known-good answer — written by a human, before any model runs
- [ ] Every question has a source: which note(s) hold the facts (the label)
- [ ] Cover the edges: one question your assistant currently fails
- [ ] Answers state facts, so scoring can check words, not feelings
- [ ] Saved as a file (JSON) — a file can be re-run, edited, and shared; a vibe cannot
- [ ] Rebuilt when your notes change — a stale ruler measures a ghost
