import threading
from pydantic import BaseModel
from typing import Dict, TypeVar, Generic


T = TypeVar("T", bound=BaseModel)


class MemoryStore(Generic[T]):
    def __init__(self):
        self._data: Dict[str, T] = {}
        self._lock = threading.RLock()  # Using RLock to allow nested acquires

    def get(self, item_id: str):
        with self._lock:
            if not self.exists(item_id):
                raise KeyError(f"Item with ID {item_id} does not exists")
            
            return self._data[item_id].model_copy(deep=True)

    def get_all(self):
        with self._lock:
            return [item.model_copy(deep=True) for item in self._data.values()]

    def add(self, item_id: str, item: T):
        with self._lock:
            if self.exists(item_id):
                raise KeyError(f"Item with ID {item_id} already exists")

            self._data[item_id] = item.model_copy(deep=True)
            return self._data[item_id]

    def update(self, item_id, values: dict):
        with self._lock:
            if not self.exists(item_id):
                raise KeyError(f"Item with ID {item_id} does not exists")
            
            self._data[item_id] = self._data[item_id].model_copy(
                update=values, deep=True
            )
            return self._data[item_id]

    def delete(self, item_id: str):
        with self._lock:
            if not self.exists(item_id):
                raise KeyError(f"Item with ID {item_id} does not exists")
            
            del self._data[item_id]

    def exists(self, item_id: str):
        with self._lock:
            return item_id in self._data

    def clear(self):
        with self._lock:
            self._data.clear()

    def size(self):
        return len(self._data)
