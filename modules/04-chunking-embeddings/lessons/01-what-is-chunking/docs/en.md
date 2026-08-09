# 01 — What Is Chunking

## MOTTO
> A document is a wall of text. Chunking builds the doors.

## PROBLEM
Your note is 5,000 words. A retriever that returns the whole note buries the one sentence that answers the question — the answer is diluted in noise. A naive fixed-size cut splits sentences mid-thought, so "the largest living rodent" ends up in two chunks and neither one is answerable. Long text needs to be cut into pieces that each still mean something.

## CONCEPT
A [chunk](../../../../../glossary.md#chunk) is a small piece of text. Chunking is the job of deciding where the cuts go. There are two families:

- A [section chunker](../../../../../glossary.md#section-chunker) cuts at headings — each section becomes one chunk, so one idea stays together.
- A [fixed-size chunker](../../../../../glossary.md#fixed-size-chunker) cuts every N words, no matter what the text says.

Both have a hole: a section can be longer than the model's [context window](../../../../../glossary.md#context-window), and a fixed cut lands mid-sentence. The patch is [chunk overlap](../../../../../glossary.md#chunk-overlap) — repeat the tail of one chunk at the head of the next, so a sentence that straddles a cut is still whole somewhere.

```mermaid
flowchart LR
    D["5000-word note"] --> H["find headings"]
    H --> S["cut into sections"]
    S --> O["add overlap where a piece is too long"]
    O --> C["chunks: one idea each"]
    C --> R["retriever pulls the right piece"]
```

**Diagram (whiteboard):** open `diagrams/chunking.excalidraw` in excalidraw.com — same picture, traceable by hand.

## BUILD IT

```bash
python3 lessons/01-what-is-chunking/code/build.py
```

A plain-Python [section chunker](../../../../../glossary.md#section-chunker): split a note at `#`-level headings, then re-split any section longer than `max_words` into pieces that carry `overlap_words` of the previous tail. It prints every chunk with its heading and word count, and proves the overlap by showing the words two neighbors share.

## USE IT
Framework splitters (LangChain's recursive text splitter is the common one) do the same with separator priority built in.

| Framework gives you | Framework hides from you |
|---|---|
| separators (headings, paragraphs, sentences) tried in order | that you still pick the separators and the size |
| overlap out of the box | what happens when your text has no headings |
| a consistent API across file types | the measurement of whether the cuts are good |

Honest trade-off: the framework saves you the splitting loop. It does not choose the chunk size for you — that choice is the next lesson.

## SHIP IT
The chunk-by-sections pattern — `outputs/artifact.md`: the function to paste into any pipeline, plus the checklist (keep headings, cap the size, add overlap).
