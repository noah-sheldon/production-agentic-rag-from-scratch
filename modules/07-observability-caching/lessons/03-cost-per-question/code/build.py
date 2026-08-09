"""Build it: token counting + a pricing table + the 1,000-question math.

Run:  python3 build.py
Prints the pricing table, one question's cost, the model-vs-retrieval ratio
(the 150-400x band), and the cost of 1,000 questions with and without a cache.
"""
import random


# ---- pricing table: USD per 1 million tokens (edit to your real prices) ----
PRICES = {
    "embed": 0.02,   # embedding model (retrieval)
    "input": 2.50,   # LLM input tokens
    "output": 10.00, # LLM output tokens
}

EMBED_TOKENS = 1000  # retrieval tokens per question
INPUT_TOKENS = 1000  # prompt tokens per question
OUTPUT_TOKENS = 300  # answer tokens per question
N_QUESTIONS = 1000


def count_tokens(text: str) -> int:
    """Naive token count: 4 characters ≈ 1 token."""
    return len(text) // 4


def call_cost(in_tokens: int, out_tokens: int) -> float:
    """Dollars for one model call."""
    return (in_tokens * PRICES["input"] + out_tokens * PRICES["output"]) / 1_000_000


def main() -> None:
    retrieval = EMBED_TOKENS * PRICES["embed"] / 1_000_000
    model = call_cost(INPUT_TOKENS, OUTPUT_TOKENS)
    ratio = model / retrieval

    print("== pricing table (per 1M tokens) ==")
    for name, price in PRICES.items():
        print(f"  {name:<8}${price:>7.2f}")
    print(f"\ntoken demo: count_tokens('production agentic rag') = "
          f"{count_tokens('production agentic rag')}")
    print(f"retrieval per question: ${retrieval:.5f} ({EMBED_TOKENS} embedding tokens)")
    print(f"model call per question: ${model:.5f} ({INPUT_TOKENS} in + {OUTPUT_TOKENS} out)")
    print(f"-> the model call is {ratio:.0f}x the retrieval cost (150-400x band)")

    # 1,000 questions: a tiny FAQ — only 4 unique questions, everything else repeats
    unique = ["what is rag?", "how do chunks work?", "why do tokens matter?", "what is a ttl cache?"]
    random.seed(7)
    questions = [random.choice(unique) for _ in range(N_QUESTIONS)]

    cache = set()
    cost_with = 0.0
    cost_without = 0.0
    for q in questions:
        cost_without += model + retrieval   # no cache: full price every time
        if q in cache:
            cost_with += 0.0                # exact-match hit: 0 tokens, 0 dollars
        else:
            cache.add(q)
            cost_with += model + retrieval  # miss: one full answer

    factor = cost_without / cost_with
    hit_rate = (N_QUESTIONS - len(cache)) / N_QUESTIONS

    print(f"\n== {N_QUESTIONS} questions ==")
    print(f"unique questions : {len(cache)}")
    print(f"cache hits       : {N_QUESTIONS - len(cache)} ({hit_rate:.1%})")
    print(f"cost without cache: ${cost_without:.2f}")
    print(f"cost with cache   : ${cost_with:.4f}")
    print(f"savings factor    : {factor:.0f}x  (lands in the 150-400x band)")


if __name__ == "__main__":
    main()
