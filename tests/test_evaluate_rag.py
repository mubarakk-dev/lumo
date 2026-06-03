import unittest

from scripts.evaluate_rag import (
    avoids_unsupported_phrases,
    contains_all_terms,
    contains_required_citations,
    evaluate_case,
    load_cases,
    summarize,
)


class RagEvaluationScriptTests(unittest.TestCase):
    def test_contains_all_terms_is_case_insensitive(self):
        answer = "Docker Desktop starts the Docker service."

        self.assertTrue(contains_all_terms(answer, ["docker desktop", "SERVICE"]))
        self.assertFalse(contains_all_terms(answer, ["docker desktop", "compose"]))

    def test_contains_required_citations_checks_expected_labels(self):
        answer = "Start Docker Desktop. [1]"

        self.assertTrue(contains_required_citations(answer, ["[1]"]))
        self.assertFalse(contains_required_citations(answer, ["[2]"]))

    def test_avoids_unsupported_phrases(self):
        self.assertTrue(avoids_unsupported_phrases("Start Docker Desktop. [1]"))
        self.assertFalse(avoids_unsupported_phrases("I do not know from the context."))

    def test_summarize_reports_answer_quality_metrics(self):
        results = [
            {
                "source_hit": True,
                "terms_present": True,
                "citations_present": True,
                "no_unsupported_phrases": True,
                "passed": True,
            },
            {
                "source_hit": True,
                "terms_present": False,
                "citations_present": True,
                "no_unsupported_phrases": True,
                "passed": False,
            },
        ]

        summary = summarize(results)

        self.assertEqual(summary["cases"], 2)
        self.assertEqual(summary["source_hit_rate"], 1.0)
        self.assertEqual(summary["required_terms_rate"], 0.5)
        self.assertEqual(summary["citation_rate"], 1.0)
        self.assertEqual(summary["grounded_response_rate"], 1.0)
        self.assertEqual(summary["pass_rate"], 0.5)

    def test_evaluate_case_returns_expected_shape(self):
        result = evaluate_case(load_cases()[0])

        self.assertIn("source_hit", result)
        self.assertIn("terms_present", result)
        self.assertIn("citations_present", result)
        self.assertIn("passed", result)


if __name__ == "__main__":
    unittest.main()
