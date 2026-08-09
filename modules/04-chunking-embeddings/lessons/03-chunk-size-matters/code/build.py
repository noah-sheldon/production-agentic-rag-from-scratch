"""Build it: the same text at 3 chunk sizes — see the trade (stdlib only).

Run:  python3 build.py
A fixed-size chunker cuts one note at 30 / 100 / 300 words. For each size it
finds the chunk holding the answer sentence and measures: chunk length,
whether the fact is whole or cut, and the signal ratio (answer words inside
the chunk). Too small = the fact is split in half; too big = the fact drowns.
"""
FACT = ("The capybara is the largest living rodent, a water-loving "
        "cousin of the guinea pig.")

NOTE = """# Zoo Notes

This note collects facts from a weekend trip to the zoo, written down so the
semantic index can find them again later. The keeper talked fast, so these
notes capture only the parts that stood out, names, sizes, and where the
animals live. Here is the list.

The capybara is the largest living rodent, a water-loving cousin of the
guinea pig. It lives in South America near rivers and ponds. Visitors often
call it a giant guinea pig, and it is easy to see why. The keeper said a
grown capybara can weigh as much as a small adult, which surprised everyone
in the group.

A mammal is a warm-blooded animal that feeds its babies milk. A rodent is a
mammal with front teeth that keep growing, which is why a rodent must keep
gnawing on things to wear the teeth down. Both are simple words that carry
precise meanings, which is exactly why the index needs full sentences, not
single words, to tell them apart.

The feeding time drew the biggest crowd of the day. The keepers brought
buckets of fruit and the animals lined up in order, patient and unhurried.
My favorite moment was watching the capybaras wade into the pond together,
calm and steady, while the crowd whispered and took photos. One capybara
sank so low that only its nose showed above the water.

Back at home I wrote these notes down quickly, before the details faded.
The zoo visit was short but the facts are worth keeping, and a semantic
index makes them findable again next month. Next visit I want to bring a
small notebook and ask the keeper about the night animals, which I still
know almost nothing about. The plan is to tag each note with a date, so the
index can sort the entries and keep the newest facts on top."""


def fixed_chunks(text: str, size_words: int) -> list[str]:
    """Cut text into equal-length word pieces (the naive chunker)."""
    words = text.split()
    return [" ".join(words[i:i + size_words]) for i in range(0, len(words), size_words)]


def fact_ratio(chunk: str) -> float:
    """Signal ratio: fraction of the chunk that is answer words."""
    fact_words = set(FACT.lower().split())
    chunk_words = chunk.lower().split()
    if not chunk_words:
        return 0.0
    signal = sum(1 for w in chunk_words if w in fact_words)
    return signal / len(chunk_words)


def run_size(size: int) -> None:
    chunks = fixed_chunks(NOTE, size)
    hits = [i for i, c in enumerate(chunks) if "capybara" in c]
    print(f"\n== chunk size {size} words -> {len(chunks)} chunks ==")
    for i, c in enumerate(chunks):
        marker = "  <-- capybara" if i in hits else ""
        print(f"  [{i:2d}] {len(c.split()):3d} words  {c[:44]}...{marker}")
    if not hits:
        print("  fact not found at this size")
        return
    i = hits[0]
    chunk = chunks[i]
    fact_complete = FACT in chunk
    if not fact_complete:
        verdict = "lost context — the answer sentence is cut in half"
    elif len(chunk.split()) > 150:
        verdict = "buried — one answer inside a wall of noise"
    else:
        verdict = "balanced — answer whole, chunk still small"
    print(f"  fact chunk [{i}]: {len(chunk.split())} words, "
          f"signal ratio {fact_ratio(chunk):.2f}")
    print(f"  fact sentence whole in one chunk: {fact_complete}")
    print(f"  -> {verdict}")


if __name__ == "__main__":
    print(f"one note, {len(NOTE.split())} words, fact sentence "
          f"{len(FACT.split())} words")
    for size in (30, 100, 300):
        run_size(size)
