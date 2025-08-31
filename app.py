#!/usr/bin/env python3
"""
Yamama Warehouse AI Agent - INSTANT VERSION
Zero dependencies startup, deploys in seconds
"""
from flask import Flask, jsonify, request
import os
import json
from datetime import datetime

app = Flask(__name__)

# Simple responses
responses = {
    'hello': 'مرحباً بك في وكيل الذكاء الاصطناعي لشركة يمامة للأسمنت!',
    'help': 'يمكنني مساعدتك في إدارة المستودعات والأسمنت',
    'default': 'شكراً لك. أنا مساعد ذكي لشركة يمامة للأسمنت'
}

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head><meta charset="UTF-8"><title>Yamama AI</title>
<style>
body{font-family:Arial;background:#4CAF50;padding:20px;color:white}
.container{max-width:600px;margin:0 auto;text-align:center}
.logo{font-size:60px;margin:20px}
h1{margin:20px 0}
.chat{background:white;color:#333;padding:20px;border-radius:10px;margin:20px 0}
input{width:80%;padding:10px;margin:10px;border:1px solid #ddd;border-radius:5px}
button{background:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer}
.message{margin:10px 0;padding:10px;background:#f0f0f0;border-radius:5px}
</style>
</head>
<body>
<div class="container">
<div class="logo">🏭</div>
<h1>Yamama Warehouse AI Agent</h1>
<p>Your intelligent assistant for warehouse management</p>
<div class="chat" id="chat">
<div class="message">مرحباً بك في وكيل الذكاء الاصطناعي لشركة يمامة للأسمنت!</div>
</div>
<input type="text" id="msg" placeholder="اكتب رسالتك هنا..." onkeypress="if(event.key==='Enter')send()">
<button onclick="send()">إرسال</button>
</div>
<script>
function send(){
var msg=document.getElementById('msg').value;
if(!msg)return;
document.getElementById('chat').innerHTML+='<div class="message" style="background:#e3f2fd;text-align:right;">'+msg+'</div>';
document.getElementById('msg').value='';
fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})})
.then(r=>r.json()).then(d=>document.getElementById('chat').innerHTML+='<div class="message">'+d.response+'</div>')
.catch(e=>document.getElementById('chat').innerHTML+='<div class="message">خطأ في الاتصال</div>');
}
</script>
</body></html>'''

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'startup': 'instant', 'version': 'ultra-fast'})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json() or {}
        message = data.get('message', '').lower()
        
        if 'hello' in message or 'مرحب' in message:
            response = responses['hello']
        elif 'help' in message or 'مساعد' in message:
            response = responses['help']
        else:
            response = responses['default']
            
        return jsonify({'response': response, 'status': 'success'})
    except:
        return jsonify({'response': 'عذراً، حدث خطأ', 'status': 'error'})

if __name__ == '__main__':
    print("🚀 YAMAMA AI - INSTANT START!")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
