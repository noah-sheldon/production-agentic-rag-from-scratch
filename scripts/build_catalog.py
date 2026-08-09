#!/usr/bin/env python3
"""Build catalog.json — filesystem-derived course truth (no hardcoding).

Run:  python3 scripts/build_catalog.py [--stdout]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalog = {"modules": []}

for m in sorted((ROOT / "modules").iterdir()) if (ROOT / "modules").exists() else []:
    entry = {
        "module": m.name,
        "lessons": [],
        "exercises": [],
        "quiz": (m / "quizzes" / "quiz.md").exists(),
        "project": (m / "project" / "project.md").exists(),
    }
    for l in sorted((m / "lessons").iterdir()) if (m / "lessons").exists() else []:
        code = [p.name for p in (l / "code").glob("*.py")] if (l / "code").exists() else []
        entry["lessons"].append({
            "lesson": l.name,
            "docs": (l / "docs" / "en.md").exists(),
            "code": code,
            "artifact": (l / "outputs" / "artifact.md").exists(),
        })
    for p in sorted((m / "exercises").glob("*.py")) if (m / "exercises").exists() else []:
        entry["exercises"].append(p.name)
    catalog["modules"].append(entry)

catalog["lesson_count"] = sum(len(e["lessons"]) for e in catalog["modules"])
out = json.dumps(catalog, indent=2)
if "--stdout" in sys.argv:
    print(out)
else:
    (ROOT / "catalog.json").write_text(out + "\n")
    print(f"wrote catalog.json — {catalog['lesson_count']} lessons across {len(catalog['modules'])} modules")
