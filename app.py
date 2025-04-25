
import streamlit as st
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
perplexity_key = os.getenv("PERPLEXITY_API_KEY")

st.set_page_config(page_title="Lance's AI Dashboard", layout="wide")
st.title("Lance’s AI Model Comparison Tool")

st.sidebar.title("Lance’s AI Model Comparison Tool")
st.sidebar.markdown("Enter your question below to compare how the top AI models respond.")

if "token_count" not in st.session_state:
    st.session_state.token_count = 0

prompt = st.text_area("Your question", height=150)

col1, col2, col3 = st.columns(3)

if st.button("Submit to All Models") and prompt:
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
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": anthropic_key,
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": "claude-3-opus-20240229",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1024
                }
            ).json()
            anthropic_response = response["content"][0]["text"]
            anthropic_tokens = response.get("usage", {}).get("output_tokens", 0)
            anthropic_time = round(time.time() - start, 2)
        except Exception as e:
            anthropic_response = f"Error: {e}"
            anthropic_tokens = 0
            anthropic_time = "N/A"

        try:
            start = time.time()
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={"Authorization": f"Bearer {perplexity_key}"},
                json={
                    "model": "sonar-medium-online",
                    "messages": [{"role": "user", "content": prompt}]
                }
            ).json()
            perplexity_response = response["choices"][0]["message"]["content"]
            perplexity_time = round(time.time() - start, 2)
        except Exception as e:
            perplexity_response = f"Error: {e}"
            perplexity_time = "N/A"

    total_tokens = openai_tokens + anthropic_tokens
    st.session_state.token_count += total_tokens
    st.sidebar.markdown(f"**Total Tokens This Session:** {st.session_state.token_count}")
    if st.session_state.token_count > 5000:
        st.sidebar.warning("You’re approaching your free tier limit.")

    with col1:
        st.subheader("ChatGPT")
        st.write(openai_response)
        st.caption(f"Tokens used: {openai_tokens}")
        st.caption(f"Response time: {openai_time} seconds")

    with col2:
        st.subheader("Claude")
        st.write(anthropic_response)
        st.caption(f"Tokens used: {anthropic_tokens}")
        st.caption(f"Response time: {anthropic_time} seconds")

    with col3:
        st.subheader("Perplexity")
        st.write(perplexity_response)
        st.caption(f"Response time: {perplexity_time} seconds")
