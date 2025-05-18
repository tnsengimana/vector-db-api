from fastapi import status, HTTPException


def raise_chunk_not_found(chunk_id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Chunk with ID {chunk_id} does not exist.",
    )


def raise_document_not_found(document_id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Document with ID {document_id} does not exist.",
    )


def raise_library_not_found(library_id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Library with ID {library_id} does not exist.",
    )
