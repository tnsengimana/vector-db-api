from fastapi import Depends
from app.services import ChunkService, DocumentService, LibraryService
from app.database import create_data_store
from app.common.embeddings import create_embedding_vector


def get_data_store():
    return create_data_store()


def get_vectorizer():
    return create_embedding_vector


def get_chunk_service(
    store=Depends(get_data_store), vectorizer=Depends(get_vectorizer)
):
    return ChunkService(store=store, create_vector=vectorizer)


def get_document_service(store=Depends(get_data_store)):
    return DocumentService(store=store)


def get_library_service(store=Depends(get_data_store)):
    return LibraryService(store=store)
