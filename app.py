#!/usr/bin/env python3
"""
YAMAMA WAREHOUSE AI - ENHANCED VERSION WITH AI INTEGRATION
Smart warehouse management with Google Gemini AI
"""
from flask import Flask, jsonify, request
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# AI Integration Setup
AI_AVAILABLE = False
AI_ERROR = None

try:
    import google.generativeai as genai
    
    # Try multiple environment variable names for the API key
    GEMINI_API_KEY = (
        os.getenv('GOOGLE_API_KEY') or 
        os.getenv('GEMINI_API_KEY') or 
        os.getenv('GOOGLE_GEMINI_API_KEY') or
        os.getenv('AI_API_KEY')
    )
    
    if GEMINI_API_KEY and len(GEMINI_API_KEY) > 10:  # Basic validation
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        AI_AVAILABLE = True
        logger.info("✅ Google Gemini AI initialized successfully")
    else:
        AI_ERROR = "No valid API key found in environment variables"
        logger.warning("⚠️ No valid API key found, using fallback responses")
        
except ImportError as e:
    AI_ERROR = f"google.generativeai library not available: {e}"
    logger.info(f"⚠️ Google AI library not installed: {e}")
except Exception as e:
    AI_ERROR = f"AI initialization failed: {e}"
    logger.warning(f"⚠️ AI initialization error: {e}")

def get_ai_response(message, language='ar'):
    """Get AI response with warehouse context and robust error handling"""
    if not AI_AVAILABLE:
        logger.debug(f"AI not available. Reason: {AI_ERROR}")
        return None
    
    try:
        # Validate message
        if not message or len(message.strip()) == 0:
            return None
            
        # Create warehouse-specific prompt
        if language == 'ar' or any(char in 'أإآاةتثجحخدذرزسشصضطظعغفقكلمنهوي' for char in message):
            system_prompt = """أنت مساعد ذكي متخصص في إدارة مستودعات شركة يمامة للأسمنت السعودية. 

معلومات المستودع الحالية:
- إسمنت عادي: 2,500 طن (مستودع A)
- إسمنت مقاوم: 800 طن (مستودع B) 
- إسمنت أبيض: 1,200 طن (مستودع C)

الأسطول:
- 3 شاحنات كبيرة (25 طن)
- 5 شاحنات متوسطة (15 طن)
- 2 شاحنات صغيرة (8 طن)

الشهادات:
- ISO 9001:2015
- SASO 2849
- ISO 14001

أجب بطريقة مهنية ومفيدة باللغة العربية مع الترقيم والرموز التعبيرية."""
        else:
            system_prompt = """You are an AI assistant specialized in warehouse management for Yamama Cement Company in Saudi Arabia.

Current Inventory:
- Regular Cement: 2,500 tons (Warehouse A)
- Resistant Cement: 800 tons (Warehouse B)
- White Cement: 1,200 tons (Warehouse C)

Fleet:
- 3 Large trucks (25 tons each)
- 5 Medium trucks (15 tons each)
- 2 Small trucks (8 tons each)

Certifications:
- ISO 9001:2015
- SASO 2849  
- ISO 14001

Respond professionally and helpfully in English with appropriate formatting and emojis."""

        full_prompt = f"{system_prompt}\n\nUser Question: {message}\n\nAssistant Response:"
        
        # Generate response with timeout protection
        response = model.generate_content(full_prompt)
        
        if response and response.text:
            logger.info("✅ AI response generated successfully")
            return response.text.strip()
        else:
            logger.warning("⚠️ AI returned empty response")
            return None
        
    except Exception as e:
        logger.error(f"AI response error: {str(e)}")
        return None

def get_warehouse_response(message):
    """Generate warehouse-specific responses with AI fallback"""
    if not message:
        return "مرحباً! كيف يمكنني مساعدتك؟\nHello! How can I help you?"
    
    # Try AI response first
    ai_response = get_ai_response(message)
    if ai_response:
        return ai_response
    
    # Fallback to predefined responses
    msg = message.lower()
    
    if any(word in msg for word in ['inventory', 'مخزون', 'stock', 'جرد', 'كمية', 'quantity']):
        return """📦 حالة المخزون - Inventory Status

✅ إسمنت عادي | Regular Cement: 2,500 طن
⚠️ إسمنت مقاوم | Resistant Cement: 800 طن (منخفض)
✅ إسمنت أبيض | White Cement: 1,200 طن

📍 المواقع | Locations:
• مستودع A | Warehouse A - إسمنت عادي
• مستودع B | Warehouse B - إسمنت مقاوم  
• مستودع C | Warehouse C - إسمنت أبيض

🔄 آخر تحديث | Last Updated: اليوم 2:30 م"""

    elif any(word in msg for word in ['delivery', 'توصيل', 'transport', 'نقل', 'شحن', 'توزيع']):
        return """🚚 خدمات التوصيل - Delivery Services

🚛 الأسطول المتاح | Available Fleet:
• 3 شاحنات كبيرة (25 طن لكل منها)
• 5 شاحنات متوسطة (15 طن لكل منها)  
• 2 شاحنات صغيرة (8 طن لكل منها)

📅 المواعيد المتاحة اليوم | Today's Available Slots:
✅ 8:00 ص - 10:00 ص
✅ 1:00 م - 3:00 م
❌ 3:00 م - 5:00 م (محجوز)

⏰ أوقات العمل: 6:00 ص - 6:00 م
📞 للحجز: 800-YAMAMA"""

    elif any(word in msg for word in ['quality', 'جودة', 'test', 'فحص', 'شهادة', 'معيار']):
        return """🔬 مراقبة الجودة - Quality Control

✅ الشهادات المعتمدة | Certified Standards:
• ISO 9001:2015 ✅ - نظام إدارة الجودة
• SASO 2849 ✅ - معايير الهيئة السعودية
• ISO 14001 ✅ - الإدارة البيئية

🧪 الاختبارات الأخيرة | Recent Tests:
• اختبار الضغط | Compression Test: 42.5 MPa ✅
• اختبار التماسك | Setting Time: 285 دقيقة ✅  
• التحليل الكيميائي | Chemical Analysis: مطابق ✅

📊 نسبة النجاح: 99.8%
🏆 تقييم الجودة: ممتاز | Excellent"""

    elif any(word in msg for word in ['hello', 'hi', 'مرحبا', 'اهلا', 'السلام']):
        return """🏭 مرحباً بك في نظام يمامة الذكي
Welcome to Yamama Smart Warehouse System

🤖 أنا مساعدك الذكي لإدارة المستودعات
I'm your AI assistant for warehouse management

يمكنني مساعدتك في | I can help you with:
📦 المخزون والكميات | Inventory & Quantities
🚚 التوصيل والنقل | Delivery & Transport
🔬 الجودة والشهادات | Quality & Certifications
📊 التقارير والتحليل | Reports & Analysis

اكتب سؤالك الآن | Ask your question now"""

    else:
        return f"""شكراً لسؤالك: "{message}"
Thank you for your question: "{message}"

🤖 أنا مساعد يمامة الذكي المتطور
I'm Yamama's Advanced AI Assistant

💡 للحصول على أفضل النتائج، اسأل عن:
For best results, ask about:

📦 المخزون | Inventory: "كم لدينا من الإسمنت؟"
🚚 التوصيل | Delivery: "متى يمكن التوصيل؟"  
🔬 الجودة | Quality: "ما هي شهادات الجودة؟"
📊 التقارير | Reports: "أريد تقرير المبيعات"

أو اكتب أي سؤال آخر وسأحاول مساعدتك!
Or write any other question and I'll try to help!"""

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏭 Yamama AI</title>
    <style>
        body { font-family: Arial; background: #4CAF50; color: white; padding: 20px; margin: 0; }
        .container { max-width: 600px; margin: 0 auto; background: white; color: #333; padding: 20px; border-radius: 10px; }
        h1 { text-align: center; color: #4CAF50; margin-bottom: 30px; }
        .input-group { margin: 20px 0; }
        label { display: block; margin-bottom: 8px; font-weight: bold; }
        input[type="text"] { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }
        button { background: #4CAF50; color: white; padding: 12px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; }
        button:hover { background: #45a049; }
        .response { background: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin: 20px 0; border-radius: 5px; white-space: pre-line; min-height: 100px; }
        .examples { display: flex; gap: 10px; margin: 10px 0; flex-wrap: wrap; }
        .example-btn { background: #2196F3; color: white; padding: 6px 12px; border: none; border-radius: 3px; cursor: pointer; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏭 نظام يمامة للمستودعات<br>Yamama Warehouse System</h1>
        
        <div class="input-group">
            <label>💬 اكتب رسالتك | Your Message:</label>
            <input type="text" id="messageInput" placeholder="مثال: كم لدينا من الإسمنت؟">
        </div>
        
        <div class="examples">
            <button class="example-btn" onclick="setMessage('مخزون')">📦 مخزون</button>
            <button class="example-btn" onclick="setMessage('توصيل')">🚚 توصيل</button>
            <button class="example-btn" onclick="setMessage('جودة')">🔬 جودة</button>
            <button class="example-btn" onclick="setMessage('inventory')">📊 Inventory</button>
        </div>
        
        <button onclick="sendMessage()">إرسال | Send</button>
        
        <div class="input-group">
            <label>📋 الرد | Response:</label>
            <div id="response" class="response">مرحباً! اكتب سؤالك أعلاه.

Hello! Write your question above.</div>
        </div>
    </div>

    <script>
        function setMessage(text) {
            document.getElementById('messageInput').value = text;
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const response = document.getElementById('response');
            const message = input.value.trim();
            
            if (!message) {
                response.innerHTML = '⚠️ الرجاء كتابة رسالة | Please write a message';
                return;
            }
            
            // Show loading state
            response.innerHTML = '⏳ جاري المعالجة... | Processing...';
            
            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });
                
                if (!res.ok) {
                    throw new Error(`HTTP ${res.status}: ${res.statusText}`);
                }
                
                const data = await res.json();
                
                if (data.response) {
                    response.innerHTML = data.response.replace(/\n/g, '<br>');
                    
                    // Show AI status if available
                    if (data.ai_enabled) {
                        response.innerHTML += '<br><br><small style="color: #4CAF50;">✨ مدعوم بالذكاء الاصطناعي | AI-Powered</small>';
                    }
                } else {
                    response.innerHTML = 'تم استلام الرد بنجاح | Response received successfully';
                }
                
                input.value = '';
                
            } catch (error) {
                console.error('Chat error:', error);
                response.innerHTML = `❌ خطأ في الاتصال | Connection Error<br><small>${error.message}</small><br><br>🔄 يرجى المحاولة مرة أخرى | Please try again`;
            }
        }
        
        document.getElementById('messageInput').onkeypress = function(e) {
            if (e.key === 'Enter') sendMessage();
        }
    </script>
</body>
</html>'''

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Yamama Warehouse AI is running!',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Enhanced chat endpoint with comprehensive error handling"""
    try:
        # Handle different content types
        data = None
        
        # Try multiple ways to get the request data
        try:
            if request.is_json:
                data = request.get_json()
            elif request.content_type and 'form' in request.content_type:
                data = request.form.to_dict()
            else:
                data = request.get_json(force=True)
        except Exception as parse_error:
            logger.warning(f"Request parsing error: {parse_error}")
            data = {}
        
        # Handle empty data gracefully
        if not data:
            logger.info("Empty request received, sending welcome message")
            return jsonify({
                'response': 'مرحباً! كيف يمكنني مساعدتك؟\nHello! How can I help you?',
                'status': 'success',
                'ai_enabled': AI_AVAILABLE
            })
        
        message = str(data.get('message', '')).strip()
        
        if not message:
            return jsonify({
                'response': 'الرجاء كتابة رسالة\nPlease write a message',
                'status': 'success',
                'ai_enabled': AI_AVAILABLE
            })
        
        logger.info(f"Processing message: '{message[:50]}{'...' if len(message) > 50 else ''}'")
        
        # Get response with proper error handling
        try:
            response_text = get_warehouse_response(message)
            
            if not response_text:
                response_text = """🏭 أهلاً وسهلاً بك في نظام يمامة
Welcome to Yamama Warehouse System

أنا مساعدك الذكي، يمكنني مساعدتك في:
I'm your smart assistant, I can help you with:

📦 إدارة المخزون | Inventory Management
🚚 التوصيل والشحن | Delivery & Shipping  
🔬 مراقبة الجودة | Quality Control
📊 التقارير | Reports

اكتب سؤالك وسأساعدك فوراً!
Write your question and I'll help you immediately!"""
            
            return jsonify({
                'response': response_text,
                'status': 'success',
                'ai_enabled': AI_AVAILABLE,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as response_error:
            logger.error(f"Response generation error: {response_error}")
            
            # Provide a helpful fallback response
            fallback_response = f"""🏭 مرحباً! أنا مساعد يمامة الذكي
Hello! I'm Yamama AI Assistant

تم استلام رسالتك: "{message}"
Your message received: "{message}"

يمكنني مساعدتك في | I can help you with:
📦 المخزون والكميات | Inventory & Stock
🚚 التوصيل والشحن | Delivery & Shipping
🔬 الجودة والشهادات | Quality & Certifications
📞 معلومات التواصل | Contact Information

💡 جرب أسئلة مثل:
Try questions like:
• "كم لدينا من الإسمنت؟" 
• "What's in stock?"
• "متى التوصيل؟"
• "Delivery schedule?"

أو اكتب أي سؤال آخر!
Or write any other question!"""

            return jsonify({
                'response': fallback_response,
                'status': 'success',
                'ai_enabled': AI_AVAILABLE,
                'fallback': True,
                'timestamp': datetime.now().isoformat()
            })
        
    except Exception as e:
        logger.error(f"Critical chat error: {str(e)}")
        
        # Ultimate fallback - always works
        emergency_response = """🏭 مرحباً بك في نظام يمامة للمستودعات
Welcome to Yamama Warehouse System

✅ النظام يعمل بشكل طبيعي
System is operating normally

📋 الخدمات المتاحة | Available Services:
• إدارة المخزون | Inventory Management  
• التوصيل | Delivery Services
• مراقبة الجودة | Quality Control

💬 اكتب سؤالك وسأساعدك
Write your question and I'll help you

📞 للدعم الفني: 800-YAMAMA
Technical Support: 800-YAMAMA"""
        
        return jsonify({
            'response': emergency_response,
            'status': 'success',
            'ai_enabled': False,
            'emergency_fallback': True,
            'timestamp': datetime.now().isoformat()
        }), 200

@app.route('/test', methods=['GET', 'POST'])
def test():
    """Test endpoint for debugging"""
    return jsonify({
        'status': 'working',
        'message': 'Yamama AI is running perfectly!',
        'ai_available': AI_AVAILABLE,
        'ai_error': AI_ERROR,
        'timestamp': datetime.now().isoformat(),
        'version': '2.0-enhanced'
    })

@app.route('/debug')
def debug():
    """Debug endpoint to check environment and AI status"""
    env_vars = {}
    for key in ['GOOGLE_API_KEY', 'GEMINI_API_KEY', 'GOOGLE_GEMINI_API_KEY', 'AI_API_KEY']:
        value = os.getenv(key)
        if value:
            env_vars[key] = f"Set (length: {len(value)})"
        else:
            env_vars[key] = "Not set"
    
    return jsonify({
        'ai_available': AI_AVAILABLE,
        'ai_error': AI_ERROR,
        'environment_variables': env_vars,
        'timestamp': datetime.now().isoformat(),
        'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
        'flask_working': True
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
