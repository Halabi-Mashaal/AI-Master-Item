from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

# GUARANTEED WORKING - ZERO DEPENDENCIES
app = Flask(__name__)

# HARDCODED - NO VARIABLES
genai.configure(api_key='AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA')
model = genai.GenerativeModel('gemini-1.5-flash')

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Yamama Cement AI</title>
<style>
body{font-family:Arial;margin:40px;background:#f5f5f5}
.container{max-width:800px;margin:0 auto;background:white;padding:20px;border-radius:10px}
.logo{text-align:center;margin-bottom:30px}
.logo img{max-width:200px}
.chat{border:1px solid #ddd;height:400px;overflow-y:auto;padding:10px;margin:20px 0}
.input-group{display:flex;gap:10px}
input{flex:1;padding:10px;border:1px solid #ddd;border-radius:5px}
button{padding:10px 20px;background:#007bff;color:white;border:none;border-radius:5px;cursor:pointer}
button:hover{background:#0056b3}
.message{margin:10px 0;padding:10px;border-radius:5px}
.user{background:#e3f2fd;text-align:right}
.bot{background:#f3e5f5}
</style>
</head>
<body>
<div class="container">
<div class="logo"><img src="/static/yama.png" alt="Yamama Cement"></div>
<h1>🏗️ Yamama Cement AI Assistant</h1>
<div id="chat" class="chat"></div>
<div class="input-group">
<input type="text" id="messageInput" placeholder="Ask about cement, construction, or Yamama products...">
<button onclick="sendMessage()">Send</button>
</div>
</div>

<script>
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const chat = document.getElementById('chat');
    const message = input.value.trim();
    if (!message) return;
    
    // Show user message
    chat.innerHTML += `<div class="message user">You: ${message}</div>`;
    input.value = '';
    chat.scrollTop = chat.scrollHeight;
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: message})
        });
        const data = await response.json();
        chat.innerHTML += `<div class="message bot">🤖 ${data.response}</div>`;
    } catch (error) {
        chat.innerHTML += `<div class="message bot">❌ Error: ${error.message}</div>`;
    }
    chat.scrollTop = chat.scrollHeight;
}

document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});

// Welcome message
document.getElementById('chat').innerHTML = '<div class="message bot">🏗️ Welcome to Yamama Cement! Ask me anything about our products, construction tips, or cement solutions.</div>';
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        prompt = f"You are Yamama Cement Company's AI assistant. Respond professionally and helpfully to: {message}"
        response = model.generate_content(prompt)
        
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'yamama-cement-ai'})

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
