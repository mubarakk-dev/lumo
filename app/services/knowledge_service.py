from pathlib import Path
import re


KNOWLEDGE_DIR = Path("knowledge")


STOP_WORDS = {
    "i", "am", "a", "an", "the", "and", "or", "to", "with", "of",
    "in", "on", "for", "how", "do", "does", "is", "are", "it",
    "my", "me", "got", "get", "working", "please", "can", "you",
    "why", "each", "other"
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
    message_lower = message.lower()
    query_words = clean_words(message)

    filename = file_data["filename"].lower()
    category = file_data["category"].lower()
    content = file_data["content"].lower()
    path = file_data["path"].lower()

    score = 0

    # Strong phrase / meaning boosts

    if "daemon not running" in message_lower and "daemon" in filename:
        score += 120

    if "cannot connect to docker daemon" in message_lower and "daemon" in filename:
        score += 120

    if (
        "communicate" in message_lower
        or "talk to each other" in message_lower
        or "connect to each other" in message_lower
        or "reach each other" in message_lower
        or "cannot connect" in message_lower
        or "can't connect" in message_lower
    ):
        if "network" in filename or "network" in content:
            score += 120

    if (
        "browser" in message_lower
        or "website" in message_lower
        or "localhost" in message_lower
        or "not accessible" in message_lower
        or "cannot access" in message_lower
        or "can't access" in message_lower
        or "does not load" in message_lower
        or "not load" in message_lower
    ):
        if "reachable" in filename or "not reachable" in filename:
            score += 140

    if "port mapping" in message_lower and "port mapping" in filename:
        score += 120

    if "port" in message_lower and (
        "already" in message_lower
        or "use" in message_lower
        or "allocated" in message_lower
    ):
        if "port already" in filename or "port" in filename:
            score += 120

    if "expose" in message_lower:
        if "port" in filename:
            score += 100

    if "volume" in message_lower or "volumes" in message_lower:
        if "volume" in filename:
            score += 120

    if "cpu" in message_lower and ("limit" in message_lower or "limits" in message_lower):
        if "resource" in filename or "limit" in filename:
            score += 120

    if "memory" in message_lower and ("limit" in message_lower or "limits" in message_lower):
        if "resource" in filename or "limit" in filename:
            score += 120

    if "logs" in message_lower or "log" in message_lower:
        if "logs" in filename:
            score += 120

    if "cleanup" in message_lower or "clean up" in message_lower or "prune" in message_lower:
        if "cleanup" in filename:
            score += 120

    if (
        "docker hub" in message_lower
        or "push image" in message_lower
        or "push an image" in message_lower
        or "registry" in message_lower
    ):
        if "registry" in filename:
            score += 120

    if "exec" in message_lower or "enter" in message_lower or "inside container" in message_lower:
        if "exec" in filename:
            score += 120

    if "permission denied" in message_lower:
        if "permission" in filename:
            score += 120

    if "exits immediately" in message_lower or "container exits" in message_lower:
        if "exits" in filename:
            score += 120

    if "inspect" in message_lower or "stats" in message_lower or "monitor" in message_lower:
        if "inspection" in filename:
            score += 120

    if "dockerfile" in message_lower or "copy" in message_lower or "cmd" in message_lower:
        if "dockerfile" in filename:
            score += 120

    if "best practices" in message_lower or "secure" in message_lower or "security" in message_lower:
        if "best practices" in filename:
            score += 120

    if "multi stage" in message_lower or "multi-stage" in message_lower:
        if "multi stage" in filename:
            score += 120

    if "build failing" in message_lower or "build fails" in message_lower or "build keeps failing" in message_lower:
        if "build failures" in filename:
            score += 120

    # Category boosts

    if "cheat" in message_lower or "cheatsheet" in message_lower or "commands" in message_lower:
        if category == "cheatsheets":
            score += 80

    if "troubleshoot" in message_lower or "error" in message_lower or "not running" in message_lower:
        if category == "troubleshoot":
            score += 60

    if "generate" in message_lower or "write" in message_lower or "create" in message_lower:
        if category == "generate":
            score += 50

    if "what is" in message_lower or "explain" in message_lower or "how does" in message_lower:
        if category == "learn":
            score += 50

    # Word-level scoring

    for word in query_words:
        if word in filename:
            score += 25
        if word in category:
            score += 10
        if word in content:
            score += 1

    return score


def retrieve_top_matches(topic: str, message: str, k: int = 3) -> list[dict]:
    files = load_markdown_files(topic)

    if not files:
        return []

    scored_files = []

    for file_data in files:
        score = score_file(message, file_data)

        if score > 0:
            scored_files.append(
                {
                    **file_data,
                    "score": score,
                }
            )

    if not scored_files:
        return []

    scored_files.sort(key=lambda item: item["score"], reverse=True)

    best_score = scored_files[0]["score"]

    filtered_files = [
        item for item in scored_files
        if item["score"] >= best_score * 0.8
    ]

    return filtered_files[:k]