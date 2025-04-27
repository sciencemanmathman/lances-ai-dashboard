import streamlit as st
import requests
import openai
import os

# Load your API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

def ask_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # <-- use cheaper model
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def ask_gemini(prompt):
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    params = {"key": gemini_api_key}
    response = requests.post(endpoint, headers=headers, params=params, json=payload)

    if response.status_code == 200:
        candidates = response.json().get("candidates", [])
        if candidates:
            return candidates[0]['content']['parts'][0]['text']
        else:
            return "No candidates returned."
    else:
        return f"Error: {response.text}"

# Streamlit UI
st.title("Lance’s AI Model Comparison Tool")

user_input = st.text_input("Enter your question")

if st.button("Submit to Both Models"):
    if user_input:
        with st.spinner('Getting answers...'):
            try:
                openai_answer = ask_openai(user_input)
            except Exception as e:
                openai_answer = f"Error: {str(e)}"
            
            try:
                gemini_answer = ask_gemini(user_input)
            except Exception as e:
                gemini_answer = f"Error: {str(e)}"
        
        st.subheader("ChatGPT (OpenAI)")
        st.write(openai_answer)

        st.subheader("Gemini (Google)")
        st.write(gemini_answer)
