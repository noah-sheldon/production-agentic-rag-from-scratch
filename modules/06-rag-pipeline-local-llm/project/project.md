# Module 06 Project — Ask Your Notes (private, local)

**Goal:** a CLI that answers questions from YOUR notes — retrieve → trim →
prompt → model → answer, with sources, streaming, and measurements. No cloud
API: your notes never leave your machine. The RAG flow from lesson 01, the
trimming from lesson 02, the streaming from lesson 03 — wired together.

## What ships

`project/skeleton/`:

| File | What it is |
|---|---|
| `ask.py` | the CLI: ties retrieve → trim → prompt → model together, prints sources + measurements |
| `retrieve.py` | keyword retrieval over `notes/` (TODO: swap scoring for module 03's BM25) |
| `prompt.py` | prompt template + sentence-level trim with a token budget |
| `model.py` | the fake stand-in model + a real Ollama client (with fallback) |
| `stream.py` | SSE-style token stream for `--stream` |
| `notes/*.md` | sample notes so it runs out of the box — replace with YOURS |

## How to run it

```bash
cd modules/06-rag-pipeline-local-llm/project/skeleton
python3 ask.py "how do I run a local model?"
python3 ask.py --stream "why does the deploy fail?"
python3 ask.py --model ollama "what is RAG?"      # when Ollama is running
```

## Acceptance criteria — done means all of these pass

1. **Grounded answer.** `python3 ask.py "how do I run a local model?"` answers
   from the notes and shows the sources — the answer text comes from a note,
   not from thin air.
2. **No guessing.** A question with no matching note (try "what is the capital
   of france?") gets "I don't know" — never an invented answer.
3. **Trimmed prompt.** The prompt stays under `--budget` tokens; the tool
   prints the prompt size in chars and tokens every run.
4. **Streaming.** `--stream` prints the answer word by word (flush after each),
   not as one big print.
5. **Measured.** Every run prints retrieve/trim/model latency in ms.
6. **Real model optional.** `--model ollama` calls the real local model when
   Ollama is up; when it is not, it falls back to the fake with a clear
   warning instead of crashing.
7. **Your notes.** Dropping your own `.md` files into `notes/` changes what
   the tool answers — that is the point.

## TODOs (each ties to a lesson)

1. Swap the word-overlap scoring in `retrieve.py` for the BM25 you built in
   module 03 (Lesson 01).
2. Tune the budget and the sentence trim in `prompt.py` for your notes; measure
   how quality changes with the budget (Lesson 02).
3. Make `ollama_model` the default once Ollama runs on your machine, and give
   it a timeout + retry like module 02 (Lesson USE IT).
4. Stream from the real model: set `"stream": true` in the Ollama call and
   forward each token to `token_stream` (Lesson 03).
5. (Stretch) Add a cache so repeated questions skip the model — the setup for
   Module 07.
