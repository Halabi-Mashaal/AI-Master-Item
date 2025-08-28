import os
import asyncio
import logging
from flask import Flask, request, Response

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

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

    # Custom message handling logic
    message = body.get("text", "").lower()

    if "hello" in message:
        response_text = "Hi there! How can I assist you today?"
    elif "help" in message:
        response_text = "Sure! Let me know what you need help with."
    else:
        response_text = f"Sorry, I didn't understand that. You said: {message}"

    return Response(response_text, status=200)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
