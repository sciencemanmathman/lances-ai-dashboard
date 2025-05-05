import google.generativeai as genai
import json
import yaml
import streamlit as st
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

# Load credentials from users.json
with open("users.json") as f:
    users = json.load(f)

credentials = {
    "usernames": {
        email: {"name": email, "password": password}
        for email, password in users.items()
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "bluefrog_auth",       # Cookie name
    "abcdef123456",        # Signature key (keep this secret in production)
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login(
    "Login", fields=["Email", "Password"], location="main"
)

if authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
else:
    authenticator.logout("Logout", "sidebar")
    st.title("Lance's AI Model Comparison Tool")
    # Add the main app logic below
