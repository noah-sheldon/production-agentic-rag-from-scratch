---
name: learn
version: 1.0.0
description: >
  Tutor loop for the Production Agentic RAG from Scratch course — reads
  LEARNING.md, teaches one lesson, quizzes with human-in-the-loop review,
  tracks progress. Trigger phrases: "learn", "next lesson", "teach me",
  "continue the course"
tags: [tutor, curriculum, agentic-rag, learning]
---

# Learn

Tutor loop for one lesson. Reads `LEARNING.md` (the learner's source of truth)
to find the current lesson; updates it after each session.

## Course content location

Repo: `noah-sheldon/production-agentic-rag-from-scratch` (public).
Raw base: `https://raw.githubusercontent.com/noah-sheldon/production-agentic-rag-from-scratch/master/`

- Current dir or parent has `modules/`? Read locally.
- Otherwise FETCH from the raw base (`modules/<NN>-<name>/lessons/<NN>-<slug>/docs/en.md`).
- Never search the whole disk.

## The loop

1. **Locate** — read LEARNING.md; find the next `To Do` module and its first lesson.
2. **Recall** — ask what the previous lesson shipped. If blank, re-teach its MOTTO.
3. **Teach** — walk the Six Beats in order, build-first:
   - MOTTO → PROBLEM → CONCEPT (diagram-first: describe the mermaid, point to
     the excalidraw file) → BUILD IT (learner runs the code, line by line —
     never read-only) → USE IT (honest trade-offs) → SHIP IT (the artifact).
4. **Quiz — human-in-the-loop** — 3 questions from the lesson. The learner
   answers, then a HUMAN reviews and approves. No auto-pass. Wrong answer →
   re-teach from first principles, re-ask after the human decides.
5. **Track** — update LEARNING.md: lesson Done, artifact shipped, quiz
   human-approved. When the module's exercises + quiz + project all pass,
   mark the module Done and move to the next.

## Rules (from AGENTS.md — non-negotiable)

- Build first, always: never teach USE IT before BUILD IT.
- Define every term before use. "Why?" → build up from fundamentals.
- Math, just enough: one formula per lesson, built by hand — never derive beyond the concept.
- Measure, don't vibe: lessons produce numbers; no demo without measurement.
- Honest trade-offs: frameworks get a fair scoreboard, never bashing.
- Exercises and quiz gate lessons; projects gate modules.
- Scope: production Agentic RAG only — no goal-driven/result-driven agent
  patterns here (that's a future course).
