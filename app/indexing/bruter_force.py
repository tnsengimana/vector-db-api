import numpy as np
from typing import Dict, List
from app.database.models import ChunkModel
from app.schemas.search import SearchOutput
from ._base import VectorIndex


class BruteForceIndex(VectorIndex):
    def __init__(self) -> None:
        self.chunks: Dict[str, ChunkModel] = {}
        self.vectors: Dict[str, np.ndarray] = {}

    def build(self, chunks: List[ChunkModel]) -> None:
        with self._lock:
            for chunk in chunks:
                self.add(chunk)

    def search(self, vector: List[float], k: int = 10) -> List[SearchOutput]:
        with self._lock:
            query_vector = self.np_array(vector)
            scores = [
                (chunk_id, self.cosine_similarity(chunk_vector, query_vector))
                for chunk_id, chunk_vector in self.vectors.items()
            ]

            scores.sort(key=lambda x: x[1], reverse=True)

            return [
                SearchOutput(chunk=self.chunks.get(item[0]), score=item[1])
                for item in scores[:k]
            ]

    def add(self, chunk: ChunkModel) -> None:
        with self._lock:
            self.chunks[chunk.id] = chunk
            self.vectors[chunk.id] = self.np_array(chunk.vector)

    def remove(self, chunk_id: str) -> None:
        with self._lock:
            if chunk_id not in self.chunks:
                return

            del self.chunks[chunk_id]
            del self.vectors[chunk_id]

    def update(self, chunk: ChunkModel) -> None:
        with self._lock:
            if chunk.id not in self.chunks:
                return

            self.chunks[chunk.id] = chunk
            self.vectors[chunk.id] = self.np_array(chunk.vector)

    def get_all(self) -> List[ChunkModel]:
        with self._lock:
            return list([item.model_copy(deep=True) for item in self.chunks.values()])
