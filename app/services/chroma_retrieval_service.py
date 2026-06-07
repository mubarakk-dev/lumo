from pathlib import Path

import chromadb

from app.services.chunking_service import load_knowledge_chunks
from app.services.embedding_service import DEFAULT_EMBEDDING_PROVIDER, embed_texts
from app.services.knowledge_service import score_file
from app.services.query_service import (
    detect_comparison_target,
    detect_definition_target,
    detect_generation_target,
    detect_troubleshooting_target,
)


CHROMA_DIR = Path(".chroma")
DEFAULT_COLLECTION = "lumo_docker"


def get_client():
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def collection_name(topic: str, embedding_provider: str) -> str:
    safe_provider = embedding_provider.replace("-", "_")
    return f"{DEFAULT_COLLECTION}_{topic}_{safe_provider}"


def target_matches_record(target: str | None, filename: str, path: str) -> bool:
    if not target:
        return False

    normalized_target = target.replace("_", " ")
    normalized_path = Path(path).stem.replace("_", " ").lower()

    return normalized_target in filename or normalized_target in normalized_path


def get_collection(topic: str, embedding_provider: str = DEFAULT_EMBEDDING_PROVIDER):
    client = get_client()
    return client.get_or_create_collection(
        name=collection_name(topic, embedding_provider),
        metadata={
            "topic": topic,
            "embedding_provider": embedding_provider,
        },
    )


def build_chroma_index(
    topic: str,
    embedding_provider: str = DEFAULT_EMBEDDING_PROVIDER,
) -> int:
    chunks = load_knowledge_chunks(topic)
    collection = get_collection(topic, embedding_provider)

    if collection.count() > 0:
        collection.delete(ids=collection.get()["ids"])

    documents = [chunk["content"] for chunk in chunks]
    embeddings = embed_texts(
        [
            "\n".join([chunk["filename"], chunk["category"], chunk["content"]])
            for chunk in chunks
        ],
        provider=embedding_provider,
    )

    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=documents,
        embeddings=embeddings,
        metadatas=[
            {
                "path": chunk["path"],
                "category": chunk["category"],
                "filename": chunk["filename"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ],
    )

    return len(chunks)


def retrieve_chroma_matches(
    topic: str,
    message: str,
    k: int = 3,
    preferred_category: str | None = None,
    embedding_provider: str = DEFAULT_EMBEDDING_PROVIDER,
) -> list[dict]:
    collection = get_collection(topic, embedding_provider)
    expected_chunk_count = len(load_knowledge_chunks(topic))

    if collection.count() != expected_chunk_count:
        build_chroma_index(topic, embedding_provider)

    query_embedding = embed_texts([message], provider=embedding_provider)[0]
    where = {"category": preferred_category} if preferred_category else None
    candidate_count = min(collection.count(), max(k * 5, 20))
    definition_target = detect_definition_target(message)
    comparison_target = detect_comparison_target(message)
    generation_target = detect_generation_target(message)
    troubleshooting_target = detect_troubleshooting_target(message)
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=candidate_count,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    matches = []
    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    for chunk_id, document, metadata, distance in zip(ids, documents, metadatas, distances):
        semantic_score = 1 - distance
        keyword_score = score_file(
            message,
            {
                "path": metadata["path"],
                "category": metadata["category"],
                "filename": metadata["filename"],
                "content": document,
            },
        )
        target_boost = 0
        if target_matches_record(definition_target, metadata["filename"], metadata["path"]):
            target_boost += 0.5
        if target_matches_record(comparison_target, metadata["filename"], metadata["path"]):
            target_boost += 0.5
        if target_matches_record(generation_target, metadata["filename"], metadata["path"]):
            target_boost += 0.5
        if target_matches_record(troubleshooting_target, metadata["filename"], metadata["path"]):
            target_boost += 0.5
        combined_score = semantic_score + min(keyword_score / 200, 1) * 0.25 + target_boost
        matches.append(
            {
                "id": chunk_id,
                "path": metadata["path"],
                "category": metadata["category"],
                "filename": metadata["filename"],
                "chunk_index": metadata["chunk_index"],
                "content": document,
                "score": combined_score,
                "semantic_score": semantic_score,
                "keyword_score": keyword_score,
            }
        )

    matches.sort(key=lambda match: match["score"], reverse=True)
    return matches[:k]
