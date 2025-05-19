import threading
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from app.database.models import ChunkModel
from app.schemas.search import SearchOutput


class VectorIndex(ABC):
    """
    Base class for our vector db index. Different indexing algorithms will
    subclass it and provide implementation of each method. We are using the
    ChunkModel as-is but we could also have a separate class like IndexedChunk
    which contains additional metadata not available on ChunkModel.
    """

    def __init__(self) -> None:
        self.chunks: Dict[str, ChunkModel] = {}
        # A lock to ensure that only one thread can read & write to this index.
        self._lock = threading.RLock()
        super().__init__()

    def build(self, chunks: List[ChunkModel]) -> None:
        with self._lock:
            for chunk in chunks:
                self.add(chunk)

    @abstractmethod
    def search(self, vector: np.ndarray, top_k: int = 10) -> List[SearchOutput]:
        pass

    @abstractmethod
    def add(self, chunk: ChunkModel) -> None:
        pass

    @abstractmethod
    def remove(self, chunk_id: str) -> None:
        pass

    @abstractmethod
    def update(self, chunk: ChunkModel) -> None:
        pass

    def get_all(self) -> List[ChunkModel]:
        with self._lock:
            # Return a copy of each chunk to avoid unintentional modifcation by the caller
            return list([item.model_copy(deep=True) for item in self.chunks.values()])

    def _get_search_outputs(self, results: Tuple[str, float]) -> List[SearchOutput]:
        return [
            # Return a copy of each chunk to avoid unintentional modifcation by the caller
            SearchOutput(
                chunk=self.chunks.get(item[0]).model_copy(deep=True), score=item[1]
            )
            for item in results
        ]

    @staticmethod
    def _cosine_similarity(first: np.ndarray, second: np.ndarray) -> float:
        return np.dot(first, second) / (np.linalg.norm(first) * np.linalg.norm(second))
