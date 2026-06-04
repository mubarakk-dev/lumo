import unittest
from unittest.mock import Mock, patch

import requests

from app.services.generation_service import generate_grounded_answer


class GenerationServiceTests(unittest.TestCase):
    def test_ollama_provider_returns_model_answer(self):
        matches = [
            {
                "content": "# Docker Daemon Not Running\n\nStart Docker Desktop.",
                "path": "knowledge/docker/troubleshoot/docker_daemon.md",
                "category": "troubleshoot",
                "score": 1.0,
            }
        ]
        sources = [
            {
                "path": "knowledge/docker/troubleshoot/docker_daemon.md",
                "category": "troubleshoot",
                "score": 1.0,
            }
        ]
        mock_response = Mock()
        mock_response.json.return_value = {
            "message": {
                "content": "Start Docker Desktop, then rerun the command. [1]"
            }
        }
        mock_response.raise_for_status.return_value = None

        with patch("app.services.generation_service.requests.post", return_value=mock_response) as mock_post:
            result = generate_grounded_answer(
                message="Docker daemon is not running",
                matches=matches,
                sources=sources,
                intent="troubleshooting",
                generation_provider="ollama",
            )

        self.assertEqual(result["generation_provider"], "ollama")
        self.assertEqual(result["answer_provider"], "ollama")
        self.assertFalse(result["used_fallback"])
        self.assertIn("Start Docker Desktop", result["answer"])
        called_url = mock_post.call_args.args[0]
        called_payload = mock_post.call_args.kwargs["json"]
        self.assertTrue(called_url.endswith("/api/chat"))
        self.assertFalse(called_payload["stream"])
        self.assertEqual(called_payload["model"], "qwen2.5:0.5b")
        self.assertEqual(called_payload["options"]["temperature"], 0.1)
        self.assertEqual(called_payload["options"]["num_ctx"], 1024)
        self.assertEqual(called_payload["options"]["num_predict"], 120)
        self.assertEqual(called_payload["keep_alive"], "5m")

    def test_ollama_provider_falls_back_when_server_is_unavailable(self):
        matches = [
            {
                "content": "# Docker Daemon Not Running\n\nStart Docker Desktop.",
                "path": "knowledge/docker/troubleshoot/docker_daemon.md",
                "category": "troubleshoot",
                "score": 1.0,
            }
        ]
        sources = [
            {
                "path": "knowledge/docker/troubleshoot/docker_daemon.md",
                "category": "troubleshoot",
                "score": 1.0,
            }
        ]

        with patch(
            "app.services.generation_service.requests.post",
            side_effect=requests.ConnectionError("connection refused"),
        ):
            result = generate_grounded_answer(
                message="Docker daemon is not running",
                matches=matches,
                sources=sources,
                intent="troubleshooting",
                generation_provider="ollama",
            )

        self.assertEqual(result["generation_provider"], "ollama")
        self.assertEqual(result["answer_provider"], "extractive")
        self.assertTrue(result["used_fallback"])
        self.assertIn("Ollama is not reachable", result["generation_error"])
        self.assertIn("Start Docker Desktop", result["answer"])

    def test_rejects_unknown_provider(self):
        result = generate_grounded_answer(
            message="Docker daemon is not running",
            matches=[],
            sources=[],
            intent="troubleshooting",
            generation_provider="unknown",
        )

        self.assertIn("Unsupported generation provider", result["error"])


if __name__ == "__main__":
    unittest.main()
