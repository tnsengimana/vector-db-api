from app.common.misc import model_dump_without_none_values
from app.database import DataStore
from app.database.models import DocumentModel
from app.schemas.document import CreateDocumentInput, UpdateDocumentInput
from app.common.exceptions import raise_document_not_found, raise_library_not_found


class DocumentService:
    def __init__(self, db: DataStore):
        self.db = db

    def get_document(self, document_id: str):
        return self.db.documents.get(document_id)

    def get_all_documents(self):
        return self.db.documents.get_all()

    def create_document(self, payload: CreateDocumentInput):
        if not self.db.libraries.exists(payload.library_id):
            return raise_library_not_found(payload.library_id)

        document = DocumentModel(
            name=payload.name,
            description=payload.description,
            library_id=payload.library_id,
        )
        return self.db.documents.add(document.id, document)

    def update_document(self, document_id: str, payload: UpdateDocumentInput):
        if not self.db.documents.exists(document_id):
            return raise_document_not_found(document_id)

        if payload.library_id is not None and not self.db.libraries.exists(
            payload.library_id
        ):
            return raise_library_not_found(payload.library_id)

        data = model_dump_without_none_values(payload)
        return self.db.documents.update(document_id, data)

    def delete_document(self, document_id: str):
        if not self.db.documents.exists(document_id):
            return raise_document_not_found(document_id)

        # TODO: Could use optimization here to avoid O(n) by, for example, keeping a dict mapping a document to the corresponding chunks.
        for chunk in self.get_all_chunks(document_id):
            self.db.chunks.delete(chunk.id)

        return self.db.documents.delete(document_id)

    def get_all_chunks(self, document_id: str):
        # TODO: Could use optimization here to avoid O(n). For example, we can keep a reference of "chunks" on the DocumentModel which we update on insert, update & delete.
        return [
            chunk
            for chunk in self.db.chunks.get_all()
            if chunk.document_id == document_id
        ]
