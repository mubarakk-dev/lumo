import unittest
import warnings
from unittest.mock import patch

import requests

warnings.filterwarnings(
    "ignore",
    message="Using `httpx` with `starlette.testclient` is deprecated.*",
)
from fastapi.testclient import TestClient

from app.main import app
from app.services.chat_service import detect_topic


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
        self.assertEqual(data["response_mode"], "answer")
        self.assertIn("[1]", data["answer"])
        self.assertIn("Docker Desktop", data["answer"])
        self.assertIn("Docker Daemon Not Running", data["retrieved_content"])
        self.assertTrue(data["sources"])

    def test_detects_docker_topic_from_operational_terms(self):
        operational_messages = [
            "how to inspect logs",
            "show container stats",
            "exec into a shell",
            "why is the service restarting",
            "how do I prune old images",
        ]

        for message in operational_messages:
            with self.subTest(message=message):
                self.assertEqual(detect_topic(message), "docker")

    def test_chat_endpoint_handles_operational_docker_question_without_explicit_docker_word(self):
        response = self.client.post(
            "/chat",
            json={"message": "how to inspect logs"},
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["topic"], "docker")
        self.assertTrue(data["sources"])
        self.assertNotIn("error", data)

    def test_chat_endpoint_expands_chroma_chunks_for_answers(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "What is Docker?",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("package applications", data["answer"])
        self.assertIn("containers", data["answer"])

    def test_chroma_retrieval_routes_docker_image_definition(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "What is a Docker image?",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["intent"], "definition")
        self.assertEqual(data["embedding_provider"], "sentence_transformers")
        self.assertIn("images_vs_containers.md", data["sources"][0]["path"])
        self.assertIn("read-only template", data["answer"])

    def test_chroma_retrieval_routes_docker_container_definition(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "What is a Docker container?",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["intent"], "definition")
        self.assertEqual(data["embedding_provider"], "sentence_transformers")
        self.assertIn("images_vs_containers.md", data["sources"][0]["path"])
        self.assertIn("running instance", data["answer"])

    def test_chat_endpoint_supports_retrieval_response_mode(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "Docker daemon is not running",
                "response_mode": "retrieval",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["response_mode"], "retrieval")
        self.assertEqual(data["content"], data["retrieved_content"])
        self.assertIn("Docker Daemon Not Running", data["content"])

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
        self.assertEqual(data["embedding_provider"], "sentence_transformers")
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

    def test_chat_endpoint_rejects_unknown_response_mode(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "Docker daemon is not running",
                "response_mode": "unknown",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Unsupported response mode", data["error"])

    def test_chat_endpoint_rejects_unknown_generation_provider(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "Docker daemon is not running",
                "generation_provider": "unknown",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Unsupported generation provider", data["error"])

    def test_chat_endpoint_falls_back_when_ollama_is_unavailable(self):
        with patch(
            "app.services.generation_service.requests.post",
            side_effect=requests.ConnectionError("connection refused"),
        ):
            response = self.client.post(
                "/chat",
                json={
                    "message": "Docker daemon is not running",
                    "generation_provider": "ollama",
                },
            )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["generation_provider"], "ollama")
        self.assertEqual(data["answer_provider"], "extractive")
        self.assertTrue(data["used_fallback"])
        self.assertIn("Ollama is not reachable", data["generation_error"])


if __name__ == "__main__":
    unittest.main()
