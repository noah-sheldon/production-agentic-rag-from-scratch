---
name: check-understanding
version: 1.0.0
description: >
  Per-module quiz for the Production Agentic RAG from Scratch course — runs
  the module's quiz.md with human-in-the-loop review and recommends lessons
  to review. Trigger: "check understanding", "quiz me on module N"
tags: [quiz, curriculum, agentic-rag, hitl]
---

# Check Understanding

Run a module's quiz with HITL review. Content source: course repo
`noah-sheldon/production-agentic-rag-from-scratch` — read `modules/<NN>/quizzes/quiz.md`
locally if present, else fetch from
`https://raw.githubusercontent.com/noah-sheldon/production-agentic-rag-from-scratch/master/`.

## Flow

1. Load `modules/<NN>-*/quizzes/quiz.md` for the requested module.
2. Ask each question, one at a time. The learner answers from memory — no
   peeking at lessons.
3. **Human-in-the-loop:** after the learner answers, a HUMAN reviews every
   answer against the quiz.md review guide. No auto-pass, no skipping.
4. Wrong answers → list the exact lessons to re-read (use course-guide to
   map the topic to a lesson).
5. Update LEARNING.md: quiz result + review queue entries.

## Rules

- Never reveal the review guide to the learner before they answer.
- Never auto-approve — a human decides, always.
- Module 0 quiz gates the whole course start.
