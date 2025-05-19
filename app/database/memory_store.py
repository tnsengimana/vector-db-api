import threading
from pydantic import BaseModel
from typing import Dict, TypeVar, Generic


class _BaseModel(BaseModel):
    id: str


T = TypeVar("T", bound=_BaseModel)


class MemoryStore(Generic[T]):
    """
    Memory store. Uses copy-on-read to avoid accessors from unintentionally modifying stored copies.
    """

    def __init__(self):
        self._data: Dict[str, T] = {}
        # A lock to ensure that only one thread can read and write from this store at a time. 
        # Also, using RLock to allow nested acquires
        self._lock = threading.RLock()  

    def get(self, item_id: str):
        with self._lock:
            if not self.exists(item_id):
                raise KeyError(f"Item with ID {item_id} does not exists")
            return self._data[item_id].model_copy(deep=True)

    def get_all(self):
        with self._lock:
            return [item.model_copy(deep=True) for item in self._data.values()]

    def upsert(self, item: T):
        with self._lock:
            self._data[item.id] = item.model_copy(deep=True)
            return item

    def delete(self, item_id: str):
        with self._lock:
            if not self.exists(item_id):
                raise KeyError(f"Item with ID {item_id} does not exists")
            return self._data.pop(item_id)

    def exists(self, item_id: str):
        with self._lock:
            return item_id in self._data

    def clear(self):
        with self._lock:
            self._data.clear()

    def size(self):
        return len(self._data)
