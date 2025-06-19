from dotenv import load_dotenv
load_dotenv()  # Load API keys from .env file into os.environ

from flask import Flask, request, jsonify
from qa_chain import get_chain

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "")
    model = data.get("model", "mistralai/mistral-7b-instruct")  # Default fallback

    try:
        chain = get_chain(model)
        result = chain.invoke({"question": query, "chat_history": []})
        return jsonify({"response": result.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001)
