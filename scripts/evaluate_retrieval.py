import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.knowledge_service import retrieve_top_matches
from app.services.query_service import detect_query_intent


CASES_PATH = PROJECT_ROOT / "eval" / "retrieval_cases.json"


def normalize_path(path: str) -> str:
    return Path(path).as_posix()


def load_cases() -> list[dict]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def source_matches(actual_path: str, expected_path: str) -> bool:
    return normalize_path(expected_path) in normalize_path(actual_path)


def evaluate_case(case: dict) -> dict:
    query = case["query"]
    matches = retrieve_top_matches(
        topic="docker",
        message=query,
        k=3,
        preferred_category=case.get("preferred_category"),
    )

    returned_sources = [match["path"] for match in matches]
    expected_source = case["expected_source"]
    detected_intent = detect_query_intent(query)

    return {
        "id": case["id"],
        "query": query,
        "expected_intent": case["expected_intent"],
        "detected_intent": detected_intent,
        "expected_source": expected_source,
        "returned_sources": returned_sources,
        "intent_correct": detected_intent == case["expected_intent"],
        "top_1_correct": bool(matches) and source_matches(matches[0]["path"], expected_source),
        "hit_in_top_k": any(source_matches(path, expected_source) for path in returned_sources),
    }


def print_report(results: list[dict]) -> None:
    total = len(results)
    intent_correct = sum(result["intent_correct"] for result in results)
    top_1_correct = sum(result["top_1_correct"] for result in results)
    hits = sum(result["hit_in_top_k"] for result in results)

    print("Retrieval Evaluation")
    print("====================")
    print(f"Cases: {total}")
    print(f"Intent accuracy: {intent_correct}/{total} ({intent_correct / total:.1%})")
    print(f"Top-1 source accuracy: {top_1_correct}/{total} ({top_1_correct / total:.1%})")
    print(f"Hit rate @3: {hits}/{total} ({hits / total:.1%})")
    print()

    failures = [
        result for result in results
        if not result["intent_correct"] or not result["hit_in_top_k"]
    ]

    if not failures:
        print("All evaluation cases passed.")
        return

    print("Failures")
    print("--------")
    for result in failures:
        print(f"- {result['id']}: {result['query']}")
        if not result["intent_correct"]:
            print(
                f"  intent: expected {result['expected_intent']}, "
                f"got {result['detected_intent']}"
            )
        if not result["hit_in_top_k"]:
            print(f"  expected source: {result['expected_source']}")
            print(f"  returned sources: {result['returned_sources']}")


def main() -> int:
    results = [evaluate_case(case) for case in load_cases()]
    print_report(results)

    if all(result["intent_correct"] and result["hit_in_top_k"] for result in results):
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
