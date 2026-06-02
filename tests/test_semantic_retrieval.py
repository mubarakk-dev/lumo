import unittest

from app.services.chroma_retrieval_service import build_chroma_index, retrieve_chroma_matches
from app.services.chunking_service import load_knowledge_chunks
from app.services.embedding_service import cosine_similarity, embed_text
from app.services.semantic_retrieval_service import build_vector_index, retrieve_semantic_matches
from app.services.vector_store import load_index_metadata
from tests.test_retrieval import load_retrieval_cases, path_contains


class SemanticRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build_vector_index("docker")
        build_chroma_index("docker")

    def test_loads_chunks_with_metadata(self):
        chunks = load_knowledge_chunks("docker")

        self.assertTrue(chunks)
        self.assertIn("path", chunks[0])
        self.assertIn("category", chunks[0])
        self.assertIn("content", chunks[0])

    def test_vector_index_stores_metadata(self):
        metadata = load_index_metadata("docker")

        self.assertEqual(metadata["topic"], "docker")
        self.assertEqual(metadata["embedding_provider"], "local_hashing")
        self.assertGreater(metadata["chunk_count"], 0)

    def test_embedding_similarity_prefers_related_text(self):
        query = embed_text("Docker daemon is not running")
        related = embed_text("Cannot connect to the Docker daemon")
        unrelated = embed_text("Docker volume cleanup commands")

        self.assertGreater(
            cosine_similarity(query, related),
            cosine_similarity(query, unrelated),
        )

    def test_semantic_retrieval_finds_expected_sources(self):
        cases = load_retrieval_cases()

        for case in cases:
            with self.subTest(query=case["query"]):
                matches = retrieve_semantic_matches(
                    topic="docker",
                    message=case["query"],
                    k=3,
                    preferred_category=case["preferred_category"],
                )

                self.assertTrue(matches)
                self.assertTrue(
                    any(path_contains(match["path"], case["expected_source"]) for match in matches),
                    f"Expected {case['expected_source']} in {[match['path'] for match in matches]}",
                )

    def test_chroma_retrieval_finds_expected_sources(self):
        cases = load_retrieval_cases()

        for case in cases:
            with self.subTest(query=case["query"]):
                matches = retrieve_chroma_matches(
                    topic="docker",
                    message=case["query"],
                    k=3,
                    preferred_category=case["preferred_category"],
                )

                self.assertTrue(matches)
                self.assertTrue(
                    any(path_contains(match["path"], case["expected_source"]) for match in matches),
                    f"Expected {case['expected_source']} in {[match['path'] for match in matches]}",
                )


if __name__ == "__main__":
    unittest.main()
