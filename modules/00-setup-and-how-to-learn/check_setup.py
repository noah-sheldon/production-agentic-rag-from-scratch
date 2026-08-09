#!/usr/bin/env python3
"""Module 00 — check your setup: Python, git, Docker, repo, tutor skill.

Run:  python3 check_setup.py

Prints PASS/FAIL per check and exactly what to install if something is missing.
"""
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return r.returncode == 0, r.stdout.strip().splitlines()[0] if r.stdout.strip() else ""
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, ""


REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    print("=" * 60)
    print("Setup check — Production Agentic RAG from Scratch")
    print("=" * 60)
    results = []

    # Python
    ok, ver = run([sys.executable, "--version"])
    v = sys.version_info
    results.append(("Python 3.12+", (v.major, v.minor) >= (3, 12), ver))

    # git
    ok, ver = run(["git", "--version"])
    results.append(("git", ok, ver or "brew install git"))

    # Docker
    ok, ver = run(["docker", "--version"])
    results.append(("Docker", ok, ver or "install Docker Desktop"))

    # Repo cloned (we are inside it)
    results.append(("Course repo", (REPO_ROOT / ".git").exists(), "clone the repo first"))

    # Tutor skill files present
    skills = REPO_ROOT / "skills"
    has_skills = (skills / "start-learning" / "SKILL.md").exists() and \
                 (skills / "learn" / "SKILL.md").exists()
    results.append(("Tutor skills", has_skills,
                    "repo is missing skills/ — re-clone"))

    print(f"\n{'CHECK':<14}{'STATUS':<10}DETAIL")
    print("-" * 60)
    all_ok = True
    for name, ok, detail in results:
        print(f"{name:<14}{'PASS' if ok else 'FAIL':<10}{detail}")
        all_ok = all_ok and ok

    print("\n" + ("ALL CHECKS PASS — module 00 done. Next: Module 01."
                  if all_ok else
                  "Fix the FAILs above, then re-run. Module 00 is the gate."))


if __name__ == "__main__":
    main()
