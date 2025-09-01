#!/usr/bin/env python3
"""
RENDER DEBUG APP - ULTIMATE TROUBLESHOOTING
This app provides extensive logging and debugging information
to identify exactly what's happening on Render
"""
from flask import Flask, jsonify, request, Response
import os
import sys
import traceback
import logging
from datetime import datetime
import json

# Configure extensive logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global debug info
DEBUG_INFO = {
    'startup_time': datetime.now().isoformat(),
    'python_version': sys.version,
    'python_path': sys.executable,
    'working_directory': os.getcwd(),
    'environment_variables': dict(os.environ),
    'sys_path': sys.path,
    'modules_loaded': list(sys.modules.keys()),
    'errors': []
}

print("🔧 RENDER DEBUG APP STARTING")
print("=" * 50)
print(f"📅 Startup Time: {DEBUG_INFO['startup_time']}")
print(f"🐍 Python: {DEBUG_INFO['python_version'][:50]}...")
print(f"📁 Working Dir: {DEBUG_INFO['working_directory']}")

# Test Google Gemini immediately on startup
print("\n🧪 TESTING GOOGLE GEMINI API...")
GEMINI_STATUS = "unknown"
GEMINI_ERROR = None
GEMINI_RESPONSE = None

try:
    import google.generativeai as genai
    print("✅ google.generativeai imported successfully")
    
    api_key = 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA'
    genai.configure(api_key=api_key)
    print(f"✅ API configured with key: {api_key[:10]}...")
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ Model created: gemini-1.5-flash")
    
    test_response = model.generate_content("RENDER DEBUG: Say 'Gemini working on Render'")
    if test_response and test_response.text:
        GEMINI_STATUS = "working"
        GEMINI_RESPONSE = test_response.text
        print(f"✅ GEMINI WORKING: {GEMINI_RESPONSE[:50]}...")
    else:
        GEMINI_STATUS = "no_response"
        print("❌ No response from Gemini")
        
except Exception as e:
    GEMINI_STATUS = "error"
    GEMINI_ERROR = str(e)
    DEBUG_INFO['errors'].append(f"Gemini setup error: {e}")
    print(f"❌ GEMINI ERROR: {e}")
    traceback.print_exc()

print(f"🔍 Final Gemini Status: {GEMINI_STATUS}")
print("=" * 50)

@app.route('/')
def home():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔧 RENDER DEBUG DASHBOARD</title>
        <style>
            body {{ font-family: monospace; margin: 20px; background: #1a1a1a; color: #00ff00; }}
            .status {{ padding: 10px; margin: 10px 0; background: #333; border-radius: 5px; }}
            .working {{ background: #004400 !important; }}
            .error {{ background: #440000 !important; }}
            .warning {{ background: #444400 !important; }}
            pre {{ background: #222; padding: 10px; overflow: auto; max-height: 300px; }}
        </style>
    </head>
    <body>
        <h1>🔧 YAMAMA AI RENDER DEBUG DASHBOARD</h1>
        
        <div class="status {'working' if GEMINI_STATUS == 'working' else 'error'}">
            <h2>📊 GEMINI API STATUS: {GEMINI_STATUS.upper()}</h2>
            <p><strong>Response:</strong> {GEMINI_RESPONSE or 'None'}</p>
            <p><strong>Error:</strong> {GEMINI_ERROR or 'None'}</p>
        </div>
        
        <div class="status">
            <h2>⏰ SYSTEM INFO</h2>
            <p><strong>Startup:</strong> {DEBUG_INFO['startup_time']}</p>
            <p><strong>Python:</strong> {DEBUG_INFO['python_version']}</p>
            <p><strong>Directory:</strong> {DEBUG_INFO['working_directory']}</p>
        </div>
        
        <div class="status">
            <h2>🌍 ENVIRONMENT</h2>
            <p><strong>PORT:</strong> {os.environ.get('PORT', 'not set')}</p>
            <p><strong>PYTHON_VERSION:</strong> {os.environ.get('PYTHON_VERSION', 'not set')}</p>
            <p><strong>FLASK_ENV:</strong> {os.environ.get('FLASK_ENV', 'not set')}</p>
            <p><strong>APP_VERSION:</strong> {os.environ.get('APP_VERSION', 'not set')}</p>
        </div>
        
        <div class="status">
            <h2>🔗 ENDPOINTS</h2>
            <p><a href="/health" style="color: #00ff00;">/health</a> - Health check</p>
            <p><a href="/debug" style="color: #00ff00;">/debug</a> - Full debug info</p>
            <p><a href="/chat" style="color: #00ff00;">/chat</a> - POST chat test</p>
            <p><a href="/test-gemini" style="color: #00ff00;">/test-gemini</a> - Direct Gemini test</p>
        </div>
        
        <h2>📝 ERRORS ({len(DEBUG_INFO['errors'])})</h2>
        <pre>{'<br>'.join(DEBUG_INFO['errors']) if DEBUG_INFO['errors'] else 'No errors'}</pre>
    </body>
    </html>
    """
    return html

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'gemini_status': GEMINI_STATUS,
        'gemini_response': GEMINI_RESPONSE,
        'gemini_error': GEMINI_ERROR,
        'startup_time': DEBUG_INFO['startup_time'],
        'python_version': DEBUG_INFO['python_version'][:50],
        'working_directory': DEBUG_INFO['working_directory'],
        'port': os.environ.get('PORT'),
        'errors_count': len(DEBUG_INFO['errors'])
    })

@app.route('/debug')
def debug():
    return jsonify(DEBUG_INFO)

@app.route('/test-gemini')
def test_gemini():
    try:
        import google.generativeai as genai
        genai.configure(api_key='AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA')
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        test_message = f"LIVE TEST from Render at {datetime.now().strftime('%H:%M:%S')}"
        response = model.generate_content(test_message)
        
        return jsonify({
            'status': 'success',
            'test_message': test_message,
            'gemini_response': response.text if response else None,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if request.method == 'GET':
        return jsonify({'message': 'Use POST with JSON: {"message": "your message"}'})
    
    try:
        data = request.get_json() or {}
        user_message = data.get('message', 'Hello from Render debug')
        
        if GEMINI_STATUS != 'working':
            return jsonify({
                'status': 'error',
                'error': f'Gemini not working: {GEMINI_STATUS}',
                'gemini_error': GEMINI_ERROR,
                'response': 'I apologize, but I encountered an error processing your request. Please try again.',
                'timestamp': datetime.now().isoformat()
            }), 500
        
        import google.generativeai as genai
        genai.configure(api_key='AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA')
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"You are Yamama Cement Company's AI assistant. Respond professionally to: {user_message}"
        response = model.generate_content(prompt)
        
        return jsonify({
            'status': 'success',
            'response': response.text if response else 'No response generated',
            'user_message': user_message,
            'gemini_status': GEMINI_STATUS,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        error_info = {
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc(),
            'user_message': data.get('message') if 'data' in locals() else 'unknown',
            'gemini_status': GEMINI_STATUS,
            'response': 'I apologize, but I encountered an error processing your request. Please try again.',
            'timestamp': datetime.now().isoformat()
        }
        
        # Log the error
        DEBUG_INFO['errors'].append(f"Chat error: {e}")
        logger.error(f"Chat error: {e}", exc_info=True)
        
        return jsonify(error_info), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"\n🚀 DEBUG APP STARTING ON PORT {port}")
    print(f"📊 GEMINI STATUS: {GEMINI_STATUS}")
    print(f"🌐 Access at: http://0.0.0.0:{port}/")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=False)
