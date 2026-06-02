import json
from pathlib import Path


INDEX_DIR = Path(".lumo_index")
INDEX_SCHEMA_VERSION = 1


def index_path(topic: str) -> Path:
    return INDEX_DIR / f"{topic}_vectors.json"


def save_index(topic: str, records: list[dict], metadata: dict | None = None) -> Path:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    path = index_path(topic)
    payload = {
        "schema_version": INDEX_SCHEMA_VERSION,
        "topic": topic,
        "metadata": metadata or {},
        "records": records,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def load_index(topic: str) -> list[dict]:
    path = index_path(topic)

    if not path.exists():
        return []

    payload = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(payload, list):
        return payload

    return payload.get("records", [])


def load_index_metadata(topic: str) -> dict:
    path = index_path(topic)

    if not path.exists():
        return {}

    payload = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(payload, list):
        return {}

    return {
        "schema_version": payload.get("schema_version"),
        "topic": payload.get("topic"),
        **payload.get("metadata", {}),
    }
