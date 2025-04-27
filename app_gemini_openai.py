import streamlit as st
import openai
import requests
import time

# Set your API keys
openai.api_key = st.secrets["OPENAI_API_KEY"]
google_api_key = st.secrets["GEMINI_API_KEY"]

# Functions
def ask_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

def ask_gemini(question):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }
    params = {
        "key": google_api_key
    }
    response = requests.post(url, headers=headers, json=payload, params=params)
    result = response.json()
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error: {e}\nFull response: {result}"

# Streamlit UI
st.title("Lance’s AI Model Comparison Tool")

user_input = st.text_input("Enter your question")

if st.button("Submit to Both Models") and user_input:
    with st.spinner("Asking ChatGPT..."):
        openai_start = time.time()
        openai_response = ask_openai(user_input)
        openai_time = time.time() - openai_start

    with st.spinner("Asking Gemini..."):
        gemini_start = time.time()
        gemini_response = ask_gemini(user_input)
        gemini_time = time.time() - gemini_start

    # Display responses
    st.subheader("ChatGPT (OpenAI)")
    st.write(openai_response)
    st.caption(f"Response time: {openai_time:.2f} seconds")

    st.subheader("Gemini (Google)")
    st.write(gemini_response)
    st.caption(f"Response time: {gemini_time:.2f} seconds")
