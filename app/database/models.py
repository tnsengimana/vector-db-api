import uuid
import numpy as np
from typing import List, Set
from pydantic import BaseModel, ConfigDict, Field, field_serializer
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
    documents: Set[str] = set()
    created_at: str = Field(default_factory=get_timestamp)
    updated_at: str = Field(default_factory=get_timestamp)


class DocumentModel(BaseModel):
    id: str = Field(default_factory=_get_uuid)
    name: str
    description: str
    library_id: str
    chunks: Set[str] = set()
    created_at: str = Field(default_factory=get_timestamp)
    updated_at: str = Field(default_factory=get_timestamp)


class ChunkModel(BaseModel):
    id: str = Field(default_factory=_get_uuid)
    text: str
    document_id: str
    vector: np.ndarray
    created_at: str = Field(default_factory=get_timestamp)
    updated_at: str = Field(default_factory=get_timestamp)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_serializer('vector')
    def serialize_array(self, array: np.ndarray) -> List[float]:
        return array.tolist()
