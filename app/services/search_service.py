from typing import List
from fastapi import HTTPException, status
from app.database import MemoryDatabase
from app.indexing import IndexCollection
from app.common.embeddings import create_embedding_vector
from app.schemas.search import SearchInput, SearchOutput


class SearchService:
    def __init__(self, store: MemoryDatabase, indices=IndexCollection):
        self.store = store
        self.indices = indices

    def index_library(self, library_id: str) -> None:
        if self.indices.exists(library_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Library has already been indexed",
            )
        
        self.indices.add(library_id)
        library = self.store.libraries.get(library_id)

        for document_id in library.documents:
            document = self.store.documents.get(document_id)

            for chunk_id in document.chunks:
                chunk = self.store.chunks.get(chunk_id)
                self.indices.get(library_id).add(chunk)

    def search_library(
        self, library_id: str, payload: SearchInput
    ) -> List[SearchOutput]:
        if not self.indices.exists(library_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Library has not been indexed yet",
            )
        
        query_vector = create_embedding_vector(payload.query)
        return self.indices.get(library_id).search(query_vector, payload.top_k)
