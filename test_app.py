"""
Simple test application for debugging
"""
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['USE_LIGHTWEIGHT_NLP'] = '1'
os.environ['DISABLE_HEAVY_MODELS'] = '1'
os.environ['AI_PROVIDER'] = 'gemini'
os.environ['GEMINI_API_KEY'] = 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA'

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': '2025-08-31T12:00:00Z',
        'ai_provider': 'gemini',
        'lightweight_mode': True
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', 'Hello')
        
        # Simple response without heavy AI
        response = f"I received your message: '{message}'. The Yamama AI Agent is working!"
        
        return jsonify({
            'response': response,
            'timestamp': '2025-08-31T12:00:00Z',
            'provider': 'test'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return """
    <html>
    <head><title>Yamama Warehouse AI Agent</title></head>
    <body style="font-family: Arial; padding: 20px; background: linear-gradient(135deg, #4CAF50, #2196F3); color: white;">
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
            <h1>🚀 Yamama Warehouse AI Agent</h1>
            <p>Your intelligent assistant for warehouse management and optimization</p>
            <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h3>🤖 AI Agent Status: ONLINE</h3>
                <p>✅ Lightweight mode active</p>
                <p>✅ Fast startup completed</p>
                <p>✅ Ready to process requests</p>
            </div>
            <p><strong>API Endpoints:</strong></p>
            <ul>
                <li><code>/health</code> - Health check</li>
                <li><code>/chat</code> - Chat with AI (POST)</li>
            </ul>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🚀 Starting Yamama AI Agent (Test Mode)")
    print("✅ Lightweight mode enabled")
    print("✅ No heavy model loading")
    app.run(debug=False, host='0.0.0.0', port=8000)
