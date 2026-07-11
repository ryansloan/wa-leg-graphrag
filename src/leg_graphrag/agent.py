"""Two PydanticAI agents over the same model and instructions; only the toolset differs.

- control_agent: flat-vector semantic search ONLY (the baseline substrate).
- graph_agent:   semantic search PLUS graph traversal tools (HelixDB substrate).

The point of the comparison: relational questions are edge patterns, and the
control has no tool that can see an edge.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

from .embed import Embedder
from .stores.flat import FlatVectorStore
from .stores.graph import GraphStore

MODEL = "anthropic:claude-sonnet-5"

INSTRUCTIONS = """You answer questions about the Washington State Legislature, 2025-26 biennium
(bills that reached a floor vote, their sponsors, and roll-call votes), using ONLY your tools.

- Ground every claim in tool results; cite bill ids (e.g. "SB 5041") and member names exactly.
- If your tools cannot retrieve the information a question needs, say so plainly and answer
  with what you can support. Do not guess member names, vote counts, or bill numbers.
- Party is "D" or "R"; chambers are "House" and "Senate"; votes are Yea/Nay/Absent/Excused.
- A bill's decisive votes are the motions containing "Final Passage".
- Distinguish three kinds of claims, and label the second two:
  facts from tool results (state plainly); inferences from vote patterns (mark as
  inference: "the flip suggests...", never motive-as-fact); and background knowledge
  not available through your tools — committee assignments, leadership roles,
  caucus dynamics, amendment text. Flag background knowledge explicitly
  ("from general knowledge, not this dataset — verify independently") or omit it.
- Amendment roll calls show only the motion label, author, and votes — not the
  amendment's text or intent. Do not assert an amendment strengthened or weakened
  a bill; say a floor amendment by X split the caucus and let the reader check its text.
- Members' chamber comes from the roll call itself. When listing voters, keep House
  and Senate votes separate and make counts match the tallies you report.
- For theme/landscape questions, start with survey_bills (broad, compact) and build the
  answer around multiple bills; drill into at most a handful with the detailed tools.
- Never intersect or aggregate vote lists across bills in your head: use voting_bloc for
  "who opposed/supported all of these" and party_crossovers for caucus-breakers.
- Before finalizing, run every specific member-voted-X-on-bill-Y statement in your draft
  through verify_claims and fix anything not CONFIRMED."""

_MAX_ROWS = 300


@dataclass
class Deps:
    flat: FlatVectorStore
    graph: GraphStore
    embedder: Embedder


def _cap(rows: list, limit: int = _MAX_ROWS) -> list:
    if len(rows) > limit:
        return rows[:limit] + [f"... truncated, {len(rows) - limit} more rows; narrow with filters"]
    return rows


# pydantic-ai defaults Anthropic max_tokens to 4096, which extended thinking plus a
# long answer can exhaust — the reply then truncates mid-sentence (finish reason
# "length"). Raise the ceiling well above any real answer.
_SETTINGS = {"max_tokens": 32768}

control_agent = Agent(MODEL, instructions=INSTRUCTIONS, deps_type=Deps, name="control",
                      defer_model_check=True, model_settings=_SETTINGS)
graph_agent = Agent(MODEL, instructions=INSTRUCTIONS, deps_type=Deps, name="graph",
                    defer_model_check=True, model_settings=_SETTINGS)


@control_agent.tool
def search_bills(ctx: RunContext[Deps], query: str, k: int = 10) -> list[dict]:
    """Semantic search over bill digests. Returns bill_id, title, digest, status, score."""
    return ctx.deps.flat.search(query, k)


@graph_agent.tool
def search_bills_semantic(ctx: RunContext[Deps], query: str, k: int = 10) -> list[dict]:
    """Semantic search over bill digests. Returns bill_id, title, digest, status, distance (lower = closer)."""
    return ctx.deps.graph.semantic_search(ctx.deps.embedder.embed_query(query), k)


@graph_agent.tool
def bill_info(ctx: RunContext[Deps], bill_id: str) -> list[dict]:
    """Look up a bill by id (e.g. 'HB 1217'): title, digest, status, current version."""
    return ctx.deps.graph.bill_info(bill_id)


@graph_agent.tool
def bill_sponsors(ctx: RunContext[Deps], bill_id: str) -> list[str]:
    """Sponsors of a bill, as 'bill_id | Name (party) [role]', primary sponsor first."""
    rows = sorted(ctx.deps.graph.bill_sponsors(bill_id), key=lambda r: r.get("order", 0))
    return [f"{r['bill_id']} | {r['member_name']} ({r['party']}) [{r['role']}]" for r in rows]


@graph_agent.tool
def bill_vote_summary(ctx: RunContext[Deps], bill_id: str) -> list[dict]:
    """Per-motion tallies for a bill: chamber, motion, date, and Yea/Nay/Absent/Excused counts."""
    rows = ctx.deps.graph.bill_votes(bill_id)
    by_motion: dict[tuple, Counter] = {}
    dates: dict[tuple, str] = {}
    for r in rows:
        key = (r["chamber"], r["sequence_number"], r["motion"])
        by_motion.setdefault(key, Counter())[r["vote"]] += 1
        dates[key] = r["vote_date"]
    return [
        {"bill_id": bill_id, "chamber": c, "motion": m, "date": dates[(c, s, m)], **dict(counts)}
        for (c, s, m), counts in sorted(by_motion.items(), key=lambda kv: (kv[0][0], kv[0][1]))
    ]


@graph_agent.tool
def bill_votes(ctx: RunContext[Deps], bill_id: str, vote: str | None = None,
               motion_contains: str | None = None, chamber: str | None = None) -> list[str]:
    """Individual roll-call votes on a bill, as 'bill_id | Name (party-chamber): vote — motion'.
    Filter by vote ('Yea'/'Nay'/...), motion substring (e.g. 'Final Passage'), or chamber."""
    rows = ctx.deps.graph.bill_votes(bill_id, vote=vote, motion_contains=motion_contains)
    if chamber:
        rows = [r for r in rows if r["chamber"] == chamber]
    return _cap([f"{r['bill_id']} | {r['member_name']} ({r['party']}-{r['chamber']}): "
                 f"{r['vote']} — {r['motion']}" for r in rows])


@graph_agent.tool
def member_votes(ctx: RunContext[Deps], member_name: str, vote: str | None = None,
                 motion_contains: str | None = None) -> list[str]:
    """All votes cast by a member (name substring match), as 'Name | bill_id: vote — motion'.
    Large unless filtered; prefer vote and motion_contains='Final Passage' filters."""
    rows = ctx.deps.graph.member_votes(member_name, vote=vote, motion_contains=motion_contains)
    return _cap([f"{r['member_name']} | {r['bill_id']}: {r['vote']} — {r['motion']}" for r in rows])


@graph_agent.tool
def member_sponsorships(ctx: RunContext[Deps], member_name: str) -> list[str]:
    """Bills a member sponsored (name substring match), as 'Name | bill_id [role]'."""
    rows = ctx.deps.graph.member_sponsorships(member_name)
    return _cap([f"{r['member_name']} | {r['bill_id']} [{r['role']}]" for r in rows])


@graph_agent.tool
def survey_bills(ctx: RunContext[Deps], query: str, k: int = 40) -> list[str]:
    """Broad landscape scan: top-k semantically similar bills as compact 'bill_id: digest [status]'
    rows. Use this FIRST for theme/landscape questions, then drill into specific bills."""
    rows = ctx.deps.graph.semantic_search(ctx.deps.embedder.embed_query(query), k)
    return [f"{r['bill_id']}: {r['digest']} [{r['status']}]" for r in rows]


@graph_agent.tool
def voting_bloc(ctx: RunContext[Deps], bill_ids: list[str], vote: str = "Nay",
                motion_contains: str = "Final Passage") -> dict:
    """Members who cast the given vote on matching motions of EVERY listed bill (exact set
    intersection, computed in code). Also returns near-misses (all but one bill).
    Use this instead of intersecting bill_votes lists yourself."""
    counts: Counter = Counter()
    for bid in bill_ids:
        rows = ctx.deps.graph.bill_votes(bid, vote=vote, motion_contains=motion_contains)
        for key in {(r["member_name"], r["party"], r["chamber"]) for r in rows}:
            counts[key] += 1
    n = len(bill_ids)
    return {
        "bills": bill_ids,
        f"{vote} on all {n}": sorted(f"{m} ({p}-{c})" for (m, p, c), k in counts.items() if k == n),
        f"{vote} on {n - 1} of {n}": sorted(f"{m} ({p}-{c})" for (m, p, c), k in counts.items()
                                            if k == n - 1) if n > 2 else [],
    }


@graph_agent.tool
def party_crossovers(ctx: RunContext[Deps], bill_ids: list[str],
                     motion_contains: str = "Final Passage") -> list[str]:
    """Members who voted against their own party's majority on any matching motion of the
    listed bills (exact computation in code). The reliable way to find caucus-breakers."""
    out = []
    for bid in bill_ids:
        rows = ctx.deps.graph.bill_votes(bid, motion_contains=motion_contains)
        by_motion: dict[tuple, list] = defaultdict(list)
        for r in rows:
            by_motion[(r["chamber"], r["sequence_number"], r["motion"])].append(r)
        for (ch, _seq, motion), rs in sorted(by_motion.items()):
            for party in ("D", "R"):
                pv = [r for r in rs if r["party"] == party and r["vote"] in ("Yea", "Nay")]
                yea = sum(1 for r in pv if r["vote"] == "Yea")
                nay = len(pv) - yea
                if yea == nay or not pv:
                    continue
                majority = "Yea" if yea > nay else "Nay"
                out.extend(
                    f"{bid} | {r['member_name']} ({party}-{ch}) voted {r['vote']} against "
                    f"{party} majority ({max(yea, nay)}-{min(yea, nay)}) — {motion}"
                    for r in pv if r["vote"] != majority
                )
    return _cap(out)


class VoteClaim(BaseModel):
    member_name: str
    bill_id: str
    vote: str  # Yea | Nay | Absent | Excused
    motion_contains: str | None = None


@graph_agent.tool
def verify_claims(ctx: RunContext[Deps], claims: list[VoteClaim]) -> list[str]:
    """Check specific (member, bill, vote) statements against the roll-call record before
    presenting them. Returns CONFIRMED or WRONG with the member's actual votes on that bill."""
    results = []
    for c in claims:
        rows = ctx.deps.graph.bill_votes(c.bill_id, motion_contains=c.motion_contains)
        mine = [r for r in rows if c.member_name.lower() in r["member_name"].lower()]
        if not mine:
            results.append(f"NO RECORD: {c.member_name} has no matching vote on {c.bill_id}")
        elif any(r["vote"] == c.vote for r in mine):
            results.append(f"CONFIRMED: {c.member_name} voted {c.vote} on {c.bill_id}")
        else:
            actual = "; ".join(f"{r['vote']} — {r['motion']}" for r in mine)
            results.append(f"WRONG: {c.member_name} on {c.bill_id} actually voted: {actual}")
    return results


def run_control(question: str, deps: Deps):
    return control_agent.run_sync(question, deps=deps)


def run_graph(question: str, deps: Deps):
    return graph_agent.run_sync(question, deps=deps)
