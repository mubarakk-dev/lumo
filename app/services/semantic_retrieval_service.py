from app.services.chunking_service import load_knowledge_chunks
from app.services.embedding_service import EMBEDDING_DIMENSIONS, cosine_similarity, embed_text
from app.services.query_service import (
    detect_comparison_target,
    detect_definition_target,
    detect_generation_target,
    detect_troubleshooting_target,
)
from app.services.vector_store import load_index, load_index_metadata, save_index


def target_matches_record(target: str | None, record: dict) -> bool:
    if not target:
        return False

    normalized_target = target.replace("_", " ")
    normalized_path = record["path"].replace("\\", "/").rsplit("/", 1)[-1].replace(".md", "").replace("_", " ").lower()

    return normalized_target in record["filename"] or normalized_target in normalized_path


def build_vector_index(topic: str) -> list[dict]:
    records = []

    for chunk in load_knowledge_chunks(topic):
        embedding_text = "\n".join(
            [
                chunk["filename"],
                chunk["category"],
                chunk["content"],
            ]
        )
        records.append(
            {
                **chunk,
                "embedding": embed_text(embedding_text),
            }
        )

    save_index(
        topic=topic,
        records=records,
        metadata={
            "embedding_dimensions": EMBEDDING_DIMENSIONS,
            "chunk_count": len(records),
            "embedding_provider": "local_hashing",
        },
    )
    return records


def retrieve_semantic_matches(
    topic: str,
    message: str,
    k: int = 3,
    preferred_category: str | None = None,
) -> list[dict]:
    records = load_index(topic)
    metadata = load_index_metadata(topic)
    expected_chunk_count = len(load_knowledge_chunks(topic))

    if not records or metadata.get("chunk_count") != expected_chunk_count:
        records = build_vector_index(topic)

    query_embedding = embed_text(message)
    definition_target = detect_definition_target(message)
    comparison_target = detect_comparison_target(message)
    generation_target = detect_generation_target(message)
    troubleshooting_target = detect_troubleshooting_target(message)
    scored_records = []

    for record in records:
        if preferred_category is not None and record["category"] != preferred_category:
            continue

        target_boost = 0
        if target_matches_record(definition_target, record):
            target_boost += 2.0
        if target_matches_record(comparison_target, record):
            target_boost += 2.0
        if target_matches_record(generation_target, record):
            target_boost += 2.0
        if target_matches_record(troubleshooting_target, record):
            target_boost += 2.0

        scored_records.append(
            {
                **record,
                "score": cosine_similarity(query_embedding, record["embedding"]) + target_boost,
            }
        )

    scored_records = [record for record in scored_records if record["score"] > 0]
    scored_records.sort(key=lambda record: record["score"], reverse=True)

    return scored_records[:k]
