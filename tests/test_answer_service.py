import unittest

from app.services.answer_service import build_grounded_answer


class AnswerServiceTests(unittest.TestCase):
    def test_builds_grounded_answer_with_sources(self):
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

        self.assertIn("grounded troubleshooting answer", answer)
        self.assertIn("Docker service is not running", answer)
        self.assertIn("Sources:", answer)
        self.assertIn("knowledge/docker/troubleshoot/docker_daemon.md", answer)

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
