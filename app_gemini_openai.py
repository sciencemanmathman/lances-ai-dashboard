import os
import time
import streamlit as st
import openai
import google.generativeai as genai

# Set up API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to call OpenAI
def ask_openai(question):
    start = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}],
        temperature=0.7,
        max_tokens=500
    )
    end = time.time()
    answer = response['choices'][0]['message']['content'].strip()
    return answer, round(end - start, 2)

# Function to call Gemini
def ask_gemini(question):
    start = time.time()
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    end = time.time()
    if hasattr(response, 'text') and response.text:
        answer = response.text.strip()
    else:
        answer = "Error: No response from Gemini."
    return answer, round(end - start, 2)

# Streamlit app
st.title("Lance’s AI Model Comparison Tool")

user_question = st.text_input("Enter your question")

if st.button("Submit to Both Models") and user_question:
    with st.spinner("Getting responses..."):
        try:
            openai_answer, openai_time = ask_openai(user_question)
        except Exception as e:
            openai_answer = f"Error: {e}"
            openai_time = None

        try:
            gemini_answer, gemini_time = ask_gemini(user_question)
        except Exception as e:
            gemini_answer = f"Error: {e}"
            gemini_time = None

    st.subheader("ChatGPT (OpenAI)")
    st.write(openai_answer)
    if openai_time is not None:
        st.caption(f"Response time: {openai_time} seconds")

    st.subheader("Gemini (Google)")
    st.write(gemini_answer)
    if gemini_time is not None:
        st.caption(f"Response time: {gemini_time} seconds")
