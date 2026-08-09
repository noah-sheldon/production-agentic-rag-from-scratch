#!/usr/bin/env python3
"""Smoke-check every lesson's Python code.

Run:  python3 scripts/lesson_run.py [--execute] [--strict]
Default: byte-compile every code/*.py under modules/. --execute runs each
entry file with a 10s timeout (skips files whose first line starts with
'# requires:').
"""
import py_compile
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
execute = "--execute" in sys.argv
strict = "--strict" in sys.argv
errors = []

for py in sorted(ROOT.rglob("code/*.py")):
    if ".git" in py.parts:
        continue
    try:
        py_compile.compile(str(py), doraise=True)
    except py_compile.PyCompileError as exc:
        errors.append(f"compile {py.relative_to(ROOT)}: {exc}")
        continue
    if execute:
        first = py.read_text(errors="ignore").lstrip().splitlines()[0] if py.read_text(errors="ignore").strip() else ""
        if first.startswith("# requires:"):
            continue
        try:
            r = subprocess.run([sys.executable, str(py)], capture_output=True,
                               text=True, timeout=10)
            if r.returncode != 0:
                errors.append(f"run {py.relative_to(ROOT)}: {r.stderr.strip()[:200]}")
        except subprocess.TimeoutExpired:
            errors.append(f"run {py.relative_to(ROOT)}: TIMEOUT")

if errors:
    print(f"{len(errors)} problem(s):")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1 if strict else 0)
print("OK — all lesson code compiles" + (" and runs" if execute else "") + ".")
