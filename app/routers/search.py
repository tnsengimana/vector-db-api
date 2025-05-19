from fastapi import APIRouter, Depends, status
from app.dependencies import get_search_service
from app.schemas.search import SearchInput
from app.services.search_service import SearchService


router = APIRouter(
    prefix="",
    tags=["search"],
    responses={400: {"description": "Bad request"}}
)


@router.post("/libraries/{library_id}/index", status_code=status.HTTP_204_NO_CONTENT)
def index_library(
    library_id: str,
    service: SearchService = Depends(get_search_service)
):
    return service.index_library(library_id)


@router.post("/libraries/{library_id}/search")
def search_library(
    library_id: str,
    payload: SearchInput,
    service: SearchService = Depends(get_search_service)
):
    return service.search_library(library_id, payload)
