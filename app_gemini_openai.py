import streamlit as st
import openai
import requests
import time
import os

# Set your API keys from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
gemini_api_key = st.secrets["GEMINI_API_KEY"]

# Function to query OpenAI
def ask_openai(question):
    start_time = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can change to "gpt-4" if you have access
        messages=[
            {"role": "user", "content": question}
        ]
    )
    end_time = time.time()
    answer = response['choices'][0]['message']['content']
    tokens_used = response['usage']['total_tokens']
    response_time = end_time - start_time
    return answer, tokens_used, response_time

# Function to query Google Gemini
def ask_gemini(question):
    start_time = time.time()
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": gemini_api_key}
    data = {
        "contents": [{"parts": [{"text": question}]}]
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    end_time = time.time()

    if response.status_code == 200:
        gemini_response = response.json()
        try:
            answer = gemini_response['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            answer = "Error: Unexpected Gemini response format."
    else:
        answer = f"Error: {response.status_code} {response.text}"

    response_time = end_time - start_time
    return answer, response_time

# Streamlit Frontend
st.title("Lance’s AI Model Comparison Tool")
st.write("Enter your question below to compare ChatGPT (OpenAI) and Gemini (Google) models:")

user_question = st.text_input("Enter your question:")

if st.button("Submit to Both Models") and user_question:
    with st.spinner("Asking ChatGPT..."):
        try:
            chatgpt_answer, tokens_used, chatgpt_time = ask_openai(user_question)
        except Exception as e:
            chatgpt_answer = f"Error: {e}"
            tokens_used = 0
            chatgpt_time = 0

    with st.spinner("Asking Gemini..."):
        try:
            gemini_answer, gemini_time = ask_gemini(user_question)
        except Exception as e:
            gemini_answer = f"Error: {e}"
            gemini_time = 0

    st.header("ChatGPT (OpenAI)")
    st.write(chatgpt_answer)
    st.caption(f"Tokens used: {tokens_used}")
    st.caption(f"Response time: {chatgpt_time:.2f} seconds")

    st.header("Gemini (Google)")
    st.write(gemini_answer)
    st.caption(f"Response time: {gemini_time:.2f} seconds")


    st.subheader("Gemini (Google)")
    st.write(gemini_answer)
    if gemini_time is not None:
        st.caption(f"Response time: {gemini_time} seconds")
