from pathlib import Path


KNOWLEDGE_DIR = Path("knowledge")


TOPIC_KEYWORDS = {
    "docker": ["docker", "container", "image", "dockerfile"],
    "git": ["git", "commit", "branch", "merge", "push", "pull"],
    "python": ["python", "pip", "venv", "module", "package"],
    "fastapi": ["fastapi", "api", "endpoint", "uvicorn"],
    "pytorch": ["pytorch", "torch", "tensor", "training loop"],
}


def detect_topic(message: str) -> str | None:
    message_lower = message.lower()

    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                return topic

    return None


def load_knowledge(topic: str) -> str | None:
    file_path = KNOWLEDGE_DIR / f"{topic}.md"

    if not file_path.exists():
        return None

    return file_path.read_text(encoding="utf-8")


def handle_chat(mode: str, message: str):
    topic = detect_topic(message)

    if topic is None:
        return {
            "error": "I could not detect the topic.",
            "suggestion": "Try asking about Docker, Git, Python, FastAPI, or PyTorch."
        }

    knowledge = load_knowledge(topic)

    if knowledge is None:
        return {
            "error": f"I detected the topic '{topic}', but I do not have a knowledge file for it yet.",
            "suggestion": f"Create knowledge/{topic}.md"
        }

    if mode == "learn":
        return {
            "mode": "learn",
            "topic": topic,
            "source": f"knowledge/{topic}.md",
            "content": knowledge
        }

    return {
        "message": f"Mode '{mode}' is not implemented yet.",
        "detected_topic": topic
    }