"""Build it: trace every step of a RAG-style flow in plain Python (stdlib only).

Run:  python3 build.py
Prints a per-step breakdown — retrieve, prompt, answer — in milliseconds and
percent of total, and names the slowest step.
"""
import time


def retrieve(question: str) -> list[str]:
    """Pretend search — in module 06 this is your real retriever."""
    time.sleep(0.020)
    return [f"chunk about: {question}"]


def build_prompt(question: str, chunks: list[str]) -> str:
    """Pretend prompt building — the model call starts here."""
    time.sleep(0.005)
    return "Q: " + question + "\nContext:\n" + "\n".join(chunks)


def answer(prompt: str) -> str:
    """Pretend model call — usually the slowest step."""
    time.sleep(0.035)
    return "Answer: " + prompt.splitlines()[0][3:]


class Tracer:
    """A named timer around every step. That's all a trace is."""

    def __init__(self) -> None:
        self.steps: list[tuple[str, float]] = []  # (name, milliseconds)

    def step(self, name: str, fn):
        t0 = time.perf_counter()
        result = fn()
        self.steps.append((name, (time.perf_counter() - t0) * 1000.0))
        return result


def main() -> None:
    question = "What is RAG?"
    tracer = Tracer()

    chunks = tracer.step("retrieve", lambda: retrieve(question))
    prompt = tracer.step("prompt", lambda: build_prompt(question, chunks))
    out = tracer.step("answer", lambda: answer(prompt))

    total = sum(ms for _, ms in tracer.steps)
    print(f"question: {question}")
    print(f"{'step':<10}{'ms':>8}{'% of total':>12}")
    for name, ms in tracer.steps:
        print(f"{name:<10}{ms:>8.1f}{100.0 * ms / total:>11.1f}%")
    print(f"{'total':<10}{total:>8.1f}{'100.0%':>12}")

    slowest = max(tracer.steps, key=lambda s: s[1])
    print(f"\nanswer: {out}")
    print(f"where the time goes: {slowest[0]} ({slowest[1]:.1f} ms)")


if __name__ == "__main__":
    main()
