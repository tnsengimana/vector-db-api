from app.common.embeddings import bulk_create_embedding_vector, create_embedding_vector
from tests._utils.testcase import BaseTestCase
from app.indexing.lsh_index import LSHVectorIndex


class LSHVectorIndexTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.index = LSHVectorIndex(table_count=10, hasher_count=5)

    def test_search(self):
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
        chunks = [
            self.create_chunk(text=value, vector=embeddings[key])
            for key, value in enumerate(sentences)
        ]

        # Build index
        self.index.build(chunks)

        # Perform a search
        vector = create_embedding_vector(
            "He completed the project before the deadline."
        )
        results = self.index.search(vector, top_k=1)

        # Make assertions
        self.assertEqual(
            results[0].chunk.text, "He finished the assignment ahead of schedule."
        )

    def test_add(self):
        chunk = self.create_chunk(
            text="some text", vector=create_embedding_vector("some text")
        )
        self.index.add(chunk)
        self.assertEqual(len(self.index.get_all()), 1)

    def test_update(self):
        chunk = self.create_chunk(
            text="some text", vector=create_embedding_vector("some text")
        )
        self.index.add(chunk)

        chunk = chunk.model_copy(
            update={
                "text": "updated text",
                "vector": create_embedding_vector("updated text"),
            }
        )
        self.index.update(chunk)
        self.assertEqual(self.index.get_all()[0].text, "updated text")

    def test_remove(self):
        chunk = self.create_chunk(
            text="some text", vector=create_embedding_vector("some text")
        )
        self.index.add(chunk)

        self.index.remove(chunk.id)
        self.assertEqual(len(self.index.get_all()), 0)
