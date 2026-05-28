from app.services.knowledge_service import retrieve_best_match


TOPIC_KEYWORDS = {
    "docker": ["docker", "container", "image", "dockerfile", "compose", "daemon", "port"],
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


def handle_chat(mode: str, message: str):
    topic = detect_topic(message)

    if topic is None:
        return {
            "error": "I could not detect the topic.",
            "suggestion": "Try asking about Docker, Git, Python, FastAPI, or PyTorch."
        }

    match = retrieve_best_match(topic=topic, message=message)

    if match is None:
        return {
            "error": f"I detected the topic '{topic}', but could not find a specific knowledge chunk.",
            "suggestion": f"Add more markdown files under knowledge/{topic}/"
        }

    return {
        "mode": mode,
        "topic": topic,
        "category": match["category"],
        "source": match["path"],
        "score": match["score"],
        "content": match["content"]
    }