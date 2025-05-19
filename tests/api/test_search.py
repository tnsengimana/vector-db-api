from app.common.embeddings import bulk_create_embedding_vector
from tests._utils.testcase import BaseTestCase


class SearchTestCase(BaseTestCase):
    def test_index_library(self):
        # Prep data
        libraries = [
            self.create_library(),
            self.create_library(),
        ]
        documents = [
            self.create_document(library_id=libraries[0].id),
            self.create_document(library_id=libraries[0].id),
            self.create_document(library_id=libraries[1].id),
            self.create_document(library_id=libraries[1].id),
        ]
        chunks = [
            self.create_chunk(document_id=documents[0].id),
            self.create_chunk(document_id=documents[1].id),
            self.create_chunk(document_id=documents[2].id),
            self.create_chunk(document_id=documents[3].id),
        ]

        # Send request
        response = self.client.post(f"/libraries/{libraries[0].id}/index")
        self.assertTrue(response.is_success)

        # Make assertions
        self.assertTrue(self.indices.exists(libraries[0].id))

        actual = sorted([item.id for item in self.indices.get(libraries[0].id).get_all()])
        expected = sorted([chunks[0].id, chunks[1].id])
        self.assertListEqual(actual, expected)

    def test_search_library(self):
        # Prep data
        sentences = [
            "He finished the assignment ahead of schedule.",
            "The baby giggled when the puppy licked her face.",
            "She painted the entire room in one afternoon.",
            "Lightning flashed across the night sky.",
            "They argued about where to go for dinner.",
            "A lone cyclist sped down the empty road.",
        ]
        embeddings = bulk_create_embedding_vector(sentences)

        library = self.create_library()
        document = self.create_document(library_id=library.id)
        chunks = [
            self.create_chunk(
                document_id=document.id, text=value, vector=embeddings[key]
            )
            for key, value in enumerate(sentences)
        ]
        payload = {"query": "He completed the project before the deadline.", "top_k": 2}

        # Set up index
        self.indices.add(library.id)
        self.indices.get(library.id).build(chunks)

        # Send request
        response = self.client.post(f"/libraries/{library.id}/search", json=payload)
        self.assertTrue(response.is_success)

        # Make assertions
        actual = response.json()
        self.assertEqual(
            actual[0]["chunk"]["text"], "He finished the assignment ahead of schedule."
        )
        self.assertEqual(
            actual[1]["chunk"]["text"], "She painted the entire room in one afternoon."
        )
