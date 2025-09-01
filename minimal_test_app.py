#!/usr/bin/env python3
"""
ULTRA-MINIMAL RENDER TEST APP
Absolute minimal version to test Render deployment
"""
from flask import Flask, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

# Hardcoded API test
def test_api():
    try:
        import google.generativeai as genai
        genai.configure(api_key='AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA')
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'API working'")
        return f"✅ {response.text}" if response else "❌ No response"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route('/')
def home():
    return f"""
    <h1>🔧 YAMAMA AI RENDER TEST</h1>
    <p><strong>Time:</strong> {datetime.now()}</p>
    <p><strong>API Test:</strong> {test_api()}</p>
    <p><strong>Port:</strong> {os.environ.get('PORT', 'not set')}</p>
    <p><strong>Python:</strong> {os.environ.get('PYTHON_VERSION', 'not set')}</p>
    <hr>
    <p><a href="/chat">/chat</a> | <a href="/health">/health</a></p>
    """

@app.route('/health')
def health():
    api_status = test_api()
    return jsonify({
        'status': 'healthy',
        'time': datetime.now().isoformat(),
        'api_test': api_status,
        'port': os.environ.get('PORT')
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        import google.generativeai as genai
        genai.configure(api_key='AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA')
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        data = request.get_json() or {}
        message = data.get('message', 'Hello')
        
        response = model.generate_content(f"You are Yamama Cement AI assistant. Respond to: {message}")
        
        return jsonify({
            'status': 'success',
            'response': response.text if response else 'No response',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error', 
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 MINIMAL TEST APP STARTING ON PORT {port}")
    print(f"📊 API TEST: {test_api()}")
    app.run(host='0.0.0.0', port=port, debug=False)
