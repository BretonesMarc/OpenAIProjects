import openai
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

openai.api_key = os.environ["OPENAI_API_KEY"]

def chat_with_gpt3(message, conversation_history):
    prompt = f"{conversation_history}\nUser: {message}\nAI:"
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data["message"]
    conversation_history = data.get("conversation_history", "")
    response = chat_with_gpt3(message, conversation_history)
    return jsonify({"response": response})

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
