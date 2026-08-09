# Agents

An agent is a loop plus tools. The model decides what to do next, calls a
tool, checks the result, and repeats until it can answer.

Key ideas:

- The loop is the agent — decide, call, check, repeat.
- The tool registry holds every tool with its schema.
- Guardrails stop bad questions before any tool runs.
- Grade every retrieved document before it reaches the prompt.
- Log every decision with a reason — that is reasoning transparency.
