from app.services.knowledge_service import retrieve_top_matches
from app.services.query_service import detect_query_intent, get_retrieval_k


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


def detect_topic(message: str) -> str | None:
    message_lower = message.lower()

    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in message_lower for keyword in keywords):
            return topic

    return None


def combine_matches(matches: list[dict]) -> str:
    combined_content = ""

    for match in matches:
        combined_content += f"""

{match["content"]}

"""

    return combined_content.strip()


def handle_chat(message: str):
    topic = detect_topic(message)

    if topic is None:
        return {
            "error": "I could not detect the topic.",
            "suggestion": "Try asking about Docker, containers, images, Docker Compose, ports, volumes, or networking."
        }

    intent = detect_query_intent(message)
    retrieval_k = get_retrieval_k(intent)
    preferred_category = INTENT_TO_CATEGORY.get(intent)

    print(f"Intent: {intent}")
    print(f"Preferred category: {preferred_category}")
    
    matches = retrieve_top_matches(
        topic=topic,
        message=message,
        k=retrieval_k,
        preferred_category=preferred_category,
    )

    if not matches:
        return {
            "error": f"I detected the topic '{topic}', but could not find a specific knowledge chunk.",
            "suggestion": f"Add more markdown files under knowledge/{topic}/"
        }

    return {
        "topic": topic,
        "intent": intent,
        "top_k": len(matches),
        "sources": [
            {
                "path": match["path"],
                "category": match["category"],
                "score": match["score"],
            }
            for match in matches
        ],
        "content": combine_matches(matches)
    }

    if not matches:
        return {
            "error": f"I detected the topic '{topic}', but could not find a specific knowledge chunk.",
            "suggestion": f"Add more markdown files under knowledge/{topic}/"
        }

    return {
        "topic": topic,
        "intent": intent,
        "top_k": len(matches),
        "sources": [
            {
                "path": match["path"],
                "category": match["category"],
                "score": match["score"],
            }
            for match in matches
        ],
        "content": combine_matches(matches)
    }