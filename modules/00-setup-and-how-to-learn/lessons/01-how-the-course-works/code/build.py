"""Build it: the course at a glance (stdlib only).

Run:  python3 build.py
"""
MODULES = [
    ("0", "Setup + How to Learn", "gate: check_setup passes"),
    ("1", "Production Infrastructure", "gate: dev lab skeleton"),
    ("2", "Data Ingestion", "gate: read-it-later pipeline"),
    ("3", "Keyword Search First (BM25)", "gate: BM25 over your notes"),
    ("4", "Chunking + Embeddings", "gate: semantic index"),
    ("5", "Hybrid Search (RRF)", "gate: hybrid search"),
    ("6", "RAG Pipeline + Local LLM", "gate: ask your notes"),
    ("7", "Observability + Caching", "gate: cost + cache dashboard"),
    ("8", "Agentic RAG: Tools + the Loop", "gate: notes assistant"),
    ("9", "Evaluation + Capstone", "gate: measure, ship, publish"),
]


def main() -> None:
    print("Production Agentic RAG from Scratch — the map\n")
    for num, title, gate in MODULES:
        print(f"  M{num}  {title:<38} {gate}")
    print("\nYou are here: M0. Build first. Frameworks second. Always.")


if __name__ == "__main__":
    main()
