import numpy as np
from abc import ABC, abstractmethod
from typing import List, Tuple
from app.database.models import ChunkModel
from app.schemas.search import SearchOutput


class VectorIndex(ABC):
    @abstractmethod
    def build(self, chunks: List[ChunkModel]) -> None:
        pass

    @abstractmethod
    def search(self, query_vector: List[float], k: int = 10) -> List[SearchOutput]:
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

    @abstractmethod
    def get_all(self) -> List[ChunkModel]:
        pass

    @staticmethod
    def cosine_similarity(first: np.ndarray, second: np.ndarray) -> float:
        return np.dot(first, second) / (np.linalg.norm(first) * np.linalg.norm(second))

    @staticmethod
    def np_array(vector: List[float]) -> np.ndarray:
        return np.array(vector, dtype=np.float32)
