MAX_CONTEXT_CHARS = 6000


def build_rag_prompt(
    message: str,
    matches: list[dict],
    sources: list[dict],
    intent: str,
) -> str:
    return "\n\n".join(
        [
            build_system_instructions(intent),
            build_source_map(sources),
            build_context(matches, sources),
            f"User question:\n{message}",
        ]
    ).strip()


def build_system_instructions(intent: str) -> str:
    return "\n".join(
        [
            "You are Lumo, a practical Docker assistant.",
            "Answer only from the retrieved context below.",
            "If the context is not enough, say what is missing instead of guessing.",
            "Use concise, beginner-friendly language.",
            "Cite supporting facts with source numbers like [1] or [2].",
            f"Detected user intent: {intent}.",
        ]
    )


def build_source_map(sources: list[dict]) -> str:
    if not sources:
        return "Sources: none"

    lines = ["Sources:"]

    for index, source in enumerate(sources, start=1):
        lines.append(f"[{index}] {source['path']}")

    return "\n".join(lines)


def build_context(matches: list[dict], sources: list[dict]) -> str:
    source_indexes = {
        source["path"]: index
        for index, source in enumerate(sources, start=1)
    }
    blocks = []

    for match in matches:
        index = source_indexes.get(match["path"], 1)
        content = match["content"].strip()
        blocks.append(f"[{index}] {match['path']}\n{content}")

    context = "\n\n---\n\n".join(blocks)

    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS].rsplit("\n", 1)[0].strip()

    return f"Retrieved context:\n{context}"
