# WA Legislature Retrieval Agent — Design Doc

**Status:** Draft for one-day build
**Thesis:** The useful questions about legislation are *relational* (sponsor coalitions, vote splits, cross-bill behavior). Flat-vector RAG over bill text can't answer them well. A structured/agentic substrate can. Build the thing that makes that difference legible.

---

## 1. Goal

An agent that answers questions about WA legislative sessions — bills, sponsorship, and roll-call votes — where the demonstrable payoff is the **query class that breaks flat-vector retrieval**.

Not "a chatbot over legislation." The point is the contrast: same questions, two substrates, one wins on the relational ones.

## 2. Scope (one day)

**In:**
- Ingest structured data for one session (or one chamber) from the WA leg APIs.
- **HelixDB graph+vector store (primary path):** nodes for bills and members, edges for sponsored/voted-on, plus digest embeddings on bill nodes. Relational queries = graph traversals; semantic queries = vector search; hybrid = both, in one substrate.
- **Flat-vector-only baseline (control):** same digest embeddings, no graph. This is the thing the primary path is measured against — not a hedge, the control.
- A curated set of ~8–12 eval questions spanning "semantic," "relational," and "hybrid" types.
- Public repo + short writeup: the query taxonomy and where each substrate wins/loses.

**Out (honest cut):**
- Multi-session scale, full text of bills, amendments history.
- Auth, deployment, UI polish. CLI or notebook is fine today — but keep the retrieval/query core cleanly separated from the interface (a callable module, not logic buried in notebook cells) so it's trivial to wrap in a web UI later.

## 3. Data

Source: WA Legislature web services, via the `wa-leg-api` wrapper (`pip install wa-leg-api`; returns dicts). Sessions are addressed by **biennium** (format `"2023-24"`), not single year.

Relevant calls:
- `legislation.get_legislation_by_year(year)` / `get_legislation(...)` — bill list + digests.
- `sponsor.get_sponsors(...)` / `legislation.get_house_sponsors` / `get_senate_sponsors` — sponsorship.
- `legislation.get_roll_calls(biennium, bill_number)` — **per-bill** roll calls; each vote record carries `member_id`, `vote_date`, `sequence_number`.

Entities to pull:
- **Bills** — id, title, digest/summary, status.
- **Legislators** — assembled from sponsors + roll-call `member_id`s (no bulk roster endpoint).
- **Sponsorships** — bill ↔ member (primary vs. co-sponsor).
- **Roll-call votes** — bill ↔ member ↔ vote, per motion (`sequence_number`).

**Ingest is N+1:** roll calls are fetched one bill at a time, so cost scales with bill count. Scope by ingesting **only bills that reached a recorded floor vote** — cheaper *and* higher-signal, since bills with no roll call have nothing for the relational queries to bite on.

Graph model (HelixDB):
```
nodes:
  Bill(bill_id, biennium, bill_number, title, digest, status)   -- digest embedded as vector
  Member(member_id, name, chamber, party, district)
edges:
  (Member)-[:SPONSORED {role}]->(Bill)          -- role: primary | cosponsor
  (Member)-[:VOTED {vote, sequence_number}]->(Bill)   -- vote: yea | nay | absent
```

Baseline (control): the same bill digests embedded in a flat vector index — no nodes, no edges. Can be a throwaway FAISS/Chroma index, or HelixDB vectors with traversal simply not used.

## 4. Architecture

```
                          ┌─> HelixDB graph+vector  ─┐   [primary]
WA leg APIs ──ingest──┤    (nodes+edges+digest vecs) │
                          └─> flat vector index      ─┘   [control]
                                        │
                                   Agent / eval harness
                                     queries both, compares
```

Primary path: graph traversal (sponsored / voted edges) + vector search over digests, in one substrate. Control: vector search only. The interesting result is the class of question the control *can't* answer because the answer is an edge pattern, not a text passage.

## 5. The query taxonomy (this is the artifact)

Three buckets. The writeup is organized around these.

- **Semantic** — "bills about water rights in rural counties." Flat vector handles fine. The control is legitimately good here; say so.
- **Relational** — "which members co-sponsored the transportation package but voted against the gas-tax provision." Flat vector *can't* — there's no passage that encodes this; it's an edge pattern. Graph traversal nails it.
- **Hybrid** — "find bills semantically about housing where the sponsor coalition split on the floor vote." Needs both: vector to find candidate bills, traversal to filter on vote edges.

The relational + hybrid buckets are the evidence for the graph thesis. Each documented failure of the control is a point in the post.

## 6. Eval

Lightweight, honest. Not a benchmark — a demonstration.

- ~8–12 hand-written questions, ~4 per bucket.
- For each: run both paths (graph+vector vs. flat control), record what each returns.
- Score: does the answer contain the correct members/bills? (Manual check is acceptable at this N.)
- Output a small results table: question × bucket × control correct? × graph+vector correct?

The expected shape — control strong on semantic, collapses on relational — *is the result*, provided it actually holds. If the control does better than expected on relational queries, that's a more interesting finding; report it straight.

## 7. Public output

- **Repo:** ingest script, graph model, both retrieval paths, eval questions + results table, README.
- **Post:** the query taxonomy, one worked example per bucket, the results table, and the honest takeaway — "here's the query class where flat vector loses the relational structure, and here's the graph+vector substrate that recovers it." Frame as started-and-shipped, not finished.

## 8. Open decisions (work through with the agent)

1. HelixDB setup friction — confirm graph+vector modeling and the embedding workflow early; it's the one dependency that can eat the day. The flat control is trivial (FAISS) if HelixDB slips.
2. Embedding model — API vs. local; digest length may allow a small local model.
3. Agent framework — direct tool-calling loop vs. PydanticAI (relevant to your interview stack; may be worth the friction).
4. Session/chamber to target — pick one with contested votes so relational queries have signal. A session with lopsided unanimous votes kills the demo.
5. Hardcoded two-path comparison vs. agent routing. Hardcoded is cleaner for the writeup (deterministic contrast); routing is a better demo. Do the hardcoded comparison first — it's what the post needs — and add routing only if time allows.
