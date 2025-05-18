import uuid
from typing import List
from pydantic import BaseModel, Field
from app.common.misc import get_timestamp


"""
Database models. In a real-world application, this would be ORM models and may or may not be pydantic models.
"""


def _get_uuid():
    return str(uuid.uuid4())


class LibraryModel(BaseModel):
    id: str = Field(default_factory=_get_uuid)
    name: str
    description: str
    created_at: str = Field(default_factory=get_timestamp)
    updated_at: str = Field(default_factory=get_timestamp)


class DocumentModel(BaseModel):
    id: str = Field(default_factory=_get_uuid)
    name: str
    description: str
    library_id: str
    created_at: str = Field(default_factory=get_timestamp)
    updated_at: str = Field(default_factory=get_timestamp)


class ChunkModel(BaseModel):
    id: str = Field(default_factory=_get_uuid)
    text: str
    document_id: str
    library_id: str
    vector: List[float]
    created_at: str = Field(default_factory=get_timestamp)
    updated_at: str = Field(default_factory=get_timestamp)
