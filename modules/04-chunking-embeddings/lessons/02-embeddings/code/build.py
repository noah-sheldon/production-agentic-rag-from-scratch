"""Build it: the 384-number idea + cosine similarity by hand (stdlib only).

Run:  python3 build.py
Part 1 proves the math on random 384-number vectors (a vector vs itself = 1.0,
vs an unrelated vector ~ 0). Part 2 proves closeness = similarity: word-count
stand-ins put "a puppy that barks" close to "a dog that barks" and far from
"a printer that prints" — no ML libraries anywhere.
"""
import hashlib
import math
import random

DIM = 384  # the magic number: 384 dimensions


def make_random_vector(seed: int, dim: int = DIM) -> list[float]:
    """Deterministic stand-in for a trained embedding — seeded randomness."""
    rng = random.Random(seed)
    return [rng.uniform(-1.0, 1.0) for _ in range(dim)]


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def length(v: list[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Angle between two vectors: 1 = same direction, 0 = unrelated, -1 = opposite."""
    denom = length(a) * length(b)
    if denom == 0.0:
        return 0.0
    return dot(a, b) / denom


def word_count_embedding(text: str, dim: int = DIM) -> list[float]:
    """A stand-in embedding: count words into 384 hash buckets.

    Real embedders are trained to place meanings close; this crude version
    already shows the SHAPE: text that shares words shares numbers, text
    that shares nothing does not.
    """
    vec = [0.0] * dim
    for word in text.lower().split():
        digest = hashlib.blake2b(word.encode(), digest_size=8).digest()
        vec[int.from_bytes(digest, "big") % dim] += 1.0
    return vec


if __name__ == "__main__":
    print("== Part 1 — the math on random 384-number vectors ==")
    a = make_random_vector(1)
    b = make_random_vector(2)
    print(f"  vector vs itself:    {cosine_similarity(a, a):.3f}   (same numbers = 1.0)")
    print(f"  vector vs unrelated: {cosine_similarity(a, b):.3f}   (random = ~0)")
    print(f"  384 dimensions, each a number between -1 and 1\n")

    print("== Part 2 — closeness = similarity (word-count stand-ins) ==")
    puppy = word_count_embedding("a puppy that barks and fetches a ball")
    dog = word_count_embedding("a dog that barks and fetches a ball")
    printer = word_count_embedding("a printer that prints paper all day")
    pairs = [
        ("puppy vs dog", puppy, dog, "same topic"),
        ("puppy vs printer", puppy, printer, "different topic"),
    ]
    for label, x, y, why in pairs:
        print(f"  {label:<16} cosine = {cosine_similarity(x, y):.3f}   ({why})")

    print("\n== rank the candidates for the query 'a dog that barks' ==")
    query = dog
    names = ["puppy text", "printer text", "dog text"]
    vectors = [puppy, printer, dog]
    order = sorted(range(len(vectors)),
                   key=lambda i: cosine_similarity(query, vectors[i]),
                   reverse=True)
    for position, i in enumerate(order):
        print(f"  #{position + 1}: {names[i]}  "
              f"cosine = {cosine_similarity(query, vectors[i]):.3f}")
