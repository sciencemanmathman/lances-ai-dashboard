import streamlit as st
import openai
import google.generativeai as genai
import json
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

# Load credentials from users.json
with open("users.json") as f:
    users = json.load(f)

credentials = {
    "usernames": {
        email: {"name": email.split('@')[0], "password": password}
        for email, password in users.items()
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "bluefrog_auth",  # cookie name
    "abcdef123456",   # signature key (change this for production)
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Username or password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")

if authentication_status:
    st.title("Lance’s AI Model Comparison Tool")
    question = st.text_input("Enter your question")

    if st.button("Submit to Both Models") and question:
        # Replace with actual OpenAI & Gemini logic
        st.subheader("OpenAI Response:")
        st.write("...")

        st.subheader("Gemini Response:")
        st.write("...")
