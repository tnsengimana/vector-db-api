from .memory_store import MemoryStore
from .models import ChunkModel, DocumentModel, LibraryModel


class DataStore:
    def __init__(
        self,
        chunks: MemoryStore[ChunkModel],
        documents: MemoryStore[DocumentModel],
        libraries: MemoryStore[LibraryModel],
    ):
        self.chunks = chunks
        self.documents = documents
        self.libraries = libraries


def create_data_store():
    return DataStore(
        chunks=MemoryStore[ChunkModel](),
        documents=MemoryStore[DocumentModel](),
        libraries=MemoryStore[LibraryModel](),
    )
