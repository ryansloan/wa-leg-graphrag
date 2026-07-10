"""Run every eval question through both retrieval paths and write results.md.

Usage:
    uv run python -m leg_graphrag.eval.run              # all questions
    uv run python -m leg_graphrag.eval.run --only R1 H2 # subset
    uv run python -m leg_graphrag.eval.run --path graph # one path

Requires ANTHROPIC_API_KEY and a seeded HelixDB instance (scripts/seed_helix.py).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml
from dotenv import load_dotenv

from ..agent import Deps, graph_agent, control_agent
from ..embed import default_embedder
from ..ingest import DATASET_PATH
from ..stores.flat import FlatVectorStore
from ..stores.graph import GraphStore

EVAL_DIR = Path(__file__).resolve().parent
RESULTS_MD = EVAL_DIR.parents[2] / "eval" / "results.md"
RESULTS_JSON = EVAL_DIR.parents[2] / "eval" / "results.json"

AGENTS = {"control": control_agent, "graph": graph_agent}


def _tool_calls(result) -> list[str]:
    calls = []
    for msg in result.all_messages():
        for part in getattr(msg, "parts", []):
            if getattr(part, "part_kind", "") == "tool-call":
                calls.append(part.tool_name)
    return calls


def _auto_check(answer: str, required: list[str]) -> bool:
    low = answer.lower()
    return all(str(r).lower() in low for r in required)


def run_eval(only: list[str] | None, paths: list[str]) -> None:
    questions = yaml.safe_load((EVAL_DIR / "questions.yaml").read_text())
    if only:
        questions = [q for q in questions if q["id"] in only]

    dataset = json.loads(DATASET_PATH.read_text())
    embedder = default_embedder()
    deps = Deps(
        flat=FlatVectorStore.build(dataset, embedder),
        graph=GraphStore(),
        embedder=embedder,
    )

    rows = []
    for q in questions:
        row = {"id": q["id"], "bucket": q["bucket"], "question": q["question"].strip(),
               "expected": q["expected"].strip(), "paths": {}}
        for path in paths:
            print(f"[{q['id']}] {path} ...", flush=True)
            result = AGENTS[path].run_sync(q["question"], deps=deps)
            answer = result.output
            row["paths"][path] = {
                "answer": answer,
                "tool_calls": _tool_calls(result),
                "auto_pass": _auto_check(answer, q["required"]),
            }
        rows.append(row)

    if only and RESULTS_JSON.exists():
        # merge a partial rerun into the existing results, preserving question order
        merged = {r["id"]: r for r in json.loads(RESULTS_JSON.read_text())}
        merged.update({r["id"]: r for r in rows})
        all_ids = [q["id"] for q in yaml.safe_load((EVAL_DIR / "questions.yaml").read_text())]
        rows = [merged[i] for i in all_ids if i in merged]

    RESULTS_JSON.parent.mkdir(exist_ok=True)
    RESULTS_JSON.write_text(json.dumps(rows, indent=1))
    RESULTS_MD.write_text(_render_md(rows, paths))
    print(f"wrote {RESULTS_MD} and {RESULTS_JSON}")


def _render_md(rows: list[dict], paths: list[str]) -> str:
    def mark(r, p):
        if p not in r["paths"]:
            return "—"
        return "✅" if r["paths"][p]["auto_pass"] else "❌"

    lines = [
        "# Eval results — flat-vector control vs HelixDB graph+vector",
        "",
        "Auto-scored by required-substring check; see per-question transcripts below.",
        "",
        "| id | bucket | question | control | graph |",
        "|----|--------|----------|:-------:|:-----:|",
    ]
    for r in rows:
        q_short = (r["question"][:80] + "…") if len(r["question"]) > 80 else r["question"]
        lines.append(f"| {r['id']} | {r['bucket']} | {q_short} | {mark(r, 'control')} | {mark(r, 'graph')} |")

    lines.append("\n---\n")
    for r in rows:
        lines.append(f"## {r['id']} ({r['bucket']})\n")
        lines.append(f"**Q:** {r['question']}\n")
        lines.append(f"**Expected:** {r['expected']}\n")
        for p in paths:
            if p not in r["paths"]:
                continue
            res = r["paths"][p]
            status = "pass" if res["auto_pass"] else "FAIL"
            lines.append(f"### {p} — {status}\n")
            lines.append(f"tools: {', '.join(res['tool_calls']) or 'none'}\n")
            lines.append(f"> {res['answer'].replace(chr(10), chr(10) + '> ')}\n")
    return "\n".join(lines)


if __name__ == "__main__":
    load_dotenv(EVAL_DIR.parents[2] / ".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None, help="question ids to run")
    ap.add_argument("--path", choices=["control", "graph"], default=None, help="run one path only")
    args = ap.parse_args()
    run_eval(args.only, [args.path] if args.path else ["control", "graph"])
