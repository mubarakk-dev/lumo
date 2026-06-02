from app.services.chunking_service import load_knowledge_chunks
from app.services.embedding_service import EMBEDDING_DIMENSIONS, cosine_similarity, embed_text
from app.services.vector_store import load_index, save_index


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

    if not records:
        records = build_vector_index(topic)

    query_embedding = embed_text(message)
    scored_records = []

    for record in records:
        if preferred_category is not None and record["category"] != preferred_category:
            continue

        scored_records.append(
            {
                **record,
                "score": cosine_similarity(query_embedding, record["embedding"]),
            }
        )

    scored_records = [record for record in scored_records if record["score"] > 0]
    scored_records.sort(key=lambda record: record["score"], reverse=True)

    return scored_records[:k]
