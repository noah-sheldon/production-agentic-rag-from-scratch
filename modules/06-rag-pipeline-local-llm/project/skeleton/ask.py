#!/usr/bin/env python3
"""Ask your notes — private, local.

A CLI that answers questions from your own notes folder:
  retrieve -> trim -> prompt -> model -> answer (with sources + measurements)

Run:
    python3 ask.py "how do I run a local model?"
    python3 ask.py --stream "what is RAG?"
    python3 ask.py --k 5 --budget 300 "why does the deploy fail?"
    python3 ask.py --model ollama "what is RAG?"     # real local model

Stdlib only. Your notes never leave this machine.
"""
from __future__ import annotations

import argparse
import sys
import time

from model import fake_model, ollama_model
from prompt import build_prompt, count_tokens, trim_context
from retrieve import load_notes, retrieve
from stream import token_stream


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ask your notes.")
    parser.add_argument("question", help="the question you want answered")
    parser.add_argument("--k", type=int, default=3, help="notes to retrieve (default 3)")
    parser.add_argument("--budget", type=int, default=200, help="max prompt tokens (default 200)")
    parser.add_argument("--stream", action="store_true", help="print the answer token by token")
    parser.add_argument(
        "--model", choices=["fake", "ollama"], default="fake",
        help="which model answers: the fake stand-in, or the real local Ollama",
    )
    args = parser.parse_args(argv)

    notes = load_notes()
    if not notes:
        print("no notes found in notes/ — drop some .md files in there first.")
        return 1

    if args.model == "ollama":
        def model(prompt: str) -> str:
            try:
                return ollama_model(prompt)
            except OSError as exc:
                print(f"  ! ollama not reachable ({exc}) — falling back to the fake model")
                return fake_model(prompt)
    else:
        model = fake_model

    t0 = time.perf_counter()
    top = retrieve(args.question, notes, k=args.k)
    t1 = time.perf_counter()
    context = trim_context(top, args.question, budget_tokens=args.budget)
    prompt = build_prompt(context, args.question)
    t2 = time.perf_counter()

    print(f"question: {args.question}")
    print(f"retrieved: {', '.join(title for title, _ in top)}")
    print(f"prompt: {len(prompt)} chars, ~{count_tokens(prompt)} tokens (budget {args.budget})")

    t3 = time.perf_counter()
    reply = model(prompt)
    t4 = time.perf_counter()

    if args.stream:
        for token in token_stream(reply):
            print(token, end=" ", flush=True)
        print()
    else:
        print(f"answer: {reply}")

    print(f"\nretrieve {(t1 - t0) * 1000:.0f} ms | trim {(t2 - t1) * 1000:.0f} ms | "
          f"model {(t4 - t3) * 1000:.0f} ms | total {(t4 - t0) * 1000:.0f} ms")
    print(f"sources: {', '.join(title for title, _ in top)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
