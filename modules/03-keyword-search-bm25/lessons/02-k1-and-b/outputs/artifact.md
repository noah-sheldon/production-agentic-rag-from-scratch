# Artifact — choosing k1 and b

Experiment: same query, same docs, three settings. What changed:

- k1=0 → repetition stops mattering; a word present in a doc scores the same
  whether it appears once or twenty times.
- k1 high → repetition still pays, but each extra mention earns less.
- b=0 → long docs are not penalized (a 1000-word doc can win on raw counts).
- b=1 → long docs fully penalized; short precise docs favored.

How to pick yours: build a small query set with known-good answers, run each
setting, count correct top-1s. Choose the setting that wins on YOUR data —
defaults are a starting point, not a verdict.
