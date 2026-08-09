# Artifact — the tool-design checklist

Before a model ever sees a tool, check every line:

- [ ] **Name like a verb** — `search_notes`, `read_note`, `list_notes`. Not `notes`.
- [ ] **Description says WHEN to use it** — "use AFTER search_notes to read one
      full note", not "reads a note".
- [ ] **Parameters minimal and typed** — `query: string`, `k: integer`. The
      model guesses from the schema; make the guess easy.
- [ ] **`required` lists only what's truly required** — every required param
      is one more chance to fail.
- [ ] **Each tool is testable by hand** — `registry.call("read_note", name=...)`
      works before the model touches it.
- [ ] **Unknown names and bad arguments fail loudly** — never silently return
      empty text; raise with the list of known tools.
- [ ] **The schema is the manual** — the model never sees your code, only
      name + description + params. A lazy docstring is a broken tool.

Wiring the schema to a real model call (binding) is lesson 02's job. The
registry is done when `describe()` prints schemas and `call()` runs tools.
