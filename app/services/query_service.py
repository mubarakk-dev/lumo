def detect_query_intent(message: str) -> str:
    message_lower = message.lower().strip()

    if (
        "cheat sheet" in message_lower
        or "cheatsheet" in message_lower
        or "commands" in message_lower
        or "list commands" in message_lower
        or "list dockerfile instructions" in message_lower
    ):
        return "cheatsheet"

    if (
        message_lower.startswith("what is")
        or message_lower.startswith("what are")
        or message_lower.startswith("explain")
        or message_lower.startswith("define")
    ):
        return "definition"

    if (
        "difference between" in message_lower
        or "compare" in message_lower
        or "vs" in message_lower
        or "versus" in message_lower
    ):
        return "comparison"

    if (
        "error" in message_lower
        or "not working" in message_lower
        or "failed" in message_lower
        or "cannot" in message_lower
        or "can't" in message_lower
        or "not running" in message_lower
        or "not starting" in message_lower
        or "not loading" in message_lower
        or "keeps failing" in message_lower
        or "not responding" in message_lower
        or "not reachable" in message_lower
        or "not accessible" in message_lower
        or "not connecting" in message_lower
        or "troubleshoot" in message_lower
        or "issue" in message_lower
        or "problem" in message_lower
        or "allocated" in message_lower
        or "exits" in message_lower
        or "missing" in message_lower
    ):
        return "troubleshooting"

    if (
        "write" in message_lower
        or "create" in message_lower
        or "generate" in message_lower
        or "template" in message_lower
        or "yaml" in message_lower
        or "dockerfile" in message_lower
    ):
        return "generation"

    if " and " in message_lower:
        return "multi_part"

    return "general"


def get_retrieval_k(intent: str) -> int:
    if intent == "definition":
        return 1

    if intent == "comparison":
        return 1

    if intent == "generation":
        return 1

    if intent == "cheatsheet":
        return 1

    if intent == "troubleshooting":
        return 2

    if intent == "multi_part":
        return 3

    return 2

DEFINITION_FILE_MAP = {
    "docker compose": "what is docker compose",
    "dockerfile": "what is dockerfile",
    "docker image": "images vs containers",
    "docker images": "images vs containers",
    "docker container": "images vs containers",
    "docker containers": "images vs containers",
    "docker volumes": "volumes",
    "volumes": "volumes",
    "docker networking": "networking",
    "networking": "networking",
    "multi-stage builds": "multi stage builds",
}

def detect_definition_target(message: str) -> str | None:
    message_lower = message.lower()

    for term, target in DEFINITION_FILE_MAP.items():
        if term in message_lower:
            return target

    return None
