from flask import Flask, render_template, request, jsonify
import requests
import webbrowser
from threading import Timer

app = Flask(__name__)

key = "votre_clé_api_groq_ici"  # Remplacez par votre clé API Groq

API_KEY = key

def ask_groq(question):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "Tu es Hope Assistant, assistant étudiant intelligent."},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()["choices"][0]["message"]["content"]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    question = request.json["question"]

    try:
        reponse = ask_groq(question)
    except Exception as e:
        reponse = f"Erreur : {str(e)}"

    return jsonify({"reponse": reponse})


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True)