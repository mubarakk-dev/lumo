import requests

from app.core.config import (
    get_ollama_host,
    get_ollama_model,
    get_ollama_timeout_seconds,
)
from app.services.answer_service import build_grounded_answer
from app.services.prompt_service import build_rag_prompt


SUPPORTED_GENERATION_PROVIDERS = {"extractive", "ollama"}


def generate_grounded_answer(
    message: str,
    matches: list[dict],
    sources: list[dict],
    intent: str,
    generation_provider: str = "extractive",
) -> dict:
    if generation_provider == "extractive":
        return build_extractive_result(message, matches, sources, intent)

    if generation_provider == "ollama":
        return build_ollama_result(message, matches, sources, intent)

    return {
        "error": f"Unsupported generation provider '{generation_provider}'.",
        "suggestion": "Use 'extractive' or 'ollama'.",
    }


def build_extractive_result(
    message: str,
    matches: list[dict],
    sources: list[dict],
    intent: str,
    requested_provider: str = "extractive",
    fallback_reason: str | None = None,
) -> dict:
    result = {
        "answer": build_grounded_answer(
            message=message,
            matches=matches,
            sources=sources,
            intent=intent,
        ),
        "generation_provider": requested_provider,
        "answer_provider": "extractive",
        "used_fallback": requested_provider != "extractive",
    }

    if fallback_reason:
        result["generation_error"] = fallback_reason

    return result


def build_ollama_result(
    message: str,
    matches: list[dict],
    sources: list[dict],
    intent: str,
) -> dict:
    model = get_ollama_model()
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": build_rag_prompt(
                    message=message,
                    matches=matches,
                    sources=sources,
                    intent=intent,
                ),
            }
        ],
        "stream": False,
        "options": {
            "temperature": 0.2,
        },
    }

    try:
        response = requests.post(
            f"{get_ollama_host()}/api/chat",
            json=payload,
            timeout=get_ollama_timeout_seconds(),
        )
        response.raise_for_status()
        data = response.json()
        answer = data.get("message", {}).get("content", "").strip()
    except requests.RequestException as exc:
        return build_extractive_result(
            message=message,
            matches=matches,
            sources=sources,
            intent=intent,
            requested_provider="ollama",
            fallback_reason=f"Ollama is not reachable: {exc}",
        )
    except ValueError as exc:
        return build_extractive_result(
            message=message,
            matches=matches,
            sources=sources,
            intent=intent,
            requested_provider="ollama",
            fallback_reason=f"Ollama returned invalid JSON: {exc}",
        )

    if not answer:
        return build_extractive_result(
            message=message,
            matches=matches,
            sources=sources,
            intent=intent,
            requested_provider="ollama",
            fallback_reason="Ollama returned an empty answer.",
        )

    return {
        "answer": answer,
        "generation_provider": "ollama",
        "answer_provider": "ollama",
        "used_fallback": False,
        "model": model,
    }
