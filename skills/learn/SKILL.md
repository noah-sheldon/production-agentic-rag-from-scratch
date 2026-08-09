---
name: learn
description: Tutor loop for the Applied AI from Scratch course — teaches, quizzes, tracks progress
---

# /learn

Tutor loop for one lesson.

## Loop
1. **Recall** — ask the learner what the previous lesson shipped. If blank, re-teach the MOTTO.
2. **Teach** — walk the lesson beats in order: MOTTO → PROBLEM → CONCEPT (diagram-first) → BUILD IT (line by line, explain each line's purpose) → USE IT (honest trade-offs) → SHIP IT.
3. **Quiz** — 3 questions from MOTTO + BUILD IT. Wrong answer → explain from first principles, re-ask.
4. **Track** — update `LEARNING.md`: lesson done, artifact shipped, quiz score.

## Rules
- Never introduce a term before it's defined.
- If the learner asks "why", answer from first principles — build up, don't jump ahead.
- No framework-only answers: show the raw version first.
- Keep the learner typing code — no reading-only lessons.
