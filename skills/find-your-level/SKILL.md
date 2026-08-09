---
name: find-your-level
version: 1.0.0
description: >
  Five-question placement quiz for the Production Agentic RAG from Scratch
  course — maps knowledge to a starting module and produces a personalized
  path. Used by /start-learning. Trigger: "find your level", "placement"
tags: [placement, curriculum, agentic-rag]
---

# Find Your Level

Five questions, then a starting module. Human-reviewed where it matters.

## Questions

1. Comfort with Python? (none / basic / confident)
2. Built a RAG system? (never / tried / shipped)
3. Built an agent loop? (never / tried / shipped)
4. Comfort with Docker / infra? (none / some / comfortable)
5. What do you want to build? (RAG / agents / production / everything)

## Mapping

- Python none OR infra none → **Module 0** (setup first)
- RAG never → **Module 1**
- RAG tried, loop never → **Module 4** (chunking/embeddings onward)
- Shipped RAG + loop → **Module 8** (tools + the loop), then 9
- Unsure → default **Module 0** (safe: build-up rule means no skipping)

## Output

Starting module + a Path table (modules 0-9, statuses To Do / In progress /
Done) with the gates (exercises + HITL quiz + project). Ask the human to
confirm the entry point before writing the plan.
