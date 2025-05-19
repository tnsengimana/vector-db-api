from app.common.misc import model_dump_without_none_values
from app.database import MemoryDatabase
from app.database.models import DocumentModel
from app.schemas.document import CreateDocumentInput, UpdateDocumentInput
from app.common.exceptions import raise_document_not_found, raise_library_not_found


class DocumentService:
    def __init__(self, store: MemoryDatabase):
        self.store = store

    def get_document(self, document_id: str):
        if not self.store.documents.exists(document_id):
            return raise_document_not_found(document_id)

        return self.store.documents.get(document_id)

    def get_all_documents(self):
        return self.store.documents.get_all()

    def create_document(self, payload: CreateDocumentInput):
        if not self.store.libraries.exists(payload.library_id):
            return raise_library_not_found(payload.library_id)

        # Create the document first
        document = self.store.documents.upsert(
            DocumentModel(
                name=payload.name,
                description=payload.description,
                library_id=payload.library_id,
            )
        )

        # Add this document to the library
        library = self.store.libraries.get(document.library_id)
        library.documents.add(document.id)
        self.store.libraries.upsert(library)

        return document

    def update_document(self, document_id: str, payload: UpdateDocumentInput):
        if payload.library_id is not None and not self.store.libraries.exists(
            payload.library_id
        ):
            return raise_library_not_found(payload.library_id)

        document = self.get_document(document_id)
        data = model_dump_without_none_values(payload)
        return self.store.documents.upsert(document.model_copy(update=data, deep=True))

    def delete_document(self, document_id: str):
        document = self.get_document(document_id)

        # Remove chunks associated with this document
        for chunk_id in document.chunks:
            self.store.chunks.delete(chunk_id)

        # Remove this document from the library
        library = self.store.libraries.get(document.library_id)
        library.documents.remove(document.id)
        self.store.libraries.upsert(library)

        # Then finally delete it
        return self.store.documents.delete(document_id)

    def get_all_chunks(self, document_id: str):
        document = self.get_document(document_id)
        return [self.store.chunks.get(chunk_id) for chunk_id in document.chunks]
