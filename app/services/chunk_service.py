from typing import Callable, List
from app.common.misc import model_dump_without_none_values
from app.database import DataStore
from app.database.models import ChunkModel
from app.schemas.chunk import CreateChunkInput, UpdateChunkInput
from app.common.embeddings import create_embedding_vector
from app.common.exceptions import raise_chunk_not_found, raise_document_not_found


class ChunkService:
    def __init__(self, db: DataStore, create_vector: Callable[[str], List[float]]):
        self.db = db
        self.create_vector = create_vector

    def get_chunk(self, chunk_id: str):
        return self.db.chunks.get(chunk_id)

    def get_all_chunks(self):
        return self.db.chunks.get_all()

    def create_chunk(self, payload: CreateChunkInput):
        if not self.db.documents.exists(payload.document_id):
            return raise_document_not_found(payload.document_id)

        document = self.db.documents.get(payload.document_id)
        chunk = ChunkModel(
            text=payload.text,
            document_id=document.id,
            library_id=document.library_id,
            vector=self.create_vector(payload.text),
        )
        return self.db.chunks.add(chunk.id, chunk)

    def update_chunk(self, chunk_id: str, payload: UpdateChunkInput):
        if not self.db.chunks.exists(chunk_id):
            return raise_chunk_not_found(chunk_id)

        if payload.document_id is not None and not self.db.documents.exists(
            payload.document_id
        ):
            return raise_document_not_found(payload.document_id)

        data = model_dump_without_none_values(payload)
        if payload.text is not None:
            data["vector"] = self.create_vector(payload.text)

        return self.db.chunks.update(chunk_id, data)

    def delete_chunk(self, chunk_id: str):
        if not self.db.chunks.exists(chunk_id):
            return raise_chunk_not_found(chunk_id)

        return self.db.chunks.delete(chunk_id)
