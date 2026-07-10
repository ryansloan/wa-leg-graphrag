"""Embedding layer: a swappable Embedder protocol with a local sentence-transformers default.

To ship with an API provider later, implement Embedder with the same three
members and pass it wherever an embedder is accepted; the disk cache keys on
model_id so switching models never serves stale vectors.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Protocol

EMBED_CACHE_DIR = Path(__file__).resolve().parents[2] / "data" / "embeddings"

# BGE models want this prefix on retrieval *queries* (not on the indexed passages).
_BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


class Embedder(Protocol):
    model_id: str
    dim: int

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed passages for indexing."""
        ...

    def embed_query(self, text: str) -> list[float]:
        """Embed a search query (models may apply a query-side prefix)."""
        ...


class SentenceTransformerEmbedder:
    def __init__(self, model_id: str = "BAAI/bge-small-en-v1.5"):
        from sentence_transformers import SentenceTransformer  # deferred: heavy import

        self.model_id = model_id
        self._model = SentenceTransformer(model_id)
        self.dim = self._model.get_embedding_dimension()
        self._query_prefix = _BGE_QUERY_PREFIX if "bge" in model_id.lower() else ""

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self._model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self._model.encode([self._query_prefix + text], normalize_embeddings=True)[0].tolist()


class CachedEmbedder:
    """Wraps any Embedder with a JSON disk cache keyed by (model_id, sha256(text))."""

    def __init__(self, inner: Embedder):
        self._inner = inner
        self.model_id = inner.model_id
        self.dim = inner.dim
        safe = inner.model_id.replace("/", "__")
        self._path = EMBED_CACHE_DIR / f"{safe}.json"
        self._cache: dict[str, list[float]] = (
            json.loads(self._path.read_text()) if self._path.exists() else {}
        )

    @staticmethod
    def _key(text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    def embed(self, texts: list[str]) -> list[list[float]]:
        missing = [t for t in texts if self._key(t) not in self._cache]
        if missing:
            for text, vec in zip(missing, self._inner.embed(missing)):
                self._cache[self._key(text)] = vec
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(json.dumps(self._cache))
        return [self._cache[self._key(t)] for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._inner.embed_query(text)


def default_embedder() -> CachedEmbedder:
    return CachedEmbedder(SentenceTransformerEmbedder())


def bill_embed_text(bill: dict) -> str:
    """The text embedded for a bill: id + title + digest, matching what both stores index."""
    return f"{bill['bill_id']}: {bill['title']} {bill['digest']}".strip()
