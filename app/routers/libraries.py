from typing import List
from fastapi import APIRouter, Depends, status
from app.schemas.document import DocumentOutput
from app.services import LibraryService
from app.dependencies import get_library_service
from app.schemas.library import (
    CreateLibraryInput,
    UpdateLibraryInput,
    LibraryOutput,
)

router = APIRouter(
    prefix="/libraries",
    tags=["libraries"],
    responses={404: {"description": "Not found"}}
)


@router.get("", response_model=List[LibraryOutput])
def list_libraries(service: LibraryService = Depends(get_library_service)):
    return service.get_all_libraries()


@router.post("", response_model=LibraryOutput, status_code=status.HTTP_201_CREATED)
def create_library(
    payload: CreateLibraryInput, service: LibraryService = Depends(get_library_service)
):
    return service.create_library(payload)


@router.get("/{library_id}", response_model=LibraryOutput)
def read_library(
    library_id: str, service: LibraryService = Depends(get_library_service)
):
    return service.get_library(library_id)


@router.patch("/{library_id}", response_model=LibraryOutput)
def update_library(
    library_id: str,
    payload: UpdateLibraryInput,
    service: LibraryService = Depends(get_library_service),
):
    return service.update_library(library_id, payload)


@router.delete("/{library_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_library(
    library_id: str, service: LibraryService = Depends(get_library_service)
):
    return service.delete_library(library_id)


@router.get("/{library_id}/documents", response_model=List[DocumentOutput])
def list_library_documents(
    library_id: str, service: LibraryService = Depends(get_library_service)
):
    # TODO: Could add pagination here to avoid overwheelming the system in case there are lots of documents
    return service.get_all_documents(library_id)
