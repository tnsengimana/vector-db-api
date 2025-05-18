from tests._utils.testcase import BaseTestCase


class LibrariesTestCase(BaseTestCase):
    def test_list_libraries(self):
        libraries = [self.create_library(), self.create_library()]

        response = self.client.get("/libraries")
        self.assertTrue(response.is_success)

        actual = response.json()
        expected = [item.model_dump(mode="json") for item in libraries]
        self.assertEqual(actual, expected)

    def test_create_library(self):
        payload = {"name": "my library", "description": "some description"}

        response = self.client.post("/libraries", json=payload)
        self.assertTrue(response.is_success)

        actual = response.json()
        self.assertEqual(actual["name"], payload["name"])
        self.assertEqual(actual["description"], payload["description"])
        self.assertEqual(self.store.libraries.size(), 1)

    def test_read_library(self):
        library = self.create_library()

        response = self.client.get(f"/libraries/{library.id}")
        self.assertTrue(response.is_success)

        actual = response.json()
        expected = library.model_dump(mode="json")
        self.assertEqual(actual, expected)

    def test_update_library(self):
        library = self.create_library()
        payload = {"name": "some new name"}

        response = self.client.patch(f"/libraries/{library.id}", json=payload)
        self.assertTrue(response.is_success)

        updated = self.store.libraries.get(library.id)
        self.assertEqual(updated.name, payload["name"])

    def test_delete_library(self):
        library = self.create_library()
        document = self.create_document(library_id=library.id)
        chunk = self.create_chunk(document_id=document.id, library_id=library.id)

        response = self.client.delete(f"/libraries/{library.id}")
        self.assertTrue(response.is_success)

        self.assertEqual(self.store.libraries.size(), 0)
        self.assertEqual(self.store.chunks.size(), 0)

    def test_list_library_documents(self):
        library = self.create_library()
        document = self.create_document(library_id=library.id)

        response = self.client.get(f"/libraries/{library.id}/documents")
        self.assertTrue(response.is_success)

        actual = response.json()
        expected = [document.model_dump(mode="json")]
        self.assertEqual(actual, expected)
