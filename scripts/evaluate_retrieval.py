import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.chroma_retrieval_service import retrieve_chroma_matches
from app.services.knowledge_service import retrieve_top_matches
from app.services.query_service import detect_query_intent
from app.services.semantic_retrieval_service import retrieve_semantic_matches


CASES_PATH = PROJECT_ROOT / "eval" / "retrieval_cases.json"


def normalize_path(path: str) -> str:
    return Path(path).as_posix()


def load_cases() -> list[dict]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def source_matches(actual_path: str, expected_path: str) -> bool:
    return normalize_path(expected_path) in normalize_path(actual_path)


RETRIEVERS = {
    "chroma": retrieve_chroma_matches,
    "keyword": retrieve_top_matches,
    "semantic": retrieve_semantic_matches,
}


def evaluate_case(
    case: dict,
    retriever_name: str,
    embedding_provider: str = "local_hashing",
) -> dict:
    query = case["query"]
    retriever = RETRIEVERS[retriever_name]
    retriever_kwargs = {
        "topic": "docker",
        "message": query,
        "k": 3,
        "preferred_category": case.get("preferred_category"),
    }

    if retriever_name == "chroma":
        retriever_kwargs["embedding_provider"] = embedding_provider

    matches = retriever(**retriever_kwargs)

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
        "retriever": retriever_name,
        "intent_correct": detected_intent == case["expected_intent"],
        "top_1_correct": bool(matches) and source_matches(matches[0]["path"], expected_source),
        "hit_in_top_k": any(source_matches(path, expected_source) for path in returned_sources),
    }


def print_report(results: list[dict], retriever_name: str) -> None:
    total = len(results)
    intent_correct = sum(result["intent_correct"] for result in results)
    top_1_correct = sum(result["top_1_correct"] for result in results)
    hits = sum(result["hit_in_top_k"] for result in results)

    print(f"Retrieval Evaluation: {retriever_name}")
    print("=" * (22 + len(retriever_name)))
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


def summarize(results: list[dict]) -> dict:
    total = len(results)
    intent_correct = sum(result["intent_correct"] for result in results)
    top_1_correct = sum(result["top_1_correct"] for result in results)
    hits = sum(result["hit_in_top_k"] for result in results)

    return {
        "cases": total,
        "intent_accuracy": intent_correct / total,
        "top_1_accuracy": top_1_correct / total,
        "hit_rate_at_3": hits / total,
    }


def print_comparison_report(cases: list[dict], embedding_provider: str) -> None:
    keyword_results = [evaluate_case(case, "keyword") for case in cases]
    semantic_results = [evaluate_case(case, "semantic") for case in cases]
    chroma_results = [
        evaluate_case(case, "chroma", embedding_provider=embedding_provider)
        for case in cases
    ]
    keyword_summary = summarize(keyword_results)
    semantic_summary = summarize(semantic_results)
    chroma_summary = summarize(chroma_results)

    print("Retrieval Comparison")
    print("====================")
    print("Metric               Keyword   Semantic  Chroma")
    print("-----------------------------------------------")
    print(
        f"Intent accuracy      {keyword_summary['intent_accuracy']:.1%}    "
        f"{semantic_summary['intent_accuracy']:.1%}    "
        f"{chroma_summary['intent_accuracy']:.1%}"
    )
    print(
        f"Top-1 accuracy       {keyword_summary['top_1_accuracy']:.1%}    "
        f"{semantic_summary['top_1_accuracy']:.1%}    "
        f"{chroma_summary['top_1_accuracy']:.1%}"
    )
    print(
        f"Hit rate @3          {keyword_summary['hit_rate_at_3']:.1%}    "
        f"{semantic_summary['hit_rate_at_3']:.1%}    "
        f"{chroma_summary['hit_rate_at_3']:.1%}"
    )
    print()

    regressions = []
    for keyword_result, semantic_result, chroma_result in zip(
        keyword_results,
        semantic_results,
        chroma_results,
    ):
        if keyword_result["hit_in_top_k"] and not semantic_result["hit_in_top_k"]:
            regressions.append(semantic_result)
        if keyword_result["hit_in_top_k"] and not chroma_result["hit_in_top_k"]:
            regressions.append(chroma_result)

    if not regressions:
        print("No semantic regressions against the keyword baseline.")
        return

    print("Semantic Regressions")
    print("--------------------")
    for result in regressions:
        print(f"- {result['id']}: expected {result['expected_source']}")
        print(f"  returned sources: {result['returned_sources']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate Lumo retrieval quality.")
    parser.add_argument(
        "--retriever",
        choices=sorted(RETRIEVERS),
        default="keyword",
        help="Retrieval strategy to evaluate.",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare keyword and semantic retrieval side by side.",
    )
    parser.add_argument(
        "--embedding-provider",
        choices=["local_hashing", "sentence_transformers"],
        default="local_hashing",
        help="Embedding provider to use when evaluating the Chroma retriever.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cases = load_cases()

    if args.compare:
        print_comparison_report(cases, embedding_provider=args.embedding_provider)
        return 0

    results = [
        evaluate_case(
            case,
            args.retriever,
            embedding_provider=args.embedding_provider,
        )
        for case in cases
    ]
    print_report(results, args.retriever)

    if all(result["intent_correct"] and result["hit_in_top_k"] for result in results):
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
