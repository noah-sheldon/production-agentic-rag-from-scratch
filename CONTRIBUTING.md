# Contributing

This course is open source and build-first. Before you submit anything, read
AGENTS.md (the 10 teaching rules) and LESSON_TEMPLATE.md (the Six Beats).

## Adding or fixing a lesson

1. Every lesson lives in `modules/<NN>-<module>/lessons/<NN>-<slug>/` with
   `docs/en.md` (Six Beats), `code/*.py` (plain Python, stdlib, runnable),
   `outputs/artifact.md` (what the lesson ships).
2. Originality is law: no copied code, no copied projects (the arXiv curator
   is off-limits), no re-telling another course's lesson.
3. BUILD IT before USE IT. Frameworks appear only in USE IT, with an honest
   scoreboard — never framework bashing.
4. Every term defined before use. Diagram-first (mermaid + excalidraw).
5. Results measured (numbers, tokens, latency) — never vibes.

## Before submitting

```bash
python3 scripts/audit_lessons.py --strict   # pattern + compile checks
python3 scripts/lesson_run.py --execute     # smoke-run every lesson build
python3 scripts/build_catalog.py            # keep catalog.json fresh
```

CI fails if `catalog.json` is stale or any lesson code doesn't compile.

## Process

- Branch → PR → 1 human review (branch protection requires it). Master is
  protected: linear history, no force-push, PR required for non-admins.
- Keep commits small and focused. One module per PR is ideal.
