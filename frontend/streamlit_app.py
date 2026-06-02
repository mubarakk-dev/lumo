import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/chat"

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

if st.button("Send"):
    payload = {
        "message": user_input,
        "retrieval_mode": retrieval_mode,
        "embedding_provider": embedding_provider,
    }

    response = requests.post(API_URL, json=payload, timeout=10)

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

        if "content" in data:
            st.markdown(data["content"])
        else:
            st.json(data)
    else:
        st.error("Something went wrong.")
