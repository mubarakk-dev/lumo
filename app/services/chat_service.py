from app.services.knowledge_service import retrieve_top_matches


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
        "nginx",
    ],
    "git": ["git", "commit", "branch", "merge", "push", "pull"],
    "python": ["python", "pip", "venv", "module", "package", "error"],
    "fastapi": ["fastapi", "api", "endpoint", "uvicorn"],
    "pytorch": ["pytorch", "torch", "tensor", "training loop"],
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
            "suggestion": "Try asking about Docker."
        }

    matches = retrieve_top_matches(
        topic=topic,
        message=message,
        k=3
    )

    if not matches:
        return {
            "error": f"I detected the topic '{topic}', but could not find a specific knowledge chunk.",
            "suggestion": f"Add more markdown files under knowledge/{topic}/"
        }

    return {
        "topic": topic,
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