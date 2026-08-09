# Module 08 Project — Notes Assistant with Tools

**Goal:** a runnable assistant over your notes folder that *acts* — it
guards the question, rewrites it, searches, reads, grades, cites, and logs
every decision. It runs keyless (FAKE mode) or against any OpenAI-compatible
endpoint with `OPENAI_API_KEY`. The module 06 RAG pipeline grows hands.

## What ships

`project/skeleton/`:

| File | What it is |
|---|---|
| `assistant.py` | the entry point: guard → rewrite → agent loop (decide/call/result/repeat) → grounded answer, decision log on every step |
| `tools.py` | the tool registry over `notes/`: `list_notes`, `search_notes`, `read_note` (lesson 01) |
| `guard.py` | guardrail + query rewriting + the decision log (lessons 03 + 04) |
| `notes/` | four sample notes (replace with YOURS) — drop your own `.md` files in |

## How to run it

```bash
cd modules/08-agentic-rag-tools-loop/project/skeleton
python3 assistant.py                                   # FAKE mode, keyless
python3 assistant.py "what did I write about agents?"  # your question
OPENAI_API_KEY=... python3 assistant.py "does my evals note mention grading?"  # real
cat decision_log.jsonl                                 # the trace — every decision, with why
```

Environment: `OPENAI_API_KEY` switches FAKE → real. Optional
`OPENAI_BASE_URL` (default `https://api.openai.com/v1`) and `OPENAI_MODEL`
(default `gpt-4o-mini`) — any OpenAI-compatible endpoint works.

## Acceptance criteria — done means all of these pass

1. **Keyless.** `python3 assistant.py` answers a question end to end with no
   API key — FAKE mode exercises the real loop.
2. **Guarded.** An out-of-domain question ("best pizza in London") is rejected
   with a reason before any tool call — no search, no cost.
3. **Rewritten.** A bad query ("the one about evals") is rewritten before it
   searches, and the before/after is logged with chars saved.
4. **Tools work.** The registry runs `list_notes`, `search_notes`, `read_note`
   over `notes/`; the answer cites the file it came from.
5. **Evidence graded.** Only relevant documents reach the answer — the grade
   (score + verdict) is in the log.
6. **Every decision logged.** `decision_log.jsonl` tells the story of the run:
   guard verdict, rewrite, search scores, grade, answer — each with a why.
7. **Real mode works.** With `OPENAI_API_KEY`, the model drives the tools
   itself (same loop, real decisions).
8. **YOUR notes.** Replace the sample notes with your own; the assistant
   answers from them.

## TODOs (each ties to a lesson)

1. Expand `tools.py` — add `search_notes` improvements from Module 05
   (hybrid search) so the agent searches like Module 05 does (Lesson 01).
2. Swap the FAKE model for a real model in `assistant.py` and watch the loop
   make its own decisions (Lesson 02).
3. Tighten the guardrail to YOUR domain — the topic list in `guard.py` is a
   stand-in (Lesson 03).
4. Add your own rewriting heuristics ("the one about X", pronouns) to
   `guard.py` and re-measure (Lesson 04).
5. Point `notes/` at your real notes folder and re-run the trace (Lessons 01–04).
