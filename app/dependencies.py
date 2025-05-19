from fastapi import Depends
from app.database import MemoryDatabase
from app.indexing import IndexCollection
from app.services import ChunkService, DocumentService, LibraryService, SearchService


def get_data_store():
    return MemoryDatabase()


def get_search_indices():
    return IndexCollection()


def get_chunk_service(store=Depends(get_data_store), indices=Depends(get_search_indices)):
    return ChunkService(store=store, indices=indices)


def get_document_service(store=Depends(get_data_store)):
    return DocumentService(store=store)


def get_library_service(store=Depends(get_data_store)):
    return LibraryService(store=store)


def get_search_service(store=Depends(get_data_store), indices=Depends(get_search_indices)):
    return SearchService(store=store, indices=indices)
