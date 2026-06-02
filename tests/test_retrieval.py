import json
import unittest
from pathlib import Path

from app.services.chat_service import handle_chat
from app.services.knowledge_service import retrieve_top_matches
from app.services.query_service import detect_query_intent


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RETRIEVAL_CASES_PATH = PROJECT_ROOT / "eval" / "retrieval_cases.json"


def load_retrieval_cases() -> list[dict]:
    return json.loads(RETRIEVAL_CASES_PATH.read_text(encoding="utf-8"))


def path_contains(source_path: str, expected_path: str) -> bool:
    normalized_source = Path(source_path).as_posix()
    normalized_expected = expected_path.replace("\\", "/")
    return normalized_expected in normalized_source


class IntentDetectionTests(unittest.TestCase):
    def test_detects_core_intents(self):
        cases = load_retrieval_cases()

        for case in cases:
            with self.subTest(message=case["query"]):
                self.assertEqual(detect_query_intent(case["query"]), case["expected_intent"])


class RetrievalTests(unittest.TestCase):
    def test_retrieves_expected_sources_for_representative_queries(self):
        cases = load_retrieval_cases()

        for case in cases:
            with self.subTest(message=case["query"]):
                matches = retrieve_top_matches(
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

    def test_chat_response_includes_sources_and_content(self):
        response = handle_chat("Docker daemon is not running")

        self.assertEqual(response["topic"], "docker")
        self.assertEqual(response["intent"], "troubleshooting")
        self.assertEqual(response["retrieval_mode"], "keyword")
        self.assertGreaterEqual(response["top_k"], 1)
        self.assertIn("Docker Daemon Not Running", response["content"])
        self.assertTrue(
            any(
                path_contains(source["path"], "knowledge/docker/troubleshoot/docker_daemon.md")
                for source in response["sources"]
            )
        )


if __name__ == "__main__":
    unittest.main()
