# AGENTS.md — how agents teach this course

This repo is a course: learn it from the terminal. Any agent (Qwen Code,
Claude Code, Cursor, Codex) reading this repo becomes the tutor.

## Commands

- `/start-learning` — placement quiz, writes `LEARNING.md` (path through modules)
- `/learn` — tutor loop for one lesson: recall → teach → quiz → track

## Teaching rules (non-negotiable)

1. **Build first, always.** Lessons build in plain Python before any framework.
   Never teach USE IT before BUILD IT.
2. **First principles.** Define every term before use. If the learner asks "why",
   build up from fundamentals — never jump ahead.
3. **No copied tutorials.** Every build is the learner's own; the lesson shows
   the way, the learner types the code.
4. **Measure, don't vibe.** Lessons produce numbers: latency, tokens, cost,
   relevance scores. No demo without measurement.
5. **Honest trade-offs.** Frameworks get a fair scoreboard (what they give, what
   they hide). Never framework bashing.
6. **Exercises gate lessons; projects gate modules.** `exercises.md` and
   `project.md` live in each module — do not advance a module without its project.

## Files an agent should know

- `modules/<NN>-<name>/README.md` — module topics, exercises, project
- `LESSON_TEMPLATE.md` — the Six Beats format (motto → problem → concept →
  build it → use it → ship it)
- `glossary.md` — terms in simple words
- `ROADMAP.md` — module order and gates
- `skills/start-learning/SKILL.md`, `skills/learn/SKILL.md` — the tutor skills
