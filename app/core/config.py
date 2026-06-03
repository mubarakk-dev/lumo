import os

from dotenv import load_dotenv


load_dotenv()


DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "llama3.2"
DEFAULT_OLLAMA_TIMEOUT_SECONDS = 20


def get_ollama_host() -> str:
    return os.getenv("OLLAMA_HOST", DEFAULT_OLLAMA_HOST).rstrip("/")


def get_ollama_model() -> str:
    return os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)


def get_ollama_timeout_seconds() -> int:
    raw_timeout = os.getenv("OLLAMA_TIMEOUT_SECONDS")

    if raw_timeout is None:
        return DEFAULT_OLLAMA_TIMEOUT_SECONDS

    try:
        return int(raw_timeout)
    except ValueError:
        return DEFAULT_OLLAMA_TIMEOUT_SECONDS
