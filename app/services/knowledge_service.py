from pathlib import Path
import re


KNOWLEDGE_DIR = Path("knowledge")


STOP_WORDS = {
    "i", "am", "a", "an", "the", "and", "or", "to", "with", "of",
    "in", "on", "for", "how", "do", "does", "is", "are", "it",
    "my", "me", "got", "get", "working"
}


def clean_words(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9_]+", text.lower())
    return [word for word in words if word not in STOP_WORDS]


def load_markdown_files(topic: str) -> list[dict]:
    topic_dir = KNOWLEDGE_DIR / topic

    if not topic_dir.exists():
        return []

    files = []

    for file_path in topic_dir.rglob("*.md"):
        files.append(
            {
                "path": str(file_path),
                "content": file_path.read_text(encoding="utf-8"),
                "filename": file_path.stem.replace("_", " "),
                "category": file_path.parent.name,
            }
        )

    return files


def score_file(message: str, file_data: dict) -> int:
    query_words = clean_words(message)

    filename = file_data["filename"].lower()
    category = file_data["category"].lower()
    content = file_data["content"].lower()
    path = file_data["path"].lower()

    score = 0

    # Strong phrase matches
    if "daemon not running" in message.lower() and "daemon" in filename:
        score += 100

    if "port" in message.lower() and ("already" in message.lower() or "use" in message.lower()):
        if "port" in filename:
            score += 100

    if "cheat" in message.lower() or "commands" in message.lower():
        if "cheatsheets" in path:
            score += 80

    if "troubleshoot" in message.lower() or "error" in message.lower() or "not running" in message.lower():
        if category == "troubleshoot":
            score += 50

    if "generate" in message.lower() or "write" in message.lower() or "create" in message.lower():
        if category == "generate":
            score += 50

    if "what is" in message.lower() or "explain" in message.lower():
        if category == "learn":
            score += 50

    # Word-level scoring
    for word in query_words:
        if word in filename:
            score += 20
        if word in category:
            score += 10
        if word in content:
            score += 1

    return score


def retrieve_best_match(topic: str, message: str) -> dict | None:
    files = load_markdown_files(topic)

    if not files:
        return None

    scored_files = []

    for file_data in files:
        scored_files.append(
            {
                **file_data,
                "score": score_file(message, file_data),
            }
        )

    scored_files.sort(key=lambda item: item["score"], reverse=True)

    best_match = scored_files[0]

    if best_match["score"] == 0:
        return None

    return best_match