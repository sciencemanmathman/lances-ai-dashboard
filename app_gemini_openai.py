import streamlit as st
import streamlit_authenticator as stauth
import json
from yaml.loader import SafeLoader

# Load credentials from users.json
with open("users.json", "r") as f:
    users = json.load(f)

# Format credentials as expected by stauth
credentials = {
    "usernames": {
        email: {"name": email.split("@")[0], "password": password}
        for email, password in users.items()
    }
}

# Create the authenticator object
authenticator = stauth.Authenticate(
    credentials,
    "bluefrog_auth",         # Cookie name
    "abcdef123456",          # Signature key (keep secret in production)
    cookie_expiry_days=30
)

# Render login widget
name, authentication_status, username = authenticator.login("Login", fields=["Email", "Password"], location="main")

# Handle authentication status
if authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
else:
    authenticator.logout("Logout", "sidebar")
    st.title("Lance's AI Model Comparison Tool")
    st.write(f"Welcome, {name}!")

    # --- ADD YOUR APP CODE BELOW THIS LINE ---
    st.write("This is where your app content will go.")
