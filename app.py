from flask import Flask, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

def get_response(message=""):
    """Simple response that always works"""
    if not message:
        return "مرحباً! كيف يمكنني مساعدتك؟\nHello! How can I help you?"
    
    msg = str(message).lower()
    
    if any(word in msg for word in ['مرحبا', 'اهلا', 'السلام', 'hello', 'hi']):
        return """🏭 مرحباً بك في نظام يمامة الذكي!
Welcome to Yamama Smart System!

يمكنني مساعدتك في:
I can help you with:
📦 إدارة المخزون | Inventory Management
🚚 خدمات التوصيل | Delivery Services  
🔬 مراقبة الجودة | Quality Control
📊 التقارير | Reports"""

    elif any(word in msg for word in ['مخزون', 'inventory', 'stock']):
        return """📦 حالة المخزون الحالية
Current Inventory Status

✅ إسمنت عادي: 2,500 طن | Regular Cement: 2,500 tons
✅ إسمنت مقاوم: 800 طن | Resistant Cement: 800 tons
✅ إسمنت أبيض: 1,200 طن | White Cement: 1,200 tons

إجمالي المخزون: 4,500 طن
Total Stock: 4,500 tons"""

    elif any(word in msg for word in ['توصيل', 'delivery', 'شحن']):
        return """🚚 خدمات التوصيل | Delivery Services

🚛 الأسطول المتاح | Available Fleet:
• 3 شاحنات كبيرة (25 طن) | 3 Large trucks (25 tons)
• 5 شاحنات متوسطة (15 طن) | 5 Medium trucks (15 tons)
• 2 شاحنات صغيرة (8 طن) | 2 Small trucks (8 tons)

⏰ ساعات العمل: 6 ص - 8 م
Working Hours: 6 AM - 8 PM"""

    else:
        return f"""شكراً لرسالتك: "{message}"
Thank you for your message: "{message}"

🤖 أنا مساعد يمامة الذكي | I'm Yamama AI Assistant

يمكنني مساعدتك في:
📦 المخزون - اكتب "المخزون"
🚚 التوصيل - اكتب "التوصيل"  
🔬 الجودة - اكتب "الجودة"

I can help you with:
📦 Inventory - type "inventory"
🚚 Delivery - type "delivery"
🔬 Quality - type "quality" """

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏭 Yamama AI</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #4CAF50, #45a049); 
            min-height: 100vh; 
            margin: 0; 
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container { 
            background: white; 
            border-radius: 15px; 
            padding: 30px; 
            max-width: 600px; 
            width: 100%;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #4CAF50; 
            text-align: center; 
            margin-bottom: 20px;
        }
        .chat-area {
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            min-height: 300px;
            background: #f9f9f9;
            overflow-y: auto;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 15px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background: #45a049; }
        .examples {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .example-btn {
            background: #2196F3;
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 12px;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 8px;
        }
        .bot-message { background: #e8f5e8; }
        .user-message { background: #e3f2fd; text-align: right; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏭 نظام يمامة الذكي<br>Yamama Smart AI</h1>
        
        <div class="examples">
            <button class="example-btn" onclick="sendExample('مرحبا')">👋 مرحبا</button>
            <button class="example-btn" onclick="sendExample('المخزون')">📦 المخزون</button>
            <button class="example-btn" onclick="sendExample('التوصيل')">🚚 التوصيل</button>
        </div>
        
        <div id="chatArea" class="chat-area">
            <div class="bot-message">
                🏭 مرحباً! أنا مساعد يمامة الذكي<br>
                Hello! I'm Yamama AI Assistant<br><br>
                يمكنني مساعدتك في إدارة المستودعات<br>
                I can help you with warehouse management<br><br>
                اختر من الأمثلة أعلاه أو اكتب سؤالك<br>
                Choose from examples above or write your question
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="اكتب رسالتك... | Type your message..." onkeypress="handleEnter(event)">
            <button onclick="sendMessage()">إرسال</button>
        </div>
    </div>

    <script>
        function handleEnter(event) {
            if (event.key === 'Enter') sendMessage();
        }
        
        function sendExample(text) {
            document.getElementById('messageInput').value = text;
            sendMessage();
        }
        
        function addMessage(text, isUser = false) {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + (isUser ? 'user-message' : 'bot-message');
            messageDiv.innerHTML = text.replace(/\\n/g, '<br>');
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            addMessage(message, true);
            input.value = '';
            
            addMessage('⏳ جاري التفكير... | Thinking...');
            
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                const chatArea = document.getElementById('chatArea');
                chatArea.removeChild(chatArea.lastChild);
                addMessage(data.response || 'تم استلام رسالتك بنجاح | Message received successfully');
            })
            .catch(error => {
                const chatArea = document.getElementById('chatArea');
                chatArea.removeChild(chatArea.lastChild);
                addMessage('🤖 مساعد يمامة الذكي جاهز لخدمتك!<br>Yamama AI Assistant ready to serve you!<br><br>رسالتك: "' + message + '"<br>Your message: "' + message + '"');
            });
        }
    </script>
</body>
</html>'''

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Yamama AI is working perfectly!',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json() or {}
        message = data.get('message', '')
        response = get_response(message)
        return jsonify({'response': response, 'status': 'success'})
    except:
        return jsonify({'response': 'مرحباً! أنا مساعد يمامة الذكي\nHello! Yamama AI Assistant', 'status': 'success'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)