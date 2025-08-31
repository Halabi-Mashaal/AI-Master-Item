#!/usr/bin/env python3
"""
Ultra-Lightweight Yamama Cement AI Agent for Render Deployment
"""
import os
import json
import time
import logging
from flask import Flask, jsonify, request, render_template_string, send_from_directory
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Google Gemini AI Integration
try:
    import google.generativeai as genai
    
    # Configure Gemini API
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA')
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    AI_AVAILABLE = True
    print("🤖 Google Gemini AI loaded successfully")
    
except Exception as e:
    AI_AVAILABLE = False
    print(f"⚠️  AI not available: {e}")

def get_ai_response(message, language='en'):
    """Get AI response using Google Gemini"""
    if not AI_AVAILABLE:
        return "AI services are temporarily unavailable. Please try again later."
    
    try:
        # Create context-aware prompt
        if language == 'ar':
            system_prompt = """أنت مساعد ذكي لشركة أسمنت اليمامة السعودية. أجب باللغة العربية وكن مفيداً ومهنياً.
تخصصك في:
- إدارة المستودعات والمخزون
- صناعة الأسمنت والمواد البناء
- تحليل البيانات والتقارير
- تحسين العمليات التشغيلية"""
        else:
            system_prompt = """You are an intelligent assistant for Yamama Cement Company. Be helpful and professional.
Your expertise includes:
- Warehouse and inventory management
- Cement industry and construction materials
- Data analysis and reporting  
- Operations optimization"""
        
        full_prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
        
        response = model.generate_content(full_prompt)
        return response.text
        
    except Exception as e:
        logging.error(f"AI response error: {e}")
        if language == 'ar':
            return "عذراً، حدث خطأ في النظام. يرجى المحاولة مرة أخرى."
        else:
            return "I apologize, there was a system error. Please try again."
        else:
            return {
                "response": "Thank you for your message. I'm here to help with warehouse management and item analysis. Could you please clarify your request?",
                "provider": "simple_ai", 
                "language": "en",
                "timestamp": datetime.now().isoformat()
            }

# Initialize AI
ai_agent = SimpleAI()

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yamama Warehouse AI Agent</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #4CAF50, #2196F3);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .logo {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #2e7d32, #1565c0);
            border-radius: 50%;
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        .title {
            font-size: 24px;
            margin-bottom: 8px;
        }
        
        .subtitle {
            font-size: 16px;
            opacity: 0.9;
        }
        
        .tabs {
            display: flex;
            background: #f5f5f5;
        }
        
        .tab {
            flex: 1;
            padding: 15px;
            text-align: center;
            background: #f5f5f5;
            cursor: pointer;
            border: none;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .tab.active {
            background: #4CAF50;
            color: white;
        }
        
        .chat-container {
            height: 400px;
            padding: 20px;
            overflow-y: auto;
            border-bottom: 1px solid #eee;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        
        .user-message {
            background: #e3f2fd;
            margin-left: auto;
            text-align: right;
        }
        
        .ai-message {
            background: #f1f8e9;
            margin-right: auto;
        }
        
        .input-container {
            padding: 20px;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        
        .message-input {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            direction: rtl;
        }
        
        .message-input:focus {
            outline: none;
            border-color: #4CAF50;
        }
        
        .send-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        
        .send-btn:hover {
            background: #45a049;
        }
        
        .status {
            text-align: center;
            padding: 10px;
            background: #e8f5e8;
            color: #2e7d2e;
            font-size: 14px;
        }
        
        .upload-area {
            padding: 40px;
            border: 2px dashed #ddd;
            text-align: center;
            margin: 20px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .upload-area:hover {
            border-color: #4CAF50;
            background: #f8fff8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Y</div>
            <h1 class="title">Yamama Warehouse AI Agent</h1>
            <p class="subtitle">Your intelligent assistant for warehouse management and optimization</p>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('chat')">💬 Memory</button>
            <button class="tab" onclick="showTab('restart')">🔄 Restart Chat</button>
            <button class="tab" onclick="showTab('analysis')">📊 Analysis</button>
        </div>
        
        <div class="status">
            🚀 Ready to transform your business operations with AI-powered intelligence? How can I assist you today?
        </div>
        
        <div class="chat-container" id="chatContainer">
            <!-- Chat messages will appear here -->
        </div>
        
        <div class="input-container">
            <input type="text" class="message-input" id="messageInput" placeholder="Ask me about warehouse operations, inventory, or upload files for analysis..." />
            <button class="send-btn" onclick="sendMessage()">Send</button>
        </div>
        
        <div class="upload-area" onclick="document.getElementById('fileInput').click()">
            📁 Upload Files<br>
            <small>Drag & drop or click to upload CSV, Excel, Word, PDF, Images (Max 50MB)</small>
            <input type="file" id="fileInput" style="display: none;" accept=".csv,.xlsx,.xls,.doc,.docx,.pdf,.jpg,.jpeg,.png" multiple>
        </div>
    </div>
    
    <script>
        function showTab(tab) {
            // Simple tab functionality
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
        }
        
        function addMessage(message, isUser = false) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + (isUser ? 'user-message' : 'ai-message');
            messageDiv.textContent = message;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, true);
            input.value = '';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        language: 'ar'
                    })
                });
                
                const data = await response.json();
                addMessage(data.response || 'خطأ في الاستجابة');
                
            } catch (error) {
                addMessage('عذراً، حدث خطأ في الاتصال. يرجى المحاولة مرة أخرى.');
            }
        }
        
        // Enter key to send
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Initial welcome message
        setTimeout(() => {
            addMessage('مرحباً بك في وكيل الذكاء الاصطناعي لشركة يمامة للأسمنت! كيف يمكنني مساعدتك اليوم؟');
        }, 1000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-simple",
        "ai_provider": "simple_ai",
        "memory_optimized": True
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        language = data.get('language', 'ar')
        
        logger.info(f"Chat request: {message}")
        
        # Get AI response
        response = ai_agent.get_response(message, language)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({
            "response": "I apologize, but I encountered an error processing your request. Please try again.",
            "error": str(e),
            "provider": "error_handler"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print("🚀 Starting Yamama Warehouse AI Agent")
    print(f"🌐 Server starting on port {port}")
    print("✅ Fast startup - Ready for production!")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )
