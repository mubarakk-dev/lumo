from pathlib import Path

from app.services.knowledge_service import load_markdown_files


def split_markdown_sections(content: str) -> list[str]:
    sections = []
    current_lines = []

    for line in content.splitlines():
        if line.startswith("#") and current_lines:
            sections.append("\n".join(current_lines).strip())
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append("\n".join(current_lines).strip())

    return [section for section in sections if section]


def chunk_markdown_file(file_data: dict) -> list[dict]:
    chunks = []

    for index, section in enumerate(split_markdown_sections(file_data["content"])):
        chunk_id = f"{Path(file_data['path']).as_posix()}::chunk-{index}"
        chunks.append(
            {
                "id": chunk_id,
                "path": file_data["path"],
                "category": file_data["category"],
                "filename": file_data["filename"],
                "content": section,
                "chunk_index": index,
            }
        )

    return chunks


def load_knowledge_chunks(topic: str) -> list[dict]:
    chunks = []

    for file_data in load_markdown_files(topic):
        chunks.extend(chunk_markdown_file(file_data))

    return chunks
