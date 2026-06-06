import unittest

from app.services.answer_service import build_grounded_answer


class AnswerServiceTests(unittest.TestCase):
    def test_builds_clean_grounded_answer_with_citation(self):
        matches = [
            {
                "content": "# Docker Daemon Not Running\n\n## Problem\nDocker service is not running.\n\n## Fix\nOpen Docker Desktop.",
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

        answer = build_grounded_answer(
            message="Docker daemon is not running",
            matches=matches,
            sources=sources,
            intent="troubleshooting",
        )

        self.assertTrue(answer.startswith("[1] Docker service is not running"))
        self.assertIn("Docker service is not running", answer)
        self.assertIn("Open Docker Desktop", answer)
        self.assertNotIn("Docker Daemon Not Running", answer)
        self.assertNotIn("Problem", answer)
        self.assertNotIn("Sources:", answer)

    def test_removes_related_questions_from_answer(self):
        matches = [
            {
                "content": (
                    "# What is a Dockerfile?\n\n"
                    "A Dockerfile is a text file that contains instructions for building a Docker image.\n\n"
                    "## Related Questions\n\n"
                    "- What is a Dockerfile?\n"
                    "- Explain Dockerfile."
                ),
                "path": "knowledge/docker/learn/what_is_dockerfile.md",
                "category": "learn",
                "score": 1.0,
            }
        ]
        sources = [
            {
                "path": "knowledge/docker/learn/what_is_dockerfile.md",
                "category": "learn",
                "score": 1.0,
            }
        ]

        answer = build_grounded_answer(
            message="What is a Dockerfile?",
            matches=matches,
            sources=sources,
            intent="definition",
        )

        self.assertIn("A Dockerfile is a text file", answer)
        self.assertNotIn("Related Questions", answer)
        self.assertNotIn("Explain Dockerfile", answer)

    def test_returns_safe_message_without_matches(self):
        answer = build_grounded_answer(
            message="Unknown Docker issue",
            matches=[],
            sources=[],
            intent="general",
        )

        self.assertIn("could not find enough grounded", answer)

    def test_does_not_repeat_duplicate_source_matches(self):
        matches = [
            {
                "content": "# Docker Daemon Not Running\n\n## Problem\nDocker service is not running.",
                "path": "knowledge/docker/troubleshoot/docker_daemon.md",
                "category": "troubleshoot",
                "score": 1.0,
            },
            {
                "content": "# Docker Daemon Not Running\n\n## Problem\nDocker service is not running.",
                "path": "knowledge/docker/troubleshoot/docker_daemon.md",
                "category": "troubleshoot",
                "score": 0.9,
            },
        ]
        sources = [
            {
                "path": "knowledge/docker/troubleshoot/docker_daemon.md",
                "category": "troubleshoot",
                "score": 1.0,
            }
        ]

        answer = build_grounded_answer(
            message="Docker daemon is not running",
            matches=matches,
            sources=sources,
            intent="troubleshooting",
        )

        self.assertEqual(answer.count("Docker service is not running"), 1)


if __name__ == "__main__":
    unittest.main()
