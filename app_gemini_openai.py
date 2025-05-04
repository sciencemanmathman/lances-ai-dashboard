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
"bluefrog_auth", # cookie name
"abcdef123456", # signature key
cookie_expiry_days=30,
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
st.error("Username/password is incorrect")
elif authentication_status is None:
st.warning("Please enter your username and password")
elif authentication_status:
authenticator.logout("Logout", "sidebar")
st.title("Lance’s AI Model Comparison Tool")
st.write("Enter your question below:")

user_input = st.text_input("")

if st.button("Submit to Both Models"):
# OpenAI response
openai.api_key = st.secrets["OPENAI_API_KEY"]
try:
openai_response = openai.ChatCompletion.create(
model="gpt-4",
messages=[{"role": "user", "content": user_input}]
)
st.subheader("GPT-4 Response")
st.write(openai_response['choices'][0]['message']['content'])
except Exception as e:
st.error(f"OpenAI Error: {e}")

# Gemini response
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
try:
model = genai.GenerativeModel("gemini-pro")
gemini_response = model.generate_content(user_input)
st.subheader("Gemini Response")
st.write(gemini_response.text)
except Exception as e:
st.error(f"Gemini Error: {e}")
