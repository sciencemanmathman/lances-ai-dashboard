import streamlit as st
import openai
import google.generativeai as genai
import time
import os

# Set API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Streamlit UI
st.title("Lance’s AI Model Comparison Tool")
st.sidebar.title("Lance’s AI Model Comparison Tool")
st.sidebar.write("Enter your question below to compare how the top AI models respond.")

user_question = st.text_input("Your question")

if st.button("Submit to Both Models"):

    if not user_question:
        st.warning("Please enter a question.")
    else:
        # ChatGPT Response
        with st.spinner("ChatGPT is thinking..."):
            try:
                start_time = time.time()
                openai_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_question}]
                )
                openai_answer = openai_response['choices'][0]['message']['content']
                openai_tokens = openai_response['usage']['total_tokens']
                openai_time = round(time.time() - start_time, 2)
            except Exception as e:
                openai_answer = f"Error: {e}"
                openai_tokens = "N/A"
                openai_time = "N/A"

        # Gemini Response
        with st.spinner("Gemini is thinking..."):
            try:
                start_time = time.time()
                gemini_response = genai.GenerativeModel('gemini-pro').generate_content(user_question)
                gemini_answer = gemini_response.candidates[0].content.parts[0].text
                gemini_time = round(time.time() - start_time, 2)
            except Exception as e:
                gemini_answer = f"Error: {e}"
                gemini_time = "N/A"

        # Results
        st.header("ChatGPT")
        st.write(openai_answer)
        st.caption(f"Tokens used: {openai_tokens}")
        st.caption(f"Response time: {openai_time} seconds")

        st.header("Gemini")
        st.write(gemini_answer)
        st.caption(f"Response time: {gemini_time} seconds")
