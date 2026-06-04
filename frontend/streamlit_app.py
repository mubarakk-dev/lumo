import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/chat"
API_TIMEOUT_SECONDS = 90

st.set_page_config(
    page_title="Lumo",
    page_icon="L",
)

st.title("Lumo")
st.subheader("Your AI Docker Companion.")

user_input = st.text_input("Ask me anything about Docker...")
retrieval_mode = st.selectbox(
    "Retrieval mode",
    options=["keyword", "semantic", "chroma"],
)
embedding_provider = st.selectbox(
    "Embedding provider",
    options=["local_hashing", "sentence_transformers"],
)
response_mode = st.selectbox(
    "Response mode",
    options=["answer", "retrieval"],
)
generation_provider = st.selectbox(
    "Generation provider",
    options=["extractive", "ollama"],
)

if st.button("Send"):
    payload = {
        "message": user_input,
        "retrieval_mode": retrieval_mode,
        "embedding_provider": embedding_provider,
        "response_mode": response_mode,
        "generation_provider": generation_provider,
    }

    try:
        with st.spinner("Generating grounded answer..."):
            response = requests.post(API_URL, json=payload, timeout=API_TIMEOUT_SECONDS)
    except requests.Timeout:
        st.error("The backend took too long to respond. Try again, or switch generation provider to extractive.")
        st.stop()
    except requests.RequestException as exc:
        st.error(f"Could not reach the backend: {exc}")
        st.stop()

    if response.status_code == 200:
        data = response.json()

        if "intent" in data:
            st.caption(f"Detected intent: {data['intent']}")

        if "topic" in data:
            st.caption(f"Detected topic: {data['topic']}")
            st.success("Lumo response")

        if "retrieval_mode" in data:
            st.caption(f"Retrieval mode: {data['retrieval_mode']}")

        if data.get("embedding_provider"):
            st.caption(f"Embedding provider: {data['embedding_provider']}")

        if "response_mode" in data:
            st.caption(f"Response mode: {data['response_mode']}")

        if "answer_provider" in data:
            st.caption(f"Answer provider: {data['answer_provider']}")

        if data.get("used_fallback"):
            st.warning(data.get("generation_error", "Using extractive fallback."))

        if "content" in data:
            st.markdown(data["content"])
        else:
            st.json(data)
    else:
        st.error("Something went wrong.")
