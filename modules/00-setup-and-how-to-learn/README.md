# Module 00 — Setup & How to Learn

**Goal:** your machine ready, the tutor installed, and you know how this course works. No AI knowledge needed to start — only following steps.
**Math you'll meet:** None — setup only.

## Topics

- Terminal basics: what it is, how to run a command, paths
- Install: Python 3.12+, git, Docker Desktop
- Clone the course repo
- Install the terminal tutor (`npx skills add` — optional, works on any machine with an agent)
- How the course works: the Six Beats, build-first, exercises, HITL quiz, projects

## What this course is NOT

- NOT model training from scratch — no backprop, no attention math, no
  building a transformer. That's a different course.
- NOT a math prerequisite course — the only math you'll meet (cosine, IDF,
  RRF, cost) is built by hand inside the lesson that uses it.
- This IS: the production systems layer, built in plain Python, measured,
  for applied AI/ML engineers.

## How the course works (read this once)

1. **Build first.** Every lesson builds the concept in plain Python BEFORE a framework is imported. You type the code, you see the system.
2. **Six Beats per lesson:** MOTTO → PROBLEM → CONCEPT (diagrams) → BUILD IT (raw) → USE IT (framework, honest trade-offs) → SHIP IT (artifact).
3. **Exercises gate lessons** (2-3 per module). **Quiz gates the module — human-reviewed**, no auto-pass. **Project gates the module.**
4. **Diagrams first:** every CONCEPT has mermaid + excalidraw. Less text, more picture.
5. **You build YOUR personal knowledge assistant** — one piece per module, from infra to a tool-wielding agent.

## Check your setup

```bash
cd modules/00-setup-and-how-to-learn
python3 check_setup.py
```

It checks Python, git, Docker, and prints exactly what to install if missing.

## Learn — three ways (pick any)

1. **Terminal tutor:** `npx skills add noah-sheldon/production-agentic-rag-from-scratch`, then `/start-learning` — placement quiz, personalized path, `/learn` teaches each lesson with quizzes.
2. **Clone and read:** lessons are markdown + runnable code. Read `docs/en.md`, run `code/build.py`.
3. **Videos:** one high-level long-form per module + shorts per concept (from the content-planner pipeline).

## Quiz (human-in-the-loop)

`quizzes/quiz.md` — 5 questions, answered from memory, a human reviews. No auto-pass.

**Project (gate):** your environment passes `check_setup.py` — every dependency installed, the repo cloned, the tutor skill loads. That's the whole module.
