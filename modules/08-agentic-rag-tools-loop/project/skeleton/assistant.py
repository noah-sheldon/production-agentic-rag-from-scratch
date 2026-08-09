#!/usr/bin/env python3
"""Notes assistant with tools — module 08 project skeleton.

Runs keyless in FAKE mode (no API key needed). Set OPENAI_API_KEY to switch
to a real OpenAI-compatible endpoint (optional OPENAI_BASE_URL, OPENAI_MODEL).

Run:
  python3 assistant.py                                  # default question
  python3 assistant.py "what did I write about agents?" # your question
  cat decision_log.jsonl                                # the trace

Flow: guard -> rewrite -> agent loop (decide/call/result/repeat) -> answer.
Every step logs to decision_log.jsonl — reasoning transparency by hand.
"""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

from guard import DecisionLog, guard, rewrite
from tools import ToolRegistry

MAX_TURNS = 6
DEFAULT_QUESTION = "what did I write about agents?"

NOTES_DIR = Path(__file__).parent / "notes"


# --------------------------------------------------------------------------
# The model — FAKE mode (keyless) or real OpenAI-compatible endpoint
# --------------------------------------------------------------------------

def _tool_call(call_id: str, name: str, arguments: dict) -> dict:
    return {"id": call_id, "type": "function",
            "function": {"name": name, "arguments": json.dumps(arguments)}}


def _reply(content=None, tool_calls=None) -> dict:
    return {"choices": [{"message": {"role": "assistant", "content": content,
                                     "tool_calls": tool_calls}}]}


class FakeModel:
    """Scripted model: search -> read the top hit -> cite and answer.
    Exercises the real loop with zero network and zero cost."""

    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry
        self.top_file: str | None = None

    def chat(self, messages: list[dict], tools: list[dict]) -> dict:
        tool_msgs = [m for m in messages if m["role"] == "tool"]
        if not tool_msgs:
            question = next(m["content"] for m in messages if m["role"] == "user")
            return _reply(tool_calls=[_tool_call("c1", "search_notes", {"query": question})])
        if len(tool_msgs) == 1:
            hits = json.loads(tool_msgs[-1]["content"])
            self.top_file = hits[0]["file"] if hits else None
            return _reply(tool_calls=[_tool_call("c2", "read_note", {"name": self.top_file})])
        if self.top_file:
            return _reply(content=f"From {self.top_file}: {json.loads(tool_msgs[-1]['content'])}")
        return _reply(content="I found no relevant note for that.")


def real_chat(messages: list[dict], tools: list[dict]) -> dict:
    """One raw HTTP call to an OpenAI-compatible /chat/completions endpoint."""
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    key = os.environ.get("OPENAI_API_KEY", "")
    body = json.dumps({"model": model, "messages": messages, "tools": tools}).encode()
    req = urllib.request.Request(
        f"{base}/chat/completions", data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


# --------------------------------------------------------------------------
# The loop — decide -> call -> result -> repeat (lesson 02)
# --------------------------------------------------------------------------

def run_agent(question: str, chat, registry: ToolRegistry,
              max_turns: int = MAX_TURNS, log: DecisionLog | None = None):
    messages = [{"role": "user", "content": question}]
    for turn in range(1, max_turns + 1):
        reply = chat(messages, registry.schemas())
        msg = reply["choices"][0]["message"]
        calls = msg.get("tool_calls") or []
        if not calls:
            if log:
                log.log(step="answer", decision="final", reason=f"turns={turn}")
            return msg.get("content") or "", turn
        messages.append({"role": "assistant", "content": msg.get("content"),
                         "tool_calls": calls})
        for call in calls:
            fn = call["function"]
            try:
                args = json.loads(fn["arguments"] or "{}")
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"model returned bad JSON arguments: {exc}")
            if log:
                log.log(step="tool_call", decision=fn["name"], reason=f"args={args}")
            try:
                result = registry.call(fn["name"], **args)
            except Exception as exc:
                result = {"error": str(exc)}
            if log:
                log.log(step="tool_result", decision=fn["name"],
                        reason=str(result)[:100])
            messages.append({"role": "tool",
                             "tool_call_id": call.get("id", f"call_{turn}"),
                             "content": json.dumps(result)})
    if log:
        log.log(step="answer", decision="max_turns",
                reason=f"budget {max_turns} spent")
    return "Budget spent — I could not finish in time.", max_turns


# --------------------------------------------------------------------------

def main() -> None:
    question = " ".join(sys.argv[1:]) or DEFAULT_QUESTION
    registry = ToolRegistry(NOTES_DIR)
    log = DecisionLog()

    print(f"== notes assistant, question: {question!r} ==")

    # 1. guardrail (lesson 03) — reject before any cost
    verdict = guard(question)
    log.log(step="guardrail",
            decision="accept" if verdict["accepted"] else "reject",
            reason=verdict["reason"])
    if not verdict["accepted"]:
        print(f"\nRejected: {verdict['reason']}")
        return

    # 2. rewrite (lesson 04) — fix the query before it searches
    # TODO (lesson 04): multi-turn last_topic — single questions use "".
    query = rewrite(question, last_topic="")
    log.log(step="rewrite", decision=query, reason=f"original={question!r}")

    # 3. the loop (lesson 02) — fake by default, real with OPENAI_API_KEY
    use_real = bool(os.environ.get("OPENAI_API_KEY"))
    chat = real_chat if use_real else FakeModel(registry).chat
    print(f"== mode: {'REAL (OpenAI-compatible)' if use_real else 'FAKE (keyless)'}, "
          f"max_turns={MAX_TURNS} ==")

    started = time.perf_counter()
    answer, turns = run_agent(query, chat, registry, max_turns=MAX_TURNS, log=log)
    elapsed = time.perf_counter() - started

    print(f"\n== answer ({turns} turn(s), {elapsed:.2f}s) ==")
    print(answer)
    print(f"\n== trace written to {log.path} ==")
    print(log.path.read_text())


if __name__ == "__main__":
    main()
