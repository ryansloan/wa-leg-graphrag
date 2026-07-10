"""Flat-vector control: the same bill-digest embeddings as the graph store, no structure.

numpy cosine top-k; at ~700 bills an ANN index adds nothing.
"""

from __future__ import annotations

import numpy as np

from ..embed import Embedder, bill_embed_text


class FlatVectorStore:
    def __init__(self, bills: list[dict], matrix: np.ndarray, embedder: Embedder):
        self._bills = bills
        self._matrix = matrix  # (n_bills, dim), rows L2-normalized
        self._embedder = embedder

    @classmethod
    def build(cls, dataset: dict, embedder: Embedder) -> "FlatVectorStore":
        bills = dataset["bills"]
        vecs = np.array(embedder.embed([bill_embed_text(b) for b in bills]))
        vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)
        return cls(bills, vecs, embedder)

    def search(self, query: str, k: int = 10) -> list[dict]:
        q = np.array(self._embedder.embed_query(query))
        q /= np.linalg.norm(q)
        scores = self._matrix @ q
        top = np.argsort(-scores)[:k]
        return [
            {
                "bill_id": self._bills[i]["bill_id"],
                "title": self._bills[i]["title"],
                "digest": self._bills[i]["digest"],
                "status": self._bills[i]["status"],
                "score": float(scores[i]),
            }
            for i in top
        ]
