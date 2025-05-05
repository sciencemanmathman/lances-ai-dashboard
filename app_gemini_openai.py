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
        email: {"name": email.split("@")[0], "password": password}
        for email, password in users.items()
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "bluefrog_auth",  # cookie name
    "abcdef123456",   # signature key (replace with a secure one)
    cookie_expiry_days=30
)

# Login
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
else:
    authenticator.logout("Logout", "sidebar")
    st.title("Lance’s AI Model Comparison Tool")

    # The rest of your app code goes here
    st.write("Welcome to the dashboard!")
