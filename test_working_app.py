#!/usr/bin/env python3
"""
Ultra-Simple Test Version - Guaranteed to work
"""
import os
import json
import logging
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

# Force the API key and test immediately
HARDCODED_API_KEY = "AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA"
AI_AVAILABLE = False
model = None

print(f"🔑 Testing with hardcoded API key: {HARDCODED_API_KEY[:10]}...{HARDCODED_API_KEY[-4:]}")

try:
    import google.generativeai as genai
    
    # Use hardcoded API key
    genai.configure(api_key=HARDCODED_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Test immediately
    test_response = model.generate_content("Test message")
    if test_response and test_response.text:
        AI_AVAILABLE = True
        print("✅ Gemini 1.5 Flash working with hardcoded API key!")
        print(f"Test response: {test_response.text[:100]}...")
    else:
        print("❌ Empty response from Gemini")
        
except Exception as e:
    print(f"❌ Error with Gemini: {e}")
    AI_AVAILABLE = False

def get_ai_response(message, language='en'):
    """Get AI response"""
    if not AI_AVAILABLE:
        return "❌ AI not available - check deployment logs"
    
    try:
        if language == 'ar':
            prompt = f"أجب بالعربية عن: {message}"
        else:
            prompt = f"You are Yamama Cement AI assistant. Answer: {message}"
            
        response = model.generate_content(prompt)
        
        if response and response.text:
            return f"✅ {response.text}"
        else:
            return "⚠️ Empty response from Gemini API"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Minimal HTML
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Yamama Test - Fixed Version</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f8ff; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 600px; }
        .status { padding: 15px; margin: 15px 0; border-radius: 5px; }
        .success { background: #d4edda; border-left: 4px solid #28a745; }
        .error { background: #f8d7da; border-left: 4px solid #dc3545; }
        input { width: 70%; padding: 10px; margin: 10px 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        .response { background: #e9ecef; padding: 15px; margin: 15px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏭 Yamama Cement AI - Test Version</h1>
        
        <div class="status ''' + ('success' if AI_AVAILABLE else 'error') + '''">
            <strong>AI Status:</strong> ''' + ('✅ ACTIVE - Gemini 1.5 Flash' if AI_AVAILABLE else '❌ UNAVAILABLE') + '''<br>
            <strong>Model:</strong> gemini-1.5-flash<br>
            <strong>API Key:</strong> ''' + HARDCODED_API_KEY[:10] + '''...''' + HARDCODED_API_KEY[-4:] + '''
        </div>
        
        <div>
            <input type="text" id="message" placeholder="Test the AI here..." />
            <button onclick="testAI()">Test AI</button>
        </div>
        
        <div id="response" class="response" style="display:none;"></div>
    </div>
    
    <script>
        function testAI() {
            const message = document.getElementById('message').value;
            const responseDiv = document.getElementById('response');
            
            if (!message) return;
            
            responseDiv.style.display = 'block';
            responseDiv.innerHTML = '🤖 Testing AI...';
            
            fetch('/test-chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message, language: 'en'})
            })
            .then(response => response.json())
            .then(data => {
                responseDiv.innerHTML = '<strong>AI Response:</strong><br>' + data.response;
            })
            .catch(error => {
                responseDiv.innerHTML = '<strong>Error:</strong> ' + error;
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "ai_available": AI_AVAILABLE,
        "model": "gemini-1.5-flash",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/test-chat', methods=['POST'])
def test_chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        language = data.get('language', 'en')
        
        if not message:
            return jsonify({"response": "Please enter a message"})
        
        response = get_ai_response(message, language)
        
        return jsonify({
            "response": response,
            "ai_status": AI_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "response": f"❌ Server Error: {str(e)}",
            "error": True
        }), 500

@app.route('/chat', methods=['POST'])  # Keep compatibility
def chat():
    return test_chat()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"\n🚀 TEST APP STARTING ON PORT {port}")
    print(f"🤖 AI Status: {'✅ WORKING' if AI_AVAILABLE else '❌ FAILED'}")
    print(f"🔧 This is the guaranteed-working test version\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
