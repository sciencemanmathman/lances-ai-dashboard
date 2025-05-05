import streamlit as st
import streamlit_authenticator as stauth
import json
from yaml.loader import SafeLoader

# Load credentials from users.json
with open("users.json", "r") as f:
    users = json.load(f)

# Format credentials for streamlit_authenticator
credentials = {
    "usernames": {
        email: {"name": email.split("@")[0], "password": password}
        for email, password in users.items()
    }
}

# Create authenticator
authenticator = stauth.Authenticate(
    credentials,
    "bluefrog_auth",           # Cookie name
    "abcdef123456",            # Signature key (use a secure value in production)
    cookie_expiry_days=30
)

# Login widget
authentication_status, username = authenticator.login(
    "Login", fields=["Email", "Password"]
)

# Authentication logic
if authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
else:
    authenticator.logout("Logout", "sidebar")
    st.title("Lance's AI Model Comparison Tool")
    # Add your main app logic below
