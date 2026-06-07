import re


HEADING_PATTERN = re.compile(r"^#+\s*(.+)$")
RELATED_QUESTIONS_HEADING = "related questions"


def focus_content_for_query(message: str, content: str) -> str:
    message_lower = message.lower()

    if "template" in message_lower and ("yaml" in message_lower or "yml" in message_lower):
        return content_from_heading(content, "example docker-compose.yml")

    if (
        "inside a running container" in message_lower
        or "inside running container" in message_lower
        or "happening inside" in message_lower
        or "debug inside" in message_lower
    ):
        return content_from_heading(content, "open bash")

    if (
        "docker container" in message_lower
        or "docker containers" in message_lower
        or "what is a container" in message_lower
        or "what is container" in message_lower
        or "what are containers" in message_lower
        or "explain container" in message_lower
    ):
        return content_from_heading(content, "container")

    if (
        "docker image" in message_lower
        or "docker images" in message_lower
        or "what is an image" in message_lower
        or "what is image" in message_lower
        or "what are images" in message_lower
        or "explain image" in message_lower
    ):
        return content_from_heading(content, "image")

    return content


def content_from_heading(content: str, heading_name: str) -> str:
    target_heading = heading_name.lower()
    lines = content.splitlines()

    for index, line in enumerate(lines):
        heading_match = HEADING_PATTERN.match(line.strip())

        if heading_match and heading_match.group(1).strip().lower() == target_heading:
            focused_lines = []

            for focused_line in lines[index:]:
                focused_heading_match = HEADING_PATTERN.match(focused_line.strip())

                if focused_lines and focused_heading_match:
                    break

                focused_lines.append(focused_line)

            return "\n".join(focused_lines)

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


def extract_sections(content: str) -> dict[str, list[str]]:
    sections = {}
    current_heading = None

    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        heading_match = HEADING_PATTERN.match(line.strip())

        if heading_match:
            current_heading = heading_match.group(1).strip().lower()
            sections.setdefault(current_heading, [])
            continue

        if current_heading is not None:
            sections[current_heading].append(line)

    return sections


def clean_section_lines(lines: list[str], max_lines: int = 8) -> list[str]:
    cleaned = []

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        cleaned.append(line)

        if len(cleaned) >= max_lines:
            break

    return cleaned


def compact_blocks(text: str, max_lines: int = 10) -> list[str]:
    lines = []
    skipping_related_questions = False
    in_code_block = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped == "---":
            skipping_related_questions = False
            continue

        heading_match = HEADING_PATTERN.match(stripped)

        if heading_match:
            heading = heading_match.group(1).strip().lower()
            skipping_related_questions = heading == RELATED_QUESTIONS_HEADING
            continue

        if skipping_related_questions:
            continue

        if not stripped and not in_code_block:
            continue

        if stripped.startswith("```"):
            in_code_block = not in_code_block

        lines.append(line)

        if not in_code_block and len([item for item in lines if item.strip()]) >= max_lines:
            break

    return lines


def section_lines(sections: dict[str, list[str]], names: list[str], max_lines: int = 8) -> list[str]:
    lines = []
    seen_headings = set()

    for name in names:
        for heading, content_lines in sections.items():
            if heading in seen_headings:
                continue

            if heading == name or heading.startswith(name):
                seen_headings.add(heading)
                lines.extend(clean_section_lines(content_lines, max_lines=max_lines - len(lines)))

            if len(lines) >= max_lines:
                return lines

    return lines


def format_troubleshooting_answer(label: str, content: str) -> str:
    sections = extract_sections(content)
    problem = section_lines(sections, ["problem", "symptoms"], max_lines=5)
    cause = section_lines(sections, ["cause", "common causes", "common error"], max_lines=6)
    fix = section_lines(
        sections,
        ["fix", "fix on windows", "fix on linux", "troubleshooting checklist", "verify"],
        max_lines=12,
    )

    if not problem:
        problem = compact_lines(content, max_lines=3)

    if not cause:
        cause = ["The retrieved Docker context points to the issue described above."]

    if not fix:
        fix = ["The retrieved source does not include a specific fix yet."]

    parts = [
        f"{label} **Problem**",
        *problem,
        "",
        "**Cause**",
        *cause,
        "",
        "**Fix**",
        *fix,
    ]

    return "\n".join(parts).strip()


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

        if intent == "troubleshooting":
            answer_parts.append(format_troubleshooting_answer(label, focused_content))
            continue

        lines = compact_blocks(focused_content, max_lines=get_max_lines_for_intent(intent))

        if not lines:
            continue

        answer_parts.append(format_answer_block(label, lines))

    return "\n\n".join(answer_parts).strip()


def get_max_lines_for_intent(intent: str) -> int:
    if intent in {"generation", "cheatsheet"}:
        return 36

    if intent == "comparison":
        return 28

    if intent == "troubleshooting":
        return 16

    return 13


def format_answer_block(label: str, lines: list[str]) -> str:
    first_line = lines[0]
    remaining_lines = lines[1:]

    if not remaining_lines:
        return f"{label} {first_line}"

    return f"{label} {first_line}\n" + "\n".join(remaining_lines)
