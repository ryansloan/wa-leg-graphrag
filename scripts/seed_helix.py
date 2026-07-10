"""Load data/dataset.json into the running HelixDB instance (idempotent).

The local instance is in-memory: rerun this after every `helix start/restart`.
"""

import json
from pathlib import Path

from leg_graphrag.embed import default_embedder
from leg_graphrag.ingest import DATASET_PATH
from leg_graphrag.stores.graph import GraphStore


def main() -> None:
    dataset = json.loads(Path(DATASET_PATH).read_text())
    store = GraphStore()
    store.seed(dataset, default_embedder())


if __name__ == "__main__":
    main()
