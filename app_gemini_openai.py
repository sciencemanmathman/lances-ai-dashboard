import streamlit as st
import os
import requests

# Load API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Set the models
openai_model = "gpt-4o"
gemini_model = "gemini-1.5-pro-latest"

# Function to query OpenAI
def ask_openai(question):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": openai_model,
        "messages": [{"role": "user", "content": question}]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Function to query Gemini
def ask_gemini(question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={gemini_api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts": [{"text": question}]}]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

# Streamlit UI
st.title("Lance’s AI Model Comparison Tool")
user_question = st.text_input("Enter your question")

if st.button("Submit to Both Models"):
    if user_question:
        with st.spinner("Getting response from OpenAI..."):
            try:
                openai_answer = ask_openai(user_question)
                st.subheader("ChatGPT (OpenAI)")
                st.write(openai_answer)
            except Exception as e:
                st.subheader("ChatGPT (OpenAI)")
                st.error(str(e))
        
        with st.spinner("Getting response from Gemini..."):
            try:
                gemini_answer = ask_gemini(user_question)
                st.subheader("Gemini (Google)")
                st.write(gemini_answer)
            except Exception as e:
                st.subheader("Gemini (Google)")
                st.error(str(e))
