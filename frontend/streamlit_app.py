import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env or Streamlit secrets
if os.path.exists(".env"):
    load_dotenv()
else:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["OPENAI_API_BASE"] = st.secrets["OPENAI_API_BASE"]

st.title("🗺️ Dharashiv District Chatbot 🤖")
st.markdown("Ask anything about Dharashiv district based on government site content.")

# Model selection
model = st.selectbox("Choose a model:", [
    "mistralai/mistral-7b-instruct",
    "meta-llama/llama-3-8b-instruct",
    "openchat/openchat-3.5-1210"
])

# User input
query = st.text_input("💬 Your question:")

# Send query to backend
if st.button("Ask") and query:
    with st.spinner("Thinking..."):
        try:
            response = requests.post("http://localhost:5001/chat", json={"query": query, "model": model})
            raw_response = response.json()
            st.markdown("**✅ Answer:**")
            st.success(raw_response["response"])

            # Show raw response for debugging
            with st.expander("📦 Backend raw response"):
                st.json(raw_response)

        except Exception as e:
            st.error(f"❌ Error: {e}")
