from app.services.answer_service import build_grounded_answer
from app.services.chroma_retrieval_service import retrieve_chroma_matches
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
    embedding_provider: str = "local_hashing",
    response_mode: str = "answer",
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

    retriever_kwargs = {
        "topic": topic,
        "message": message,
        "k": retrieval_k,
        "preferred_category": preferred_category,
    }

    if retrieval_mode == "chroma":
        retriever_kwargs["embedding_provider"] = embedding_provider

    matches = retriever(**retriever_kwargs)

    if not matches:
        return {
            "error": f"I detected the topic '{topic}', but could not find a specific knowledge chunk.",
            "suggestion": f"Add more markdown files under knowledge/{topic}/"
        }

    sources = build_sources(matches)
    retrieved_content = combine_matches(matches)
    answer = build_grounded_answer(
        message=message,
        matches=matches,
        sources=sources,
        intent=intent,
    )

    content = answer if response_mode == "answer" else retrieved_content

    return {
        "topic": topic,
        "intent": intent,
        "retrieval_mode": retrieval_mode,
        "embedding_provider": embedding_provider if retrieval_mode == "chroma" else None,
        "response_mode": response_mode,
        "top_k": len(matches),
        "sources": sources,
        "answer": answer,
        "retrieved_content": retrieved_content,
        "content": content
    }
