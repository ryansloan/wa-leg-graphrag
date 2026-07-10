"""HelixDB graph+vector store: Bill/Member nodes, SPONSORED/VOTED edges, digest vectors.

Edges carry denormalized member_name/party/bill_id so edge-stream queries return
self-contained rows without a second traversal.

Note: with helix-db 0.1.0 / Helix 3.0.6, `in_e(label)`/`out_e(label)` do NOT filter
by label server-side; every labeled edge step chains `.edge_has_label(label)`.

Graph model:
  (Member)-[:SPONSORED {role, order, bill_id, member_name, party}]->(Bill)
  (Member)-[:VOTED {vote, motion, sequence_number, vote_date, chamber,
                    bill_id, member_name, party}]->(Bill)
  Bill.embedding: digest vector (vector index)
"""

from __future__ import annotations

import helixdb as h

from ..embed import Embedder, bill_embed_text

_SEED_CHUNK = 2000


def _rows(result: dict, var: str) -> list[dict]:
    """Extract value_map rows from a query result variable."""
    payload = result.get(var) or {}
    return payload.get("properties") or []


class GraphStore:
    def __init__(self, url: str = "http://localhost:6969", embedder: Embedder | None = None):
        self._client = h.Client(url)
        self._embedder = embedder

    def _send(self, batch, name: str) -> dict:
        return self._client.query().dynamic(batch.to_dynamic_request(query_name=name)).send()

    # ---------- seeding ----------

    def counts(self) -> tuple[int, int]:
        rb = (
            h.read_batch()
            .var_as("bills", h.g().n_with_label("Bill").count())
            .var_as("members", h.g().n_with_label("Member").count())
            .returning(["bills", "members"])
        )
        res = self._send(rb, "counts")
        return ((res.get("bills") or {}).get("count", 0),
                (res.get("members") or {}).get("count", 0))

    def seed(self, dataset: dict, embedder: Embedder) -> None:
        """Idempotent: skips if node counts already match the dataset."""
        n_bills, n_members = self.counts()
        if n_bills == len(dataset["bills"]) and n_members == len(dataset["members"]):
            print(f"already seeded ({n_bills} bills, {n_members} members)")
            return
        if n_bills or n_members:
            raise RuntimeError(
                f"instance has partial data ({n_bills} bills, {n_members} members); "
                "restart it (helix restart dev) and re-seed"
            )

        idx = (
            h.write_batch()
            .var_as("v", h.g().create_index_if_not_exists(h.IndexSpec.node_vector("Bill", "embedding")))
            .var_as("b", h.g().create_index_if_not_exists(h.IndexSpec.node_equality("Bill", "bill_id")))
            .var_as("m", h.g().create_index_if_not_exists(h.IndexSpec.node_equality("Member", "name")))
            .returning([])
        )
        self._send(idx, "create_indexes")

        members = {m["member_id"]: m for m in dataset["members"]}
        vectors = embedder.embed([bill_embed_text(b) for b in dataset["bills"]])

        member_node: dict[int, int] = {}
        bill_node: dict[int, int] = {}

        wb = h.write_batch()
        for m in dataset["members"]:
            wb = wb.var_as(f"m{m['member_id']}", h.g().add_n("Member", {
                "member_id": m["member_id"], "name": m["name"], "last_name": m["last_name"],
                "chamber": m["chamber"], "party": m["party"], "district": m["district"],
            }))
        res = self._send(wb.returning([f"m{m['member_id']}" for m in dataset["members"]]), "seed_members")
        for m in dataset["members"]:
            member_node[m["member_id"]] = res[f"m{m['member_id']}"]["ids"][0]

        for start in range(0, len(dataset["bills"]), 200):
            chunk = dataset["bills"][start:start + 200]
            wb = h.write_batch()
            for b, vec in zip(chunk, vectors[start:start + 200]):
                wb = wb.var_as(f"b{b['bill_number']}", h.g().add_n("Bill", {
                    "bill_number": b["bill_number"], "bill_id": b["bill_id"],
                    "current_version_id": b["current_version_id"], "title": b["title"],
                    "digest": b["digest"], "status": b["status"], "embedding": vec,
                }))
            res = self._send(wb.returning([f"b{b['bill_number']}" for b in chunk]), "seed_bills")
            for b in chunk:
                bill_node[b["bill_number"]] = res[f"b{b['bill_number']}"]["ids"][0]

        bill_ids = {b["bill_number"]: b["bill_id"] for b in dataset["bills"]}

        def edge_entries():
            for s in dataset["sponsorships"]:
                m = members[s["member_id"]]
                yield (member_node[s["member_id"]], "SPONSORED", bill_node[s["bill_number"]], {
                    "role": s["role"], "order": s["order"], "bill_id": bill_ids[s["bill_number"]],
                    "member_name": m["name"], "party": m["party"],
                })
            for v in dataset["votes"]:
                m = members[v["member_id"]]
                yield (member_node[v["member_id"]], "VOTED", bill_node[v["bill_number"]], {
                    "vote": v["vote"], "motion": v["motion"], "sequence_number": v["sequence_number"],
                    "vote_date": v["vote_date"], "chamber": v["chamber"],
                    "bill_id": bill_ids[v["bill_number"]],
                    "member_name": m["name"], "party": m["party"],
                })

        buffer, total = [], 0
        for entry in edge_entries():
            buffer.append(entry)
            if len(buffer) >= _SEED_CHUNK:
                total += self._flush_edges(buffer)
                buffer = []
        total += self._flush_edges(buffer)
        print(f"seeded {len(member_node)} members, {len(bill_node)} bills, {total} edges")

    def _flush_edges(self, entries: list[tuple]) -> int:
        if not entries:
            return 0
        wb = h.write_batch()
        for i, (src, label, dst, props) in enumerate(entries):
            wb = wb.var_as(f"e{i}", h.g().n(src).add_e(label, dst, props))
        self._send(wb.returning([]), "seed_edges")
        return len(entries)

    # ---------- queries ----------

    def semantic_search(self, query_vector: list[float], k: int = 10) -> list[dict]:
        rb = (
            h.read_batch()
            .var_as("hits", h.g().vector_search_nodes("Bill", "embedding", query_vector, k)
                    .project([h.Projection.property("bill_id"), h.Projection.property("title"),
                              h.Projection.property("digest"), h.Projection.property("status"),
                              h.Projection.property("$distance", "distance")]))
            .returning(["hits"])
        )
        return _rows(self._send(rb, "semantic_search"), "hits")

    def bill_votes(self, bill_id: str, vote: str | None = None,
                   motion_contains: str | None = None) -> list[dict]:
        """VOTED edge rows for a bill: member_name, party, vote, motion, chamber, ..."""
        pred = h.Predicate.eq("bill_id", bill_id)
        tr = h.g().n_with_label("Bill").where(pred).in_e().edge_has_label("VOTED")
        if vote:
            tr = tr.where(h.Predicate.eq("vote", vote))
        if motion_contains:
            tr = tr.where(h.Predicate.contains("motion", motion_contains))
        rb = h.read_batch().var_as("votes", tr.edge_properties()).returning(["votes"])
        return _rows(self._send(rb, "bill_votes"), "votes")

    def bill_sponsors(self, bill_id: str) -> list[dict]:
        rb = (
            h.read_batch()
            .var_as("sponsors", h.g().n_with_label("Bill")
                    .where(h.Predicate.eq("bill_id", bill_id)).in_e().edge_has_label("SPONSORED").edge_properties())
            .returning(["sponsors"])
        )
        return _rows(self._send(rb, "bill_sponsors"), "sponsors")

    def member_votes(self, member_name: str, vote: str | None = None,
                     motion_contains: str | None = None) -> list[dict]:
        tr = h.g().n_with_label("Member").where(h.Predicate.contains("name", member_name)).out_e().edge_has_label("VOTED")
        if vote:
            tr = tr.where(h.Predicate.eq("vote", vote))
        if motion_contains:
            tr = tr.where(h.Predicate.contains("motion", motion_contains))
        rb = h.read_batch().var_as("votes", tr.edge_properties()).returning(["votes"])
        return _rows(self._send(rb, "member_votes"), "votes")

    def member_sponsorships(self, member_name: str) -> list[dict]:
        rb = (
            h.read_batch()
            .var_as("sp", h.g().n_with_label("Member")
                    .where(h.Predicate.contains("name", member_name)).out_e().edge_has_label("SPONSORED").edge_properties())
            .returning(["sp"])
        )
        return _rows(self._send(rb, "member_sponsorships"), "sp")

    def bill_info(self, bill_id: str) -> list[dict]:
        rb = (
            h.read_batch()
            .var_as("bill", h.g().n_with_label("Bill").where(h.Predicate.eq("bill_id", bill_id))
                    .project([h.Projection.property("bill_id"), h.Projection.property("title"),
                              h.Projection.property("digest"), h.Projection.property("status"),
                              h.Projection.property("current_version_id")]))
            .returning(["bill"])
        )
        return _rows(self._send(rb, "bill_info"), "bill")

    def semantic_hits_with_edges(self, query_vector: list[float], k: int = 10) -> dict:
        """Hybrid primitive: top-k semantic bills plus ALL their vote and sponsor edges, one request."""
        rb = (
            h.read_batch()
            .var_as("hits", h.g().vector_search_nodes("Bill", "embedding", query_vector, k))
            .var_as("bills", h.g().n(h.NodeRef.var("hits"))
                    .project([h.Projection.property("bill_id"), h.Projection.property("title"),
                              h.Projection.property("digest"), h.Projection.property("status")]))
            .var_as("votes", h.g().n(h.NodeRef.var("hits")).in_e().edge_has_label("VOTED").edge_properties())
            .var_as("sponsors", h.g().n(h.NodeRef.var("hits")).in_e().edge_has_label("SPONSORED").edge_properties())
            .returning(["bills", "votes", "sponsors"])
        )
        res = self._send(rb, "semantic_hits_with_edges")
        return {"bills": _rows(res, "bills"), "votes": _rows(res, "votes"),
                "sponsors": _rows(res, "sponsors")}
