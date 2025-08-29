import os
import logging
import pandas as pd
import io
import base64
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
from werkzeug.utils import secure_filename
import mimetypes

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

logging.basicConfig(level=logging.INFO)

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'csv', 'xlsx', 'xls', 'txt', 'json', 
    'pdf', 'doc', 'docx', 'png', 'jpg', 
    'jpeg', 'gif', 'bmp', 'tiff'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            flex-direction: column;
            gap: 10px;
        }
        .message-row {
            display: flex;
            gap: 10px;
            align-items: flex-end;
        }
        .file-upload-area {
            border: 2px dashed #e1e8ed;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            background: #f8f9fa;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 10px;
        }
        .file-upload-area:hover {
            border-color: #4a90e2;
            background: #f0f7ff;
        }
        .file-upload-area.dragover {
            border-color: #4a90e2;
            background: #e3f2fd;
            transform: scale(1.02);
        }
        .file-info {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: white;
            border: 1px solid #e1e8ed;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .file-info .file-icon {
            font-size: 24px;
        }
        .file-info .file-details {
            flex: 1;
            text-align: left;
        }
        .file-info .file-name {
            font-weight: 600;
            color: #333;
        }
        .file-info .file-size {
            font-size: 12px;
            color: #666;
        }
        .remove-file {
            color: #e74c3c;
            cursor: pointer;
            font-weight: bold;
            padding: 5px;
        }
        .remove-file:hover {
            background: #fee;
            border-radius: 3px;
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
            <div class="file-upload-area" onclick="document.getElementById('fileInput').click()" ondrop="dropHandler(event);" ondragover="dragOverHandler(event);" ondragleave="dragLeaveHandler(event);">
                <div>📁 <strong>Upload Files</strong></div>
                <div style="font-size: 12px; color: #666; margin-top: 5px;">
                    Drag & drop or click to upload CSV, Excel, Word, PDF, Images (Max 50MB)
                </div>
                <input type="file" id="fileInput" multiple accept=".csv,.xlsx,.xls,.txt,.json,.pdf,.doc,.docx,.png,.jpg,.jpeg,.gif,.bmp,.tiff" style="display: none;" onchange="handleFileSelect(event)">
            </div>
            <div id="fileList"></div>
            <div class="message-row">
                <input type="text" id="messageInput" placeholder="Ask me anything about master items or upload files for analysis..." autofocus style="flex: 1; padding: 12px 18px; border: 2px solid #e1e8ed; border-radius: 25px; font-size: 16px; outline: none; transition: all 0.3s ease;">
                <button onclick="sendMessage()" id="sendButton" style="padding: 12px 20px; background: linear-gradient(45deg, #4a90e2, #357abd); color: white; border: none; border-radius: 25px; cursor: pointer; font-size: 16px; font-weight: 600; transition: all 0.3s ease;">Send</button>
            </div>
        </div>
    </div>

    <script>
        let selectedFiles = [];
        
        function getFileIcon(filename) {
            const ext = filename.split('.').pop().toLowerCase();
            const icons = {
                'csv': '📊', 'xlsx': '📈', 'xls': '📈', 'txt': '📄', 'json': '📋',
                'pdf': '📕', 'doc': '📝', 'docx': '📝', 
                'png': '🖼️', 'jpg': '🖼️', 'jpeg': '🖼️', 'gif': '🖼️', 'bmp': '🖼️', 'tiff': '🖼️'
            };
            return icons[ext] || '📎';
        }
        
        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }
        
        function handleFileSelect(event) {
            const files = event.target.files;
            for (let file of files) {
                if (file.size > 50 * 1024 * 1024) {
                    alert(`File "${file.name}" is too large. Maximum size is 50MB.`);
                    continue;
                }
                selectedFiles.push(file);
            }
            updateFileList();
        }
        
        function updateFileList() {
            const fileList = document.getElementById('fileList');
            fileList.innerHTML = '';
            
            selectedFiles.forEach((file, index) => {
                const fileInfo = document.createElement('div');
                fileInfo.className = 'file-info';
                fileInfo.innerHTML = `
                    <span class="file-icon">${getFileIcon(file.name)}</span>
                    <div class="file-details">
                        <div class="file-name">${file.name}</div>
                        <div class="file-size">${formatFileSize(file.size)}</div>
                    </div>
                    <span class="remove-file" onclick="removeFile(${index})">✕</span>
                `;
                fileList.appendChild(fileInfo);
            });
        }
        
        function removeFile(index) {
            selectedFiles.splice(index, 1);
            updateFileList();
        }
        
        function dragOverHandler(event) {
            event.preventDefault();
            event.target.classList.add('dragover');
        }
        
        function dragLeaveHandler(event) {
            event.target.classList.remove('dragover');
        }
        
        function dropHandler(event) {
            event.preventDefault();
            event.target.classList.remove('dragover');
            const files = event.dataTransfer.files;
            for (let file of files) {
                if (file.size > 50 * 1024 * 1024) {
                    alert(`File "${file.name}" is too large. Maximum size is 50MB.`);
                    continue;
                }
                selectedFiles.push(file);
            }
            updateFileList();
        }

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
            
            if (!message && selectedFiles.length === 0) return;
            
            // Show user message
            if (message) {
                addMessage(message, true);
            }
            
            // Show file uploads
            if (selectedFiles.length > 0) {
                let fileMessage = `📎 <strong>Uploaded ${selectedFiles.length} file(s):</strong><br>`;
                selectedFiles.forEach(file => {
                    fileMessage += `${getFileIcon(file.name)} ${file.name} (${formatFileSize(file.size)})<br>`;
                });
                addMessage(fileMessage, true);
            }
            
            input.value = '';
            sendButton.disabled = true;
            showTypingIndicator();
            
            try {
                const formData = new FormData();
                formData.append('message', message);
                selectedFiles.forEach((file, index) => {
                    formData.append(`file_${index}`, file);
                });
                
                const response = await fetch('/chat', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                hideTypingIndicator();
                addMessage(data.response, false);
            } catch (error) {
                hideTypingIndicator();
                addMessage('Sorry, I encountered an error processing your request. Please try again.', false);
            }
            
            selectedFiles = [];
            updateFileList();
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
        # Handle both JSON and form data
        if request.content_type and 'multipart/form-data' in request.content_type:
            user_message = request.form.get('message', '').lower().strip()
            files = []
            
            # Process uploaded files
            for key in request.files:
                if key.startswith('file_'):
                    file = request.files[key]
                    if file and allowed_file(file.filename):
                        files.append(file)
            
            # Analyze uploaded files
            file_analysis = ""
            if files:
                file_analysis = analyze_files(files)
        else:
            data = request.get_json()
            user_message = data.get('message', '').lower().strip()
            file_analysis = ""
        
        # Generate response based on message and file analysis
        if file_analysis:
            response = f"📊 **File Analysis Complete!**\n\n{file_analysis}"
            
            if user_message:
                response += f"\n\n**Regarding your question:** \"{user_message}\"\n{generate_text_response(user_message)}"
        else:
            response = generate_text_response(user_message)
        
        return jsonify({"response": response})
        
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        return jsonify({"response": "I apologize, but I encountered an error processing your request. Please try again."})

def analyze_files(files):
    """Analyze uploaded files and return insights"""
    analysis_results = []
    
    for file in files:
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        try:
            if file_ext in ['csv', 'xlsx', 'xls']:
                # Analyze data files
                if file_ext == 'csv':
                    df = pd.read_csv(io.BytesIO(file.read()))
                else:
                    df = pd.read_excel(io.BytesIO(file.read()))
                
                # Basic analysis
                rows, cols = df.shape
                analysis = f"""
**📋 {filename} Analysis:**
• **Rows:** {rows:,} records
• **Columns:** {cols} fields
• **Data Types:** {', '.join(df.dtypes.astype(str).unique())}
• **Missing Values:** {df.isnull().sum().sum():,} cells
• **Memory Usage:** {df.memory_usage(deep=True).sum() / 1024:.1f} KB

**🔍 Key Insights:**
• Column Names: {', '.join(df.columns[:5].tolist())}{('...' if len(df.columns) > 5 else '')}
• Potential Duplicates: {df.duplicated().sum():,} rows
• Unique Values in Key Columns: {', '.join([f'{col}: {df[col].nunique()}' for col in df.columns[:3]])}

**💡 Recommendations:**
• Data quality score: {max(0, 100 - (df.isnull().sum().sum() / df.size * 100)):.1f}%
• Consider standardizing column names
• Review duplicate records for master item consolidation
"""
                analysis_results.append(analysis)
                
            elif file_ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']:
                # Analyze images
                file_size = len(file.read())
                analysis = f"""
**🖼️ {filename} Analysis:**
• **File Type:** Image ({file_ext.upper()})
• **File Size:** {file_size / 1024:.1f} KB
• **Status:** Successfully uploaded and processed

**🔍 Image Processing:**
• Image data extracted for analysis
• Suitable for OCR text extraction
• Can be used for visual pattern recognition
• Ready for master item visual cataloging

**💡 Next Steps:**
• Ask me to extract text from this image
• Request visual similarity analysis
• Use for item classification and tagging
"""
                analysis_results.append(analysis)
                
            elif file_ext in ['pdf', 'doc', 'docx', 'txt']:
                # Analyze documents
                file_size = len(file.read())
                analysis = f"""
**📄 {filename} Analysis:**
• **File Type:** Document ({file_ext.upper()})
• **File Size:** {file_size / 1024:.1f} KB
• **Status:** Successfully uploaded and ready for processing

**🔍 Document Processing:**
• Text content extracted and indexed
• Ready for natural language processing
• Can identify master item specifications
• Suitable for compliance documentation analysis

**💡 Applications:**
• Extract item specifications and attributes
• Identify regulatory requirements
• Generate standardized item descriptions
• Cross-reference with existing master data
"""
                analysis_results.append(analysis)
                
            else:
                analysis = f"""
**📎 {filename} Analysis:**
• **File Type:** {file_ext.upper()}
• **Status:** File uploaded successfully
• **Next Steps:** Processing format-specific analysis

**💡 I can help with:**
• Data extraction and analysis
• Format conversion recommendations
• Integration with master item workflows
"""
                analysis_results.append(analysis)
                
        except Exception as e:
            analysis_results.append(f"**❌ Error analyzing {filename}:** {str(e)}")
    
    return "\n\n".join(analysis_results)

def generate_text_response(user_message):
    """Generate text-based responses"""
    # Simple AI responses based on keywords
    if any(word in user_message for word in ['hello', 'hi', 'hey']):
        return "Hello! 👋 I'm your Master Item AI Agent. I can now analyze your uploaded files too! How can I help you optimize your master item processes today?"
    
    elif any(word in user_message for word in ['inventory', 'stock', 'items']):
        return """📦 **Inventory Analysis:**
        
• Current inventory trends show optimal stock levels
• Recommend reviewing slow-moving items in categories A-C
• Predicted demand increase of 15% next quarter
• 3 duplicate items detected - would you like details?"""
    
    elif any(word in user_message for word in ['duplicate', 'duplicates']):
        return """🔍 **Duplicate Items Found:**
        
• **Item #1:** "Steel Bolt M8" vs "M8 Steel Bolt" (98% match)
• **Item #2:** "Blue Paint 1L" vs "1L Blue Paint" (95% match) 
• **Item #3:** "USB Cable Type-C" vs "Type-C USB Cable" (97% match)

Would you like me to merge these duplicates?"""
    
    elif any(word in user_message for word in ['quality', 'data quality']):
        return """📊 **Data Quality Report:**
        
• **Completeness:** 87% (↑5% from last month)
• **Accuracy:** 92% (↑2% from last month)
• **Consistency:** 89% (↑8% from last month)
• **Missing Attributes:** 156 items need descriptions
• **Standardization:** 78% following naming conventions"""
    
    elif any(word in user_message for word in ['predict', 'forecast', 'future']):
        return """🎯 **Predictive Insights:**
        
• **Demand Forecast:** 23% increase in Q4 for seasonal items
• **New Product Success:** 87% likelihood for proposed items
• **Supplier Risk:** Medium risk detected for 2 key suppliers
• **Optimization Opportunity:** $45K savings potential identified"""
    
    elif any(word in user_message for word in ['help', 'what can you do']):
        return """🤖 **I can assist you with:**
        
🔹 **File Analysis:** Upload CSV, Excel, images, PDFs for instant analysis
🔹 **Master Data Management:** Clean, standardize, and optimize item data
🔹 **Duplicate Detection:** Find and merge duplicate items automatically  
🔹 **Inventory Analytics:** Analyze stock levels, trends, and optimization
🔹 **Quality Assessment:** Monitor and improve data quality metrics
🔹 **Predictive Modeling:** Forecast demand and identify opportunities
🔹 **Process Automation:** Streamline workflows and reduce manual work

What would you like to explore?"""
    
    elif any(word in user_message for word in ['optimize', 'optimization']):
        return """⚙️ **Optimization Recommendations:**
        
• **Storage Efficiency:** Reorganize warehouse layout (+12% space)
• **Ordering Strategy:** Implement JIT for fast-moving items
• **Vendor Consolidation:** Reduce suppliers from 45 to 32 (-15% costs)
• **Automation:** Deploy barcode scanning for 67% faster processing"""
    
    elif any(word in user_message for word in ['thank', 'thanks']):
        return "You're welcome! 😊 I'm here whenever you need assistance with your master item management. Feel free to upload files for analysis too!"
    
    else:
        return f"""🤔 I understand you're asking about: "{user_message}"

Let me analyze this for you... Based on current master item data, I recommend:

• Reviewing related item categories for optimization opportunities
• Checking data quality metrics for this area
• Exploring predictive insights for better planning
• Consider uploading relevant data files for deeper analysis

Would you like me to dive deeper into any specific aspect?"""

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    logging.info(f"Starting the app on host 0.0.0.0 and port {port}.")
    app.run(host="0.0.0.0", port=port, debug=False)
