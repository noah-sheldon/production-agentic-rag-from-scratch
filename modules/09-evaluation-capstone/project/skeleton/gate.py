"""The grade gate: pass good answers, retry shaky ones, refuse the rest.

Run:  python3 gate.py    (prints a quick self-check)
"""
THRESHOLD = 0.5  # groundedness at or above this ships


def decide(score: float, threshold: float = THRESHOLD) -> str:
    """pass: good enough to ship. retry: shaky, try once more.
    fallback: not trustworthy — refuse with citations."""
    if score >= threshold:
        return "pass"
    if score >= threshold / 2:
        return "retry"
    return "fallback"


def fallback_answer(question: str, note_ids: list[str], index: dict) -> str:
    """The honest refusal: 'I don't know' plus the closest notes."""
    names = [index[n]["title"] for n in note_ids] or ["nothing found"]
    return (f"I don't know — that is not in my notes. "
            f"Closest notes I found: {', '.join(names)}.")


def main() -> None:
    for score in (0.9, 0.4, 0.1):
        print(f"score {score:>4} (threshold {THRESHOLD}) -> {decide(score)}")
    print("fallback example:", fallback_answer("q", ["deploy"], {
        "deploy": {"title": "Deploy Notes"}}))


if __name__ == "__main__":
    main()
