from tests._utils.testcase import BaseTestCase


class DocumentsTestCase(BaseTestCase):
    def test_list_documents(self):
        documents = [self.create_document(), self.create_document()]

        response = self.client.get("/documents")
        self.assertTrue(response.is_success)

        actual = response.json()
        expected = [item.model_dump(mode="json") for item in documents]
        self.assertEqual(actual, expected)

    def test_create_document(self):
        library = self.create_library()
        payload = {"library_id": library.id, "name": "my document", "description": "some description"}

        response = self.client.post("/documents", json=payload)
        self.assertTrue(response.is_success)

        actual = response.json()
        self.assertEqual(actual["library_id"], payload["library_id"])
        self.assertEqual(actual["name"], payload["name"])
        self.assertEqual(actual["description"], payload["description"])
        self.assertEqual(self.store.documents.size(), 1)

    def test_read_document(self):
        document = self.create_document()

        response = self.client.get(f"/documents/{document.id}")
        self.assertTrue(response.is_success)

        actual = response.json()
        expected = document.model_dump(mode="json")
        self.assertEqual(actual, expected)

    def test_update_document(self):
        document = self.create_document()
        payload = {"name": "some new name"}

        response = self.client.patch(f"/documents/{document.id}", json=payload)
        self.assertTrue(response.is_success)

        updated = self.store.documents.get(document.id)
        self.assertEqual(updated.name, payload["name"])

    def test_delete_document(self):
        document = self.create_document()
        chunk = self.create_chunk(document_id=document.id, library_id=document.library_id)

        response = self.client.delete(f"/documents/{document.id}")
        self.assertTrue(response.is_success)

        self.assertEqual(self.store.documents.size(), 0)
        self.assertEqual(self.store.chunks.size(), 0)

    def test_list_document_chunks(self):
        document = self.create_document()
        chunk = self.create_chunk(document_id=document.id, library_id=document.library_id)

        response = self.client.get(f"/documents/{document.id}/chunks")
        self.assertTrue(response.is_success)

        actual = response.json()
        expected = [chunk.model_dump(mode="json")]
        self.assertEqual(actual, expected)
