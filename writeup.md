# Where flat-vector RAG loses the plot: relational questions about legislation

*One-day build, started and shipped, not finished. The eval-focused notes below
grew into the published post, "You can do better than retrieval", which adds the
open-ended strategy case study.*
<!-- TODO: link the post once published -->

## The thesis

Ask "which bills deal with unemployment insurance?" and a flat vector index over
bill digests answers fine. Ask "which cosponsors of SB 5041 voted against it on
final passage?" and it cannot — not because the retriever is weak, but because **no
text passage encodes the answer**. It's an edge pattern: `(member)-[:SPONSORED]->(bill)`
∩ `(member)-[:VOTED {vote: Nay}]->(bill)`. The failure is structural, and so is the fix.

I built the same QA agent twice over the WA Legislature's 2025-26 biennium (713
bills that reached a floor vote, 154 members, ~152k roll-call votes). Same LLM
(claude-sonnet-5 via PydanticAI), same prompt; the only variable is the retrieval
substrate:

- **Control:** bill-digest embeddings in a flat vector index. One tool: semantic search.
- **Graph+vector:** the same embeddings living on Bill nodes in HelixDB, plus
  SPONSORED/VOTED edges. Tools: semantic search *and* graph traversals.

## The query taxonomy

**Semantic** — "bills about X." Both paths share the same embeddings; the control
is legitimately good here and the eval says so.

**Relational** — sponsor coalitions, vote splits, cross-bill member behavior. The
answer is a subgraph, not a passage. The control's only move is to retrieve topically
similar digests and either abstain or guess.

**Hybrid** — semantic lookup to find the bill, traversal to answer the question
about it ("find the rent-stabilization bill; how close was its Senate vote?").

## Results

12 hand-written questions, 4 per bucket, ground truth hand-derived from the
ingested dataset (auto-scored on required names/numbers, then reviewed by hand —
full transcripts in `eval/results.md`):

| bucket | control (flat vector) | graph+vector |
|--------|:---:|:---:|
| semantic | **4/4** | **4/4** |
| relational | **0/4** | **4/4** |
| hybrid | **0/4** | **4/4** |

The expected shape, and it held completely: the control is genuinely good at
semantic retrieval — it found HB 1217 and eight other tenant-protection bills for
the housing-stability question, same as the graph path — and it went 0-for-8 on
anything requiring an edge.

Two details worth more than the table:

**The control abstained on all 8 relational/hybrid failures — zero hallucinations.**
And in most of them it *found the right bill first*. For H4 it located HB 1515
("alcohol service in public spaces"), then said it had no way to see who voted
against it. The information is simply absent from the substrate, and the model
could tell. With a weaker model or a pushier prompt this failure mode likely turns
into confident fabrication, which is worse; either way, no amount of better
embedding fixes it.

**The graph path composes traversals on its own.** For H2 ("did any Republican
cosponsor a capital-gains bill and vote against it?") the agent ran semantic search
→ sponsor lists for three candidate bills → roll calls for two of them, and
correctly named Paul Harris (R) on SB 5314. Nothing about that chain was hardcoded;
the substrate made it expressible.

## One worked example per bucket

**Semantic (S1):** *"Which bills passed this biennium deal with unemployment
insurance?"* Both paths return SB 5041, HB 2264, SB 6134, SB 5874 from one vector
search. No contrast — that's the point; say so and move on.

**Relational (R2):** *"Which cosponsors of SB 5041 voted against it on final
passage?"* Control: retrieves SB 5041's digest, correctly states its tool can't see
sponsors or votes, abstains. Graph: `bill_sponsors("SB 5041")` →
`bill_votes("SB 5041", vote="Nay", motion_contains="Final Passage")` → intersects →
**Lisa Wellman (D)**, who cosponsored the striking-workers unemployment bill and
voted Nay on its Senate final passage. Two tool calls, exact answer.

**Hybrid (H1):** *"Find the major bill about residential rent stabilization and
report how close its Senate final passage vote was."* Control: finds HB 1217, can't
see votes, abstains. Graph: vector search → `bill_vote_summary("HB 1217")` →
**29–20** Senate final passage.

## The honest takeaways

1. The headline number (0/8 vs 8/8) is really a statement about **where information
   lives**. Roll-call structure never appears in digest text, so no retriever over
   digest text can surface it. "GraphRAG beats RAG" undersells it — flat retrieval
   didn't lose a fair fight; it was never in the game. The fair conclusion: **the
   interesting questions about a legislature are queries against structure, and the
   substrate has to store the structure.**
2. The control's clean abstention is partly a credit to the model. The eval design
   let it say "my tools can't do this"; production RAG systems that force an answer
   from top-k passages would do worse, louder.
3. Building the eval was where the graph earned its keep a second time: my first
   ground truth for R3 (Democrats voting Nay on HB 2049's House passage) was wrong —
   I'd pooled votes without a chamber filter and swept in a senator. The *graph
   agent's* answer exposed the bug. Structured substrates are checkable; prose
   isn't.
4. Sample size is 12; this is a demonstration, not a benchmark.

## Notes on the stack

- **HelixDB v2** (mid-2026): schemaless property graph + vector indexes in one
  store; queries are a builder DSL sent as dynamic requests from Python (`helix-db`
  SDK). One substrate for both retrieval modes is genuinely convenient — the hybrid
  bucket is a single request chaining `vector_search_nodes` into edge traversals.
  The SDK is young (see README gotchas: edge-label filtering, edge property
  accessors, in-memory default).
- **PydanticAI** made the two-agents-one-toolset-apart comparison trivial: same
  model, same instructions, `@agent.tool` on different agents.
- Ingest: `wa-leg-api`, scoped to bills with a recorded floor vote — cheaper *and*
  higher-signal, since that's exactly where the relational structure lives.

## What I'd do next

- Agent-routed single entry point (one agent deciding which substrate to consult)
  now that the hardcoded contrast is on record.
- Committee membership and amendment edges — the taxonomy extends naturally.
- An API embedder behind the existing `Embedder` protocol for anyone who doesn't
  want the ~2GB torch install.
