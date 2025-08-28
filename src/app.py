import os
import asyncio
import logging
from flask import Flask, request, Response
import spacy
from spacy.cli import download

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Ensure the model is available
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

@app.route('/')
def home():
    return "Master Item AI Agent is running!"

@app.route("/api/messages", methods=["POST"])
def messages():
    """
    Endpoint for Microsoft Teams messages.
    """
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    # Process message with spaCy
    message = body.get("text", "")
    doc = nlp(message)

    # Extract entities and intent
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    response_text = f"You said: {message}. Detected entities: {entities}"

    return Response(response_text, status=200)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
