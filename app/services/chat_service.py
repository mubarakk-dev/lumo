from pathlib import Path


KNOWLEDGE_DIR = Path("knowledge")


def load_knowledge(topic: str) -> str | None:
    file_path = KNOWLEDGE_DIR / f"{topic.lower()}.md"

    if not file_path.exists():
        return None

    return file_path.read_text(encoding="utf-8")


def handle_chat(mode: str, message: str):
    topic = message.strip().lower()

    if mode == "learn":
        knowledge = load_knowledge(topic)

        if knowledge is None:
            return {
                "error": f"I don't have knowledge about '{message}' yet.",
                "suggestion": "Add a markdown file for this topic inside the knowledge folder."
            }

        return {
            "mode": "learn",
            "topic": message,
            "source": f"knowledge/{topic}.md",
            "content": knowledge
        }

    return {
        "message": f"Mode '{mode}' is not implemented yet."
    }