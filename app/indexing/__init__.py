from typing import Dict, Generic, TypeVar
from ._base import VectorIndex
from .bruter_force import BruteForceIndex


T = TypeVar("T", bound=VectorIndex)


class IndexCollection(Generic[T]):
    def __init__(self) -> None:
        self._collection: Dict[str, VectorIndex] = {}

    def add(self, library_id: str):
        if library_id in self._collection:
            raise KeyError(f"Library with ID {library_id} is already indexed")
        
        self._collection[library_id] = BruteForceIndex()

    def get(self, library_id: str):
        if library_id not in self._collection:
            raise KeyError(f"Library with ID {library_id} is yet to be indexed")

        return self._collection[library_id]
    
    def exists(self, library_id: str):
        return library_id in self._collection

