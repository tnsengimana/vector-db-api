from typing import Callable, List
from app.common.misc import model_dump_without_none_values
from app.database import DataStore
from app.database.models import ChunkModel
from app.schemas.chunk import CreateChunkInput, UpdateChunkInput
from app.common.exceptions import raise_chunk_not_found, raise_document_not_found


class ChunkService:
    def __init__(self, store: DataStore, create_vector: Callable[[str], List[float]]):
        self.store = store
        self.create_vector = create_vector

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
                vector=self.create_vector(payload.text),
            )
        )

        # Then add it to the document
        document = self.store.documents.get(payload.document_id)
        document.chunks.add(chunk.id)
        self.store.documents.upsert(document)

        return chunk

    def update_chunk(self, chunk_id: str, payload: UpdateChunkInput):
        if payload.document_id is not None and not self.store.documents.exists(
            payload.document_id
        ):
            return raise_document_not_found(payload.document_id)

        chunk = self.get_chunk(chunk_id)
        data = model_dump_without_none_values(payload)

        if payload.text is not None:
            data["vector"] = self.create_vector(payload.text)

        return self.store.chunks.upsert(chunk.model_copy(update=data, deep=True))

    def delete_chunk(self, chunk_id: str):
        chunk = self.get_chunk(chunk_id)

        # Remove this chunk from the document
        document = self.store.documents.get(chunk.document_id)
        document.chunks.remove(chunk.id)
        self.store.documents.upsert(document)

        # And finally remove the chunk
        return self.store.chunks.delete(chunk_id)
