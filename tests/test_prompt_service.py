import unittest

from app.services.prompt_service import build_rag_prompt


class PromptServiceTests(unittest.TestCase):
    def test_prompt_contains_grounding_rules_sources_and_context(self):
        matches = [
            {
                "content": "# Docker Daemon Not Running\n\nOpen Docker Desktop.",
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

        prompt = build_rag_prompt(
            message="Docker daemon is not running",
            matches=matches,
            sources=sources,
            intent="troubleshooting",
        )

        self.assertIn("Answer only from the retrieved context", prompt)
        self.assertIn("Answer in 3 to 5 short bullet points", prompt)
        self.assertIn("Every answer must include at least one citation", prompt)
        self.assertIn("[1] knowledge/docker/troubleshoot/docker_daemon.md", prompt)
        self.assertIn("Open Docker Desktop", prompt)
        self.assertIn("Docker daemon is not running", prompt)


if __name__ == "__main__":
    unittest.main()
