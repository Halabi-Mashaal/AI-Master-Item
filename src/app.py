import os
import logging
from flask import Flask, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    logging.info("Home route accessed.")
    return jsonify({
        "message": "Master Item AI Agent is running!",
        "status": "active"
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    logging.info(f"Starting the app on host 0.0.0.0 and port {port}.")
    app.run(host="0.0.0.0", port=port, debug=False)
