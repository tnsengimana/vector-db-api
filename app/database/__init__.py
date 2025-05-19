from .memory_store import MemoryStore
from .models import ChunkModel, DocumentModel, LibraryModel



class MemoryDatabase:
    def __init__(self):
        self.chunks = MemoryStore[ChunkModel]()
        self.documents = MemoryStore[DocumentModel]()
        self.libraries = MemoryStore[LibraryModel]()
