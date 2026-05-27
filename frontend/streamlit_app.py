import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="Lumo",
    page_icon="💡",
)

st.title("💡 Lumo")
st.subheader("Learn. Build. Deploy.")

mode = st.selectbox(
    "Choose Mode",
    ["learn", "generate", "troubleshoot"]
)

user_input = st.text_input(
    "Ask Lumo something..."
)

if st.button("Send"):

    payload = {
        "mode": mode,
        "message": user_input
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:

        data = response.json()

        st.success("Lumo response")

        if "content" in data:
            st.markdown(data["content"])
        else:
            st.json(data)

    else:
        st.error("Something went wrong.")