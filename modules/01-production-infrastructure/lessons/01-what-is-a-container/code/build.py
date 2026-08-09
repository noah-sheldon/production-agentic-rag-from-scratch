#!/usr/bin/env python3
"""Lesson 01 build — see process isolation with your own eyes.

Plain Python, standard library only. No Docker needed. Runs on macOS.

Run:  python3 build.py

You will see three things:
  1. Two "programs" (real child processes) sharing one filesystem and one
     inherited environment — the seed of "it works on my machine".
  2. Each program dropped into its own box: a private directory and a clean
     environment. The fight over files disappears.
  3. A measured number: how long it takes the machine to start one process —
     the thing containers build their isolation on top of.
"""

import os
import statistics
import subprocess
import sys
import tempfile
import time

# This source runs inside a CHILD process (not here). It prints its PID,
# tries to read a note file, and prints one environment variable.
WORKER_SOURCE = """\
import os

label = os.environ["BOX_LABEL"]

def peek(name):
    try:
        with open(name, encoding="utf-8") as fh:
            return fh.read().strip()
    except FileNotFoundError:
        return "<none>"

print(f"[{label}] pid={os.getpid()}")
print(f"[{label}] sees note.txt -> {peek('note.txt')}")
print(f"[{label}] secret env     -> {os.environ.get('SECRET', '<none>')}")
"""


def spawn(label: str, cwd: str, clean_env: bool) -> None:
    """Run the worker in a child process, in directory cwd."""
    if clean_env:
        # A "boxed" program: only what it is given, nothing inherited.
        env = {"PATH": "/usr/bin:/bin", "BOX_LABEL": label}
    else:
        # A "bare" program: inherits the parent's whole environment.
        env = dict(os.environ)
        env["BOX_LABEL"] = label
    result = subprocess.run(
        [sys.executable, "-c", WORKER_SOURCE],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )
    print(result.stdout.rstrip())
    if result.stderr:
        print(f"[{label}] stderr: {result.stderr.strip()}")


def main() -> None:
    work = tempfile.mkdtemp(prefix="isolation-demo-")
    shared = os.path.join(work, "shared")
    box_a = os.path.join(work, "box_a")
    box_b = os.path.join(work, "box_b")
    for path in (shared, box_a, box_b):
        os.makedirs(path)

    print("=" * 62)
    print("PART 1 — the shared world (no isolation yet)")
    print("=" * 62)
    with open(os.path.join(shared, "note.txt"), "w", encoding="utf-8") as fh:
        fh.write("one file, shared by everyone")
    # Both children inherit SECRET from the parent's environment.
    os.environ["SECRET"] = "parent-secret"
    spawn("app-a", shared, clean_env=False)
    spawn("app-b", shared, clean_env=False)
    print("\nBoth children saw the SAME file and the SAME inherited secret.")

    print("\nNow they fight over one filename:")
    with open(os.path.join(shared, "config.json"), "w", encoding="utf-8") as fh:
        fh.write('{"owner": "app-a"}')
    spawn("app-a", shared, clean_env=False)
    with open(os.path.join(shared, "config.json"), "w", encoding="utf-8") as fh:
        fh.write('{"owner": "app-b"}')
    spawn("app-b", shared, clean_env=False)
    with open(os.path.join(shared, "config.json"), "r", encoding="utf-8") as fh:
        print(f"\nconfig.json after both wrote it -> {fh.read().strip()}")
    print("app-b silently overwrote app-a's file. That is the problem.")

    print()
    print("=" * 62)
    print("PART 2 — each program in its own box (isolation)")
    print("=" * 62)
    for name, box in (("app-a", box_a), ("app-b", box_b)):
        with open(os.path.join(box, "note.txt"), "w", encoding="utf-8") as fh:
            fh.write(f"private note of {name}")
        with open(os.path.join(box, "config.json"), "w", encoding="utf-8") as fh:
            fh.write(f'{{"owner": "{name}"}}')
    spawn("app-a", box_a, clean_env=True)
    spawn("app-b", box_b, clean_env=True)
    print("\nEach box holds its own note.txt and config.json, and the")
    print("secret did not leak in: the box only got what it was given.")

    print()
    print("=" * 62)
    print("PART 3 — measured: process start time")
    print("=" * 62)
    samples = []
    for _ in range(20):
        started = time.perf_counter()
        subprocess.run([sys.executable, "-c", "pass"], capture_output=True)
        samples.append((time.perf_counter() - started) * 1000)
    median = statistics.median(samples)
    print(f"median time to start one process: {median:.2f} ms (20 runs)")
    print(f"=> a container is this process start PLUS a filesystem and")
    print(f"   network namespace. That overhead is what Docker manages.")


if __name__ == "__main__":
    main()
