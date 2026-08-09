# Publish checklist — from working code to something others can use

Walk this top to bottom. Each item is one small step; do them in order.

## 1. The repo

- [ ] Source in a public git repository (GitHub) with a clear name
- [ ] MIT license file (or the one you chose)
- [ ] `.gitignore`: `.venv/`, `__pycache__/`, `.env`, local artifacts
- [ ] `eval_report.json` committed — your measured results are part of the story
- [ ] One command to run it, written in the README — and you tested that command from a clean clone

## 2. The README

- [ ] What it is, in one sentence: "an agentic RAG assistant over my notes"
- [ ] A screenshot or short demo (an animated GIF of the CLI is enough)
- [ ] Quickstart: install, run, ask a question
- [ ] Architecture: one diagram (the agent loop + tools + gate)
- [ ] Numbers: the eval report — groundedness, recall, pass rate — and the threshold you chose, and why
- [ ] Honest limits: one question it gets wrong (module 3's lesson applies to assistants too)

## 3. The video plan (3-5 minutes, for the content pipeline)

1. **Hook (0:00-0:15):** one real question your assistant answers from YOUR notes
2. **The build (0:15-1:30):** notes in, search, agent loop with tools — plain Python
3. **The measurement (1:30-2:30):** the eval set, the score table, before/after the gate
4. **The gate (2:30-3:30):** `--mode flaky` — watch a hallucination get caught and become "I don't know"
5. **The publish (3:30-4:30):** repo, README, how someone else runs it
6. **Close (4:30-5:00):** the honest limit, and what you'd build next

## Done

When all three boxes are ticked, your assistant is no longer a project — it is a published system. That was the point of all ten modules (0-9).
