import streamlit as st
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Lance's AI Dashboard", layout="wide")
st.title("Lance’s AI Model Comparison Tool")

st.sidebar.title("Lance’s AI Model Comparison Tool")
st.sidebar.markdown("Enter your question below to compare how OpenAI and Gemini respond.")

if "token_count" not in st.session_state:
    st.session_state.token_count = 0

prompt = st.text_area("Your question", height=150)

col1, col2 = st.columns(2)

if st.button("Submit to Both Models") and prompt:
    with st.spinner("Waiting for responses..."):

        try:
            start = time.time()
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai_key}"},
                json={"model": "gpt-4", "messages": [{"role": "user", "content": prompt}]}
            ).json()
            openai_response = response["choices"][0]["message"]["content"]
            openai_tokens = response["usage"]["total_tokens"]
            openai_time = round(time.time() - start, 2)
        except Exception as e:
            openai_response = f"Error: {e}"
            openai_tokens = 0
            openai_time = "N/A"

        try:
            start = time.time()
            response = requests.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + gemini_key,
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": prompt}]}]
                }
            ).json()
            gemini_response = response["candidates"][0]["content"]["parts"][0]["text"]
            gemini_time = round(time.time() - start, 2)
        except Exception as e:
            gemini_response = f"Error: {e}"
            gemini_time = "N/A"

    st.session_state.token_count += openai_tokens
    st.sidebar.markdown(f"**Total Tokens This Session:** {st.session_state.token_count}")
    if st.session_state.token_count > 5000:
        st.sidebar.warning("You’re approaching your free tier limit.")

    with col1:
        st.subheader("ChatGPT")
        st.write(openai_response)
        st.caption(f"Tokens used: {openai_tokens}")
        st.caption(f"Response time: {openai_time} seconds")

    with col2:
        st.subheader("Gemini")
        st.write(gemini_response)
        st.caption(f"Response time: {gemini_time} seconds")
