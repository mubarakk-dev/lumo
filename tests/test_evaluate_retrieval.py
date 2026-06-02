import unittest

from scripts.evaluate_retrieval import evaluate_case, load_cases, summarize


class RetrievalEvaluationScriptTests(unittest.TestCase):
    def test_summarize_reports_accuracy_metrics(self):
        results = [
            {"intent_correct": True, "top_1_correct": True, "hit_in_top_k": True},
            {"intent_correct": True, "top_1_correct": False, "hit_in_top_k": True},
        ]

        summary = summarize(results)

        self.assertEqual(summary["cases"], 2)
        self.assertEqual(summary["intent_accuracy"], 1.0)
        self.assertEqual(summary["top_1_accuracy"], 0.5)
        self.assertEqual(summary["hit_rate_at_3"], 1.0)

    def test_keyword_and_semantic_evaluate_same_case_shape(self):
        case = load_cases()[0]

        keyword_result = evaluate_case(case, "keyword")
        semantic_result = evaluate_case(case, "semantic")
        chroma_result = evaluate_case(case, "chroma")

        self.assertEqual(keyword_result["id"], case["id"])
        self.assertEqual(semantic_result["id"], case["id"])
        self.assertEqual(chroma_result["id"], case["id"])
        self.assertIn("returned_sources", keyword_result)
        self.assertIn("returned_sources", semantic_result)
        self.assertIn("returned_sources", chroma_result)


if __name__ == "__main__":
    unittest.main()
