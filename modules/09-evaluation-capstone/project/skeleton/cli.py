"""A terminal chat with the capstone assistant — decisions visible.

Run:  python3 cli.py              # honest model
      python3 cli.py --mode flaky # watch the gate catch the liar
Type a question, press enter. Type 'quit' to leave.
"""
import sys

from assistant import Assistant


def _mode(argv: list[str]) -> str:
    if "--mode" in argv:
        i = argv.index("--mode")
        if i + 1 < len(argv) and argv[i + 1] == "flaky":
            return "flaky"
    return "grounded"


def main() -> None:
    mode = _mode(list(sys.argv[1:]))
    agent = Assistant(mode=mode)
    print(f"notes assistant (mode: {mode}). Type a question, 'quit' to leave.")
    print(f"indexed notes: {', '.join(sorted(agent.notes))}\n")
    while True:
        try:
            question = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not question:
            continue
        if question.lower() in ("quit", "exit"):
            break
        result = agent.answer(question)
        print(f"tool: {result['used_tool']}  citations: {result['citations']}  "
              f"decision: {result['decision']}  groundedness: {result['groundedness']}")
        print(f"assistant> {result['answer']}\n")


if __name__ == "__main__":
    main()
