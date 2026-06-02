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

if st.button("Send"):
    payload = {
        "message": user_input,
    }

    response = requests.post(API_URL, json=payload, timeout=10)

    if response.status_code == 200:
        data = response.json()

        if "intent" in data:
            st.caption(f"Detected intent: {data['intent']}")

        if "topic" in data:
            st.caption(f"Detected topic: {data['topic']}")
            st.success("Lumo response")

        if "content" in data:
            st.markdown(data["content"])
        else:
            st.json(data)
    else:
        st.error("Something went wrong.")
