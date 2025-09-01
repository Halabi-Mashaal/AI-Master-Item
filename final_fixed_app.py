#!/usr/bin/env python3
"""
FINAL FIXED VERSION - Yamama Cement AI Agent with FORCED Gemini 1.5 Flash
"""
import os
import json
import time
import logging
from flask import Flask, jsonify, request, render_template_string, send_from_directory
from datetime import datetime

# Force environment setup
os.environ.setdefault('GOOGLE_API_KEY', 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

print("🔧 FINAL VERSION - FORCING GEMINI-1.5-FLASH")

# FORCED Google Gemini AI Integration
AI_AVAILABLE = False
model = None
API_KEY = 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA'  # Hardcoded as backup

try:
    import google.generativeai as genai
    print("✅ Google Generative AI library imported successfully")
    
    # Force configure with hardcoded key
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')  # FORCED MODEL NAME
    
    # Test the connection immediately
    test_response = model.generate_content("Test connection")
    if test_response and test_response.text:
        AI_AVAILABLE = True
        print("✅ GEMINI-1.5-FLASH CONFIRMED WORKING")
        print(f"✅ Test response: {test_response.text[:50]}...")
    else:
        print("❌ Test response failed")
        
except Exception as e:
    print(f"❌ AI initialization failed: {e}")
    AI_AVAILABLE = False

def get_ai_response(message, language='en'):
    """Get AI response using FORCED Gemini 1.5 Flash"""
    if not AI_AVAILABLE:
        return "🔧 AI system temporarily unavailable. Please contact support."
    
    try:
        # Context prompt
        if language == 'ar':
            prompt = f"""أنت مساعد ذكي لشركة أسمنت اليمامة السعودية. أجب باللغة العربية بشكل مفيد ومهني.

المستخدم: {message}
المساعد:"""
        else:
            prompt = f"""You are an intelligent assistant for Yamama Cement Company. Be helpful and professional.

User: {message}
Assistant:"""
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            return "⚠️ Empty response received. Please try again."
            
    except Exception as e:
        logger.error(f"AI error: {e}")
        return f"🔧 AI Error: {str(e)}"

# Simple HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yamama AI - FIXED VERSION</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #4CAF50, #2196F3); min-height: 100vh; }
        .container { background: white; padding: 30px; border-radius: 15px; max-width: 800px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .header { text-align: center; margin-bottom: 30px; }
        .logo { max-width: 200px; margin-bottom: 15px; }
        .status { background: #e8f5e8; padding: 15px; border-radius: 10px; margin: 20px 0; }
        .input-area { display: flex; gap: 10px; margin: 20px 0; }
        .input-field { flex: 1; padding: 15px; border: 2px solid #ddd; border-radius: 25px; font-size: 16px; }
        .send-btn { padding: 15px 25px; background: #4CAF50; color: white; border: none; border-radius: 25px; cursor: pointer; font-weight: bold; }
        .send-btn:hover { background: #45a049; }
        .response { background: #f9f9f9; padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #4CAF50; }
        .debug { background: #fff3cd; padding: 10px; border-radius: 5px; font-size: 12px; color: #856404; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="/static/yama.png" alt="Yamama Cement" class="logo" onerror="this.style.display='none'">
            <h1>🏭 Yamama AI Assistant - FIXED VERSION</h1>
            <p>Powered by Google Gemini 1.5 Flash</p>
        </div>
        
        <div class="status">
            <strong>🤖 System Status:</strong><br>
            AI Available: ''' + str(AI_AVAILABLE) + '''<br>
            Model: Gemini 1.5 Flash (FORCED)<br>
            Version: FINAL-FIXED<br>
            Deployment: ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''
        </div>
        
        <div class="input-area">
            <input type="text" id="message" class="input-field" placeholder="Ask about cement operations, inventory, or anything else..." />
            <button class="send-btn" onclick="sendMessage()">Send</button>
        </div>
        
        <div id="response" class="response" style="display:none;"></div>
        
        <div class="debug">
            DEBUG INFO: This is the FINAL FIXED version with hardcoded Gemini 1.5 Flash model.
            If you still see generic errors, there's a deployment caching issue.
        </div>
    </div>
    
    <script>
        function sendMessage() {
            const message = document.getElementById('message').value.trim();
            const responseDiv = document.getElementById('response');
            
            if (!message) return;
            
            responseDiv.style.display = 'block';
            responseDiv.innerHTML = '🤖 Processing with Gemini 1.5 Flash...';
            
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message, language: 'en'})
            })
            .then(response => response.json())
            .then(data => {
                responseDiv.innerHTML = '<strong>AI Response:</strong><br>' + data.response + 
                    '<div style="margin-top:10px; font-size:12px; color:#666;">Version: FINAL-FIXED | Model: ' + 
                    (data.model || 'gemini-1.5-flash') + '</div>';
            })
            .catch(error => {
                responseDiv.innerHTML = '<strong>Error:</strong> ' + error;
            });
            
            document.getElementById('message').value = '';
        }
        
        document.getElementById('message').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/static/<filename>')
def serve_static(filename):
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if os.path.exists(os.path.join(static_dir, filename)):
        return send_from_directory(static_dir, filename)
    return '', 404

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "ai_available": AI_AVAILABLE,
        "model": "gemini-1.5-flash-FORCED",
        "version": "FINAL-FIXED",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/test')
def test_ai():
    """Direct AI test endpoint"""
    if not AI_AVAILABLE:
        return jsonify({"error": "AI not available", "ai_status": AI_AVAILABLE})
    
    try:
        response = get_ai_response("Hello, test response", "en")
        return jsonify({
            "success": True,
            "response": response,
            "model": "gemini-1.5-flash",
            "version": "FINAL-FIXED"
        })
    except Exception as e:
        return jsonify({"error": str(e), "model": "gemini-1.5-flash"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        message = data.get('message', '').strip()
        language = data.get('language', 'en')
        
        if not message:
            return jsonify({"response": "Please enter a message"})
        
        response = get_ai_response(message, language)
        
        return jsonify({
            "response": response,
            "model": "gemini-1.5-flash",
            "version": "FINAL-FIXED",
            "ai_available": AI_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({
            "response": f"🔧 System Error: {str(e)}",
            "model": "gemini-1.5-flash",
            "version": "FINAL-FIXED"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"\n🚀 FINAL FIXED VERSION STARTING")
    print(f"🤖 AI Status: {'✅ ACTIVE' if AI_AVAILABLE else '❌ UNAVAILABLE'}")
    print(f"🔧 Model: GEMINI-1.5-FLASH (FORCED)")
    print(f"🌐 Port: {port}")
    print(f"🔗 Test endpoint: /test")
    print(f"📊 Health check: /health\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )
