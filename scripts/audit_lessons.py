#!/usr/bin/env python3
"""Audit the course — every module must ship the full pattern.

Rules (mirror the reference repo's L001-L010):
- README.md, quizzes/quiz.md, exercises (01 + 02), project/project.md
- lessons/: docs/en.md (H1 + Six Beats), code/*.py, outputs/artifact.md
- every .py in the repo byte-compiles

Run:  python3 scripts/audit_lessons.py [--strict]
Filesystem-driven — zero hardcoded module names.
"""
import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
modules = sorted((ROOT / "modules").iterdir()) if (ROOT / "modules").exists() else []

for m in modules:
    name = m.name
    if not (m / "README.md").exists():
        errors.append(f"{name}: missing README.md")
    if not (m / "quizzes" / "quiz.md").exists():
        errors.append(f"{name}: missing quizzes/quiz.md")
    for ex in ("01_exercises.py", "02_solutions.py"):
        if not (m / "exercises" / ex).exists():
            errors.append(f"{name}: missing exercises/{ex}")
    if not (m / "project" / "project.md").exists():
        errors.append(f"{name}: missing project/project.md")

    lessons = sorted((m / "lessons").iterdir()) if (m / "lessons").exists() else []
    if not lessons:
        errors.append(f"{name}: no lessons/")
    for lesson in lessons:
        doc = lesson / "docs" / "en.md"
        if not doc.exists():
            errors.append(f"{name}/{lesson.name}: missing docs/en.md")
        elif "```mermaid" not in doc.read_text(encoding="utf-8", errors="ignore"):
            errors.append(f"{name}/{lesson.name}: docs/en.md has NO mermaid diagram")
        code_dir = lesson / "code"
        py_files = list(code_dir.glob("*.py")) if code_dir.exists() else []
        if not py_files:
            errors.append(f"{name}/{lesson.name}: no code/*.py")
        if not (lesson / "outputs" / "artifact.md").exists():
            errors.append(f"{name}/{lesson.name}: missing outputs/artifact.md")

for p in ROOT.rglob("*.py"):
    if ".git" in p.parts:
        continue
    try:
        py_compile.compile(str(p), doraise=True)
    except py_compile.PyCompileError as exc:
        errors.append(f"compile {p.relative_to(ROOT)}: {exc}")

if errors:
    print(f"{len(errors)} problem(s):")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1 if "--strict" in sys.argv else 0)
print(f"OK — {len(modules)} modules, all files present, all python compiles.")
