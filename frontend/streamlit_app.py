import os

import requests
import streamlit as st

from app.services.chat_service import handle_chat


API_URL = "http://127.0.0.1:8000/chat"
API_TIMEOUT_SECONDS = 90
CHAT_BACKEND = os.getenv("LUMO_CHAT_BACKEND", "direct")
DEFAULT_RETRIEVAL_MODE = "chroma"
DEFAULT_EMBEDDING_PROVIDER = "local_hashing"
DEFAULT_RESPONSE_MODE = "answer"
DEFAULT_GENERATION_PROVIDER = "extractive"


def call_chat_service(payload: dict) -> dict:
    with st.spinner("Generating grounded answer..."):
        return handle_chat(
            message=payload["message"],
            retrieval_mode=payload["retrieval_mode"],
            embedding_provider=payload["embedding_provider"],
            response_mode=payload["response_mode"],
            generation_provider=payload["generation_provider"],
        )


def call_chat_api(payload: dict) -> dict:
    try:
        with st.spinner("Generating grounded answer..."):
            response = requests.post(API_URL, json=payload, timeout=API_TIMEOUT_SECONDS)
    except requests.Timeout:
        return {
            "error": "The backend took too long to respond.",
            "suggestion": "Try again, or switch generation provider to extractive.",
        }
    except requests.RequestException as exc:
        return {
            "error": f"Could not reach the backend: {exc}",
            "suggestion": "Start FastAPI or set LUMO_CHAT_BACKEND=direct.",
        }

    if response.status_code != 200:
        return {
            "error": "Something went wrong.",
            "suggestion": f"Backend returned HTTP {response.status_code}.",
        }

    return response.json()


st.set_page_config(
    page_title="Lumo",
    page_icon="L",
)

st.title("Lumo")
st.subheader("Your AI Docker Companion.")

user_input = st.text_input("Ask me anything about Docker...")

retrieval_mode = DEFAULT_RETRIEVAL_MODE
embedding_provider = DEFAULT_EMBEDDING_PROVIDER
response_mode = DEFAULT_RESPONSE_MODE
generation_provider = DEFAULT_GENERATION_PROVIDER

with st.expander("Advanced settings"):
    retrieval_mode = st.selectbox(
        "Retrieval mode",
        options=["keyword", "semantic", "chroma"],
        index=["keyword", "semantic", "chroma"].index(DEFAULT_RETRIEVAL_MODE),
    )
    embedding_provider = st.selectbox(
        "Embedding provider",
        options=["local_hashing", "sentence_transformers"],
        index=["local_hashing", "sentence_transformers"].index(DEFAULT_EMBEDDING_PROVIDER),
    )
    response_mode = st.selectbox(
        "Response mode",
        options=["answer", "retrieval"],
        index=["answer", "retrieval"].index(DEFAULT_RESPONSE_MODE),
    )
    generation_provider = st.selectbox(
        "Generation provider",
        options=["extractive", "ollama"],
        index=["extractive", "ollama"].index(DEFAULT_GENERATION_PROVIDER),
    )

if st.button("Send"):
    payload = {
        "message": user_input,
        "retrieval_mode": retrieval_mode,
        "embedding_provider": embedding_provider,
        "response_mode": response_mode,
        "generation_provider": generation_provider,
    }

    if CHAT_BACKEND == "api":
        data = call_chat_api(payload)
    else:
        data = call_chat_service(payload)

    if "error" in data:
        st.error(data["error"])

        if "suggestion" in data:
            st.info(data["suggestion"])

        st.stop()

    if "topic" in data:
        st.success("Lumo response")

    if data.get("used_fallback"):
        st.warning(data.get("generation_error", "Using extractive fallback."))

    if "content" in data:
        st.markdown(data["content"])
    else:
        st.json(data)

    if data.get("sources"):
        st.divider()
        st.markdown("**Sources**")
        for index, source in enumerate(data["sources"], start=1):
            st.caption(f"[{index}] {source['path']}")

    if "topic" in data:
        with st.expander("Retrieval details"):
            st.write(
                {
                    "topic": data.get("topic"),
                    "intent": data.get("intent"),
                    "retrieval_mode": data.get("retrieval_mode"),
                    "embedding_provider": data.get("embedding_provider"),
                    "response_mode": data.get("response_mode"),
                    "generation_provider": data.get("generation_provider"),
                    "answer_provider": data.get("answer_provider"),
                    "model": data.get("model"),
                    "top_k": data.get("top_k"),
                    "used_fallback": data.get("used_fallback"),
                    "chat_backend": CHAT_BACKEND,
                }
            )
