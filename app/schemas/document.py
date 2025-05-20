from pydantic import BaseModel
from typing import Optional
from app.database.models import DocumentModel


"""
Contains pydantic models for document's request and response payloads.
"""


class CreateDocumentInput(BaseModel):
    name: str
    description: str
    library_id: str


class UpdateDocumentInput(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    library_id: Optional[str] = None


class DocumentOutput(DocumentModel):
    """In a real-world scenario, this class may not be the same as our db model"""
    pass
