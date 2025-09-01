#!/usr/bin/env python3
"""
FULL DIAGNOSTIC SCRIPT - YAMAMA AI TROUBLESHOOTING
Comprehensive testing of all components to identify exact failure points
"""
import os
import sys
import requests
import subprocess
import json
from datetime import datetime

print("🔍 YAMAMA AI FULL DIAGNOSTIC SCRIPT")
print("=" * 60)
print(f"📅 Diagnostic Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 1. ENVIRONMENT CHECK
print("1️⃣ ENVIRONMENT CHECK")
print("-" * 30)
print(f"🐍 Python Version: {sys.version}")
print(f"📁 Current Directory: {os.getcwd()}")
print(f"🌐 Python Path: {sys.executable}")
print()

# 2. REQUIRED MODULES CHECK
print("2️⃣ REQUIRED MODULES CHECK")
print("-" * 30)
modules = ['flask', 'google.generativeai', 'requests', 'gunicorn']
for module in modules:
    try:
        __import__(module)
        print(f"✅ {module}: Available")
    except ImportError as e:
        print(f"❌ {module}: Missing - {e}")
print()

# 3. GOOGLE GEMINI API TEST
print("3️⃣ GOOGLE GEMINI API TEST")
print("-" * 30)
try:
    import google.generativeai as genai
    
    # Test with hardcoded API key
    API_KEY = 'AIzaSyASSS8H6lPc6P6dd6hBtVHhOXCWZV2qxKA'
    genai.configure(api_key=API_KEY)
    
    # Test model availability
    print("🔍 Testing available models...")
    try:
        models = list(genai.list_models())
        gemini_models = [m for m in models if 'gemini' in m.name.lower()]
        print(f"📊 Found {len(gemini_models)} Gemini models:")
        for model in gemini_models[:3]:  # Show first 3
            print(f"   - {model.name}")
    except Exception as e:
        print(f"❌ Model list error: {e}")
    
    # Test specific model
    print("\n🧪 Testing gemini-1.5-flash model...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    test_response = model.generate_content("Say 'Diagnostic test successful' in English")
    
    if test_response and test_response.text:
        print(f"✅ Gemini Response: {test_response.text[:100]}...")
        gemini_working = True
    else:
        print("❌ No response from Gemini")
        gemini_working = False
        
except Exception as e:
    print(f"❌ Gemini API Error: {e}")
    gemini_working = False
print()

# 4. FILE SYSTEM CHECK
print("4️⃣ FILE SYSTEM CHECK")
print("-" * 30)
files_to_check = [
    'yamama_ai_v3.py',
    'requirements.txt', 
    'render.yaml',
    'static/yama.png'
]

for file_path in files_to_check:
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {file_path}: {size} bytes")
    else:
        print(f"❌ {file_path}: Missing")
print()

# 5. NETWORK CONNECTIVITY TEST
print("5️⃣ NETWORK CONNECTIVITY TEST")
print("-" * 30)
try:
    response = requests.get('https://generativelanguage.googleapis.com', timeout=10)
    print(f"✅ Google AI API endpoint: HTTP {response.status_code}")
except Exception as e:
    print(f"❌ Google AI API endpoint: {e}")

try:
    response = requests.get('https://www.google.com', timeout=5)
    print(f"✅ Internet connectivity: HTTP {response.status_code}")
except Exception as e:
    print(f"❌ Internet connectivity: {e}")
print()

# 6. APP IMPORT TEST
print("6️⃣ APP IMPORT TEST")
print("-" * 30)
try:
    import yamama_ai_v3
    print("✅ yamama_ai_v3.py imports successfully")
    
    if hasattr(yamama_ai_v3, 'app'):
        print("✅ Flask app object found")
    else:
        print("❌ Flask app object not found")
        
    if hasattr(yamama_ai_v3, 'AI_AVAILABLE'):
        print(f"📊 AI_AVAILABLE: {yamama_ai_v3.AI_AVAILABLE}")
    
except Exception as e:
    print(f"❌ Import error: {e}")
print()

# 7. PORT AVAILABILITY TEST
print("7️⃣ PORT AVAILABILITY TEST")
print("-" * 30)
import socket
ports_to_check = [5000, 8000, 10000]
for port in ports_to_check:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', port))
        sock.close()
        print(f"✅ Port {port}: Available")
    except OSError:
        print(f"❌ Port {port}: In use")
print()

# 8. SUMMARY
print("8️⃣ DIAGNOSTIC SUMMARY")
print("-" * 30)
if gemini_working:
    print("✅ GEMINI API: WORKING - API responds correctly")
else:
    print("❌ GEMINI API: FAILED - This is likely the deployment issue")

print("\n🔧 RECOMMENDED NEXT STEPS:")
if not gemini_working:
    print("1. Fix Gemini API connection first")
    print("2. Check API key validity")
    print("3. Verify network connectivity on Render")
else:
    print("1. Local environment looks good")
    print("2. Issue likely on Render platform")
    print("3. Check Render deployment logs")

print("\n" + "=" * 60)
print("🏁 DIAGNOSTIC COMPLETE")
