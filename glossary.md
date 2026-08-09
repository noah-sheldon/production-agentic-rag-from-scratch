# Glossary — terms in simple words

Every term defined as Noah would explain it: grade-5 words, no jargon.

- **RAG** — a way to let an AI answer from your own data
- **LLM** — a big AI model that reads and writes text
- **context window** — how much text the model can see at once
- **tokens** — small pieces of words
- **chunk** — a small piece of text
- **embedding** — numbers that capture meaning
- **vector** — a list of numbers
- **vector store** — a database that searches by meaning
- **sparse vector** — a word-count list with lots of zeros
- **dense embedding** — a short list of numbers learned by a model
- **semantic similarity search** — finding text that means the same thing
- **retriever** — the part that fishes out relevant documents
- **k** — how many chunks you pull back
- **prompt template** — fill-in-the-blanks instructions for the AI
- **output parser** — turns the AI's reply into clean text
- **chain** — steps wired together in order
- **query translation** — rewriting the question to search better
- **reranking / rank fusion** — re-sorting the search results
- **function calling** — the model uses a tool to build a filter
- **DSL / domain specific language** — the special query language of a database (SQL, filters)
- **hallucination** — the AI makes things up
- **grading** — checking whether documents or answers are good enough
- **nodes / edges** — steps and decisions in a flow diagram
- **trace** — a recorded log of every step for debugging (LangSmith)
- **needle-in-haystack** — a test that hides one fact in a lot of text to see if the model finds it
- **agent loop** — the model decides what to do next, does it, checks the result, and repeats until done
- **tool / tool definition** — a small program the model can call
- **tool-calling** — the model asking a tool to run
- **semantic RAG** — the classic way: grab matching documents once, then ask the model once
- **LLM API call** — one request to the model
- **docstring** — the description of a tool that teaches the model how to use it
- **grep** — search that finds every matching line, with line numbers
- **subprocess** — a Python program starting another program (Ripgrep) and reading its output
- **structured output** — the answer forced into a fixed shape other programs can rely on
- **citations** — the exact file, quote, and line the answer came from
- **memory** — the agent keeping track of what it already found while working
- **reflection** — the model looking at its own result and judging if it is good enough
- **planner** — a step where the model writes out a plan before acting
- **ReAct** — a pattern where the model thinks, then acts, then looks at the result
- **re-ranker** — a second step that sorts the best matches first

## Module 01 — Production Infrastructure

- **process** — a running program, with its own memory and a number the system uses to name it
- **PID** — the process ID, the number the operating system uses to name a running program
- **subprocess** — a Python program starting another program and reading its output
- **isolation** — keeping one program's files and settings away from another's
- **container** — a lightweight box that runs one program with its own files, settings, and network ports
- **image** — the frozen blueprint a container is built from
- **Docker** — a tool that builds and runs containers
- **Docker Compose** — a tool that starts many containers from one config file with one command
- **port** — a numbered door on a machine programs use to talk to each other
- **volume** — a folder on your machine shared with a container, so data survives restarts
- **endpoint** — one address (URL) where a program answers a request
- **API** — a set of defined requests one program makes to another
- **health check** — a small request a program answers to prove it is truly working, not just alive
- **status code** — the number a server sends back to say how a request went (200 = ok, 503 = not ready)
- **async** — code that waits without blocking, so one slow request does not freeze the rest
- **database** — a program that stores data and answers queries
- **SQL** — the query language of relational databases
- **schema** — the fixed shape of the data a database stores
- **index** — a structure a database builds so it can find data fast without scanning everything
- **ORM** — a layer that turns database rows into Python objects
- **search engine** — a program that builds an index of text and answers "find me the best matches" queries
- **inverted index** — the search engine's map from words to the documents that contain them
- **PostgreSQL (Postgres)** — a server database that many programs can connect to over the network
- **OpenSearch** — a search engine that indexes text for fast keyword search
- **Ollama** — a tool that runs large language models on your own machine
- **linter** — a tool that checks code style and catches mistakes before the code runs
- **formatter** — a tool that rewrites your code to one consistent style
- **type checker** — a tool that checks the data types in your code before it runs
- **test** — a small program that checks your code does what you expect
- **pre-commit** — a tool that runs checks automatically before you save a change to git

## Module 04 — Chunking and Embeddings

- **section chunker** — a chunker that cuts a document at its headings
- **fixed-size chunker** — a chunker that cuts text into equal-length pieces
- **chunk overlap** — a few words repeated at the end of one chunk and the start of the next, so no idea is cut in half
- **dimension** — one of the numbers in a vector (384 numbers = 384 dimensions)
- **cosine similarity** — a score between -1 and 1 for how close two vectors point; near 1 = similar
- **normalized vector** — a vector scaled so its length is 1, which makes cosine similarity equal to a plain dot product
- **fallback** — the backup plan when the main tool is down (cached data, then keyword search, then a smaller model)

## Module 08 — Agentic RAG: Tools + the Loop

- **tool schema** — the name, description, and list of inputs that tell the model what a tool does
- **tool registry** — one place that holds every tool and lets you look it up by name
- **max turns** — the biggest number of decide-call-repeat rounds an agent is allowed
- **guardrail** — a rule that stops the flow when the input is out of bounds
- **out-of-domain** — a question about a topic the system was never given
- **relevant / irrelevant** — a retrieved document's verdict: does it actually answer the query, or not
- **query rewriting** — fixing a bad question before it goes to search
- **decision log** — a written record of every choice the agent made, and why
- **reasoning transparency** — showing the agent's work: what it called and why
- **LangGraph** — a library that draws the agent loop as a graph of nodes and edges
- **fake mode** — running the agent with a pretend model, so the loop works without an API key

## Module 09 — Evaluation + Capstone

- **eval set** — a list of questions with known-good answers, used to score an assistant
- **known-good answer** — the answer a human agrees is correct for one eval question
- **label** — the correct answer (or the correct note) written by a human for a question
- **ground truth** — the real answer we know is true, written down before the model answers
- **groundedness** — the share of an answer's words that came from the retrieved notes, not invented
- **faithfulness** — another word for groundedness: does the answer stick to the source
- **grade gate** — a check that rejects low-scoring answers before they reach the user
- **retry** — running the answer step again with more context or a better search
- **fallback** — the safe answer when the assistant is not sure: "I don't know" plus citations
- **pass rate** — the share of eval questions the assistant answers well enough to ship
- **acceptance criteria** — the tests that decide if a project is done
- **publish checklist** — the list of things to do before showing your assistant to others

## Module 07 — Observability & Caching

- **observability** — being able to see what your system does: timings, tokens, costs, and failures
- **span** — one named step inside a trace (for example, the retrieve step)
- **cache** — a place that remembers past answers so the work isn't repeated
- **cache key** — the thing that names a cached answer (usually the question, cleaned up)
- **hit** — the cache already has the answer, so the pipeline is skipped
- **miss** — the cache doesn't have the answer, so the pipeline runs
- **hit rate** — hits divided by total questions; how often the cache saves you
- **TTL (time-to-live)** — how long a cached answer lives before it expires
- **cost per question** — the price of one answer: tokens times prices
- **dashboard** — one screen that shows the numbers that matter (latency, cost, hit rate)
- **Langfuse** — a tool that records traces and cost per call, shown in a web UI
- **Redis** — a fast cache many programs can share over the network
