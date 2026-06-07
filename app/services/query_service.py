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

    if "template" in message_lower and ("yaml" in message_lower or "yml" in message_lower):
        return "generation"

    if (
        "difference between" in message_lower
        or "compare" in message_lower
        or "vs" in message_lower
        or "versus" in message_lower
    ):
        return "comparison"

    if (
        message_lower.startswith("what is")
        or message_lower.startswith("what are")
        or message_lower.startswith("explain")
        or message_lower.startswith("define")
    ):
        return "definition"

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
        or "no space" in message_lower
        or "space left" in message_lower
        or "disk full" in message_lower
        or "disk space" in message_lower
        or "device full" in message_lower
        or "storage full" in message_lower
        or "out of space" in message_lower
    ):
        return "troubleshooting"

    if (
        "inside a running container" in message_lower
        or "inside running container" in message_lower
        or "happening inside" in message_lower
        or "see what is happening" in message_lower
        or "inspect inside" in message_lower
        or "debug inside" in message_lower
        or "copy a file" in message_lower
        or "copy file" in message_lower
        or "docker cp" in message_lower
    ):
        return "generation"

    if (
        "write" in message_lower
        or "create" in message_lower
        or "generate" in message_lower
        or "template" in message_lower
        or "yaml" in message_lower
        or ".yaml" in message_lower
        or "dockerfile" in message_lower
        or "yml" in message_lower
        or ".yml" in message_lower
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
    ".yaml": "what is yaml",
    ".yml": "what is yaml",
    "yaml file": "what is yaml",
    "yml file": "what is yaml",
    "docker compose": "what is docker compose",
    "dockerfile": "what is dockerfile",
    "docker image": "images vs containers",
    "docker images": "images vs containers",
    "docker container": "images vs containers",
    "docker containers": "images vs containers",
    "container": "images vs containers",
    "containers": "images vs containers",
    "image": "images vs containers",
    "images": "images vs containers",
    "docker volumes": "volumes",
    "volumes": "volumes",
    "docker networking": "networking",
    "networking": "networking",
    "multi-stage builds": "multi stage builds",
    "virtual machine": "virtual machines",
    "virtual machines": "virtual machines",
    "vm": "virtual machines",
    "vms": "virtual machines",
}


COMPARISON_FILE_MAP = {
    "dockerfile and docker compose": "docker compose vs dockerfile",
    "docker compose and dockerfile": "docker compose vs dockerfile",
    "dockerfile vs docker compose": "docker compose vs dockerfile",
    "docker compose vs dockerfile": "docker compose vs dockerfile",
    "dockerfile and compose": "docker compose vs dockerfile",
    "compose and dockerfile": "docker compose vs dockerfile",
}


GENERATION_FILE_MAP = {
    "inside a running container": "exec into container",
    "inside running container": "exec into container",
    "happening inside": "exec into container",
    "see what is happening": "exec into container",
    "inspect inside": "exec into container",
    "debug inside": "exec into container",
    "exec": "exec into container",
    "copy a file": "copy files",
    "copy file": "copy files",
    "copy files": "copy files",
    "docker cp": "copy files",
    "multi-stage build": "dockerfile template",
    "multi stage build": "dockerfile template",
    "multi-stage dockerfile": "dockerfile template",
    "multi stage dockerfile": "dockerfile template",
    ".yaml": "docker compose",
    ".yml": "docker compose",
    "yaml file": "docker compose",
    "yml file": "docker compose",
    "compose yaml": "docker compose",
    "docker-compose.yml": "docker compose",
}


TROUBLESHOOTING_FILE_MAP = {
    "no space left on device": "no space left",
    "no space left": "no space left",
    "no space": "no space left",
    "space left": "no space left",
    "disk full": "no space left",
    "disk space": "no space left",
    "device full": "no space left",
    "storage full": "no space left",
    "out of space": "no space left",
}


def is_definition_query(message_lower: str) -> bool:
    return (
        message_lower.startswith("what is")
        or message_lower.startswith("what are")
        or message_lower.startswith("explain")
        or message_lower.startswith("define")
    )


def detect_definition_target(message: str) -> str | None:
    message_lower = message.lower()

    if not is_definition_query(message_lower):
        return None

    for term, target in DEFINITION_FILE_MAP.items():
        if term in message_lower:
            return target

    return None


def detect_comparison_target(message: str) -> str | None:
    message_lower = message.lower()

    if (
        "difference between" not in message_lower
        and "compare" not in message_lower
        and " vs " not in message_lower
        and " versus " not in message_lower
    ):
        return None

    for term, target in COMPARISON_FILE_MAP.items():
        if term in message_lower:
            return target

    return None


def detect_generation_target(message: str) -> str | None:
    message_lower = message.lower()

    if (
        "template" not in message_lower
        and "generate" not in message_lower
        and "create" not in message_lower
        and "write" not in message_lower
        and "inside" not in message_lower
        and "happening" not in message_lower
        and "exec" not in message_lower
        and "copy" not in message_lower
        and "docker cp" not in message_lower
    ):
        return None

    for term, target in GENERATION_FILE_MAP.items():
        if term in message_lower:
            return target

    return None


def detect_troubleshooting_target(message: str) -> str | None:
    message_lower = message.lower()

    for term, target in TROUBLESHOOTING_FILE_MAP.items():
        if term in message_lower:
            return target

    return None
