#!/usr/bin/env python3
"""Generate one excalidraw spec + .excalidraw per lesson.

Run:  python3 scripts/gen_lesson_diagrams.py   (from repo root)
Reusable content tool — regenerates all lesson whiteboard diagrams.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIAGRAM = ROOT.parent / "content-planner" / "scripts" / "diagram.py"

# (module/lesson-slug, spec_title, [elements]) — boxes/arrows/text, canvas <= 1200x675
SPECS = {
 "00-setup-and-how-to-learn/01-how-the-course-works": ("course-gates", [
   {"type":"rectangle","x":60,"y":140,"w":180,"h":70,"text":"Lesson","fill":"#a5d8ff"},
   {"type":"rectangle","x":330,"y":60,"w":200,"h":70,"text":"Exercises gate","fill":"#ffffff"},
   {"type":"rectangle","x":330,"y":150,"w":200,"h":70,"text":"Quiz — human reviews","fill":"#ffd8a8"},
   {"type":"rectangle","x":330,"y":240,"w":200,"h":70,"text":"Project gate","fill":"#ffffff"},
   {"type":"rectangle","x":660,"y":140,"w":200,"h":70,"text":"Module done","fill":"#b2f2bb"},
   {"type":"arrow","x1":240,"y1":175,"x2":330,"y2":95,"endArrowhead":"arrow"},
   {"type":"arrow","x1":240,"y1":175,"x2":330,"y2":185,"endArrowhead":"arrow"},
   {"type":"arrow","x1":240,"y1":175,"x2":330,"y2":275,"endArrowhead":"arrow"},
   {"type":"arrow","x1":530,"y1":185,"x2":660,"y2":175,"endArrowhead":"arrow"},
   {"type":"text","x":60,"y":30,"w":500,"h":40,"text":"Build first. Frameworks second."}]),
 "02-data-ingestion/01-what-is-an-ingestion-pipeline": ("pipeline-resume", [
   {"type":"rectangle","x":60,"y":120,"w":150,"h":70,"text":"Sources","fill":"#a5d8ff"},
   {"type":"rectangle","x":300,"y":120,"w":170,"h":70,"text":"Fetch (retries)","fill":"#ffffff"},
   {"type":"rectangle","x":560,"y":120,"w":160,"h":70,"text":"Parse + store","fill":"#ffffff"},
   {"type":"rectangle","x":820,"y":120,"w":180,"h":70,"text":"Done-set","fill":"#b2f2bb"},
   {"type":"arrow","x1":210,"y1":155,"x2":300,"y2":155,"endArrowhead":"arrow"},
   {"type":"arrow","x1":470,"y1":155,"x2":560,"y2":155,"endArrowhead":"arrow"},
   {"type":"arrow","x1":720,"y1":155,"x2":820,"y2":155,"endArrowhead":"arrow"},
   {"type":"text","x":60,"y":30,"w":700,"h":40,"text":"Re-run: done items are skipped. No duplicates."}]),
 "02-data-ingestion/02-retries-and-backoff": ("retry-backoff", [
   {"type":"rectangle","x":60,"y":60,"w":150,"h":70,"text":"Request","fill":"#a5d8ff"},
   {"type":"rectangle","x":300,"y":60,"w":150,"h":70,"text":"OK?","fill":"#ffffff"},
   {"type":"rectangle","x":560,"y":60,"w":160,"h":70,"text":"Next item","fill":"#b2f2bb"},
   {"type":"rectangle","x":300,"y":240,"w":200,"h":70,"text":"Wait: 1s, 2s, 4s...","fill":"#ffd8a8"},
   {"type":"arrow","x1":210,"y1":95,"x2":300,"y2":95,"endArrowhead":"arrow"},
   {"type":"arrow","x1":450,"y1":95,"x2":560,"y2":95,"endArrowhead":"arrow"},
   {"type":"arrow","x1":370,"y1":130,"x2":370,"y2":240,"endArrowhead":"arrow"},
   {"type":"arrow","x1":300,"y1":275,"x2":210,"y2":105,"endArrowhead":"arrow"},
   {"type":"text","x":560,"y":240,"w":300,"h":70,"text":"Budget exhausted →\nmark failed, move on."}]),
 "02-data-ingestion/03-parsing-documents": ("parse-formats", [
   {"type":"rectangle","x":60,"y":130,"w":160,"h":70,"text":"Raw document","fill":"#a5d8ff"},
   {"type":"rectangle","x":330,"y":60,"w":190,"h":70,"text":"HTML: strip tags","fill":"#ffffff"},
   {"type":"rectangle","x":330,"y":150,"w":190,"h":70,"text":"Markdown: frontmatter","fill":"#ffffff"},
   {"type":"rectangle","x":330,"y":240,"w":190,"h":70,"text":"PDF: text layer","fill":"#ffffff"},
   {"type":"rectangle","x":660,"y":130,"w":200,"h":70,"text":"Title + clean body","fill":"#b2f2bb"},
   {"type":"arrow","x1":220,"y1":165,"x2":330,"y2":95,"endArrowhead":"arrow"},
   {"type":"arrow","x1":220,"y1":165,"x2":330,"y2":185,"endArrowhead":"arrow"},
   {"type":"arrow","x1":220,"y1":165,"x2":330,"y2":275,"endArrowhead":"arrow"},
   {"type":"arrow","x1":520,"y1":165,"x2":660,"y2":165,"endArrowhead":"arrow"},
   {"type":"text","x":60,"y":30,"w":600,"h":40,"text":"PDF is the worst: text can be drawn as shapes."}]),
 "03-keyword-search-bm25/01-bm25-by-hand": ("bm25-score", [
   {"type":"rectangle","x":60,"y":60,"w":170,"h":70,"text":"Query words","fill":"#a5d8ff"},
   {"type":"rectangle","x":330,"y":60,"w":180,"h":70,"text":"Term frequency (TF)","fill":"#ffffff"},
   {"type":"rectangle","x":330,"y":180,"w":180,"h":70,"text":"Rarity (IDF)","fill":"#ffffff"},
   {"type":"rectangle","x":640,"y":120,"w":200,"h":70,"text":"Score = TF × IDF","fill":"#ffd8a8"},
   {"type":"rectangle","x":900,"y":120,"w":180,"h":70,"text":"Rank by score","fill":"#b2f2bb"},
   {"type":"arrow","x1":230,"y1":95,"x2":330,"y2":95,"endArrowhead":"arrow"},
   {"type":"arrow","x1":230,"y1":95,"x2":330,"y2":215,"endArrowhead":"arrow"},
   {"type":"arrow","x1":510,"y1":155,"x2":640,"y2":155,"endArrowhead":"arrow"},
   {"type":"arrow","x1":840,"y1":155,"x2":900,"y2":155,"endArrowhead":"arrow"},
   {"type":"text","x":60,"y":280,"w":700,"h":40,"text":"A word in every doc teaches you nothing → score ~0."}]),
 "03-keyword-search-bm25/02-k1-and-b": ("two-knobs", [
   {"type":"rectangle","x":60,"y":120,"w":160,"h":70,"text":"BM25 score","fill":"#a5d8ff"},
   {"type":"rectangle","x":330,"y":60,"w":220,"h":70,"text":"k1: saturation speed","fill":"#ffffff"},
   {"type":"rectangle","x":330,"y":180,"w":220,"h":70,"text":"b: length penalty","fill":"#ffffff"},
   {"type":"text","x":60,"y":30,"w":700,"h":40,"text":"k1=0: presence only. b=0: length ignored."},
   {"type":"text","x":600,"y":60,"w":420,"h":120,"text":"Same query, same docs,\nthree settings →\nwatch the ranking change."}]),
 "03-keyword-search-bm25/03-precision-and-recall": ("prec-recall", [
   {"type":"ellipse","x":60,"y":60,"w":220,"h":160,"text":"Retrieved","fill":"#a5d8ff"},
   {"type":"ellipse","x":260,"y":120,"w":240,"h":160,"text":"Relevant","fill":"#ffc9c9"},
   {"type":"ellipse","x":440,"y":300,"w":260,"h":120,"text":"Both = good hits","fill":"#b2f2bb"},
   {"type":"text","x":60,"y":440,"w":700,"h":40,"text":"Precision = hits/retrieved · Recall = hits/relevant"},
   {"type":"text","x":600,"y":60,"w":400,"h":120,"text":"Trade-off: return everything = recall 100%,\nprecision awful."}]),
 "04-chunking-embeddings/01-what-is-chunking": ("chunking", [
   {"type":"rectangle","x":60,"y":60,"w":300,"h":60,"text":"Whole document","fill":"#a5d8ff"},
   {"type":"rectangle","x":60,"y":160,"w":300,"h":50,"text":"Section 1","fill":"#ffffff"},
   {"type":"rectangle","x":60,"y":230,"w":300,"h":50,"text":"Section 2 (with overlap)","fill":"#ffffff"},
   {"type":"rectangle","x":60,"y":300,"w":300,"h":50,"text":"Section 3","fill":"#ffffff"},
   {"type":"arrow","x1":360,"y1":90,"x2":360,"y2":160,"endArrowhead":"arrow"},
   {"type":"text","x":430,"y":60,"w":480,"h":200,"text":"Models read a small window.\nCut docs into pieces (chunks).\nOverlap keeps context across cuts.\nChunk size decides quality."}]),
 "04-chunking-embeddings/02-embeddings": ("embeddings-map", [
   {"type":"text","x":60,"y":40,"w":500,"h":40,"text":"Words become points on a map"},
   {"type":"ellipse","x":150,"y":120,"w":120,"h":70,"text":"puppy","fill":"#b2f2bb"},
   {"type":"ellipse","x":300,"y":110,"w":120,"h":70,"text":"dog","fill":"#b2f2bb"},
   {"type":"ellipse","x":480,"y":200,"w":120,"h":70,"text":"printer","fill":"#ffc9c9"},
   {"type":"text","x":60,"y":320,"w":700,"h":40,"text":"Similar meaning = close numbers. The map IS the search."},
   {"type":"text","x":620,"y":40,"w":400,"h":200,"text":"384 numbers per sentence.\nNo dictionary — the model\nnoticed which words\nhang out together."}]),
 "04-chunking-embeddings/03-chunk-size-matters": ("chunk-size", [
   {"type":"rectangle","x":60,"y":60,"w":220,"h":80,"text":"size 30","fill":"#ffc9c9"},
   {"type":"rectangle","x":60,"y":180,"w":220,"h":80,"text":"size 100","fill":"#b2f2bb"},
   {"type":"rectangle","x":60,"y":300,"w":220,"h":80,"text":"size 300","fill":"#ffd8a8"},
   {"type":"text","x":360,"y":60,"w":500,"h":220,"text":"Too small: the answer is cut in half.\nBalanced: answer intact, signal high.\nToo big: buried in a wall of noise.\nChunk size is a measurement, not a guess."}]),
 "05-hybrid-search-rrf/01-rrf-by-hand": ("rrf-fusion", [
   {"type":"rectangle","x":60,"y":60,"w":180,"h":70,"text":"Keyword ranks","fill":"#a5d8ff"},
   {"type":"rectangle","x":60,"y":180,"w":180,"h":70,"text":"Semantic ranks","fill":"#b2f2bb"},
   {"type":"rectangle","x":400,"y":120,"w":200,"h":70,"text":"Fuse: 1/(k+rank)","fill":"#ffd8a8"},
   {"type":"rectangle","x":720,"y":120,"w":200,"h":70,"text":"Fused ranking","fill":"#ffffff"},
   {"type":"arrow","x1":240,"y1":95,"x2":400,"y2":145,"endArrowhead":"arrow"},
   {"type":"arrow","x1":240,"y1":215,"x2":400,"y2":175,"endArrowhead":"arrow"},
   {"type":"arrow","x1":600,"y1":155,"x2":720,"y2":155,"endArrowhead":"arrow"},
   {"type":"text","x":400,"y":30,"w":400,"h":40,"text":"Rank-based fusion beats score averaging"}]),
 "05-hybrid-search-rrf/02-when-hybrid-wins": ("hybrid-wins", [
   {"type":"rectangle","x":60,"y":60,"w":200,"h":70,"text":"One query","fill":"#a5d8ff"},
   {"type":"rectangle","x":340,"y":60,"w":200,"h":70,"text":"Keyword finds A","fill":"#ffffff"},
   {"type":"rectangle","x":340,"y":180,"w":200,"h":70,"text":"Semantic finds B","fill":"#ffffff"},
   {"type":"rectangle","x":680,"y":120,"w":220,"h":70,"text":"Hybrid finds A and B","fill":"#b2f2bb"},
   {"type":"arrow","x1":260,"y1":95,"x2":340,"y2":95,"endArrowhead":"arrow"},
   {"type":"arrow","x1":260,"y1":95,"x2":340,"y2":215,"endArrowhead":"arrow"},
   {"type":"arrow","x1":540,"y1":155,"x2":680,"y2":155,"endArrowhead":"arrow"},
   {"type":"text","x":60,"y":300,"w":700,"h":40,"text":"Each alone misses half. Fusion = both."}]),
 "05-hybrid-search-rrf/03-unified-search-api": ("unified-api", [
   {"type":"rectangle","x":60,"y":120,"w":200,"h":70,"text":"search(query, mode)","fill":"#a5d8ff"},
   {"type":"rectangle","x":360,"y":60,"w":180,"h":70,"text":"mode=keyword","fill":"#ffffff"},
   {"type":"rectangle","x":360,"y":140,"w":180,"h":70,"text":"mode=semantic","fill":"#ffffff"},
   {"type":"rectangle","x":360,"y":220,"w":180,"h":70,"text":"mode=hybrid","fill":"#ffffff"},
   {"type":"text","x":600,"y":120,"w":400,"h":120,"text":"One function, three modes,\nthe same result shape.\nCallers never care which."}]),
 "06-rag-pipeline-local-llm/01-the-rag-flow": ("rag-flow", [
   {"type":"rectangle","x":60,"y":120,"w":150,"h":70,"text":"Question","fill":"#a5d8ff"},
   {"type":"rectangle","x":300,"y":120,"w":160,"h":70,"text":"Retrieve chunks","fill":"#ffffff"},
   {"type":"rectangle","x":550,"y":120,"w":160,"h":70,"text":"Prompt: Q + chunks","fill":"#ffffff"},
   {"type":"rectangle","x":800,"y":120,"w":180,"h":70,"text":"Model answers","fill":"#b2f2bb"},
   {"type":"arrow","x1":210,"y1":155,"x2":300,"y2":155,"endArrowhead":"arrow"},
   {"type":"arrow","x1":460,"y1":155,"x2":550,"y2":155,"endArrowhead":"arrow"},
   {"type":"arrow","x1":710,"y1":155,"x2":800,"y2":155,"endArrowhead":"arrow"},
   {"type":"text","x":60,"y":30,"w":700,"h":40,"text":"The model only sees your chunks, not your library."}]),
 "06-rag-pipeline-local-llm/02-prompt-trimming": ("prompt-trim", [
   {"type":"rectangle","x":60,"y":60,"w":260,"h":90,"text":"Fat prompt: everything","fill":"#ffc9c9"},
   {"type":"rectangle","x":60,"y":220,"w":260,"h":90,"text":"Trimmed: only the chunks","fill":"#b2f2bb"},
   {"type":"text","x":400,"y":60,"w":500,"h":200,"text":"Smaller prompt = faster answer,\nless cost, less hallucination.\n1253 → 74 tokens ≈ 17× faster.\nMeasure it, don't feel it."}]),
 "06-rag-pipeline-local-llm/03-streaming": ("streaming", [
   {"type":"rectangle","x":60,"y":120,"w":160,"h":70,"text":"Server","fill":"#a5d8ff"},
   {"type":"rectangle","x":380,"y":120,"w":160,"h":70,"text":"Token stream (SSE)","fill":"#b2f2bb"},
   {"type":"rectangle","x":680,"y":120,"w":180,"h":70,"text":"Reader sees words appear","fill":"#ffffff"},
   {"type":"arrow","x1":220,"y1":155,"x2":380,"y2":155,"endArrowhead":"arrow"},
   {"type":"arrow","x1":540,"y1":155,"x2":680,"y2":155,"endArrowhead":"arrow"},
   {"type":"text","x":60,"y":30,"w":700,"h":40,"text":"First token ~24ms vs ~1.2s total. Streaming = perceived speed."}]),
 "07-observability-caching/01-trace-the-request": ("trace", [
   {"type":"rectangle","x":60,"y":60,"w":150,"h":70,"text":"Request","fill":"#a5d8ff"},
   {"type":"rectangle","x":300,"y":60,"w":150,"h":70,"text":"Retrieve: 12ms","fill":"#ffffff"},
   {"type":"rectangle","x":540,"y":60,"w":150,"h":70,"text":"Prompt: 3ms","fill":"#ffffff"},
   {"type":"rectangle","x":780,"y":60,"w":180,"h":70,"text":"Model: 800ms","fill":"#ffd8a8"},
   {"type":"arrow","x1":210,"y1":95,"x2":300,"y2":95,"endArrowhead":"arrow"},
   {"type":"arrow","x1":450,"y1":95,"x2":540,"y2":95,"endArrowhead":"arrow"},
   {"type":"arrow","x1":690,"y1":95,"x2":780,"y2":95,"endArrowhead":"arrow"},
   {"type":"text","x":60,"y":200,"w":700,"h":40,"text":"Trace every step: where the time actually goes."}]),
 "07-observability-caching/02-cache-with-ttl": ("cache-ttl", [
   {"type":"rectangle","x":60,"y":120,"w":150,"h":70,"text":"Question","fill":"#a5d8ff"},
   {"type":"rectangle","x":320,"y":60,"w":190,"h":70,"text":"Cache hit → instant","fill":"#b2f2bb"},
   {"type":"rectangle","x":320,"y":180,"w":190,"h":70,"text":"Cache miss → full flow","fill":"#ffffff"},
   {"type":"rectangle","x":640,"y":120,"w":200,"h":70,"text":"Store + TTL expiry","fill":"#ffd8a8"},
   {"type":"arrow","x1":210,"y1":155,"x2":320,"y2":95,"endArrowhead":"arrow"},
   {"type":"arrow","x1":210,"y1":155,"x2":320,"y2":215,"endArrowhead":"arrow"},
   {"type":"arrow","x1":510,"y1":215,"x2":640,"y2":155,"endArrowhead":"arrow"},
   {"type":"text","x":60,"y":300,"w":700,"h":40,"text":"Hit rate is the number that matters."}]),
 "07-observability-caching/03-cost-per-question": ("cost-math", [
   {"type":"rectangle","x":60,"y":60,"w":260,"h":90,"text":"1000 questions, uncached","fill":"#ffc9c9"},
   {"type":"rectangle","x":60,"y":220,"w":260,"h":90,"text":"1000 questions, cached","fill":"#b2f2bb"},
   {"type":"text","x":400,"y":60,"w":500,"h":200,"text":"Each question = tokens = money.\nCache turns repeat questions\ninto near-zero cost.\nThe 150-400x is multiplication,\nnot magic."}]),
 "09-evaluation-capstone/01-build-an-eval-set": ("eval-set", [
   {"type":"rectangle","x":60,"y":120,"w":160,"h":70,"text":"Questions","fill":"#a5d8ff"},
   {"type":"rectangle","x":320,"y":120,"w":200,"h":70,"text":"Known-good answers","fill":"#b2f2bb"},
   {"type":"rectangle","x":640,"y":120,"w":220,"h":70,"text":"Labeled eval set","fill":"#ffffff"},
   {"type":"arrow","x1":220,"y1":155,"x2":320,"y2":155,"endArrowhead":"arrow"},
   {"type":"arrow","x1":520,"y1":155,"x2":640,"y2":155,"endArrowhead":"arrow"},
   {"type":"text","x":60,"y":30,"w":700,"h":40,"text":"Labeled evals beat vibes. 5 questions is enough to start."}]),
 "09-evaluation-capstone/02-score-your-assistant": ("score", [
   {"type":"rectangle","x":60,"y":60,"w":180,"h":70,"text":"Eval set","fill":"#a5d8ff"},
   {"type":"rectangle","x":340,"y":60,"w":200,"h":70,"text":"Run assistant","fill":"#ffffff"},
   {"type":"rectangle","x":660,"y":60,"w":200,"h":70,"text":"Groundedness + recall","fill":"#ffd8a8"},
   {"type":"rectangle","x":660,"y":220,"w":200,"h":70,"text":"Score table","fill":"#b2f2bb"},
   {"type":"arrow","x1":240,"y1":95,"x2":340,"y2":95,"endArrowhead":"arrow"},
   {"type":"arrow","x1":540,"y1":95,"x2":660,"y2":95,"endArrowhead":"arrow"},
   {"type":"arrow","x1":760,"y1":130,"x2":760,"y2":220,"endArrowhead":"arrow"},
   {"type":"text","x":60,"y":220,"w":500,"h":120,"text":"\"It works\" is a feeling.\nGroundedness 0.29 is a number."}]),
 "09-evaluation-capstone/03-the-grade-gate": ("grade-gate", [
   {"type":"rectangle","x":60,"y":120,"w":160,"h":70,"text":"Answer","fill":"#a5d8ff"},
   {"type":"rectangle","x":330,"y":60,"w":190,"h":70,"text":"Score ≥ gate → ship","fill":"#b2f2bb"},
   {"type":"rectangle","x":330,"y":180,"w":190,"h":70,"text":"Low score → retry","fill":"#ffd8a8"},
   {"type":"rectangle","x":330,"y":300,"w":190,"h":70,"text":"Still low → \"I don't know\"","fill":"#ffc9c9"},
   {"type":"arrow","x1":220,"y1":155,"x2":330,"y2":95,"endArrowhead":"arrow"},
   {"type":"arrow","x1":220,"y1":155,"x2":330,"y2":215,"endArrowhead":"arrow"},
   {"type":"arrow","x1":425,"y1":250,"x2":425,"y2":300,"endArrowhead":"arrow"},
   {"type":"text","x":620,"y":60,"w":400,"h":200,"text":"Before: hallucinations shipped.\nAfter: 0 shipped —\ncaught by the gate,\nnot by luck."}]),
}


def main() -> None:
    count = 0
    for key, (title, elements) in SPECS.items():
        mod, lesson = key.split("/", 1)
        base = ROOT / "modules" / mod / "lessons" / lesson
        if not base.exists():
            print("SKIP (missing):", key)
            continue
        diagrams = base / "diagrams"
        diagrams.mkdir(exist_ok=True)
        spec = {"title": title, "elements": elements}
        spec_file = diagrams / f"{title}.spec.json"
        spec_file.write_text(json.dumps(spec, indent=1))
        out = diagrams / f"{title}.excalidraw"
        r = subprocess.run([sys.executable, str(DIAGRAM), str(spec_file), "-o", str(out)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"GEN FAIL {key}: {r.stderr.strip()[:200]}")
            continue
        doc = base / "docs" / "en.md"
        t = doc.read_text()
        line = (f"**Diagram (whiteboard):** open `diagrams/{title}.excalidraw` "
                "in excalidraw.com — same picture, traceable by hand.")
        if line not in t and "## BUILD IT" in t:
            t = t.replace("## BUILD IT", line + "\n\n## BUILD IT")
            doc.write_text(t)
        count += 1
    print(f"generated excalidraw for {count} lessons")


if __name__ == "__main__":
    main()
