#!/usr/bin/env python3
"""Module 00 exercises — gate the setup (two exercises).

Run:  python3 01_exercises.py

The two exercises:
  1. Run check_setup.py and explain each check in your own words.
  2. Answer the course-mechanics questions (build-first, gates, HITL).
"""

from __future__ import annotations

import shutil
import subprocess
import sys


def check_python() -> bool:
    v = sys.version_info
    return (v.major, v.minor) >= (3, 12)


def check_tool(name: str) -> bool:
    return shutil.which(name) is not None


def check_ex1() -> bool:
    """Environment gate: python, git, docker present."""
    ok = True
    print(f"  python 3.12+ : {'PASS' if check_python() else 'FAIL'}")
    ok = ok and check_python()
    for tool in ("git", "docker"):
        good = check_tool(tool)
        print(f"  {tool:11s}: {'PASS' if good else 'FAIL — install it'}")
        ok = ok and good
    return ok


EX2_QUESTION = """\
Answer in your own words (2-3 sentences each):
1. BUILD_FIRST: why must a lesson build in plain Python before a framework?
2. GATES: what gates lessons, and what gates a module?
3. HITL: what does human-in-the-loop mean for quizzes, and why no auto-pass?
"""

BUILD_FIRST = ""
GATES = ""
HITL = ""


def check_ex2() -> bool:
    ok = True
    bf = BUILD_FIRST.lower()
    good = "system" in bf or "understand" in bf or "hide" in bf
    print(f"  build-first explanation: {'PASS' if good else 'FAIL'}")
    ok = ok and good
    g = GATES.lower()
    good = "exercise" in g and "project" in g
    print(f"  gates explanation:       {'PASS' if good else 'FAIL'}")
    ok = ok and good
    h = HITL.lower()
    good = "human" in h and "review" in h
    print(f"  hitl explanation:        {'PASS' if good else 'FAIL'}")
    ok = ok and good
    return ok


def main() -> None:
    print("=" * 60)
    print("EXERCISE 1 — environment gate")
    print("=" * 60)
    ok1 = check_ex1()
    print()
    print("=" * 60)
    print("EXERCISE 2 — course mechanics")
    print("=" * 60)
    print(EX2_QUESTION)
    ok2 = check_ex2()
    print()
    print(f"{int(ok1) + int(ok2)}/2 exercises passed")
    if not (ok1 and ok2):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
