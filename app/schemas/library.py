from pydantic import BaseModel
from typing import Optional
from app.database.models import LibraryModel


"""
Contains pydantic models for library's request and response payloads.
"""


class CreateLibraryInput(BaseModel):
    name: str
    description: str


class UpdateLibraryInput(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class LibraryOutput(LibraryModel):
    """In a real-world scenario, this class may not be the same as our db model"""
    pass
