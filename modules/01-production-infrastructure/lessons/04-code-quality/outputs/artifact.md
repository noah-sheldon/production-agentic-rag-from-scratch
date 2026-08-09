# Artifact — the quality gate: pre-commit + Ruff + MyPy + pytest

Use this the next time you start any Python project. It is the exact setup
this course's project ships with — copy, install, commit, done.

## Part 1 — the pre-commit config

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.10
    hooks:
      - id: ruff            # linter
      - id: ruff-format     # formatter
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.15.0
    hooks:
      - id: mypy            # type checker
        additional_dependencies: [types-requests]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
```

## Part 2 — one-command setup

```bash
# 1. environment + tools
uv init
uv add --dev ruff mypy pytest pre-commit

# 2. install the gate (runs on every commit from now on)
pre-commit install

# 3. run everything once, on the whole repo
pre-commit run --all-files
ruff check .
mypy .
pytest

# 4. prove the gate: a bad change is blocked, not committed
echo "x = 1" > broken.py && git add broken.py && git commit -m "test"
# ruff stops the commit -> fix -> commit again
```

## Part 3 — the rules this gate enforces

1. **Lint first** — style and obvious mistakes, cheapest to fix, fails first.
2. **Types second** — MyPy only looks at code that already lints clean.
3. **Tests always** — behavior is the contract; `pytest` must pass before any
   commit. If a change has no test, the change is not done.
4. **The gate is not optional** — `pre-commit` blocks the commit. No `--no-verify`
   shortcuts except in a documented emergency.

## Trade-off reminder

Green is the floor: these tools prove the code *runs clean and behaves as
tested*, not that the design is good. Use them to remove boring failures so
your review energy goes to the design.
