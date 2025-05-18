from typing import List
from fastapi import APIRouter, Depends, status
from app.services import DocumentService
from app.dependencies import get_document_service
from app.schemas.chunk import ChunkOutput
from app.schemas.document import (
    CreateDocumentInput,
    UpdateDocumentInput,
    DocumentOutput,
)


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    responses={404: {"description": "Not found"}}
)


@router.get("", response_model=List[DocumentOutput])
def list_documents(service: DocumentService = Depends(get_document_service)):
    return service.get_all_documents()


@router.post("", response_model=DocumentOutput, status_code=status.HTTP_201_CREATED)
def create_document(
    payload: CreateDocumentInput,
    service: DocumentService = Depends(get_document_service),
):
    return service.create_document(payload)


@router.get("/{document_id}", response_model=DocumentOutput)
def read_document(
    document_id: str, service: DocumentService = Depends(get_document_service)
):
    return service.get_document(document_id)


@router.patch("/{document_id}", response_model=DocumentOutput)
def update_document(
    document_id: str,
    payload: UpdateDocumentInput,
    service: DocumentService = Depends(get_document_service),
):
    return service.update_document(document_id, payload)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: str, service: DocumentService = Depends(get_document_service)
):
    return service.delete_document(document_id)


@router.get("/{document_id}/chunks", response_model=List[ChunkOutput])
def list_document_chunks(
    document_id: str, service: DocumentService = Depends(get_document_service)
):
    # TODO: Could add pagination here to avoid overwheelming the system in case there are lots of chunks
    return service.get_all_chunks(document_id)
