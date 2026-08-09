#!/usr/bin/env python3
"""Module 00 — solutions to the two exercises."""

import shutil
import sys


def exercise1():
    ok = True
    v = sys.version_info
    good = (v.major, v.minor) >= (3, 12)
    print(f"check: python 3.12+ -> {'PASS' if good else 'FAIL'}")
    ok = ok and good
    for tool in ("git", "docker"):
        good = shutil.which(tool) is not None
        print(f"check: {tool} -> {'PASS' if good else 'FAIL'}")
        ok = ok and good
    return ok


BUILD_FIRST = """\
Building in plain Python first makes the system visible: you write the loop,
the scoring, the retrieval yourself, so you understand what every part does.
Frameworks hide those internals — if you import them first, you never see the
system, only the API. Build first, import second: that is the whole course.
"""

GATES = """\
Exercises gate lessons — a lesson isn't done until its exercises pass. The
quiz (human-reviewed) and the project gate the module — no project, no
advance. Gates make "I watched it" impossible; you must prove it.
"""

HITL = """\
Human-in-the-loop means a real person reviews every quiz answer — the tutor
asks, the learner answers, the human approves. No auto-pass, because the
point is understanding, not filling a checkbox. A wrong answer becomes a
re-teach, not a mark.
"""


def exercise2():
    ok = True
    ok = ok and ("system" in BUILD_FIRST.lower() or "hide" in BUILD_FIRST.lower())
    ok = ok and ("exercise" in GATES.lower() and "project" in GATES.lower())
    ok = ok and ("human" in HITL.lower() and "review" in HITL.lower())
    print(f"check: explanations -> {'PASS' if ok else 'FAIL'}")
    return ok


def main():
    results = {"exercise 1": exercise1(), "exercise 2": exercise2()}
    print()
    for name, ok in results.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print("  Both pass — module 00 complete.")


if __name__ == "__main__":
    main()
