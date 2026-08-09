# Module 09 Project — Measure, Ship, Publish Your Assistant (the capstone)

**Goal:** your complete agentic RAG assistant over YOUR notes — tools, the
loop, an eval set, scoring, and a grade gate — assembled from every module
before it, measured with numbers, and walked through a publish checklist.
This is the module that finishes the knowledge assistant: from an empty
machine to something you can point other people at.

## What ships

`project/skeleton/` — a runnable assistant in plain Python (stdlib only,
fake-LLM mode) over `notes/`:

| File | What it is |
|---|---|
| `retrieval.py` | index your notes (ingest + chunk), search them (BM25-lite), read a note |
| `assistant.py` | the agent: tool registry, the loop (decide → call → check → repeat), fake LLM, grade gate |
| `gate.py` | the grade gate: pass / retry / fallback + the honest "I don't know" reply |
| `eval.py` | score the assistant over `eval_set.json`, write `eval_report.json` |
| `cli.py` | a terminal chat: `python3 cli.py` |
| `notes/` | sample notes — replace them with YOUR notes |
| `eval_set.json` | sample eval set — replace with questions about YOUR notes |
| `publish_checklist.md` | the repo / README / video plan you walk through at the end |

## How to run it

```bash
cd modules/09-evaluation-capstone/project/skeleton
python3 eval.py                    # score the assistant (honest model)
python3 eval.py --mode flaky       # the liar gets caught by the gate
python3 cli.py --mode flaky        # chat with the assistant, see decisions
python3 assistant.py "when does the nightly deploy run"   # one-shot answer
```

## Acceptance criteria — done means all of these pass

1. **Assembled.** All the module 0-8 pieces are present and wired: notes
   ingested + chunked (0, 2, 4), search over them (3, 5), the agent loop
   with a tool registry (8), and the module 09 eval set + scoring + gate.
2. **Measured.** `eval.py` writes `eval_report.json` — per-question and
   average groundedness/recall — and you committed it with your results.
3. **The gate works.** With `--mode flaky`, hallucinated answers become
   honest fallbacks; `eval_report.json` shows zero hallucinated answers
   shipped after the gate.
4. **Yours.** `notes/` holds at least 5 of YOUR notes, and `eval_set.json`
   has 10+ real questions about them with known-good answers and sources.
5. **Documented.** `README.md` in the skeleton (or in your repo) explains
   the assistant, how to run it, and its eval numbers.
6. **Published.** You walked the `publish_checklist.md` — repo public,
   README done, video planned (or filmed).

## TODOs (each ties to a lesson or module)

1. Replace the sample notes with YOUR notes (Modules 0-2 pieces).
2. Expand `eval_set.json` to 10+ real questions — labels first, then score
   (Lesson 01).
3. Wire your real chunker/index (Modules 4-5) behind `retrieval.py`'s
   `build_index`/`search` — the skeleton's functions are the seam.
4. Swap the fake LLM for a real one (Ollama, Module 6) behind `FakeLLM`'s
   `generate` — the gate and eval then measure the real model.
5. Tune the gate threshold on your eval set; record before/after numbers
   (Lesson 03).
6. Commit `eval_report.json`, write the README, make the video
   (publish checklist).
