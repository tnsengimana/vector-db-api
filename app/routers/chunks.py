from typing import List
from fastapi import APIRouter, Depends, status
from app.services import ChunkService
from app.dependencies import get_chunk_service
from app.schemas.chunk import CreateChunkInput, UpdateChunkInput, ChunkOutput

router = APIRouter(
    prefix="/chunks",
    tags=["chunks"],
    responses={404: {"description": "Not found"}}
)


@router.get("", response_model=List[ChunkOutput])
def list_chunks(service: ChunkService = Depends(get_chunk_service)):
    return service.get_all_chunks()


@router.post("", response_model=ChunkOutput, status_code=status.HTTP_201_CREATED)
def create_chunk(
    payload: CreateChunkInput, svc: ChunkService = Depends(get_chunk_service)
):
    return svc.create_chunk(payload)


@router.get("/{chunk_id}", response_model=ChunkOutput)
def read_chunk(chunk_id: str, service: ChunkService = Depends(get_chunk_service)):
    return service.get_chunk(chunk_id)


@router.patch("/{chunk_id}", response_model=ChunkOutput)
def update_chunk(
    chunk_id: str,
    payload: UpdateChunkInput,
    service: ChunkService = Depends(get_chunk_service),
):
    return service.update_chunk(chunk_id, payload)


@router.delete("/{chunk_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chunk(chunk_id: str, service: ChunkService = Depends(get_chunk_service)):
    return service.delete_chunk(chunk_id)
