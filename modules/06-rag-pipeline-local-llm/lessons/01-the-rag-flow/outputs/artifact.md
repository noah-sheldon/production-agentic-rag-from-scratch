# Artifact — the RAG flow skeleton

Reusable retrieve → prompt → answer flow. Point it at any note corpus.

```python
def answer(question, notes, model, k=2):
    top = retrieve(question, notes, k=k)          # 1. find matching notes
    context = "\n".join(f"[{t}] {x}" for t, x in top)
    prompt = build_prompt(context, question)      # 2. context + question
    return model(prompt)                          # 3. answer from context
```

Checklist:

- [ ] Retrieve FIRST — the model only sees the relevant notes (k of them)
- [ ] Prompt template: context before question, "say I don't know" instruction
- [ ] Model answers from the context only — grounded, no invented facts
- [ ] No matching note → honest "I don't know", never a guess
- [ ] Sources printed with the answer (which notes were used)
- [ ] Every step measured (retrieve / prompt / answer latency)
- [ ] Model is a swappable function — fake now, Ollama later, cloud never (module 06)
