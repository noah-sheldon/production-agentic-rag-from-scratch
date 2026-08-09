# Artifact — the agent-loop checklist

Every agent loop, by hand or in a framework, must:

- [ ] **Messages accumulate.** One `messages` list holds the user question,
      every assistant turn, every tool call, every tool result. Never rebuild
      it from memory.
- [ ] **Tool results are always appended** as `role: "tool"` messages —
      the model cannot "remember" a call it never sees the result of.
- [ ] **Arguments parsed with `json.loads`** — and the failure is caught:
      bad JSON from a model is a runtime event, not a crash.
- [ ] **Max turns budgeted.** A runaway agent burns tokens until the money
      runs out; the budget stops it first. Return a clear "budget spent"
      answer, never silence.
- [ ] **Unknown tools / tool errors become tool results**, not exceptions —
      the error text goes back to the model so it can recover.
- [ ] **Every turn logged** (what was called, what came back) — this is the
      trace you debug with (lesson 04 builds the full decision log).
- [ ] **Measured.** Turns used, latency, tokens — numbers on every run.

The loop is done when a model can search, read, and answer in one run —
and a model that never answers gets stopped by the budget.
