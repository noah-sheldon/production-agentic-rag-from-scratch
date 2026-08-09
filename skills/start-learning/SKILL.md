---
name: start-learning
version: 1.0.0
description: >
  One-time onboarding for the Production Agentic RAG from Scratch course (10
  modules, 0-9). Interviews the learner, runs the placement quiz, and writes
  LEARNING.md — a persistent study plan the /learn skill drives.
  Trigger phrases: "start learning", "set up the course", "begin the
  curriculum", "onboard me", "create my learning plan"
tags: [onboarding, curriculum, agentic-rag, learning-plan]
---

# Start Learning

You are onboarding a learner into the **Production Agentic RAG from Scratch**
curriculum: 10 modules (0-9) that build YOUR personal knowledge assistant —
every system built in plain Python before a framework is imported.

Your job: write `LEARNING.md` in the current directory — the learner's source
of truth. Every `/learn` session reads and updates this file. If it exists,
never overwrite it: offer Resume (run /learn), Re-run placement, or Start over
(archive to LEARNING-<date>.md first).

## Course content location

The course repo is `noah-sheldon/production-agentic-rag-from-scratch` (public).
Raw base: `https://raw.githubusercontent.com/noah-sheldon/production-agentic-rag-from-scratch/master/`

- If the current directory (or a parent) contains `modules/`, read content locally.
- Otherwise FETCH from the raw base: e.g. `modules/00-setup-and-how-to-learn/README.md`.
- Never search the whole disk for the repo — local-or-fetch, nothing else.

## Step 1 — Interview (3 questions, keep it short)

1. Why are you learning this? (ship a product / career / understand what I use / research)
2. How much time per week? (~2h / ~5h / ~10h / as fast as possible)
3. What do you most want to build by the end? (RAG product / agent / production system / not sure)

## Step 2 — Placement

Run the `find-your-level` skill (installs alongside this one): 5 questions →
entry module. If the learner already knows their entry point, respect it.
Output contract: entry module + the Path table (modules 0-9, statuses).

## Step 3 — Write LEARNING.md

```markdown
# My Path — Production Agentic RAG from Scratch
<!-- Repo: https://github.com/noah-sheldon/production-agentic-rag-from-scratch -->

## Mission
<their answer to Q1, in their words, plus the build goal from Q3>

## Placement
- Date: <YYYY-MM-DD>
- Entry point: Module <N> — <name>
- Pace: ~<hours>/week

## Path
| Module | Title | Status | Gate |
|--------|-------|--------|------|
| 0-9 | (from ROADMAP.md — local or raw fetch) | To Do / In progress / Done | exercises+quiz+project |

## Progress log
| Date | Lesson | Quiz (human-reviewed?) | Note |
|------|--------|------------------------|------|

## Review queue
<empty — /learn adds lessons the quizzes flag>
```

## Step 4 — Hand off (three lines, nothing more)

- Their entry point and what the gate is (exercises + HITL quiz + project).
- "Run `/learn` to start your first lesson — it picks up from this file every time."
- "Human-in-the-loop: every quiz answer is reviewed by a person. No auto-pass."
