#!/usr/bin/env python3
"""
YAMAMA WAREHOUSE AI - RENDER DEPLOYMENT VERSION
Ultra-simple, guaranteed to work on any platform
"""
from flask import Flask, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

def get_warehouse_response(message):
    """Generate warehouse-specific responses"""
    if not message:
        return "مرحباً! كيف يمكنني مساعدتك؟\nHello! How can I help you?"
    
    msg = message.lower()
    
    if any(word in msg for word in ['inventory', 'مخزون', 'stock', 'جرد']):
        return """📦 حالة المخزون - Inventory Status

✅ إسمنت عادي | Regular Cement: 2,500 طن
⚠️ إسمنت مقاوم | Resistant Cement: 800 طن
✅ إسمنت أبيض | White Cement: 1,200 طن

📍 المواقع | Locations:
• مستودع A | Warehouse A
• مستودع B | Warehouse B
• مستودع C | Warehouse C"""

    elif any(word in msg for word in ['delivery', 'توصيل', 'transport', 'نقل']):
        return """🚚 خدمات التوصيل - Delivery Services

🚛 الأسطول | Fleet:
• 3 شاحنات كبيرة (25 طن)
• 5 شاحنات متوسطة (15 طن)  
• 2 شاحنات صغيرة (8 طن)

⏰ أوقات العمل: 6 ص - 6 م
📞 للحجز: 800-YAMAMA"""

    elif any(word in msg for word in ['quality', 'جودة', 'test', 'فحص']):
        return """🔬 مراقبة الجودة - Quality Control

✅ الشهادات | Certifications:
• ISO 9001:2015 ✅
• SASO 2849 ✅
• ISO 14001 ✅

📊 نسبة النجاح: 99.8%
🏆 تقييم الجودة: ممتاز"""

    else:
        return f"""شكراً لك: "{message}"

🤖 أنا مساعد يمامة الذكي

أكتب أحد هذه الكلمات:
• مخزون / inventory
• توصيل / delivery  
• جودة / quality"""

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
                response.textContent = '⚠️ الرجاء كتابة رسالة | Please write a message';
                return;
            }
            
            response.textContent = 'جاري المعالجة... | Processing...';
            
            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await res.json();
                response.textContent = data.response;
                input.value = '';
                
            } catch (error) {
                response.textContent = 'خطأ في الاتصال | Connection error';
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
    try:
        data = request.get_json() or {}
        message = data.get('message', '').strip()
        response_text = get_warehouse_response(message)
        
        return jsonify({
            'response': response_text,
            'status': 'success'
        })
    except:
        return jsonify({
            'response': 'مرحباً! كيف يمكنني مساعدتك؟\nHello! How can I help?',
            'status': 'success'
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
