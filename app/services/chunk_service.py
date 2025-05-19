from app.common.misc import model_dump_without_none_values
from app.database import MemoryDatabase
from app.database.models import ChunkModel
from app.indexing import IndexCollection
from app.schemas.chunk import CreateChunkInput, UpdateChunkInput
from app.common.exceptions import raise_chunk_not_found, raise_document_not_found
from app.common.embeddings import create_embedding_vector


class ChunkService:
    def __init__(self, store: MemoryDatabase, indices: IndexCollection):
        self.store = store
        self.indices = indices

    def get_chunk(self, chunk_id: str):
        if not self.store.chunks.exists(chunk_id):
            return raise_chunk_not_found(chunk_id)

        return self.store.chunks.get(chunk_id)

    def get_all_chunks(self):
        return self.store.chunks.get_all()

    def create_chunk(self, payload: CreateChunkInput):
        if not self.store.documents.exists(payload.document_id):
            return raise_document_not_found(payload.document_id)

        # Create the chunk first
        chunk = self.store.chunks.upsert(
            ChunkModel(
                text=payload.text,
                document_id=payload.document_id,
                vector=create_embedding_vector(payload.text),
            )
        )

        # Then add it to the document
        document = self.store.documents.get(payload.document_id)
        document.chunks.add(chunk.id)
        self.store.documents.upsert(document)

        # Add chunk to our index (if applicable)
        if self.indices.exists(document.library_id):
            self.indices.get(document.library_id).add(chunk)

        return chunk

    def update_chunk(self, chunk_id: str, payload: UpdateChunkInput):
        if payload.document_id is not None and not self.store.documents.exists(
            payload.document_id
        ):
            return raise_document_not_found(payload.document_id)

        # Update the db chunk
        chunk = self.get_chunk(chunk_id)
        data = model_dump_without_none_values(payload)

        if payload.text is not None:
            data["vector"] = create_embedding_vector(payload.text)

        updated = self.store.chunks.upsert(chunk.model_copy(update=data, deep=True))

        # Update our index (if applicable)
        document = self.store.documents.get(updated.document_id)
        if self.indices.exists(document.library_id):
            self.indices.get(document.library_id).update(updated)

        return updated

    def delete_chunk(self, chunk_id: str):
        chunk = self.get_chunk(chunk_id)

        # Remove this chunk from the document
        document = self.store.documents.get(chunk.document_id)
        document.chunks.remove(chunk.id)
        self.store.documents.upsert(document)

        # Delete the chunk itself from db
        deleted = self.store.chunks.delete(chunk_id)

        # Delete the chunk from our index
        document = self.store.documents.get(deleted.document_id)
        if self.indices.exists(document.library_id):
            self.indices.get(document.library_id).remove(deleted)

        return deleted
