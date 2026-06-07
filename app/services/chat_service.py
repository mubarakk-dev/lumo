from pathlib import Path

from app.services.chroma_retrieval_service import retrieve_chroma_matches
from app.services.generation_service import (
    SUPPORTED_GENERATION_PROVIDERS,
    generate_grounded_answer,
)
from app.services.knowledge_service import retrieve_top_matches
from app.services.query_service import detect_query_intent, get_retrieval_k
from app.services.semantic_retrieval_service import retrieve_semantic_matches


TOPIC_KEYWORDS = {
    "docker": [
        "docker",
        "container",
        "containers",
        "image",
        "images",
        "dockerfile",
        "compose",
        "daemon",
        "port",
        "ports",
        "volume",
        "volumes",
        "network",
        "networks",
        "env",
        ".env",
        "environment",
        "environment variable",
        "environment variables",
        "nginx",
        "attach",
        "build",
        "builds",
        "cache",
        "command",
        "commands",
        "copy",
        "cpu",
        "debug",
        "debugging",
        "deploy",
        "deployment",
        "devcontainer",
        "digest",
        "entrypoint",
        "exec",
        "exit",
        "exited",
        "exits",
        "expose",
        "health",
        "healthcheck",
        "host",
        "inspect",
        "inspection",
        "layer",
        "layers",
        "limit",
        "limits",
        "log",
        "logs",
        "memory",
        "mount",
        "mounts",
        "prune",
        "pull",
        "push",
        "registry",
        "restart",
        "restarts",
        "shell",
        "stats",
        "status",
        "stop",
        "stopped",
        "tag",
        "terminal",
        "troubleshoot",
        "troubleshooting",
    ],
}


INTENT_TO_CATEGORY = {
    "definition": "learn",
    "comparison": "learn",
    "generation": "generate",
    "troubleshooting": "troubleshoot",
    "cheatsheet": "cheatsheets",
}


RETRIEVERS = {
    "chroma": retrieve_chroma_matches,
    "keyword": retrieve_top_matches,
    "semantic": retrieve_semantic_matches,
}


def detect_topic(message: str) -> str | None:
    message_lower = message.lower()

    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in message_lower for keyword in keywords):
            return topic

    return None


def combine_matches(matches: list[dict]) -> str:
    return "\n\n".join(match["content"] for match in matches).strip()


def expand_matches_from_sources(matches: list[dict]) -> list[dict]:
    expanded_matches = []
    seen_paths = set()

    for match in matches:
        if match["path"] in seen_paths:
            continue

        seen_paths.add(match["path"])
        source_path = Path(match["path"])

        if not source_path.exists():
            expanded_matches.append(match)
            continue

        expanded_matches.append(
            {
                **match,
                "content": source_path.read_text(encoding="utf-8"),
                "expanded_from_source": True,
            }
        )

    return expanded_matches


def build_sources(matches: list[dict]) -> list[dict]:
    sources = []
    seen_paths = set()

    for match in matches:
        if match["path"] in seen_paths:
            continue

        seen_paths.add(match["path"])
        sources.append(
            {
                "path": match["path"],
                "category": match["category"],
                "score": match["score"],
            }
        )

    return sources


def handle_chat(
    message: str,
    retrieval_mode: str = "keyword",
    embedding_provider: str = "sentence_transformers",
    response_mode: str = "answer",
    generation_provider: str = "extractive",
):
    topic = detect_topic(message)

    if topic is None:
        return {
            "error": "I could not detect the topic.",
            "suggestion": "Try asking about Docker, containers, images, Docker Compose, ports, volumes, or networking."
        }

    intent = detect_query_intent(message)
    retrieval_k = get_retrieval_k(intent)
    preferred_category = INTENT_TO_CATEGORY.get(intent)
    retriever = RETRIEVERS.get(retrieval_mode)

    if retriever is None:
        return {
            "error": f"Unsupported retrieval mode '{retrieval_mode}'.",
            "suggestion": "Use 'keyword', 'semantic', or 'chroma'."
        }

    if response_mode not in {"answer", "retrieval"}:
        return {
            "error": f"Unsupported response mode '{response_mode}'.",
            "suggestion": "Use 'answer' or 'retrieval'."
        }

    if generation_provider not in SUPPORTED_GENERATION_PROVIDERS:
        return {
            "error": f"Unsupported generation provider '{generation_provider}'.",
            "suggestion": "Use 'extractive' or 'ollama'."
        }

    retriever_kwargs = {
        "topic": topic,
        "message": message,
        "k": retrieval_k,
        "preferred_category": preferred_category,
    }

    if retrieval_mode == "chroma":
        retriever_kwargs["embedding_provider"] = embedding_provider

    matches = expand_matches_from_sources(retriever(**retriever_kwargs))

    if not matches:
        return {
            "error": f"I detected the topic '{topic}', but could not find a specific knowledge chunk.",
            "suggestion": f"Add more markdown files under knowledge/{topic}/"
        }

    sources = build_sources(matches)
    retrieved_content = combine_matches(matches)
    generation_result = generate_grounded_answer(
        message=message,
        matches=matches,
        sources=sources,
        intent=intent,
        generation_provider=generation_provider,
    )

    if "error" in generation_result:
        return generation_result

    answer = generation_result["answer"]
    content = answer if response_mode == "answer" else retrieved_content

    response = {
        "topic": topic,
        "intent": intent,
        "retrieval_mode": retrieval_mode,
        "embedding_provider": embedding_provider if retrieval_mode == "chroma" else None,
        "response_mode": response_mode,
        "generation_provider": generation_result["generation_provider"],
        "answer_provider": generation_result["answer_provider"],
        "used_fallback": generation_result["used_fallback"],
        "top_k": len(matches),
        "sources": sources,
        "answer": answer,
        "retrieved_content": retrieved_content,
        "content": content
    }

    for key in ("generation_error", "model"):
        if key in generation_result:
            response[key] = generation_result[key]

    return response
