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
    
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == 'your-api-key-here':
        print("❌ Google API Key not found or not properly set")
        AI_AVAILABLE = False
    else:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        AI_AVAILABLE = True
        print("🤖 Google Gemini AI loaded successfully")
        print(f"🔑 API Key Status: {'✅ Configured' if len(GOOGLE_API_KEY) > 20 else '❌ Invalid'}")
    
except ImportError as e:
    AI_AVAILABLE = False
    print(f"❌ Google Generative AI library not installed: {e}")
except Exception as e:
    AI_AVAILABLE = False
    print(f"⚠️  AI initialization error: {e}")

def get_ai_response(message, language='en'):
    """Get AI response using Google Gemini"""
    if not AI_AVAILABLE:
        if language == 'ar':
            return "خدمات الذكاء الاصطناعي غير متاحة مؤقتاً. يرجى المحاولة لاحقاً."
        return "AI services are temporarily unavailable. Please try again later."
    
    try:
        # Check if API key is available
        api_key = os.getenv('GOOGLE_API_KEY', 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA')
        if not api_key or api_key == 'your-api-key-here':
            logging.error("Google API Key not properly configured")
            if language == 'ar':
                return "⚠️ مفتاح API غير مكوّن بشكل صحيح. يرجى التواصل مع المطور."
            return "⚠️ API Key not properly configured. Please contact the developer."
        
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
        
        if response and response.text:
            return response.text
        else:
            logging.error("Empty response from Gemini API")
            if language == 'ar':
                return "⚠️ لم يتم الحصول على رد من النظام. يرجى المحاولة مرة أخرى."
            return "⚠️ No response received from the system. Please try again."
        
    except Exception as e:
        logging.error(f"AI response error: {str(e)} | Type: {type(e).__name__}")
        if "API_KEY" in str(e).upper() or "authentication" in str(e).lower():
            if language == 'ar':
                return "⚠️ خطأ في المصادقة مع Google Gemini. يرجى التحقق من مفتاح API."
            return "⚠️ Authentication error with Google Gemini. Please check API key."
        elif "quota" in str(e).lower() or "limit" in str(e).lower():
            if language == 'ar':
                return "⚠️ تم الوصول إلى الحد الأقصى للاستخدام. يرجى المحاولة لاحقاً."
            return "⚠️ Usage limit reached. Please try again later."
        else:
            if language == 'ar':
                return f"عذراً، حدث خطأ في النظام: {str(e)}. يرجى المحاولة مرة أخرى."
            else:
                return f"I apologize, there was a system error: {str(e)}. Please try again."

# HTML Template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
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
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 800px;
            width: 100%;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #4CAF50, #2196F3);
            padding: 20px;
            text-align: center;
            color: white;
        }
        
        .logo {
            max-width: 200px;
            height: auto;
            margin-bottom: 10px;
        }
        
        .header h1 {
            margin: 10px 0 5px 0;
            font-size: 1.8em;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .language-selector {
            margin: 15px 0;
        }
        
        .lang-btn {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            padding: 8px 15px;
            margin: 0 5px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .lang-btn.active, .lang-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        
        .content {
            padding: 30px;
        }
        
        .features {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #4CAF50;
        }
        
        .features ul {
            list-style: none;
            padding-left: 0;
        }
        
        .features li {
            padding: 5px 0;
            position: relative;
            padding-left: 20px;
        }
        
        .features li:before {
            content: '•';
            color: #4CAF50;
            font-weight: bold;
            position: absolute;
            left: 0;
        }
        
        .chat-area {
            border: 2px dashed #ddd;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            min-height: 200px;
            background: #fafafa;
        }
        
        .message {
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .user-message {
            background: #e3f2fd;
            margin-left: 20px;
        }
        
        .ai-message {
            background: #f1f8e9;
            margin-right: 20px;
        }
        
        .input-area {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        .input-field {
            flex: 1;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s ease;
        }
        
        .input-field:focus {
            border-color: #4CAF50;
        }
        
        .send-btn {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        
        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        .send-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
            color: #666;
        }
        
        .status-badges {
            text-align: center;
            margin: 15px 0;
        }
        
        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 12px;
            margin: 0 5px;
            border-radius: 15px;
            font-size: 12px;
            color: white;
        }
        
        @media (max-width: 600px) {
            .container {
                margin: 10px;
                border-radius: 15px;
            }
            
            .content {
                padding: 20px;
            }
            
            .input-area {
                flex-direction: column;
            }
            
            .send-btn {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="/static/yama.png" alt="Yamama Cement" class="logo" onerror="this.style.display='none'">
            <h1>🏭 Yamama Warehouse AI Agent</h1>
            <p>Your intelligent assistant for warehouse management and optimization</p>
            
            <div class="status-badges">
                <span class="badge">🧠 Memory</span>
                <span class="badge">🔄 Restart Chat</span>
                <span class="badge">📊 Analysis</span>
            </div>
            
            <div class="language-selector">
                <button class="lang-btn active" onclick="setLanguage('en')" id="en-btn">🇺🇸 EN</button>
                <button class="lang-btn" onclick="setLanguage('ar')" id="ar-btn">🇸🇦 AR</button>
            </div>
        </div>
        
        <div class="content">
            <div class="features">
                <ul id="features-list">
                    <li>Ask natural language questions about your business operations</li>
                    <li>Upload files (CSV, Excel, PDF, Word - up to 50MB) for AI analysis</li>
                    <li>Create and manage master data through conversation or API</li>
                    <li>Switch to Arabic (العربية) using the language toggle above</li>
                    <li>Access REST APIs for system integration and automation</li>
                </ul>
                <p style="margin-top: 15px; font-weight: bold; color: #4CAF50;">
                    🚀 Ready to transform your business operations with AI-powered intelligence? How can I assist you today?
                </p>
            </div>
            
            <div class="chat-area" id="chat-area">
                <!-- Chat messages will appear here -->
            </div>
            
            <div class="loading" id="loading">
                <p>🤖 AI is thinking...</p>
            </div>
            
            <div class="input-area">
                <input 
                    type="text" 
                    id="message-input" 
                    class="input-field" 
                    placeholder="Ask me about warehouse operations, inventory, or upload files for analysis..."
                    onkeypress="handleKeyPress(event)"
                >
                <button class="send-btn" onclick="sendMessage()" id="send-btn">Send</button>
            </div>
        </div>
    </div>

    <script>
        let currentLanguage = 'en';
        
        function setLanguage(lang) {
            currentLanguage = lang;
            document.getElementById('en-btn').classList.toggle('active', lang === 'en');
            document.getElementById('ar-btn').classList.toggle('active', lang === 'ar');
            
            const input = document.getElementById('message-input');
            if (lang === 'ar') {
                input.placeholder = 'اسأل عن عمليات المستودعات والمخزون أو ارفع ملفات للتحليل...';
                input.style.direction = 'rtl';
                updateFeaturesArabic();
            } else {
                input.placeholder = 'Ask me about warehouse operations, inventory, or upload files for analysis...';
                input.style.direction = 'ltr';
                updateFeaturesEnglish();
            }
        }
        
        function updateFeaturesEnglish() {
            document.getElementById('features-list').innerHTML = `
                <li>Ask natural language questions about your business operations</li>
                <li>Upload files (CSV, Excel, PDF, Word - up to 50MB) for AI analysis</li>
                <li>Create and manage master data through conversation or API</li>
                <li>Switch to Arabic (العربية) using the language toggle above</li>
                <li>Access REST APIs for system integration and automation</li>
            `;
        }
        
        function updateFeaturesArabic() {
            document.getElementById('features-list').innerHTML = `
                <li>اسأل أسئلة باللغة الطبيعية حول عمليات أعمالك</li>
                <li>ارفع الملفات (CSV, Excel, PDF, Word - حتى 50MB) للتحليل بالذكاء الاصطناعي</li>
                <li>إنشاء وإدارة البيانات الأساسية من خلال المحادثة أو API</li>
                <li>التبديل إلى الإنجليزية باستخدام مفتاح اللغة أعلاه</li>
                <li>الوصول إلى REST APIs للتكامل مع الأنظمة والأتمتة</li>
            `;
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        async function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Disable input and show loading
            input.disabled = true;
            document.getElementById('send-btn').disabled = true;
            document.getElementById('loading').style.display = 'block';
            
            // Add user message to chat
            addMessage(message, 'user');
            input.value = '';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        language: currentLanguage
                    })
                });
                
                const data = await response.json();
                addMessage(data.response, 'ai');
                
            } catch (error) {
                const errorMsg = currentLanguage === 'ar' ? 
                    'عذراً، حدث خطأ في الاتصال. يرجى المحاولة مرة أخرى.' : 
                    'Sorry, there was a connection error. Please try again.';
                addMessage(errorMsg, 'ai');
            } finally {
                // Re-enable input
                input.disabled = false;
                document.getElementById('send-btn').disabled = false;
                document.getElementById('loading').style.display = 'none';
                input.focus();
            }
        }
        
        function addMessage(text, sender) {
            const chatArea = document.getElementById('chat-area');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            messageDiv.innerHTML = text.replace(/\\n/g, '<br>');
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('message-input').focus();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    """Serve the main web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/static/<filename>')
def serve_static(filename):
    """Serve static files"""
    # Try to serve from static directory
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if os.path.exists(os.path.join(static_dir, filename)):
        return send_from_directory(static_dir, filename)
    
    # Try to serve from parent static directory
    parent_static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    if os.path.exists(os.path.join(parent_static_dir, filename)):
        return send_from_directory(parent_static_dir, filename)
    
    return '', 404

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ai_available": AI_AVAILABLE
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        message = data.get('message', '').strip()
        language = data.get('language', 'en')
        
        if not message:
            error_msg = "يرجى إدخال رسالة" if language == 'ar' else "Please enter a message"
            return jsonify({"response": error_msg})
        
        # Get AI response
        response = get_ai_response(message, language)
        
        return jsonify({
            "response": response,
            "language": language,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Chat error: {e}")
        error_msg = "عذراً، حدث خطأ في المعالجة" if request.get_json() and request.get_json().get('language') == 'ar' else "Sorry, there was a processing error"
        return jsonify({"response": error_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 YAMAMA AI - ULTRA FAST START!")
    print(f"🤖 AI Status: {'✅ Active' if AI_AVAILABLE else '❌ Unavailable'}")
    print(f"🌐 Starting on port {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )
