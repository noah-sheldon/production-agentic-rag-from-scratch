# RAG

Retrieve relevant chunks, then ask the model with the chunks in the prompt.

- Semantic RAG grabs matching documents once and asks once.
- Agentic RAG keeps going: search, read, search again, compare.
- The answer must cite the file it came from.
- If no document passes the grade, say "I found no relevant note" —
  never answer from nothing.
