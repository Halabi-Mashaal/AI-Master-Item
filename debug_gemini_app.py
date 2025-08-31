#!/usr/bin/env python3
"""
Debug version of Yamama Cement AI Agent for troubleshooting Gemini API
"""
import os
import json
import time
import logging
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Debug environment variables
print("🔍 ENVIRONMENT DEBUG:")
print(f"GOOGLE_API_KEY from env: {os.getenv('GOOGLE_API_KEY', 'NOT_FOUND')}")
print(f"All environment variables containing 'GOOGLE': {[k for k in os.environ.keys() if 'GOOGLE' in k.upper()]}")
print(f"All environment variables containing 'API': {[k for k in os.environ.keys() if 'API' in k.upper()]}")

# Google Gemini AI Integration with multiple fallbacks
AI_AVAILABLE = False
model = None
api_key_source = "NONE"

try:
    import google.generativeai as genai
    print("✅ Google Generative AI library imported successfully")
    
    # Try multiple API key sources
    api_keys_to_try = [
        os.getenv('GOOGLE_API_KEY'),
        os.getenv('GEMINI_API_KEY'), 
        os.getenv('GOOGLE_GEMINI_API_KEY'),
        'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA'  # Hardcoded fallback
    ]
    
    for i, api_key in enumerate(api_keys_to_try):
        if api_key and api_key != 'your-api-key-here' and len(api_key) > 20:
            try:
                print(f"🔑 Trying API key #{i+1}: {api_key[:10]}...{api_key[-4:]}")
                genai.configure(api_key=api_key)
                
                # Test the API key by making a simple request
                model = genai.GenerativeModel('gemini-1.5-flash')
                test_response = model.generate_content("Hello")
                
                if test_response and test_response.text:
                    AI_AVAILABLE = True
                    api_key_source = f"KEY_{i+1}"
                    print(f"✅ API Key #{i+1} works! Source: {api_key_source}")
                    print(f"Test response: {test_response.text[:50]}...")
                    break
                else:
                    print(f"❌ API Key #{i+1} returned empty response")
                    
            except Exception as e:
                print(f"❌ API Key #{i+1} failed: {str(e)}")
                continue
    
    if not AI_AVAILABLE:
        print("❌ All API keys failed")
        
except ImportError as e:
    print(f"❌ Failed to import google.generativeai: {e}")
except Exception as e:
    print(f"❌ Unexpected error during AI initialization: {e}")

def get_ai_response(message, language='en'):
    """Get AI response using Google Gemini with extensive debugging"""
    debug_info = {
        "ai_available": AI_AVAILABLE,
        "api_key_source": api_key_source,
        "message_length": len(message),
        "language": language,
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"AI Request Debug: {debug_info}")
    
    if not AI_AVAILABLE:
        error_msg = f"🔧 DEBUG: AI not available. Check logs. API Source: {api_key_source}"
        if language == 'ar':
            return f"خدمات الذكاء الاصطناعي غير متاحة. المصدر: {api_key_source}"
        return error_msg
    
    try:
        # Create context-aware prompt
        if language == 'ar':
            system_prompt = """أنت مساعد ذكي لشركة أسمنت اليمامة السعودية. أجب باللغة العربية وكن مفيداً ومهنياً.
تخصصك في إدارة المستودعات والمخزون وصناعة الأسمنت."""
        else:
            system_prompt = """You are an intelligent assistant for Yamama Cement Company. Be helpful and professional.
Your expertise includes warehouse management, inventory, and cement industry operations."""
        
        full_prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
        
        logger.info(f"Sending prompt to Gemini (length: {len(full_prompt)})")
        response = model.generate_content(full_prompt)
        
        if response and response.text:
            logger.info(f"Received response from Gemini (length: {len(response.text)})")
            return f"✅ SUCCESS: {response.text}"
        else:
            logger.error("Empty response from Gemini API")
            return f"⚠️ DEBUG: Empty response from Gemini. API Source: {api_key_source}"
        
    except Exception as e:
        logger.error(f"AI response error: {str(e)}")
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "api_source": api_key_source
        }
        
        if language == 'ar':
            return f"عذراً، حدث خطأ: {error_details}"
        else:
            return f"🔧 DEBUG ERROR: {error_details}"

# Simple HTML template for testing
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🔧 Yamama AI Debug</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 800px; }
        .debug { background: #f0f0f0; padding: 15px; margin: 10px 0; border-left: 4px solid #2196F3; }
        input[type="text"] { width: 70%; padding: 10px; margin: 10px 5px; }
        button { padding: 10px 20px; background: #4CAF50; color: white; border: none; cursor: pointer; }
        .response { background: #e8f5e8; padding: 15px; margin: 15px 0; border-radius: 5px; }
        .error { background: #fee; border-left: 4px solid #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Yamama AI Debug Interface</h1>
        
        <div class="debug">
            <h3>Debug Information:</h3>
            <p><strong>AI Available:</strong> ''' + str(AI_AVAILABLE) + '''</p>
            <p><strong>API Key Source:</strong> ''' + api_key_source + '''</p>
            <p><strong>Model Loaded:</strong> ''' + str(model is not None) + '''</p>
            <p><strong>Environment Check:</strong> GOOGLE_API_KEY = ''' + str(bool(os.getenv('GOOGLE_API_KEY'))) + '''</p>
        </div>
        
        <div>
            <input type="text" id="message" placeholder="Enter your message for testing..." />
            <button onclick="sendMessage()">Test AI</button>
        </div>
        
        <div id="response" class="response" style="display:none;"></div>
    </div>
    
    <script>
        function sendMessage() {
            const message = document.getElementById('message').value;
            const responseDiv = document.getElementById('response');
            
            if (!message) return;
            
            responseDiv.style.display = 'block';
            responseDiv.innerHTML = '🤖 Processing...';
            
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message, language: 'en'})
            })
            .then(response => response.json())
            .then(data => {
                responseDiv.innerHTML = '<strong>Response:</strong> ' + data.response;
            })
            .catch(error => {
                responseDiv.innerHTML = '<strong>Error:</strong> ' + error;
                responseDiv.className = 'response error';
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
def health_check():
    return jsonify({
        "status": "healthy",
        "ai_available": AI_AVAILABLE,
        "api_key_source": api_key_source,
        "model_loaded": model is not None,
        "debug_mode": True,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/debug')
def debug_info():
    return jsonify({
        "environment_vars": {k: v for k, v in os.environ.items() if 'API' in k.upper() or 'GOOGLE' in k.upper()},
        "ai_available": AI_AVAILABLE,
        "api_key_source": api_key_source,
        "model_loaded": model is not None,
        "python_version": os.sys.version,
        "current_directory": os.getcwd(),
        "imported_libraries": [
            "google.generativeai" if AI_AVAILABLE else "google.generativeai (FAILED)"
        ]
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        language = data.get('language', 'en')
        
        if not message:
            return jsonify({"response": "Please enter a message"})
        
        response = get_ai_response(message, language)
        
        return jsonify({
            "response": response,
            "debug": {
                "ai_available": AI_AVAILABLE,
                "api_key_source": api_key_source,
                "request_id": str(time.time())
            }
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({
            "response": f"🔧 DEBUG: Chat endpoint error: {str(e)}",
            "error_type": type(e).__name__
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"\n🚀 DEBUG APP STARTING ON PORT {port}")
    print(f"🤖 AI Status: {'✅ Active' if AI_AVAILABLE else '❌ Unavailable'}")
    print(f"🔑 API Key Source: {api_key_source}")
    print(f"📍 Visit /debug endpoint for detailed diagnostics\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True,
        threaded=True
    )
