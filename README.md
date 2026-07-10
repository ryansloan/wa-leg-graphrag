# leg-graphrag — graph+vector vs flat-vector RAG on the WA Legislature

An agent that answers questions about the Washington State Legislature's 2025-26
biennium — bills, sponsorship, roll-call votes — built to make one contrast legible:

> The useful questions about legislation are **relational** (sponsor coalitions, vote
> splits, cross-bill behavior). Flat-vector RAG over bill text can't answer them,
> because the answer is an edge pattern, not a text passage. A graph+vector substrate can.

Two retrieval paths answer the same questions with the same LLM; only the substrate differs:

- **Control** — the bill digests embedded in a flat vector index (numpy cosine). The
  agent's only tool is semantic search.
- **Primary** — the same digest embeddings **plus** the sponsorship/vote graph in
  [HelixDB](https://helix-db.com), one substrate. The agent gets semantic search *and*
  graph traversal tools.

## The query taxonomy (the actual artifact)

| bucket | example | expectation |
|--------|---------|-------------|
| **semantic** | "which bills deal with unemployment insurance?" | control is legitimately good — say so |
| **relational** | "which cosponsors of SB 5041 voted against it on final passage?" | no digest passage encodes this; control collapses, traversal nails it |
| **hybrid** | "find the rent-stabilization bill and report how close its Senate vote was" | vector search to find the bill, traversal to answer |

`src/leg_graphrag/eval/questions.yaml` holds 12 hand-written questions (4 per bucket)
with ground truth hand-derived from the ingested data. `eval/results.md` is the output.

## Data

Source: WA Legislature web services via [`wa-leg-api`](https://pypi.org/project/wa-leg-api/),
2025-26 biennium, **bills that reached a recorded floor vote** (713 bills, 154 members,
~6.4k sponsorships, ~152k individual votes; ingested 2026-07-10). Roll calls are
constitutionally required on final passage, so passed bills are exactly where the
relational signal lives.

Graph model (HelixDB, schemaless v2):

```
(Member {member_id, name, chamber, party, district})
  -[:SPONSORED {role, order, bill_id, member_name, party}]-> (Bill)
  -[:VOTED {vote, motion, sequence_number, vote_date, chamber, bill_id, member_name, party}]-> (Bill)
Bill {bill_number, bill_id, title, digest, status, embedding (vector index)}
```

Edges are denormalized (member_name/party/bill_id) so one edge scan answers most
questions without a second hop.

Embeddings: local `BAAI/bge-small-en-v1.5` via sentence-transformers, behind a
swappable `Embedder` protocol (`src/leg_graphrag/embed.py`) — drop in an API
provider by implementing three members.

## Setup

Requires [uv](https://docs.astral.sh/uv/), Docker (for the HelixDB local instance),
and the [Helix CLI](https://docs.helix-db.com) (`curl -sSL https://install.helix-db.com | bash`).

```bash
uv sync
uv run python -m leg_graphrag.ingest      # fetch + normalize (cached under data/raw/)
helix start dev                            # HelixDB on :6969 (in-memory — reseed after restarts)
uv run python scripts/seed_helix.py        # idempotent graph load (~2 min)
export ANTHROPIC_API_KEY=...
uv run python -m leg_graphrag.eval.run     # both paths, all questions -> eval/results.md
```

`--only R1 H2` runs a subset; `--path graph` runs one substrate.

## Layout

```
src/leg_graphrag/
  waleg.py          # fetch layer: https patch, disk cache, retry, None-vs-[] guards
  ingest.py         # normalize to data/dataset.json (substrate-independent)
  embed.py          # Embedder protocol + sentence-transformers impl + disk cache
  stores/flat.py    # control: numpy cosine over digest vectors
  stores/graph.py   # HelixDB store: seed + traversal/vector query functions
  agent.py          # two PydanticAI agents; same model+prompt, different toolsets
  eval/             # questions.yaml, run.py
scripts/seed_helix.py
```

## Findings

| bucket | control (flat vector) | graph+vector |
|--------|:---:|:---:|
| semantic | 4/4 | 4/4 |
| relational | 0/4 | 4/4 |
| hybrid | 0/4 | 4/4 |

The control abstained (rather than hallucinated) on all 8 relational/hybrid
failures — usually after correctly finding the bill semantically. The information
is structurally absent from a digest-only substrate. Full transcripts in
`eval/results.md`; analysis in `writeup.md`.

## Gotchas hit along the way (mid-2026)

- `wa-leg-api` hardcodes `http://`; some networks block port 80 — we patch
  `waleg.WSLSITE` to https. Empty API results are `None`, not `[]`; the per-member
  vote key is literally `v_ote` (the WSL XML tag is `<VOte>`).
- HelixDB v2 deprecated HelixQL/`schema.hx` — most older tutorials don't apply.
  Python SDK is `helix-db` (`import helixdb`), not the stale `helix-py`.
- With helix-db 0.1.0 / Helix 3.0.6: `in_e(label)` does **not** filter by label
  (chain `.edge_has_label(label)`); `value_map()` fails on edge streams (use
  `edge_properties()`); `$distance` only exists on the direct vector-hit stream.
- The member roster lists chamber-switchers twice under one id, sometimes with
  blank names — ingest dedupes to one member record.
