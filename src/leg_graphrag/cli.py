"""Ask your own questions against either retrieval path.

Usage:
    uv run leg "which cosponsors of SB 5041 voted against it?"   # graph path (default)
    uv run leg --control "..."      # flat-vector control
    uv run leg --both "..."         # run both, print side by side
    uv run leg                      # interactive REPL (conversation carries over turns)

Requires ANTHROPIC_API_KEY (or .env) and a seeded HelixDB instance for the graph path.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

from .agent import Deps, control_agent, graph_agent
from .embed import default_embedder
from .ingest import DATASET_PATH
from .stores.flat import FlatVectorStore
from .stores.graph import GraphStore

ROOT = Path(__file__).resolve().parents[2]


def _build_deps() -> Deps:
    dataset = json.loads(DATASET_PATH.read_text())
    embedder = default_embedder()
    return Deps(
        flat=FlatVectorStore.build(dataset, embedder),
        graph=GraphStore(),
        embedder=embedder,
    )


def _ask(agent, question: str, deps: Deps, history=None):
    result = agent.run_sync(question, deps=deps, message_history=history)
    return result


def _print_tools(result) -> None:
    calls = []
    for msg in result.all_messages():
        for part in getattr(msg, "parts", []):
            if getattr(part, "part_kind", "") == "tool-call":
                args = part.args if isinstance(part.args, str) else json.dumps(part.args)
                calls.append(f"{part.tool_name}({args})")
    if calls:
        print(f"\033[2m[tools: {'; '.join(calls)}]\033[0m")


def _run_once(question: str, paths: list[str], deps: Deps, show_tools: bool) -> None:
    agents = {"graph": graph_agent, "control": control_agent}
    for path in paths:
        if len(paths) > 1:
            print(f"\n\033[1m=== {path} ===\033[0m")
        result = _ask(agents[path], question, deps)
        if show_tools:
            _print_tools(result)
        print(result.output)


def _repl(path: str, deps: Deps, show_tools: bool) -> None:
    agent = graph_agent if path == "graph" else control_agent
    history = None
    print(f"WA Legislature 2025-26 — {path} path. Empty line or Ctrl-D to exit.")
    while True:
        try:
            question = input("\n\033[1m?>\033[0m ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question:
            break
        result = _ask(agent, question, deps, history)
        history = result.all_messages()
        if show_tools:
            _print_tools(result)
        print(result.output)


def main() -> None:
    load_dotenv(ROOT / ".env")
    ap = argparse.ArgumentParser(prog="leg", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("question", nargs="*", help="question to ask; omit for interactive mode")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--control", action="store_true", help="use the flat-vector control path")
    group.add_argument("--both", action="store_true", help="run both paths and compare")
    ap.add_argument("--no-tools", action="store_true", help="hide the tool-call trace")
    args = ap.parse_args()

    deps = _build_deps()
    show_tools = not args.no_tools
    question = " ".join(args.question).strip()

    if question:
        paths = ["control", "graph"] if args.both else (["control"] if args.control else ["graph"])
        _run_once(question, paths, deps, show_tools)
    else:
        if args.both:
            sys.exit("--both only works with a one-shot question")
        _repl("control" if args.control else "graph", deps, show_tools)


if __name__ == "__main__":
    main()
