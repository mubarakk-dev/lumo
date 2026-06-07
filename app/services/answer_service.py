import re


HEADING_PATTERN = re.compile(r"^#+\s*(.+)$")
RELATED_QUESTIONS_HEADING = "related questions"


def focus_content_for_query(message: str, content: str) -> str:
    message_lower = message.lower()

    if (
        "docker container" in message_lower
        or "docker containers" in message_lower
    ):
        return content_from_heading(content, "container")

    if (
        "docker image" in message_lower
        or "docker images" in message_lower
    ):
        return content_from_heading(content, "image")

    return content


def content_from_heading(content: str, heading_name: str) -> str:
    target_heading = heading_name.lower()
    lines = content.splitlines()

    for index, line in enumerate(lines):
        heading_match = HEADING_PATTERN.match(line.strip())

        if heading_match and heading_match.group(1).strip().lower() == target_heading:
            return "\n".join(lines[index:])

    return content


def compact_lines(text: str, max_lines: int = 10) -> list[str]:
    lines = []
    skipping_related_questions = False

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if line == "---":
            skipping_related_questions = False
            continue

        if not line:
            continue

        heading_match = HEADING_PATTERN.match(line)

        if heading_match:
            heading = heading_match.group(1).strip().lower()
            skipping_related_questions = heading == RELATED_QUESTIONS_HEADING
            continue

        if skipping_related_questions:
            continue

        lines.append(line)

        if len(lines) >= max_lines:
            break

    return lines


def source_label(index: int) -> str:
    return f"[{index + 1}]"


def build_grounded_answer(
    message: str,
    matches: list[dict],
    sources: list[dict],
    intent: str,
) -> str:
    if not matches:
        return "I could not find enough grounded Docker context to answer that."

    answer_parts = []
    source_indexes = {
        source["path"]: index
        for index, source in enumerate(sources)
    }
    seen_paths = set()

    for match in matches[:3]:
        if match["path"] in seen_paths:
            continue

        seen_paths.add(match["path"])
        label = source_label(source_indexes.get(match["path"], 0))
        focused_content = focus_content_for_query(message, match["content"])
        lines = compact_lines(focused_content, max_lines=get_max_lines_for_intent(intent))

        if not lines:
            continue

        answer_parts.append(format_answer_block(label, lines))

    return "\n\n".join(answer_parts).strip()


def get_max_lines_for_intent(intent: str) -> int:
    if intent in {"generation", "cheatsheet"}:
        return 36

    if intent == "troubleshooting":
        return 16

    return 13


def format_answer_block(label: str, lines: list[str]) -> str:
    first_line = lines[0]
    remaining_lines = lines[1:]

    if not remaining_lines:
        return f"{label} {first_line}"

    return f"{label} {first_line}\n" + "\n".join(remaining_lines)
