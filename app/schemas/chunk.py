from pydantic import BaseModel
from typing import Optional
from app.database.models import ChunkModel


"""
Contains pydantic models for chunk's request and response payloads.
"""


class CreateChunkInput(BaseModel):
    text: str
    document_id: str


class UpdateChunkInput(BaseModel):
    text: Optional[str] = None
    document_id: Optional[str] = None


class ChunkOutput(ChunkModel):
    """In a real-world scenario, this class may not be the same as our db model"""
    pass
