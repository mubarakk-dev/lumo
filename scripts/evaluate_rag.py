import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.chat_service import handle_chat
from scripts.evaluate_retrieval import source_matches


CASES_PATH = PROJECT_ROOT / "eval" / "rag_cases.json"
UNSUPPORTED_PHRASES = [
    "i don't know",
    "i do not know",
    "not enough",
    "could not find",
    "cannot answer",
]
CITATION_PATTERN = re.compile(r"\[\d+\]")


def load_cases() -> list[dict]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def contains_all_terms(answer: str, required_terms: list[str]) -> bool:
    answer_lower = answer.lower()
    return all(term.lower() in answer_lower for term in required_terms)


def contains_required_citations(answer: str, required_citations: list[str]) -> bool:
    if required_citations:
        return all(citation in answer for citation in required_citations)

    return bool(CITATION_PATTERN.search(answer))


def avoids_unsupported_phrases(answer: str) -> bool:
    answer_lower = answer.lower()
    return not any(phrase in answer_lower for phrase in UNSUPPORTED_PHRASES)


def evaluate_case(case: dict) -> dict:
    response = handle_chat(
        message=case["query"],
        retrieval_mode=case.get("retrieval_mode", "chroma"),
        embedding_provider=case.get("embedding_provider", "local_hashing"),
        response_mode="answer",
        generation_provider=case.get("generation_provider", "extractive"),
    )
    answer = response.get("answer", "")
    returned_sources = [
        source["path"]
        for source in response.get("sources", [])
    ]
    expected_source = case["expected_source"]
    source_hit = any(source_matches(path, expected_source) for path in returned_sources)
    terms_present = contains_all_terms(answer, case.get("required_terms", []))
    citations_present = contains_required_citations(
        answer,
        case.get("required_citations", []),
    )
    no_unsupported_phrases = avoids_unsupported_phrases(answer)

    return {
        "id": case["id"],
        "query": case["query"],
        "expected_source": expected_source,
        "returned_sources": returned_sources,
        "generation_provider": response.get("generation_provider"),
        "answer_provider": response.get("answer_provider"),
        "used_fallback": response.get("used_fallback", False),
        "source_hit": source_hit,
        "terms_present": terms_present,
        "citations_present": citations_present,
        "no_unsupported_phrases": no_unsupported_phrases,
        "passed": (
            source_hit
            and terms_present
            and citations_present
            and no_unsupported_phrases
        ),
    }


def summarize(results: list[dict]) -> dict:
    total = len(results)
    source_hits = sum(result["source_hit"] for result in results)
    terms_present = sum(result["terms_present"] for result in results)
    citations_present = sum(result["citations_present"] for result in results)
    no_unsupported_phrases = sum(result["no_unsupported_phrases"] for result in results)
    passed = sum(result["passed"] for result in results)

    return {
        "cases": total,
        "source_hit_rate": source_hits / total,
        "required_terms_rate": terms_present / total,
        "citation_rate": citations_present / total,
        "grounded_response_rate": no_unsupported_phrases / total,
        "pass_rate": passed / total,
    }


def print_report(results: list[dict]) -> None:
    summary = summarize(results)

    print("RAG Answer Evaluation")
    print("=====================")
    print(f"Cases: {summary['cases']}")
    print(f"Expected source hit rate: {summary['source_hit_rate']:.1%}")
    print(f"Required terms rate: {summary['required_terms_rate']:.1%}")
    print(f"Citation rate: {summary['citation_rate']:.1%}")
    print(f"Grounded response rate: {summary['grounded_response_rate']:.1%}")
    print(f"Overall pass rate: {summary['pass_rate']:.1%}")
    print()

    failures = [result for result in results if not result["passed"]]

    if not failures:
        print("All RAG answer evaluation cases passed.")
        return

    print("Failures")
    print("--------")
    for result in failures:
        print(f"- {result['id']}: {result['query']}")
        if not result["source_hit"]:
            print(f"  expected source: {result['expected_source']}")
            print(f"  returned sources: {result['returned_sources']}")
        if not result["terms_present"]:
            print("  required terms were missing")
        if not result["citations_present"]:
            print("  required citations were missing")
        if not result["no_unsupported_phrases"]:
            print("  answer contained an unsupported-response phrase")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate Lumo RAG answer quality.")
    parser.add_argument(
        "--case-id",
        help="Run one RAG evaluation case by id.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cases = load_cases()

    if args.case_id:
        cases = [case for case in cases if case["id"] == args.case_id]

    if not cases:
        print("No RAG evaluation cases matched.")
        return 1

    results = [evaluate_case(case) for case in cases]
    print_report(results)

    if all(result["passed"] for result in results):
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
