import numpy as np
from typing import List, Dict, Set
from collections import defaultdict
from sklearn.preprocessing import normalize
from app.database.models import ChunkModel
from app.common.embeddings import DIMENSION_SIZE
from app.schemas.search import SearchOutput
from .base import VectorIndex


class LSHVectorIndex(VectorIndex):
    """
    Locality-sensitive hashing index.

    Complexity variables
    t = table_count
    h = hasher_count
    a = vector size
    n = chunks count

    Time complexity:
    - build: O(n * (t * h * a))
    - search: O((t * h * a) + m) (where m is the # of chunks in the same bucket. It's possible to express m in terms of n.)
    - add: O(t * h * a)
    - remove: O(t)
    - update: O((t * h * a) + t ) = (remove + add)

    Space complexity:
    - O((n * t) + n)
    """

    def __init__(self, table_count: int, hasher_count: int) -> None:
        super().__init__()

        # Required for the functionality of LSH
        self.tables: List[Dict[str, Set[str]]] = [
            defaultdict(set) for _ in range(table_count)
        ]
        self.hashers = [
            np.random.randn(hasher_count, DIMENSION_SIZE) for _ in range(table_count)
        ]

        # Required to optimize remove operation
        self.hash_values = [defaultdict(str) for _ in range(table_count)]

        # Required to optimize search operation
        self.normalized_vectors: Dict[str, np.ndarray] = {}

    def search(self, vector: np.ndarray, top_k: int = 10) -> List[SearchOutput]:
        query_vector = self._normalize_vector(vector)
        candidate_ids = set()

        for i in range(len(self.tables)):
            hash_value = self._compute_hash(query_vector, self.hashers[i])
            candidate_ids.update(self.tables[i][hash_value])

        scores = [
            (
                chunk_id,
                self._cosine_similarity(
                    self.normalized_vectors[chunk_id], query_vector
                ),
            )
            for chunk_id in candidate_ids
        ]

        scores.sort(key=lambda x: x[1], reverse=True)
        return self._get_search_outputs(scores[:top_k])

    def add(self, chunk: ChunkModel) -> None:
        with self._lock:
            # Copy the model to avoid unintended moficiations
            self.chunks[chunk.id] = chunk.model_copy(deep=True)

            chunk_vector = self._normalize_vector(chunk.vector)
            self.normalized_vectors[chunk.id] = chunk_vector

            for i in range(len(self.tables)):
                hash_value = self._compute_hash(chunk_vector, self.hashers[i])

                self.tables[i][hash_value].add(chunk.id)
                self.hash_values[i][chunk.id] = hash_value

    def remove(self, chunk_id: str) -> None:
        with self._lock:
            if chunk_id not in self.chunks:
                return

            for i in range(len(self.tables)):
                hash_value = self.hash_values[i][chunk_id]
                self.tables[i][hash_value].remove(chunk_id)
                del self.hash_values[i][chunk_id]

            del self.chunks[chunk_id]
            del self.normalized_vectors[chunk_id]

    def update(self, chunk: ChunkModel) -> None:
        with self._lock:
            self.remove(chunk.id)
            self.add(chunk)

    @staticmethod
    def _normalize_vector(vector: np.ndarray):
        nd_vectory = vector.reshape(1, -1)
        normalized = normalize(nd_vectory)
        return normalized[0]

    @staticmethod
    def _compute_hash(vector: np.ndarray, planes: np.ndarray):
        return "".join(["1" if np.dot(vector, p) > 0 else "0" for p in planes])
