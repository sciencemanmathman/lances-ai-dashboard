import streamlit as st
import streamlit_authenticator as stauth
import json
from yaml.loader import SafeLoader

# Load credentials from users.json
with open("users.json", "r") as f:
    config = json.load(f)

# Create authenticator
authenticator = stauth.Authenticate(
    config["usernames"],
    "bluefrog_auth",           # Cookie name
    "abcdef123456",            # Signature key
    cookie_expiry_days=30
)

# Login widget
name, authentication_status, username = authenticator.login("Login", location="main")


# Authentication logic
if authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
else:
    authenticator.logout("Logout", "sidebar")
    st.title("Lance's AI Model Comparison Tool")
    # Add your app logic below
