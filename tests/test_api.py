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


if __name__ == "__main__":
    unittest.main()
