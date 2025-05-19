from tests._utils.testcase import BaseTestCase


class ChunksTestCase(BaseTestCase):
    def test_list_chunks(self):
        chunks = [self.create_chunk(), self.create_chunk()]

        response = self.client.get("/chunks")
        self.assertTrue(response.is_success)

        actual = response.json()
        expected = [item.model_dump(mode="json") for item in chunks]
        self.assertEqual(actual, expected)

    def test_create_chunk(self):
        document = self.create_document()
        payload = {"document_id": document.id, "text": "hello world"}

        response = self.client.post("/chunks", json=payload)
        self.assertTrue(response.is_success)

        actual = response.json()
        self.assertEqual(actual["document_id"], payload["document_id"])
        self.assertEqual(actual["text"], payload["text"])
        self.assertEqual(self.store.chunks.size(), 1)
    
    def test_create_chunk__updates_library_index(self):
        # Prep data
        library = self.create_library()
        document = self.create_document(library_id=library.id)
        payload = {"document_id": document.id, "text": "hello world"}

        # Set up index
        self.indices.add(library.id)

        # Send request
        response = self.client.post("/chunks", json=payload)
        self.assertTrue(response.is_success)

        # Make assertitions
        actual = response.json()
        self.assertEqual(actual["document_id"], payload["document_id"])
        self.assertEqual(actual["text"], payload["text"])
        self.assertEqual(self.store.chunks.size(), 1)

        self.assertEqual(len(self.indices.get(library.id).get_all()), 1)
        self.assertEqual(self.indices.get(library.id).get_all()[0].text, "hello world")

    def test_read_chunk(self):
        chunk = self.create_chunk()

        response = self.client.get(f"/chunks/{chunk.id}")
        self.assertTrue(response.is_success)

        actual = response.json()
        expected = chunk.model_dump(mode="json")
        self.assertEqual(actual, expected)

    def test_update_chunk(self):
        chunk = self.create_chunk(text="some text")
        payload = {"text": "Cool beans"}

        response = self.client.patch(f"/chunks/{chunk.id}", json=payload)
        self.assertTrue(response.is_success)

        updated = self.store.chunks.get(chunk.id)
        self.assertEqual(updated.text, payload["text"])
        self.assertNotEqual(updated.vector.tolist(), chunk.vector.tolist())

    def test_update_chunk__updates_library_index(self):
        # Prep data
        library = self.create_library()
        document = self.create_document(library_id=library.id)
        chunk = self.create_chunk(document_id=document.id, text="some text")
        payload = {"text": "Cool beans"}

        # Set up index
        self.indices.add(library.id)
        self.indices.get(library.id).add(chunk)

        # Send request
        response = self.client.patch(f"/chunks/{chunk.id}", json=payload)
        self.assertTrue(response.is_success)

        # Make assertitions
        updated = self.store.chunks.get(chunk.id)
        self.assertEqual(updated.text, payload["text"])
        self.assertNotEqual(updated.vector.tolist(), chunk.vector.tolist())
        
        indexed_chunk = self.indices.get(library.id).get_all()[0]
        self.assertEqual(indexed_chunk.text, payload["text"])

    def test_delete_chunk(self):
        chunk = self.create_chunk()

        response = self.client.delete(f"/chunks/{chunk.id}")
        self.assertTrue(response.is_success)

        self.assertEqual(self.store.chunks.size(), 0)

    def test_delete_chunk__updates_library_index(self):
        # Prep data
        library = self.create_library()
        document = self.create_document(library_id=library.id)
        chunk = self.create_chunk(document_id=document.id)

        # Set up index
        self.indices.add(library.id)
        self.indices.get(library.id).add(chunk)

        # Send request
        response = self.client.delete(f"/chunks/{chunk.id}")
        self.assertTrue(response.is_success)

        # Make assertitions
        self.assertEqual(self.store.chunks.size(), 0)
        self.assertEqual(len(self.indices.get(library.id).get_all()), 0)
