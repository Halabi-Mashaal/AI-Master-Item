"""
Test AI Integration - Minimal Flask App
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, render_template_string

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import Advanced AI Models
try:
    from ai_models import get_ai_response, analyze_uploaded_file, ai_provider
    ADVANCED_AI_AVAILABLE = True
    print(f"✅ Advanced AI integration loaded - Provider: {ai_provider.provider}")
except ImportError as e:
    print(f"❌ Advanced AI not available: {e}")
    ADVANCED_AI_AVAILABLE = False

app = Flask(__name__)
app.secret_key = 'test_ai_key_12345'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Test HTML template
TEST_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Integration Test</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 10px 0; }
        .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .success { background: #d4edda; color: #155724; }
        .warning { background: #fff3cd; color: #856404; }
        .error { background: #f8d7da; color: #721c24; }
        textarea { width: 100%; height: 100px; margin: 10px 0; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .response { background: white; padding: 15px; border: 1px solid #ddd; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>🤖 AI Integration Test</h1>
    
    <div class="container">
        <h2>AI Provider Status</h2>
        <div id="status">{{ status_message }}</div>
    </div>
    
    <div class="container">
        <h2>Test AI Chat</h2>
        <textarea id="message" placeholder="Enter your message here...">Hello, can you help me analyze cement production data?</textarea>
        <button onclick="sendMessage()">Send Message</button>
        <div id="response"></div>
    </div>
    
    <div class="container">
        <h2>Configuration Instructions</h2>
        <div class="status warning">
            <h3>🚀 To enable AI-powered responses:</h3>
            <ol>
                <li>Get an API key from <a href="https://platform.openai.com/api-keys">OpenAI</a> or <a href="https://makersuite.google.com/app/apikey">Google AI Studio</a></li>
                <li>Open the <code>.env</code> file in the root directory</li>
                <li>Replace <code>your_openai_api_key_here</code> with your actual API key</li>
                <li>Set <code>AI_PROVIDER=openai</code> or <code>AI_PROVIDER=gemini</code></li>
                <li>Restart the application</li>
            </ol>
        </div>
    </div>
    
    <script>
        async function sendMessage() {
            const message = document.getElementById('message').value;
            const responseDiv = document.getElementById('response');
            
            if (!message.trim()) {
                alert('Please enter a message');
                return;
            }
            
            responseDiv.innerHTML = '<div class="response">⏳ Generating AI response...</div>';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                });
                
                const data = await response.json();
                
                if (data.success) {
                    responseDiv.innerHTML = '<div class="response"><strong>AI Response:</strong><br>' + data.response.replace(/\\n/g, '<br>') + '</div>';
                } else {
                    responseDiv.innerHTML = '<div class="response error">Error: ' + data.error + '</div>';
                }
            } catch (error) {
                responseDiv.innerHTML = '<div class="response error">Connection error: ' + error + '</div>';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main test page"""
    
    # Get AI provider status
    if ADVANCED_AI_AVAILABLE:
        status = ai_provider.get_provider_status()
        if status['current_provider'] == 'fallback':
            status_message = """
            <div class="status warning">
                <strong>⚠️ Fallback Mode Active</strong><br>
                AI providers not configured. Add API keys to unlock advanced features.
            </div>
            """
        elif status['openai_configured']:
            status_message = """
            <div class="status success">
                <strong>✅ OpenAI Configured</strong><br>
                Advanced AI responses enabled with GPT-3.5-turbo
            </div>
            """
        elif status['gemini_configured']:
            status_message = """
            <div class="status success">
                <strong>✅ Gemini Configured</strong><br>
                Advanced AI responses enabled with Gemini Pro
            </div>
            """
        else:
            status_message = """
            <div class="status warning">
                <strong>⚠️ AI Libraries Available</strong><br>
                Configure API keys to enable advanced features
            </div>
            """
    else:
        status_message = """
        <div class="status error">
            <strong>❌ AI Integration Error</strong><br>
            Could not load AI models
        </div>
        """
    
    return render_template_string(TEST_HTML, status_message=status_message)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Test AI chat endpoint"""
    
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'success': False, 'error': 'No message provided'})
        
        if ADVANCED_AI_AVAILABLE:
            # Create context for the AI
            context = {
                'conversation_length': 0,
                'technical_level': 'intermediate',
                'has_files': False
            }
            
            # Get AI response
            ai_response = get_ai_response(message, context)
            
            return jsonify({
                'success': True, 
                'response': ai_response,
                'provider': ai_provider.provider
            })
        else:
            return jsonify({
                'success': False, 
                'error': 'AI integration not available'
            })
            
    except Exception as e:
        logging.error(f"Chat error: {e}")
        return jsonify({
            'success': False, 
            'error': f'Server error: {str(e)}'
        })

@app.route('/api/status')
def status():
    """Get AI provider status"""
    
    if ADVANCED_AI_AVAILABLE:
        status = ai_provider.get_provider_status()
        return jsonify({
            'success': True,
            'ai_available': True,
            'status': status
        })
    else:
        return jsonify({
            'success': False,
            'ai_available': False,
            'error': 'AI integration not loaded'
        })

if __name__ == '__main__':
    print("🚀 Starting AI Integration Test Server...")
    print("📍 Access the test interface at: http://localhost:5000")
    print("🔧 Configure API keys in .env file for full AI features")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
