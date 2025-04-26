
# Lance's AI Model Comparison Tool

This is a Streamlit web app that compares responses from **OpenAI (ChatGPT)** and **Google Gemini** models side-by-side.

[**▶️ Try the Live App**](https://zjak6kaz7pgbt.streamlit.app/)

---

## Features

- Enter a question once and get answers from both models.
- View tokens used (OpenAI) and response times.
- Built with Python, Streamlit, and the OpenAI + Gemini APIs.

## Getting Started

### 1. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/lances-ai-dashboard.git
cd lances-ai-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API keys to `.streamlit/secrets.toml`
```toml
OPENAI_API_KEY = "your-openai-key"
GEMINI_API_KEY = "your-gemini-key"
```

### 4. Run the app
```bash
streamlit run app.py
```

## Deployment

Deployed with [Streamlit Community Cloud](https://streamlit.io/cloud). To deploy your own:

1. Fork this repo
2. Upload your secrets
3. Point to `app.py` as your main file

## License

MIT © Lance
