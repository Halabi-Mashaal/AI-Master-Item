#!/usr/bin/env python3
"""
Yamama Cement AI Agent - Production Ready
"""
from flask import Flask, jsonify, request, render_template_string
import os

app = Flask(__name__)

# Simple responses
RESPONSES = {
    'hello': 'مرحباً بك في وكيل الذكاء الاصطناعي لشركة يمامة للأسمنت!',
    'help': 'يمكنني مساعدتك في إدارة المستودعات والأسمنت',
    'default': 'شكراً لك. أنا مساعد ذكي لشركة يمامة للأسمنت'
}

HTML_TEMPLATE = '''<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yamama AI</title>
    <style>
        body{font-family:Arial;background:#4CAF50;padding:20px;color:white}
        .container{max-width:600px;margin:0 auto;text-align:center}
        .logo{font-size:60px;margin:20px}
        h1{margin:20px 0}
        .chat{background:white;color:#333;padding:20px;border-radius:10px;margin:20px 0;max-height:400px;overflow-y:auto}
        input{width:80%;padding:10px;margin:10px;border:1px solid #ddd;border-radius:5px}
        button{background:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer}
        .message{margin:10px 0;padding:10px;background:#f0f0f0;border-radius:5px}
        .user-message{background:#e3f2fd;text-align:right}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🏭</div>
        <h1>Yamama Cement AI Agent</h1>
        <p>Your intelligent assistant for cement and warehouse management</p>
        <div class="chat" id="chat">
            <div class="message">مرحباً بك في وكيل الذكاء الاصطناعي لشركة يمامة للأسمنت!</div>
        </div>
        <input type="text" id="msg" placeholder="اكتب رسالتك هنا..." onkeypress="if(event.key==='Enter')send()">
        <button onclick="send()">إرسال</button>
    </div>
    <script>
        function send(){
            var msg=document.getElementById('msg').value.trim();
            if(!msg)return;
            
            document.getElementById('chat').innerHTML+='<div class="message user-message">'+msg+'</div>';
            document.getElementById('msg').value='';
            
            fetch('/chat',{
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify({message:msg})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('chat').innerHTML+='<div class="message">'+data.response+'</div>';
                document.getElementById('chat').scrollTop = document.getElementById('chat').scrollHeight;
            })
            .catch(error => {
                document.getElementById('chat').innerHTML+='<div class="message">خطأ في الاتصال - Connection Error</div>';
            });
        }
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'service': 'yamama-cement-ai',
        'version': '1.0'
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'response': 'لم يتم استلام رسالة - No message received',
                'status': 'error'
            })
        
        message = data.get('message', '').lower().strip()
        
        # Simple keyword matching
        if any(word in message for word in ['hello', 'hi', 'مرحب', 'السلام']):
            response = RESPONSES['hello']
        elif any(word in message for word in ['help', 'مساعد', 'ساعد']):
            response = RESPONSES['help']
        elif any(word in message for word in ['cement', 'اسمنت', 'إسمنت']):
            response = 'نحن شركة يمامة للأسمنت السعودي، نوفر أجود أنواع الأسمنت للبناء والتشييد'
        else:
            response = RESPONSES['default']
            
        return jsonify({
            'response': response, 
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'response': 'عذراً، حدث خطأ في النظام - Sorry, system error occurred',
            'status': 'error'
        })

if __name__ == '__main__':
    print("🚀 YAMAMA CEMENT AI - STARTING...")
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
