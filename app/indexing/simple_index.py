import numpy as np
from typing import List
from app.database.models import ChunkModel
from app.schemas.search import SearchOutput
from .base import VectorIndex


class SimpleVectorIndex(VectorIndex):
    """
    Simple linear search index.
    
    Time complexity:
    - Build: O(n) where n is the number of chunks
    - Search: O(n) where n is the number of chunks
    - Add: O(1)
    - Remove: O(1)
    - Update: O(1)
    
    Space complexity:
    - O(n) where n is the number of chunks
    """

    def search(self, vector: np.ndarray, top_k: int = 10) -> List[SearchOutput]:
        with self._lock:
            scores = [
                (chunk.id, self._cosine_similarity(chunk.vector, vector))
                for chunk in self.chunks.values()
            ]

            scores.sort(key=lambda x: x[1], reverse=True)
            return self._get_search_outputs(scores[:top_k])

    def add(self, chunk: ChunkModel) -> None:
        with self._lock:
            # Copy the model to avoid unintended moficiations
            self.chunks[chunk.id] = chunk.model_copy(deep=True)

    def remove(self, chunk_id: str) -> None:
        with self._lock:
            if chunk_id not in self.chunks:
                return

            del self.chunks[chunk_id]

    def update(self, chunk: ChunkModel) -> None:
        with self._lock:
            if chunk.id not in self.chunks:
                return

            # Copy the model to avoid unintended moficiations
            self.chunks[chunk.id] = chunk.model_copy(deep=True)

