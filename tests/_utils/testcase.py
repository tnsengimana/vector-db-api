import numpy as np
from faker import Faker
from unittest import TestCase
from fastapi.testclient import TestClient
from app.database import MemoryDatabase
from app.indexing import IndexCollection
from app.database.models import ChunkModel, DocumentModel, LibraryModel
from app.dependencies import get_data_store, get_search_indices
from app.main import app


class BaseTestCase(TestCase):
    faker = Faker()

    def setUp(self) -> None:
        self.client = TestClient(app)
        self.store = MemoryDatabase()
        self.indices = IndexCollection()

        app.dependency_overrides[get_data_store] = lambda: self.store
        app.dependency_overrides[get_search_indices] = lambda: self.indices

    def tearDown(self) -> None:
        app.dependency_overrides.clear()

    def create_library(self, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = self.faker.name()

        if "description" not in kwargs:
            kwargs["description"] = self.faker.sentence()

        return self.store.libraries.upsert(LibraryModel(**kwargs))

    def create_document(self, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = self.faker.name()

        if "description" not in kwargs:
            kwargs["description"] = self.faker.sentence()

        if "library_id" not in kwargs:
            library = self.create_library()
            kwargs["library_id"] = library.id

        document = self.store.documents.upsert(DocumentModel(**kwargs))

        libary = self.store.libraries.get(document.library_id)
        libary.documents.add(document.id)
        self.store.libraries.upsert(libary)

        return document

    def create_chunk(self, **kwargs):
        if "text" not in kwargs:
            kwargs["text"] = self.faker.name()

        if "vector" not in kwargs:
            kwargs["vector"] = np.random.randn(5)

        if "document_id" not in kwargs:
            document = self.create_document()
            kwargs["document_id"] = document.id

        chunk = self.store.chunks.upsert(ChunkModel(**kwargs))
        
        document = self.store.documents.get(chunk.document_id)
        document.chunks.add(chunk.id)
        self.store.documents.upsert(document)

        return chunk
