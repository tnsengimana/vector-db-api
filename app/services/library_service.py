from app.common.misc import model_dump_without_none_values
from app.database import DataStore
from app.database.models import LibraryModel
from app.common.exceptions import raise_library_not_found
from app.schemas.library import CreateLibraryInput, UpdateLibraryInput


class LibraryService:
    def __init__(self, db: DataStore):
        self.db = db

    def get_library(self, library_id: str):
        return self.db.libraries.get(library_id)

    def get_all_libraries(self):
        return self.db.libraries.get_all()

    def create_library(self, payload: CreateLibraryInput):
        library = LibraryModel(name=payload.name, description=payload.description)
        return self.db.libraries.add(library.id, library)

    def update_library(self, library_id: str, payload: UpdateLibraryInput):
        if not self.db.libraries.exists(library_id):
            return raise_library_not_found(library_id)

        data = model_dump_without_none_values(payload)
        return self.db.libraries.update(library_id, data)

    def delete_library(self, library_id: str):
        if not self.db.libraries.exists(library_id):
            return raise_library_not_found(library_id)

        # TODO (1): Could use optimization here to avoid O(n) by, for example, keeping a dict mapping a library to the corresponding chunks.
        for chunk in self.get_all_chunks(library_id):
            self.db.chunks.delete(chunk.id)

        # TODO: Could use optimization here to avoid O(n) by, for example, keeping a dict mapping a library to the corresponding documents.
        for document in self.get_all_documents(library_id):
            self.db.documents.delete(document.id)
        
        return self.db.libraries.delete(library_id)

    def get_all_chunks(self, library_id: str):
        # TODO: Could use optimization here to avoid O(n). For example, we can keep a reference of "chunks" on the LibraryModel which we update on insert, update & delete.
        return [
            chunk
            for chunk in self.db.chunks.get_all()
            if chunk.library_id == library_id
        ]

    def get_all_documents(self, library_id: str):
        # TODO: Could use optimization here to avoid O(n). For example, ee can keep a reference of "documents" on the LibraryModel which we update on insert, update & delete.
        return [
            document
            for document in self.db.documents.get_all()
            if document.library_id == library_id
        ]
    
