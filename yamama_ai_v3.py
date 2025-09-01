#!/usr/bin/env python3
"""
YAMAMA AI AGENT V3 - GUARANTEED WORKING VERSION
September 1, 2025 - Force fresh deployment
"""
import os
import json
import logging
from flask import Flask, jsonify, request, render_template_string, send_from_directory
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'yamama-cement-ai-2025-v3'

print("🚀 YAMAMA AI AGENT V3 - FRESH START")
print(f"📅 Deployment Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# HARDCODED Google Gemini Integration (NO ENVIRONMENT DEPENDENCIES)
AI_AVAILABLE = False
model = None

try:
    import google.generativeai as genai
    
    # HARDCODED API KEY - NO ENVIRONMENT VARIABLE DEPENDENCY
    API_KEY = 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA'
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # IMMEDIATE TEST
    test_response = model.generate_content("Test: Say 'Yamama AI is working'")
    if test_response and test_response.text:
        AI_AVAILABLE = True
        print(f"✅ GEMINI 1.5 FLASH WORKING: {test_response.text[:50]}...")
    else:
        print("❌ Test failed - no response")
        
except Exception as e:
    print(f"❌ Gemini initialization failed: {e}")
    AI_AVAILABLE = False

def get_ai_response(message, language='en'):
    """Get AI response with ZERO dependencies on environment variables"""
    if not AI_AVAILABLE:
        return "🔧 Gemini AI is temporarily offline. Please try again in a moment."
    
    try:
        if language == 'ar':
            prompt = f"""أنت مساعد ذكي لشركة أسمنت اليمامة السعودية. أجب باللغة العربية.
            
سؤال المستخدم: {message}

أجب بطريقة مهنية ومفيدة:"""
        else:
            prompt = f"""You are an AI assistant for Yamama Cement Company in Saudi Arabia. Provide helpful, professional responses about cement industry, warehouse management, and business operations.

User Question: {message}

Your Response:"""
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            return "⚠️ I received your message but couldn't generate a response. Please try again."
            
    except Exception as e:
        logger.error(f"AI Response Error: {e}")
        return f"🔧 Technical Error: {str(e)}. Please contact support."

# SIMPLE HTML INTERFACE
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yamama AI Agent V3</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2c5530, #1e3a22);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container { 
            background: rgba(255,255,255,0.95);
            color: #333;
            padding: 40px;
            border-radius: 20px;
            max-width: 900px;
            width: 100%;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        .header { text-align: center; margin-bottom: 30px; }
        .logo { max-width: 180px; margin-bottom: 15px; }
        h1 { color: #2c5530; font-size: 2.2em; margin-bottom: 10px; }
        .version-badge { 
            background: #2c5530; 
            color: white; 
            padding: 5px 15px; 
            border-radius: 20px; 
            font-size: 0.9em;
            display: inline-block;
            margin-bottom: 20px;
        }
        .status { 
            background: #d4edda; 
            border: 1px solid #c3e6cb;
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0;
            border-left: 5px solid #28a745;
        }
        .input-container { 
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin: 25px 0;
        }
        .input-group { display: flex; gap: 15px; margin-bottom: 15px; }
        .message-input { 
            flex: 1; 
            padding: 15px; 
            border: 2px solid #2c5530; 
            border-radius: 10px; 
            font-size: 16px;
            font-family: inherit;
        }
        .send-button { 
            background: #2c5530; 
            color: white; 
            border: none; 
            padding: 15px 25px; 
            border-radius: 10px; 
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: background 0.3s ease;
        }
        .send-button:hover { background: #1e3a22; }
        .response-area { 
            background: #ffffff;
            border: 2px solid #dee2e6;
            padding: 20px; 
            border-radius: 10px; 
            margin-top: 20px;
            min-height: 150px;
            display: none;
        }
        .response-area.show { display: block; }
        .loading { text-align: center; color: #6c757d; font-style: italic; }
        .debug-info { 
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            font-size: 0.9em;
        }
        @media (max-width: 768px) {
            .container { margin: 10px; padding: 25px; }
            .input-group { flex-direction: column; }
            .send-button { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="/static/yama.png" alt="Yamama Cement" class="logo" onerror="this.style.display='none'">
            <h1>🏭 Yamama Cement AI Assistant</h1>
            <div class="version-badge">Version 3.0 - September 2025</div>
            <p>Advanced AI-powered assistant for cement industry operations</p>
        </div>
        
        <div class="status">
            <h3>🤖 System Status</h3>
            <p><strong>AI Engine:</strong> Google Gemini 1.5 Flash</p>
            <p><strong>Status:</strong> ''' + ('✅ Online & Ready' if AI_AVAILABLE else '❌ Offline') + '''</p>
            <p><strong>Languages:</strong> English, العربية</p>
            <p><strong>Deployment:</strong> ''' + datetime.now().strftime("%Y-%m-%d %H:%M UTC") + '''</p>
        </div>
        
        <div class="input-container">
            <h3>💬 Chat with Yamama AI</h3>
            <div class="input-group">
                <input type="text" id="messageInput" class="message-input" 
                       placeholder="Ask about cement operations, inventory, quality control, or anything else...">
                <button onclick="sendMessage()" class="send-button">Send Message</button>
            </div>
            
            <div>
                <label>
                    <input type="radio" name="language" value="en" checked> English
                </label>
                &nbsp;&nbsp;&nbsp;
                <label>
                    <input type="radio" name="language" value="ar"> العربية
                </label>
            </div>
        </div>
        
        <div id="responseArea" class="response-area">
            <div id="responseContent"></div>
        </div>
        
        <div class="debug-info">
            <strong>🔧 Debug Info:</strong> This is Version 3.0 with hardcoded Gemini 1.5 Flash integration. 
            If you still see generic errors, please contact technical support.
        </div>
    </div>

    <script>
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
        
        async function sendMessage() {
            const messageInput = document.getElementById('messageInput');
            const message = messageInput.value.trim();
            const responseArea = document.getElementById('responseArea');
            const responseContent = document.getElementById('responseContent');
            
            if (!message) {
                alert('Please enter a message');
                return;
            }
            
            const language = document.querySelector('input[name="language"]:checked').value;
            
            // Show loading
            responseArea.className = 'response-area show';
            responseContent.innerHTML = '<div class="loading">🤖 Yamama AI is thinking...</div>';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message, language: language })
                });
                
                const data = await response.json();
                
                responseContent.innerHTML = 
                    '<h4>🤖 Yamama AI Response:</h4>' +
                    '<div style="margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 8px;">' +
                    data.response.replace(/\\n/g, '<br>') +
                    '</div>' +
                    '<small style="color: #6c757d;">Model: ' + (data.model || 'Gemini 1.5 Flash') + 
                    ' | Time: ' + new Date().toLocaleTimeString() + '</small>';
                
            } catch (error) {
                responseContent.innerHTML = 
                    '<div style="color: #dc3545; padding: 15px; background: #f8d7da; border-radius: 8px;">' +
                    '<strong>Connection Error:</strong> ' + error.message +
                    '</div>';
            }
            
            messageInput.value = '';
            messageInput.focus();
        }
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
        "version": "3.0",
        "ai_available": AI_AVAILABLE,
        "model": "gemini-1.5-flash",
        "deployment_time": datetime.now().isoformat(),
        "api_hardcoded": True
    })

@app.route('/test')
def test_endpoint():
    """Direct test of AI functionality"""
    if not AI_AVAILABLE:
        return jsonify({
            "success": False,
            "error": "AI not available",
            "ai_status": AI_AVAILABLE
        })
    
    try:
        test_msg = "Hello, this is a test. Please respond with: 'Yamama AI Version 3 is working perfectly'"
        response = get_ai_response(test_msg, "en")
        return jsonify({
            "success": True,
            "test_response": response,
            "model": "gemini-1.5-flash",
            "version": "3.0"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        message = data.get('message', '').strip()
        language = data.get('language', 'en')
        
        if not message:
            return jsonify({"response": "Please enter a message to continue."})
        
        # Get AI response
        ai_response = get_ai_response(message, language)
        
        return jsonify({
            "response": ai_response,
            "model": "gemini-1.5-flash",
            "version": "3.0",
            "language": language,
            "ai_available": AI_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify({
            "response": f"🔧 System Error: {str(e)}",
            "version": "3.0",
            "error": True
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    
    print(f"\n🚀 YAMAMA AI AGENT V3.0 STARTING")
    print(f"📊 AI Status: {'✅ READY' if AI_AVAILABLE else '❌ OFFLINE'}")
    print(f"🔧 Model: Gemini 1.5 Flash (Hardcoded)")
    print(f"🌐 Port: {port}")
    print(f"🔗 Test URL: /test")
    print(f"📋 Health Check: /health")
    print(f"⚡ Version: 3.0 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )
