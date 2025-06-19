import streamlit as st
import requests

st.set_page_config(page_title="Dharashiv District Chatbot", page_icon="🤖")
st.title("🗺️ Dharashiv District Chatbot 🤖")
st.write("Ask anything about Dharashiv district based on government site content.")

# Model selector
model = st.selectbox(
    "Choose a model:",
    ["mistralai/mistral-7b-instruct", "meta-llama/llama-3-8b-instruct", "openchat/openchat-3.5-1210"]
)

# Input box
query = st.text_input("💬 Your question:")

# Submit button
if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:5001/chat",
                    json={"query": query, "model": model},
                    timeout=30  # optional: avoid hanging
                )
                # Debug: show raw backend text (temporarily)
                st.code("Backend raw response:\n" + response.text)

                # Safely parse JSON
                data = response.json()
                st.success("✅ Answer:")
                st.write(data.get("response", "No response found."))
            except requests.exceptions.RequestException as e:
                st.error("❌ Error: Could not reach the backend.")
                st.code(str(e))
            except ValueError as e:
                st.error("❌ Error: Could not parse backend response as JSON.")
                st.code(response.text)
