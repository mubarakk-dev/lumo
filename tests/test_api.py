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
            "what is a yaml file",
            "what is a .yaml file",
            "what is a .yml file",
            "what is a yml file",
            "give me a template for a yaml file",
            "give me a template for a .yml file",
            "no space left on device",
            "how do I copy a file into a container",
            "what is a virtual machine",
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

    def test_chroma_retrieval_routes_plain_container_definition(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "What is a container?",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["intent"], "definition")
        self.assertIn("images_vs_containers.md", data["sources"][0]["path"])
        self.assertIn("running instance", data["answer"])
        self.assertNotIn("List running containers", data["answer"])

    def test_chroma_retrieval_routes_yaml_definition(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "What is a YAML file?",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["intent"], "definition")
        self.assertIn("what_is_yaml.md", data["sources"][0]["path"])
        self.assertIn("human-readable configuration format", data["answer"])

    def test_chroma_retrieval_routes_yaml_extension_definition(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "What is a .yml file?",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["intent"], "definition")
        self.assertIn("what_is_yaml.md", data["sources"][0]["path"])

    def test_chroma_retrieval_routes_yaml_template_generation(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "Give me a template for a YAML file",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["intent"], "generation")
        self.assertIn("docker_compose.md", data["sources"][0]["path"])
        self.assertIn("services:", data["answer"])

    def test_chroma_retrieval_routes_yaml_extension_template_generation(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "Give me a template for a .yaml file",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["intent"], "generation")
        self.assertIn("docker_compose.md", data["sources"][0]["path"])
        self.assertIn("services:", data["answer"])

    def test_chroma_retrieval_routes_no_space_left_to_pruning_fix(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "No space left on device",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["intent"], "troubleshooting")
        self.assertIn("no_space_left.md", data["sources"][0]["path"])
        self.assertIn("**Problem**", data["answer"])
        self.assertIn("**Cause**", data["answer"])
        self.assertIn("**Fix**", data["answer"])
        self.assertIn("docker system prune", data["answer"])

    def test_chroma_retrieval_routes_compose_dockerfile_comparison(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "What is the difference between Dockerfile and Docker Compose?",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["intent"], "comparison")
        self.assertIn("docker_compose_vs_dockerfile.md", data["sources"][0]["path"])
        self.assertIn("Dockerfile builds an image", data["answer"])

    def test_chroma_retrieval_routes_inside_running_container_to_exec(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "How do I see what is happening inside a running container?",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["intent"], "generation")
        self.assertIn("exec_into_container.md", data["sources"][0]["path"])
        self.assertIn("docker exec", data["answer"])

    def test_chroma_retrieval_routes_copy_file_to_docker_cp(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "How do I copy a file from my local machine into a running container?",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["intent"], "generation")
        self.assertIn("copy_files.md", data["sources"][0]["path"])
        self.assertIn("docker cp", data["answer"])
        self.assertNotIn("Dockerfile is a text file", data["answer"])

    def test_chroma_retrieval_preserves_dockerfile_template_code_block(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "Can you write a Dockerfile for an app using a multi-stage build",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("dockerfile_template.md", data["sources"][0]["path"])
        self.assertIn("```dockerfile", data["answer"])
        self.assertIn("FROM python:3.11-slim", data["answer"])

    def test_chroma_retrieval_routes_virtual_machine_definition(self):
        response = self.client.post(
            "/chat",
            json={
                "message": "What is a virtual machine?",
                "retrieval_mode": "chroma",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["intent"], "definition")
        self.assertIn("virtual_machines.md", data["sources"][0]["path"])
        self.assertIn("software-based computer", data["answer"])

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
