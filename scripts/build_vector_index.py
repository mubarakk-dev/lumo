import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.chroma_retrieval_service import build_chroma_index
from app.services.semantic_retrieval_service import build_vector_index
from app.services.vector_store import index_path, load_index_metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Lumo vector indexes.")
    parser.add_argument(
        "--embedding-provider",
        choices=["local_hashing", "sentence_transformers"],
        default="local_hashing",
        help="Embedding provider to use for the Chroma index.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    topic = "docker"
    records = build_vector_index(topic)
    metadata = load_index_metadata(topic)
    print(f"Indexed {len(records)} chunks for topic '{topic}'.")
    print(f"Embedding provider: {metadata.get('embedding_provider')}")
    print(f"Embedding dimensions: {metadata.get('embedding_dimensions')}")
    print(f"Index path: {index_path(topic)}")

    chroma_count = build_chroma_index(
        topic=topic,
        embedding_provider=args.embedding_provider,
    )
    print(f"Chroma embedding provider: {args.embedding_provider}")
    print(f"Chroma indexed chunks: {chroma_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
