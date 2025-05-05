import streamlit as st
import streamlit_authenticator as stauth
import json
import yaml
from yaml.loader import SafeLoader
import google.generativeai as genai

# Load credentials from users.json
with open("users.json") as f:
    users = json.load(f)

# Reformat users into credentials dict
credentials = {
    "usernames": {}
}

for email, password in users.items():
    credentials["usernames"][email] = {
        "name": email.split("@")[0],
        "password": password
    }

# Setup the authenticator
authenticator = stauth.Authenticate(
    credentials,
    "bluefrog_auth",                # Cookie name
    "abcdef123456",                 # Signature key
    cookie_expiry_days=30
)

# Login
name, authentication_status, username = authenticator.login("Login", location="main")

if authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
else:
    authenticator.logout("Logout", "sidebar")
    st.title("Lance's AI Model Comparison Tool")

    # Place your app's core logic below here
    st.write("Welcome,", name)
    st.write("Your AI dashboard will appear here.")
