import hashlib
import math
import os
import re
from functools import lru_cache


EMBEDDING_DIMENSIONS = 384
DEFAULT_EMBEDDING_PROVIDER = "local_hashing"
DEFAULT_SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"

TERM_ALIASES = {
    "compose": "docker_compose",
    "yaml": "compose_file",
    "yml": "compose_file",
    "allocated": "port_conflict",
    "busy": "port_conflict",
    "unavailable": "port_conflict",
    "missing": "not_found",
    "absent": "not_found",
    "communicate": "network_connectivity",
    "connectivity": "network_connectivity",
    "reachable": "network_connectivity",
    "restart": "restart_loop",
    "crash": "container_exits",
    "exits": "container_exits",
    "environment": "env",
    "variables": "env",
}

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+")


def tokenize(text: str) -> list[str]:
    tokens = TOKEN_PATTERN.findall(text.lower())
    return [TERM_ALIASES.get(token, token) for token in tokens]


def stable_index(token: str) -> int:
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % EMBEDDING_DIMENSIONS


def embed_text(text: str) -> list[float]:
    vector = [0.0] * EMBEDDING_DIMENSIONS

    for token in tokenize(text):
        vector[stable_index(token)] += 1.0

    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        return vector

    return [value / magnitude for value in vector]


def embed_texts(
    texts: list[str],
    provider: str = DEFAULT_EMBEDDING_PROVIDER,
) -> list[list[float]]:
    if provider == "local_hashing":
        return [embed_text(text) for text in texts]

    if provider == "sentence_transformers":
        model = load_sentence_transformer_model()
        return model.encode(texts, normalize_embeddings=True).tolist()

    raise ValueError(f"Unsupported embedding provider '{provider}'.")


@lru_cache(maxsize=1)
def load_sentence_transformer_model():
    from sentence_transformers import SentenceTransformer

    model_name = os.getenv(
        "LUMO_SENTENCE_TRANSFORMER_MODEL",
        DEFAULT_SENTENCE_TRANSFORMER_MODEL,
    )
    local_files_only = os.getenv("LUMO_HF_LOCAL_FILES_ONLY", "false").lower() == "true"
    return SentenceTransformer(model_name, local_files_only=local_files_only)


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(left_value * right_value for left_value, right_value in zip(left, right))
