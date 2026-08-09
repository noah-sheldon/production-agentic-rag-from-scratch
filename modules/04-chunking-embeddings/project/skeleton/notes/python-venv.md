# Python Virtual Environment

## Why a venv

Every project needs its own set of packages. A virtual environment is a
folder that keeps a project's dependencies separate from the system Python,
so two projects never fight over versions.

## Setup

Run `python3 -m venv .venv` in the project folder, then activate it with
`source .venv/bin/activate`. Install packages with `pip install` and they
stay inside the folder. This is the first step of every new project.

## Gotcha

Forgetting to activate the venv is the classic mistake: `pip install` writes
to the system Python, and the project still can't find the package. Check
`which python` — it should point inside `.venv`.
