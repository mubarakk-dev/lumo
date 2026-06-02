import unittest
import warnings

warnings.filterwarnings(
    "ignore",
    message="Using `httpx` with `starlette.testclient` is deprecated.*",
)
from fastapi.testclient import TestClient

from app.main import app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})

    def test_chat_endpoint_returns_retrieved_docker_content(self):
        response = self.client.post(
            "/chat",
            json={"message": "Docker daemon is not running"},
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["topic"], "docker")
        self.assertEqual(data["intent"], "troubleshooting")
        self.assertIn("Docker Daemon Not Running", data["content"])
        self.assertTrue(data["sources"])

    def test_chat_endpoint_supports_semantic_retrieval(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "Docker daemon is not running",
                "retrieval_mode": "semantic",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["retrieval_mode"], "semantic")
        self.assertEqual(data["intent"], "troubleshooting")
        self.assertTrue(data["sources"])

    def test_chat_endpoint_supports_chroma_retrieval(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "Docker daemon is not running",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["retrieval_mode"], "chroma")
        self.assertEqual(data["embedding_provider"], "local_hashing")
        self.assertEqual(data["intent"], "troubleshooting")
        self.assertTrue(data["sources"])

    def test_chat_endpoint_rejects_unknown_retrieval_mode(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "Docker daemon is not running",
                "retrieval_mode": "unknown",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Unsupported retrieval mode", data["error"])


if __name__ == "__main__":
    unittest.main()
