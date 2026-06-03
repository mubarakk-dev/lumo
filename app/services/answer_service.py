import re


HEADING_PATTERN = re.compile(r"^#+\s*", re.MULTILINE)


def strip_markdown_headings(text: str) -> str:
    return HEADING_PATTERN.sub("", text).strip()


def compact_lines(text: str, max_lines: int = 10) -> list[str]:
    lines = []

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line or line == "---":
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

    intro = build_intro(intent)
    answer_parts = [intro]
    source_indexes = {
        source["path"]: index
        for index, source in enumerate(sources)
    }

    for match in matches[:3]:
        label = source_label(source_indexes.get(match["path"], 0))
        cleaned_content = strip_markdown_headings(match["content"])
        lines = compact_lines(cleaned_content)

        if not lines:
            continue

        answer_parts.append(f"{label} " + "\n".join(lines))

    if sources:
        answer_parts.append(build_source_summary(sources))

    return "\n\n".join(answer_parts).strip()


def build_intro(intent: str) -> str:
    if intent == "troubleshooting":
        return "Here is a grounded troubleshooting answer based on the retrieved Docker knowledge:"

    if intent == "generation":
        return "Here is a grounded Docker solution based on the retrieved knowledge:"

    if intent == "cheatsheet":
        return "Here are the most relevant Docker commands from the retrieved knowledge:"

    return "Here is a grounded answer based on the retrieved Docker knowledge:"


def build_source_summary(sources: list[dict]) -> str:
    source_lines = ["Sources:"]

    for index, source in enumerate(sources):
        source_lines.append(f"{source_label(index)} {source['path']}")

    return "\n".join(source_lines)
