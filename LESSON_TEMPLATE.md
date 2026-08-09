# Lesson Template — Six Beats

Every lesson ships as `phases/<NN>-<phase>/<NN>-<lesson-slug>/` with:

```
code/       runnable plain-Python implementation (frameworks only in USE IT)
docs/
  en.md     lesson narrative (this template)
diagrams/   mermaid + excalidraw for the CONCEPT beat
outputs/    the artifact this lesson produces (skill, prompt, or module)
```

## Beats

### MOTTO
One line. The core idea, grade-5 words, memorable.

### PROBLEM
The concrete pain — a question or task that fails with naive tools. Show the
failure. Why this lesson exists.

### CONCEPT
Intuition first, from first principles. Diagrams (mermaid flow + excalidraw).
Define every term before use. Build up slowly. No unexplained jargon.

### BUILD IT
Raw implementation in plain Python. No framework imports. Every line earned.
This is the teaching core — the learner sees the system.

### USE IT
Same thing with the framework (LangChain / Pydantic AI / etc.). Honest
scoreboard: what the framework gives (time, tracing, integrations) vs what it
hides (the loop, the cost, the failure modes). Never framework bashing.

### SHIP IT
The reusable artifact: a runnable module, a prompt, a skill, or a checklist
the learner can use tomorrow. The lesson is not done until something ships.

## Rules

- Every term defined before use.
- No copied code from tutorials — build it, then compare.
- Results measured (numbers, tokens, latency) — never vibes.
- The BUILD IT beat always precedes the USE IT beat.
