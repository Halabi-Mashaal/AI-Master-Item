import os
import logging
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# HTML template for the chat interface
CHAT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Master Item AI Agent</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container { 
            background: white; 
            border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 800px;
            height: 80vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(45deg, #4a90e2, #357abd);
            color: white; 
            padding: 20px; 
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header h1 { font-size: 24px; margin-bottom: 5px; }
        .header p { opacity: 0.9; font-size: 14px; }
        .chat-container { 
            flex: 1; 
            padding: 20px; 
            overflow-y: auto; 
            background: #f8f9fa;
        }
        .message { 
            margin-bottom: 15px; 
            display: flex;
            align-items: flex-start;
        }
        .message.user { justify-content: flex-end; }
        .message-content { 
            max-width: 70%; 
            padding: 12px 18px; 
            border-radius: 18px; 
            word-wrap: break-word;
        }
        .message.user .message-content { 
            background: linear-gradient(45deg, #4a90e2, #357abd);
            color: white; 
            border-bottom-right-radius: 4px;
        }
        .message.bot .message-content { 
            background: white; 
            border: 1px solid #e1e8ed;
            color: #333;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .input-container { 
            padding: 20px; 
            background: white;
            border-top: 1px solid #e1e8ed;
            display: flex; 
            gap: 10px;
        }
        .input-container input { 
            flex: 1; 
            padding: 12px 18px; 
            border: 2px solid #e1e8ed; 
            border-radius: 25px; 
            font-size: 16px;
            outline: none;
            transition: all 0.3s ease;
        }
        .input-container input:focus { 
            border-color: #4a90e2; 
            box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
        }
        .input-container button { 
            padding: 12px 20px; 
            background: linear-gradient(45deg, #4a90e2, #357abd);
            color: white; 
            border: none; 
            border-radius: 25px; 
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .input-container button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(74, 144, 226, 0.4);
        }
        .input-container button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .typing-indicator {
            display: none;
            padding: 10px 18px;
            background: white;
            border: 1px solid #e1e8ed;
            border-radius: 18px;
            margin-bottom: 15px;
            max-width: 70%;
        }
        .typing-indicator.show { display: block; }
        .typing-dots {
            display: inline-block;
            position: relative;
            width: 40px;
            height: 10px;
        }
        .typing-dots div {
            position: absolute;
            top: 0;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4a90e2;
            animation: typing 1.4s infinite ease-in-out both;
        }
        .typing-dots div:nth-child(1) { left: 0; animation-delay: -0.32s; }
        .typing-dots div:nth-child(2) { left: 16px; animation-delay: -0.16s; }
        .typing-dots div:nth-child(3) { left: 32px; }
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Master Item AI Agent</h1>
            <p>Your intelligent assistant for master item management and optimization</p>
        </div>
        <div class="chat-container" id="chatContainer">
            <div class="message bot">
                <div class="message-content">
                    👋 Hello! I'm your Master Item AI Agent. I can help you with:
                    <br><br>
                    • 📋 Master item management
                    • 🔍 Inventory analysis
                    • 📊 Data quality insights
                    • 🎯 Predictive recommendations
                    • ⚙️ Process optimization
                    <br><br>
                    How can I assist you today?
                </div>
            </div>
            <div class="typing-indicator" id="typingIndicator">
                <div class="typing-dots">
                    <div></div>
                    <div></div>
                    <div></div>
                </div>
            </div>
        </div>
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Ask me anything about master items..." autofocus>
            <button onclick="sendMessage()" id="sendButton">Send</button>
        </div>
    </div>

    <script>
        function addMessage(content, isUser) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
            
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.innerHTML = content;
            
            messageDiv.appendChild(messageContent);
            chatContainer.insertBefore(messageDiv, document.getElementById('typingIndicator'));
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function showTypingIndicator() {
            document.getElementById('typingIndicator').classList.add('show');
            document.getElementById('chatContainer').scrollTop = document.getElementById('chatContainer').scrollHeight;
        }

        function hideTypingIndicator() {
            document.getElementById('typingIndicator').classList.remove('show');
        }

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, true);
            input.value = '';
            sendButton.disabled = true;
            showTypingIndicator();
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                hideTypingIndicator();
                addMessage(data.response, false);
            } catch (error) {
                hideTypingIndicator();
                addMessage('Sorry, I encountered an error. Please try again.', false);
            }
            
            sendButton.disabled = false;
        }

        // Enter key to send
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    logging.info("Chat interface accessed.")
    return render_template_string(CHAT_TEMPLATE)

@app.route('/api')
def api_status():
    return jsonify({
        "message": "Master Item AI Agent is running!",
        "status": "active",
        "version": "1.0.0",
        "endpoints": {
            "/": "Chat interface",
            "/api": "API status",
            "/chat": "Chat endpoint",
            "/health": "Health check"
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower().strip()
        
        # Simple AI responses based on keywords
        if any(word in user_message for word in ['hello', 'hi', 'hey']):
            response = "Hello! 👋 I'm your Master Item AI Agent. How can I help you optimize your master item processes today?"
        
        elif any(word in user_message for word in ['inventory', 'stock', 'items']):
            response = """📦 **Inventory Analysis:**
            
• Current inventory trends show optimal stock levels
• Recommend reviewing slow-moving items in categories A-C
• Predicted demand increase of 15% next quarter
• 3 duplicate items detected - would you like details?"""
        
        elif any(word in user_message for word in ['duplicate', 'duplicates']):
            response = """🔍 **Duplicate Items Found:**
            
• **Item #1:** "Steel Bolt M8" vs "M8 Steel Bolt" (98% match)
• **Item #2:** "Blue Paint 1L" vs "1L Blue Paint" (95% match) 
• **Item #3:** "USB Cable Type-C" vs "Type-C USB Cable" (97% match)

Would you like me to merge these duplicates?"""
        
        elif any(word in user_message for word in ['quality', 'data quality']):
            response = """📊 **Data Quality Report:**
            
• **Completeness:** 87% (↑5% from last month)
• **Accuracy:** 92% (↑2% from last month)
• **Consistency:** 89% (↑8% from last month)
• **Missing Attributes:** 156 items need descriptions
• **Standardization:** 78% following naming conventions"""
        
        elif any(word in user_message for word in ['predict', 'forecast', 'future']):
            response = """🎯 **Predictive Insights:**
            
• **Demand Forecast:** 23% increase in Q4 for seasonal items
• **New Product Success:** 87% likelihood for proposed items
• **Supplier Risk:** Medium risk detected for 2 key suppliers
• **Optimization Opportunity:** $45K savings potential identified"""
        
        elif any(word in user_message for word in ['help', 'what can you do']):
            response = """🤖 **I can assist you with:**
            
🔹 **Master Data Management:** Clean, standardize, and optimize item data
🔹 **Duplicate Detection:** Find and merge duplicate items automatically  
🔹 **Inventory Analytics:** Analyze stock levels, trends, and optimization
🔹 **Quality Assessment:** Monitor and improve data quality metrics
🔹 **Predictive Modeling:** Forecast demand and identify opportunities
🔹 **Process Automation:** Streamline workflows and reduce manual work

What would you like to explore?"""
        
        elif any(word in user_message for word in ['optimize', 'optimization']):
            response = """⚙️ **Optimization Recommendations:**
            
• **Storage Efficiency:** Reorganize warehouse layout (+12% space)
• **Ordering Strategy:** Implement JIT for fast-moving items
• **Vendor Consolidation:** Reduce suppliers from 45 to 32 (-15% costs)
• **Automation:** Deploy barcode scanning for 67% faster processing"""
        
        elif any(word in user_message for word in ['thank', 'thanks']):
            response = "You're welcome! 😊 I'm here whenever you need assistance with your master item management. Is there anything else I can help you with?"
        
        else:
            response = f"""🤔 I understand you're asking about: "{user_message}"

Let me analyze this for you... Based on current master item data, I recommend:

• Reviewing related item categories for optimization opportunities
• Checking data quality metrics for this area
• Exploring predictive insights for better planning

Would you like me to dive deeper into any specific aspect?"""
        
        return jsonify({"response": response})
        
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        return jsonify({"response": "I apologize, but I encountered an error. Please try rephrasing your question."})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    logging.info(f"Starting the app on host 0.0.0.0 and port {port}.")
    app.run(host="0.0.0.0", port=port, debug=False)
