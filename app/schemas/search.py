from pydantic import BaseModel
from app.database.models import ChunkModel


"""
Contains pydantic models represeting the request and response payloads of our search interface.
"""


class SearchInput(BaseModel):
    query: str
    top_k: int


class SearchOutput(BaseModel):
    score: float
    chunk: ChunkModel
