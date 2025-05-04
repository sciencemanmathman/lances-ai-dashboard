import streamlit as st
import openai
import google.generativeai as genai
import json
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

# Load user credentials from users.json
with open("users.json") as f:
    users = json.load(f)

credentials = {
    "usernames": {
        email: {"name": email.split("@")[0], "password": password}
        for email, password in users.items()
    }
}

# Setup authenticator
authenticator = stauth.Authenticate(
    credentials,
    "bluefrog_auth",     # Cookie name
    "abcdef123456",      # Signature key (replace with a secure one)
    cookie_expiry_days=30
)

# Show login form
name, authentication_status, username = authenticator.login("Login", location="main", fields=["Email", "Password"])

# Handle login outcomes
if authentication_status is False:
    st.error("Username/password is incorrect")

elif authentication_status is None:
    st.warning("Please enter your username and password")

elif authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.title("Lance's AI Model Comparison Tool")

    question = st.text_input("Enter your question")

    if question:
        st.write("Pretend this is a call to OpenAI and Gemini APIs.")
        st.write(f"Your question: {question}")
        st.success("Success! You are authenticated.")
