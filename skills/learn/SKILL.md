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
   **Never skip Module 0 lesson 01 (how-the-course-works): it teaches how to use
   this course (Six Beats, gates, HITL, the three ways to learn). Teach it
   before any other lesson — it's 5 minutes even for experienced learners.**
2. **Recall** — ask what the PREVIOUS lesson shipped, but ONLY if a previous
   lesson's quiz is human-approved in the log. If this is the first lesson, or
   the current lesson has NO human-approved quiz in the log — **it has not been
   taught. Teach the full Six Beats now (step 3), then quiz (step 4).** A
   progress-log entry alone NEVER marks a lesson as taught or done.
3. **Teach** — walk the Six Beats in order, build-first, FROM THE FULL LESSON
   DOC (don't over-compress — present the CONCEPT explanation properly, and
   tell the learner they can read `docs/en.md` alongside):
   - MOTTO → PROBLEM → CONCEPT (describe the mermaid — it renders in the
     terminal; the excalidraw file is for whiteboard FILMING, not terminal
     learning — mention it only if the learner asks or films) → BUILD IT
     (mandatory: the learner RUNS the code, line by line, never read-only —
     if they can't run Python, finish Module 0 first) → USE IT (honest
     trade-offs) → SHIP IT (the artifact).

   **BUILD IT, taught properly — the code must be UNDERSTOOD, not just run:**
   - Open `code/build.py` with the learner. Walk it SECTION BY SECTION, line by
     line, in plain words: what each function does, what each variable means,
     why each step exists. Never assume they read code fluently.
   - **Predict-then-run:** before they execute, ask "what do you expect to see?"
     They run it, compare, and explain the output back to you.
   - If they can't explain what the code does or what they saw, RE-TEACH that
     section from first principles — never move on with "it ran".
   - Every lesson's build code must be simple enough to walk this way (stdlib,
     one idea per function) — if it isn't, flag the lesson for a rewrite.
   Never quiz before teaching the current lesson's beats.
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
