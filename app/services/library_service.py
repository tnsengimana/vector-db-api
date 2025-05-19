from app.common.misc import model_dump_without_none_values
from app.database import MemoryDatabase
from app.database.models import LibraryModel
from app.common.exceptions import raise_library_not_found
from app.schemas.library import CreateLibraryInput, UpdateLibraryInput


class LibraryService:
    def __init__(self, store: MemoryDatabase):
        self.store = store

    def get_library(self, library_id: str):
        if not self.store.libraries.exists(library_id):
            return raise_library_not_found(library_id)

        return self.store.libraries.get(library_id)

    def get_all_libraries(self):
        return self.store.libraries.get_all()

    def create_library(self, payload: CreateLibraryInput):
        return self.store.libraries.upsert(
            LibraryModel(name=payload.name, description=payload.description)
        )

    def update_library(self, library_id: str, payload: UpdateLibraryInput):
        library = self.get_library(library_id)
        data = model_dump_without_none_values(payload)
        return self.store.libraries.upsert(library.model_copy(update=data, deep=True))

    def delete_library(self, library_id: str):
        # Delete all documents and their corresponding chunks first
        for document in self.get_all_documents(library_id):
            self.store.documents.delete(document.id)

            for chunk_id in document.chunks:
                self.store.chunks.delete(chunk_id)

        # Then delete this library
        return self.store.libraries.delete(library_id)

    def get_all_documents(self, library_id: str):
        library = self.get_library(library_id)
        return [
            self.store.documents.get(document_id) for document_id in library.documents
        ]
